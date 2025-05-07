from ChartMark.annotation_ast_genetic.annotation_node.BaseAnnotationNode import BaseAnnotationNode
from ChartMark.annotation_ast_genetic.method_node.ReferenceMethodNode import ReferenceMethodNode
from ChartMark.annotation_ast_genetic.data_node.SimpleDataNode import SimpleDataNode
from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique
from ChartMark.annotation_spec.reference.data_line.DataLineTechnique import DataLineTechnique
from ChartMark.annotation_spec.reference.extra_area.BoundingBoxTechnique import BoundingBoxTechnique
from ChartMark.annotation_spec.reference.extra_line.LabelLineTechnique import LabelLineTechnique
from ChartMark.annotation_spec.reference.extra_range.ShadowTechnique import ShadowTechnique
from ChartMark.annotation_spec.reference.grid_line.GridLineTechnique import GridLineTechnique
from typing import Dict, List, Type, ClassVar, Optional, Any
from ChartMark.vegalite_ast.ChartNode import Chart
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType

class BaseReference(BaseAnnotationNode):
    """
    引用注释基类，继承自BaseAnnotationNode
    用于处理引用类型的注释，从字典初始化各个组件
    技术类型是两层结构：先通过method.subtype选择引用子类型，再通过technique.name选择具体技术
    """
    # 两层技术类映射: subtype -> {name -> class}
    TECHNIQUE_CLASSES: ClassVar[Dict[str, Dict[str, Type[BaseTechnique]]]] = {
        "data_line": {
            "data_line": DataLineTechnique,
            # 可以在这里添加更多数据线引用的技术类
        },
        "extra_area": {
            "bounding_box": BoundingBoxTechnique,
            # 可以在这里添加更多区域引用的技术类
        },
        "extra_line": {
            "label_line": LabelLineTechnique,
            # 可以在这里添加更多辅助线引用的技术类
        },
        "extra_range": {
            "shadow": ShadowTechnique,
            # 可以在这里添加更多范围引用的技术类
        },
        "grid_line": {
            "grid_line": GridLineTechnique,
            # 可以在这里添加更多网格线引用的技术类
        }
    }
    
    def __init__(self, reference_obj: Dict):
        """
        从字典初始化引用注释
        
        参数:
            reference_obj: 包含引用注释配置的字典
        """
        if not isinstance(reference_obj, dict):
            raise ValueError("reference_obj必须是字典类型")
        
        # 解析id字段
        id = reference_obj.get("id", "")
        if not isinstance(id, str):
            raise ValueError("id字段必须是字符串类型")
        
        # 解析method字段并创建ReferenceMethodNode实例
        method_data = reference_obj.get("method", {})
        if not isinstance(method_data, dict):
            raise ValueError("method字段必须是字典类型")
        method = ReferenceMethodNode(method_data)
        
        # 记录subtype用于后续技术类选择
        self.subtype = method.subtype
        if not self.subtype or self.subtype not in self.TECHNIQUE_CLASSES:
            raise ValueError(f"不支持的引用子类型: {self.subtype}")
        
        # 解析data字段并创建SimpleDataNode实例
        data_obj = reference_obj.get("data", {})
        if not isinstance(data_obj, dict):
            raise ValueError("data字段必须是字典类型")
        data = SimpleDataNode(data_obj)
        
        # 解析techniques字段并创建对应的技术实例
        techniques_data = reference_obj.get("techniques", [])
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
            raise ValueError(f"不支持的引用子类型: {self.subtype}")
        
        # 再根据name获取对应的技术类
        technique_class = technique_group.get(name)
        if not technique_class:
            raise ValueError(f"不支持的引用技术类型: {self.subtype}/{name}")
        
        # 使用类的from_dict方法创建实例
        if hasattr(technique_class, 'from_dict'):
            return technique_class.from_dict(technique_data)
        else:
            # 如果没有from_dict方法，尝试直接传入字典
            return technique_class(technique_data)
    
    @classmethod
    def register_technique_class(cls, subtype: str, name: str, technique_class: Type[BaseTechnique]):
        """
        注册新的引用技术类
        
        参数:
            subtype: 引用子类型（data_line、extra_area等）
            name: 技术名称
            technique_class: 技术类
        """
        if subtype not in cls.TECHNIQUE_CLASSES:
            cls.TECHNIQUE_CLASSES[subtype] = {}
        cls.TECHNIQUE_CLASSES[subtype][name] = technique_class
    
    # 数据线引用相关方法
    def is_data_line(self) -> bool:
        """
        检查是否是数据线引用
        
        返回:
            是否是数据线引用
        """
        return self.subtype == "data_line"
    
    def get_data_line_techniques(self) -> List[DataLineTechnique]:
        """
        获取所有数据线技术
        
        返回:
            DataLineTechnique实例列表
        """
        if not self.is_data_line():
            return []
        return [tech for tech in self.techniques if isinstance(tech, DataLineTechnique)]
    
    def add_data_line_technique(self, target, line_color="red", line_size=2) -> bool:
        """
        添加数据线技术
        
        参数:
            target: 目标数据项
            line_color: 线条颜色
            line_size: 线条大小
            
        返回:
            添加是否成功
        """
        if not self.is_data_line():
            return False
            
        try:
            technique = DataLineTechnique(
                target=target,
                line_color=line_color,
                line_size=line_size
            )
            self.techniques.append(technique)
            return True
        except ValueError:
            return False
    
    # 区域引用相关方法
    def is_extra_area(self) -> bool:
        """
        检查是否是区域引用
        
        返回:
            是否是区域引用
        """
        return self.subtype == "extra_area"
    
    def get_bounding_box_techniques(self) -> List[BoundingBoxTechnique]:
        """
        获取所有边界框技术
        
        返回:
            BoundingBoxTechnique实例列表
        """
        if not self.is_extra_area():
            return []
        return [tech for tech in self.techniques if isinstance(tech, BoundingBoxTechnique)]
    
    def add_bounding_box_technique(self, target, stroke="gray", stroke_width=2) -> bool:
        """
        添加边界框技术
        
        参数:
            target: 目标坐标
            stroke: 边框颜色
            stroke_width: 边框宽度
            
        返回:
            添加是否成功
        """
        if not self.is_extra_area():
            return False
            
        try:
            technique = BoundingBoxTechnique(
                target=target,
                stroke=stroke,
                stroke_width=stroke_width
            )
            self.techniques.append(technique)
            return True
        except ValueError:
            return False
    
    # 辅助线引用相关方法
    def is_extra_line(self) -> bool:
        """
        检查是否是辅助线引用
        
        返回:
            是否是辅助线引用
        """
        return self.subtype == "extra_line"
    
    def get_label_line_techniques(self) -> List[LabelLineTechnique]:
        """
        获取所有标签线技术
        
        返回:
            LabelLineTechnique实例列表
        """
        if not self.is_extra_line():
            return []
        return [tech for tech in self.techniques if isinstance(tech, LabelLineTechnique)]
    
    def add_label_line_technique(self, target, 
                              line_color="red", line_size=2, 
                              text_field=None, text_color="black") -> bool:
        """
        添加标签线技术
        
        参数:
            target: 目标坐标
            line_color: 线条颜色
            line_size: 线条大小
            text_field: 文本字段，可选
            text_color: 文本颜色
            
        返回:
            添加是否成功
        """
        if not self.is_extra_line():
            return False
            
        try:
            technique = LabelLineTechnique(
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
    
    # 范围引用相关方法
    def is_extra_range(self) -> bool:
        """
        检查是否是范围引用
        
        返回:
            是否是范围引用
        """
        return self.subtype == "extra_range"
    
    def get_shadow_techniques(self) -> List[ShadowTechnique]:
        """
        获取所有阴影技术
        
        返回:
            ShadowTechnique实例列表
        """
        if not self.is_extra_range():
            return []
        return [tech for tech in self.techniques if isinstance(tech, ShadowTechnique)]
    
    def add_shadow_technique(self, target, rect_color="red", rect_opacity=0.5) -> bool:
        """
        添加阴影技术
        
        参数:
            target: 目标坐标范围
            rect_color: 矩形颜色
            rect_opacity: 矩形透明度
            
        返回:
            添加是否成功
        """
        if not self.is_extra_range():
            return False
            
        try:
            technique = ShadowTechnique(
                target=target,
                rect_color=rect_color,
                rect_opacity=rect_opacity
            )
            self.techniques.append(technique)
            return True
        except ValueError:
            return False
    
    # 网格线引用相关方法
    def is_grid_line(self) -> bool:
        """
        检查是否是网格线引用
        
        返回:
            是否是网格线引用
        """
        return self.subtype == "grid_line"
    
    def get_grid_line_techniques(self) -> List[GridLineTechnique]:
        """
        获取所有网格线技术
        
        返回:
            GridLineTechnique实例列表
        """
        if not self.is_grid_line():
            return []
        return [tech for tech in self.techniques if isinstance(tech, GridLineTechnique)]
    
    def add_grid_line_technique(self, target, line_color="gray", line_size=1, 
                             line_dash=None) -> bool:
        """
        添加网格线技术
        
        参数:
            target: 目标图表元素
            line_color: 线条颜色
            line_size: 线条大小
            line_dash: 线条虚线样式，可选
            
        返回:
            添加是否成功
        """
        if not self.is_grid_line():
            return False
            
        try:
            technique = GridLineTechnique(
                target=target,
                line_color=line_color,
                line_size=line_size,
                line_dash=line_dash
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
