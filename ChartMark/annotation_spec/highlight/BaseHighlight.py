from ChartMark.annotation_ast_genetic.annotation_node.BaseAnnotationNode import BaseAnnotationNode
from ChartMark.annotation_ast_genetic.method_node.HighlightMethodNode import HighlightMethodNode
from ChartMark.annotation_ast_genetic.data_node.SimpleDataNode import SimpleDataNode
from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique
from ChartMark.annotation_spec.highlight.StrokeTechnique import StrokeTechnique
from ChartMark.annotation_spec.highlight.OpacityTechnique import OpacityTechnique
from typing import Dict, List, Type, ClassVar, Optional, Literal
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType


# 导入Chart类型
from ChartMark.vegalite_ast.ChartNode import Chart

class BaseHighlight(BaseAnnotationNode):
    """
    高亮注释基类，继承自BaseAnnotationNode
    用于处理高亮类型的注释，从字典初始化各个组件
    """
    # 技术名称到技术类的映射
    TECHNIQUE_CLASSES: ClassVar[Dict[str, Type[BaseTechnique]]] = {
        "stroke": StrokeTechnique,
        "opacity": OpacityTechnique,
        # 在这里添加其他高亮技术类映射
    }
    
    def __init__(self, highlight_obj: Dict):
        """
        从字典初始化高亮注释
        
        参数:
            highlight_obj: 包含高亮注释配置的字典
        """
        if not isinstance(highlight_obj, dict):
            raise ValueError("highlight_obj必须是字典类型")
        
        # 解析id字段
        id = highlight_obj.get("id", "")
        if not isinstance(id, str):
            raise ValueError("id字段必须是字符串类型")
        
        # 解析method字段并创建EncodingMethodNode实例
        method_data = highlight_obj.get("method", {})
        if not isinstance(method_data, dict):
            raise ValueError("method字段必须是字典类型")
        method = HighlightMethodNode(method_data)
        
        # 解析data字段并创建SimpleDataNode实例
        data_obj = highlight_obj.get("data", {})
        if not isinstance(data_obj, dict):
            raise ValueError("data字段必须是字典类型")
        data = SimpleDataNode(data_obj)
        
        # 解析techniques字段并创建对应的技术实例
        techniques_data = highlight_obj.get("techniques", [])
        if not isinstance(techniques_data, list):
            raise ValueError("techniques字段必须是数组类型")
        
        techniques = []
        for technique_data in techniques_data:
            if not isinstance(technique_data, dict):
                raise ValueError("technique对象必须是字典类型")
            
            technique = self._create_technique_instance(technique_data)
            techniques.append(technique)
        
        # 调用父类初始化方法
        super().__init__(id=id, method=method, data=data, techniques=techniques)
    
    def _create_technique_instance(self, technique_data: Dict) -> BaseTechnique:
        """
        根据技术数据创建技术实例
        
        参数:
            technique_data: 技术数据字典
            
        返回:
            BaseTechnique的子类实例
        """
        name = technique_data.get("name")
        if not name or not isinstance(name, str):
            raise ValueError("technique必须包含有效的name字段")
        
        # 根据name获取对应的技术类
        technique_class = self.TECHNIQUE_CLASSES.get(name)
        if not technique_class:
            raise ValueError(f"不支持的高亮技术类型: {name}")
        
        # 使用类的from_dict方法创建实例
        if hasattr(technique_class, 'from_dict'):
            return technique_class.from_dict(technique_data)
        else:
            # 如果没有from_dict方法，尝试直接传入字典
            return technique_class(technique_data)
    
    @classmethod
    def register_technique_class(cls, name: str, technique_class: Type[BaseTechnique]):
        """
        注册新的高亮技术类
        
        参数:
            name: 技术名称
            technique_class: 技术类
        """
        cls.TECHNIQUE_CLASSES[name] = technique_class
    
    def get_stroke_highlights(self) -> List[StrokeTechnique]:
        """
        获取所有描边高亮技术
        
        返回:
            StrokeHighlight实例列表
        """
        return [tech for tech in self.techniques if isinstance(tech, StrokeHighlight)]
    
    def get_opacity_highlights(self) -> List[OpacityTechnique]:
        """
        获取所有透明度高亮技术
        
        返回:
            OpacityHighlight实例列表
        """
        return [tech for tech in self.techniques if isinstance(tech, OpacityTechnique)]
    
    def add_stroke_highlight(self, target, width=2, color="black") -> bool:
        """
        添加描边高亮技术
        
        参数:
            target: 目标节点
            width: 描边宽度
            color: 描边颜色
            
        返回:
            添加是否成功
        """
        try:
            highlight = StrokeTechnique(target=target, width=width, color=color)
            self.techniques.append(highlight)
            return True
        except ValueError:
            return False
    
    def add_opacity_highlight(self, target, selected=1.0, other=0.5) -> bool:
        """
        添加透明度高亮技术
        
        参数:
            target: 目标节点
            selected: 选中项的透明度
            other: 其他项的透明度
            
        返回:
            添加是否成功
        """
        try:
            highlight = OpacityTechnique(target=target, selected=selected, other=other)
            self.techniques.append(highlight)
            return True
        except ValueError:
            return False
    
    def parse_techniques_to_vegalite(self, original_vegalite_node: Chart, chart_type: ChartType) -> Dict:
        """
        将高亮注释应用到原始vegalite图表上，遍历并调用每个技术实例的parse_to_vegalite方法
        实现循环叠加效果，每次处理后的结果会作为下一个技术的输入
        
        参数:
            original_vegalite_node: 原始vegalite图表实例
            chart_type: 图表类型，如'bar', 'line', 'scatter', 'pie'等
            
        返回:
            应用了高亮效果的新vegalite字典
        """
        # 使用原始图表作为初始输入
        current_chart = original_vegalite_node
        
        # 遍历所有技术实例，依次应用其parse_to_vegalite方法
        for technique in self.techniques:
            try:
                # 调用技术实例的parse_to_vegalite方法
                vegalite_dict = technique.parse_to_vegalite(current_chart, chart_type)
                
                # 使用处理后的字典创建新的Chart实例作为下一个技术的输入
                current_chart = Chart(vegalite_dict)
            except Exception as e:
                # 记录错误但继续处理其他技术
                print(f"应用技术 {technique.name} 时出错: {str(e)}")
        
        # 返回最终处理结果的字典表示
        return current_chart.to_dict()
