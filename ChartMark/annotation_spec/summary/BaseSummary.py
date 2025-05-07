from ChartMark.annotation_ast_genetic.annotation_node.BaseAnnotationNode import BaseAnnotationNode
from ChartMark.annotation_ast_genetic.method_node.SummaryMethodNode import SummaryMethodNode
from ChartMark.annotation_ast_genetic.data_node.SimpleDataNode import SimpleDataNode
from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique
from ChartMark.annotation_spec.summary.LineTechnique import LineTechnique
from ChartMark.annotation_spec.summary.StrokeTechnique import StrokeTechnique
from typing import Dict, List, Type, ClassVar, Optional
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType
from ChartMark.vegalite_ast.ChartNode import Chart

class BaseSummary(BaseAnnotationNode):
    """
    摘要注释基类，继承自BaseAnnotationNode
    用于处理摘要类型的注释，从字典初始化各个组件
    技术类型是两层结构：先通过method.subtype选择摘要子类型，再通过technique.name选择具体技术
    """
    # 两层技术类映射: subtype -> {name -> class}
    TECHNIQUE_CLASSES: ClassVar[Dict[str, Dict[str, Type[BaseTechnique]]]] = {
        "max": {
            "label_line": LineTechnique,
            "stroke": StrokeTechnique,
        },
        "min": {
            "label_line": LineTechnique,
            "stroke": StrokeTechnique,
        },
        "median": {
            "label_line": LineTechnique,
            "stroke": StrokeTechnique,
        },
        "mean": {
            "label_line": LineTechnique,
            "stroke": StrokeTechnique,
        }
    }
    
    def __init__(self, summary_obj: Dict):
        """
        从字典初始化摘要注释
        
        参数:
            summary_obj: 包含摘要注释配置的字典
        """
        if not isinstance(summary_obj, dict):
            raise ValueError("summary_obj必须是字典类型")
        
        # 解析id字段
        id = summary_obj.get("id", "")
        if not isinstance(id, str):
            raise ValueError("id字段必须是字符串类型")
        
        # 解析method字段并创建SummaryMethodNode实例
        method_data = summary_obj.get("method", {})
        if not isinstance(method_data, dict):
            raise ValueError("method字段必须是字典类型")
        method = SummaryMethodNode(method_data)
        
        # 记录subtype用于后续技术类选择
        self.subtype = method.subtype
        if not self.subtype or self.subtype not in self.TECHNIQUE_CLASSES:
            raise ValueError(f"不支持的摘要子类型: {self.subtype}")
        
        # 解析data字段并创建SimpleDataNode实例
        data_obj = summary_obj.get("data", {})
        if not isinstance(data_obj, dict):
            raise ValueError("data字段必须是字典类型")
        data = SimpleDataNode(data_obj)
        
        # 解析techniques字段并创建对应的技术实例
        techniques_data = summary_obj.get("techniques", [])
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
        根据技术数据创建技术实例，使用两层查找：
        1. 根据method.subtype查找技术类组
        2. 根据technique.name查找具体技术类
        
        参数:
            technique_data: 技术数据字典
            
        返回:
            BaseTechnique的子类实例
        """
        name = technique_data.get("name")
        if not name or not isinstance(name, str):
            raise ValueError("technique必须包含有效的name字段")
        
        # 先根据subtype获取技术类组
        technique_group = self.TECHNIQUE_CLASSES.get(self.subtype)
        if not technique_group:
            raise ValueError(f"不支持的摘要子类型: {self.subtype}")
        
        # 再根据name获取对应的技术类
        technique_class = technique_group.get(name)
        if not technique_class:
            raise ValueError(f"不支持的摘要技术类型: {self.subtype}/{name}")
        
        # 使用类的from_dict方法创建实例
        if hasattr(technique_class, 'from_dict'):
            return technique_class.from_dict(technique_data)
        else:
            # 如果没有from_dict方法，尝试直接传入字典
            return technique_class(technique_data)
    
    @classmethod
    def register_technique_class(cls, subtype: str, name: str, technique_class: Type[BaseTechnique]):
        """
        注册新的摘要技术类
        
        参数:
            subtype: 摘要子类型（max、min、median、mean）
            name: 技术名称
            technique_class: 技术类
        """
        if subtype not in cls.TECHNIQUE_CLASSES:
            cls.TECHNIQUE_CLASSES[subtype] = {}
        cls.TECHNIQUE_CLASSES[subtype][name] = technique_class
    
    # 检查摘要子类型的方法
    def is_max(self) -> bool:
        """检查是否是最大值摘要"""
        return self.subtype == "max"
    
    def is_min(self) -> bool:
        """检查是否是最小值摘要"""
        return self.subtype == "min"
    
    def is_med(self) -> bool:
        """检查是否是中位值摘要"""
        return self.subtype == "median"
    
    def is_mean(self) -> bool:
        """检查是否是平均值摘要"""
        return self.subtype == "mean"
    
    # 获取特定类型的技术实例
    def get_line_techniques(self) -> List[LineTechnique]:
        """获取所有线条技术"""
        return [tech for tech in self.techniques if isinstance(tech, LineTechnique)]
    
    def get_stroke_techniques(self) -> List[StrokeTechnique]:
        """获取所有描边技术"""
        return [tech for tech in self.techniques if isinstance(tech, StrokeTechnique)]
    
    # 添加技术方法
    def add_line_technique(self, target, line_color="red", line_size=2, 
                           text_field=None, text_color="black") -> bool:
        """
        添加线条技术
        
        参数:
            target: 目标节点
            line_color: 线条颜色
            line_size: 线条大小
            text_field: 文本字段，可选
            text_color: 文本颜色，可选
            
        返回:
            添加是否成功
        """
        try:
            technique = LineTechnique(
                target=target, 
                line_color=line_color, 
                line_size=line_size,
                text_field=text_field,
                text_color=text_color
            )
            self.techniques.append(technique)
            return True
        except ValueError:
            return False
    
    def add_stroke_technique(self, target, line_width=2, stroke_color="black", 
                            text_field=None, text_color="black") -> bool:
        """
        添加描边技术
        
        参数:
            target: 目标节点
            line_width: 线宽
            stroke_color: 描边颜色
            text_field: 文本字段，可选
            text_color: 文本颜色，可选
            
        返回:
            添加是否成功
        """
        try:
            technique = StrokeTechnique(
                target=target, 
                line_width=line_width, 
                stroke_color=stroke_color,
                text_field=text_field,
                text_color=text_color
            )
            self.techniques.append(technique)
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
                vegalite_dict = technique.parse_to_vegalite(current_chart, chart_type, self.subtype)
                
                # 使用处理后的字典创建新的Chart实例作为下一个技术的输入
                current_chart = Chart(vegalite_dict)
            except Exception as e:
                # 记录错误但继续处理其他技术
                print(f"应用技术 {technique.name} 时出错: {str(e)}")
        
        # 返回最终处理结果的字典表示
        return current_chart.to_dict()
