from ChartMark.annotation_ast_genetic.annotation_node.BaseAnnotationNode import BaseAnnotationNode
from ChartMark.annotation_ast_genetic.method_node.DescriptionMethodNode import DescriptionMethodNode
from ChartMark.annotation_ast_genetic.data_node.ExternalDataNode import ExternalDataNode
from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique
from ChartMark.annotation_spec.description.global_note.OutPlotTechnique import OutPlotTechnique as GlobalOutPlotTechnique
from ChartMark.annotation_spec.description.local_note.InPlotTechnique import InPlotTechnique as LocalInPlotTechnique
from ChartMark.annotation_spec.description.local_note.OutPlotTechnique import OutPlotTechnique as LocalOutPlotTechnique
from typing import Dict, List, Type, ClassVar, Optional, Any
from ChartMark.vegalite_ast.ChartNode import Chart
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType


class BaseDescription(BaseAnnotationNode):
    """
    描述注释基类，继承自BaseAnnotationNode
    用于处理描述类型的注释，从字典初始化各个组件
    技术类型是两层结构：先通过method.subtype选择global_note或local_note，再通过technique.name选择具体技术
    """
    # 两层技术类映射: subtype -> {name -> class}
    TECHNIQUE_CLASSES: ClassVar[Dict[str, Dict[str, Type[BaseTechnique]]]] = {
        "global_note": {
            "out_plot": GlobalOutPlotTechnique,
            # 可以在这里添加更多全局注释的技术类
        },
        "local_note": {
            "in_plot": LocalInPlotTechnique,
            "out_plot": LocalOutPlotTechnique,
            # 可以在这里添加更多局部注释的技术类
        }
    }
    
    def __init__(self, description_obj: Dict):
        """
        从字典初始化描述注释
        
        参数:
            description_obj: 包含描述注释配置的字典
        """
        if not isinstance(description_obj, dict):
            raise ValueError("description_obj必须是字典类型")
        
        # 解析id字段
        id = description_obj.get("id", "")
        if not isinstance(id, str):
            raise ValueError("id字段必须是字符串类型")
        
        # 解析method字段并创建DescriptionMethodNode实例
        method_data = description_obj.get("method", {})
        if not isinstance(method_data, dict):
            raise ValueError("method字段必须是字典类型")
        method = DescriptionMethodNode(method_data)
        
        # 记录subtype用于后续技术类选择
        self.subtype = method.subtype
        if not self.subtype or self.subtype not in self.TECHNIQUE_CLASSES:
            raise ValueError(f"不支持的描述子类型: {self.subtype}")
        
        # 解析data字段并创建SimpleDataNode实例
        data_obj = description_obj.get("data", {})
        if not isinstance(data_obj, dict):
            raise ValueError("data字段必须是字典类型")
        
        data = ExternalDataNode(data_obj)
        
        # 解析techniques字段并创建对应的技术实例
        techniques_data = description_obj.get("techniques", [])
        if not isinstance(techniques_data, list):
            raise ValueError("techniques字段必须是数组类型")
        
        techniques = []
        for technique_data in techniques_data:
            if not isinstance(technique_data, dict):
                raise ValueError("technique对象必须是字典类型")
            
            technique = self._create_technique_instance(technique_data, data=data.to_dict())
            techniques.append(technique)
        
        # 调用父类初始化方法
        super().__init__(id=id, method=method, data=data, techniques=techniques)
    
    def _create_technique_instance(self, technique_data: Dict, data: Optional[Dict] = None) -> BaseTechnique:
        """
        根据技术数据创建技术实例，使用两层查找：
        1. 根据method.subtype查找技术类组
        2. 根据technique.name查找具体技术类
        
        参数:
            technique_data: 技术数据字典
            
        返回:
            BaseTechnique的子类实例
        """
        if data:
            technique_data["data"] = data
        
        name = technique_data.get("name")
        if not name or not isinstance(name, str):
            raise ValueError("technique必须包含有效的name字段")
        
        # 先根据subtype获取技术类组
        technique_group = self.TECHNIQUE_CLASSES.get(self.subtype)
        if not technique_group:
            raise ValueError(f"不支持的描述子类型: {self.subtype}")
        
        # 再根据name获取对应的技术类
        technique_class = technique_group.get(name)
        
        if not technique_class:
            raise ValueError(f"不支持的描述技术类型: {self.subtype}/{name}")
        
        # 使用类的from_dict方法创建实例
        if hasattr(technique_class, 'from_dict'):
            return technique_class.from_dict(technique_data)
        else:
            # 如果没有from_dict方法，尝试直接传入字典
            return technique_class(technique_data)
    
    @classmethod
    def register_technique_class(cls, subtype: str, name: str, technique_class: Type[BaseTechnique]):
        """
        注册新的描述技术类
        
        参数:
            subtype: 描述子类型（global_note或local_note）
            name: 技术名称
            technique_class: 技术类
        """
        if subtype not in cls.TECHNIQUE_CLASSES:
            cls.TECHNIQUE_CLASSES[subtype] = {}
        cls.TECHNIQUE_CLASSES[subtype][name] = technique_class
    
    # 全局注释相关方法
    def is_global_note(self) -> bool:
        """
        检查是否是全局注释
        
        返回:
            是否是全局注释
        """
        return self.subtype == "global_note"
    
    def get_global_out_plot_techniques(self) -> List[GlobalOutPlotTechnique]:
        """
        获取所有全局外部注释技术
        
        返回:
            GlobalOutPlotTechnique实例列表
        """
        if not self.is_global_note():
            return []
        return [tech for tech in self.techniques if isinstance(tech, GlobalOutPlotTechnique)]
    
    def add_global_out_plot_technique(self, target, 
                                     text_field=None, text_color="black",
                                     rect_color=None, rect_opacity=0.5,
                                     rect_stroke="gray", rect_stroke_width=2,
                                     rect_corner_radius=4) -> bool:
        """
        添加全局外部注释技术
        
        参数:
            target: 目标节点
            text_field: 文本字段，可选
            text_color: 文本颜色
            rect_color: 矩形颜色，可选
            rect_opacity: 矩形透明度
            rect_stroke: 矩形描边颜色
            rect_stroke_width: 矩形描边宽度
            rect_corner_radius: 矩形圆角半径
            
        返回:
            添加是否成功
        """
        if not self.is_global_note():
            return False
            
        try:
            technique = GlobalOutPlotTechnique(
                target=target,
                text_field=text_field,
                text_color=text_color,
                rect_color=rect_color,
                rect_opacity=rect_opacity,
                rect_stroke=rect_stroke,
                rect_stroke_width=rect_stroke_width,
                rect_corner_radius=rect_corner_radius
            )
            self.techniques.append(technique)
            return True
        except ValueError:
            return False
    
    # 局部注释相关方法
    def is_local_note(self) -> bool:
        """
        检查是否是局部注释
        
        返回:
            是否是局部注释
        """
        return self.subtype == "local_note"
    
    def get_local_in_plot_techniques(self) -> List[LocalInPlotTechnique]:
        """
        获取所有局部内部注释技术
        
        返回:
            LocalInPlotTechnique实例列表
        """
        if not self.is_local_note():
            return []
        return [tech for tech in self.techniques if isinstance(tech, LocalInPlotTechnique)]
    
    def get_local_out_plot_techniques(self) -> List[LocalOutPlotTechnique]:
        """
        获取所有局部外部注释技术
        
        返回:
            LocalOutPlotTechnique实例列表
        """
        if not self.is_local_note():
            return []
        return [tech for tech in self.techniques if isinstance(tech, LocalOutPlotTechnique)]
    
    def add_local_in_plot_technique(self, target, 
                                   line_color="red", line_size=2, 
                                   text_field=None, text_color="black",
                                   rect_color=None, rect_opacity=0.5,
                                   rect_stroke="gray", rect_stroke_width=2,
                                   rect_corner_radius=4) -> bool:
        """
        添加局部内部注释技术
        
        参数:
            target: 目标节点
            line_color: 线条颜色，可选
            line_size: 线条大小
            text_field: 文本字段，可选
            text_color: 文本颜色
            rect_color: 矩形颜色，可选
            rect_opacity: 矩形透明度
            rect_stroke: 矩形描边颜色
            rect_stroke_width: 矩形描边宽度
            rect_corner_radius: 矩形圆角半径
            
        返回:
            添加是否成功
        """
        if not self.is_local_note():
            return False
            
        try:
            technique = LocalInPlotTechnique(
                target=target,
                line_color=line_color,
                line_size=line_size,
                text_field=text_field,
                text_color=text_color,
                rect_color=rect_color,
                rect_opacity=rect_opacity,
                rect_stroke=rect_stroke,
                rect_stroke_width=rect_stroke_width,
                rect_corner_radius=rect_corner_radius
            )
            self.techniques.append(technique)
            return True
        except ValueError:
            return False
    
    def add_local_out_plot_technique(self, target, 
                                    line_color="red", line_size=2, 
                                    text_field=None, text_color="black",
                                    rect_color=None, rect_opacity=0.5,
                                    rect_stroke="gray", rect_stroke_width=2,
                                    rect_corner_radius=4) -> bool:
        """
        添加局部外部注释技术
        
        参数:
            target: 目标节点
            line_color: 线条颜色，可选
            line_size: 线条大小
            text_field: 文本字段，可选
            text_color: 文本颜色
            rect_color: 矩形颜色，可选
            rect_opacity: 矩形透明度
            rect_stroke: 矩形描边颜色
            rect_stroke_width: 矩形描边宽度
            rect_corner_radius: 矩形圆角半径
            
        返回:
            添加是否成功
        """
        if not self.is_local_note():
            return False
            
        try:
            technique = LocalOutPlotTechnique(
                target=target,
                line_color=line_color,
                line_size=line_size,
                text_field=text_field,
                text_color=text_color,
                rect_color=rect_color,
                rect_opacity=rect_opacity,
                rect_stroke=rect_stroke,
                rect_stroke_width=rect_stroke_width,
                rect_corner_radius=rect_corner_radius
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
                vegalite_dict = technique.parse_to_vegalite(current_chart, chart_type)
                
                # 使用处理后的字典创建新的Chart实例作为下一个技术的输入
                current_chart = Chart(vegalite_dict)
            except Exception as e:
                # 记录错误但继续处理其他技术
                print(f"应用技术 {technique.name} 时出错: {str(e)}")
        
        # 返回最终处理结果的字典表示
        return current_chart.to_dict()