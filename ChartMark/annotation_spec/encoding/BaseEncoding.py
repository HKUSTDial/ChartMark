from ChartMark.annotation_ast_genetic.annotation_node.BaseAnnotationNode import BaseAnnotationNode
from ChartMark.annotation_ast_genetic.method_node.EncodingMethodNode import EncodingMethodNode
from ChartMark.annotation_ast_genetic.data_node.SimpleDataNode import SimpleDataNode
from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique
from ChartMark.annotation_spec.encoding.LabelTechnique import LabelTechnique
from typing import Dict, List, Type, ClassVar, Optional
from ChartMark.vegalite_ast.ChartNode import Chart
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType

class BaseEncoding(BaseAnnotationNode):
    """
    编码注释基类，继承自BaseAnnotationNode
    用于处理编码类型的注释，从字典初始化各个组件
    """
    # 技术名称到技术类的映射
    TECHNIQUE_CLASSES: ClassVar[Dict[str, Type[BaseTechnique]]] = {
        "label": LabelTechnique,
        # 在这里添加其他技术类映射
    }
    
    def __init__(self, encoding_obj: Dict):
        """
        从字典初始化编码注释
        
        参数:
            encoding_obj: 包含编码注释配置的字典
        """
        if not isinstance(encoding_obj, dict):
            raise ValueError("encoding_obj必须是字典类型")
        
        # 解析id字段
        id = encoding_obj.get("id", "")
        if not isinstance(id, str):
            raise ValueError("id字段必须是字符串类型")
        
        # 解析method字段并创建EncodingMethodNode实例
        method_data = encoding_obj.get("method", {})
        if not isinstance(method_data, dict):
            raise ValueError("method字段必须是字典类型")
        method = EncodingMethodNode(method_data)
        
        # 解析data字段并创建SimpleDataNode实例
        data_obj = encoding_obj.get("data", {})
        if not isinstance(data_obj, dict):
            raise ValueError("data字段必须是字典类型")
        data = SimpleDataNode(data_obj)
        
        # 解析techniques字段并创建对应的技术实例
        techniques_data = encoding_obj.get("techniques", [])
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
            raise ValueError(f"不支持的技术类型: {name}")
        
        # 使用类的from_dict方法创建实例
        if hasattr(technique_class, 'from_dict'):
            return technique_class.from_dict(technique_data)
        else:
            # 如果没有from_dict方法，尝试直接传入字典
            return technique_class(technique_data)

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

    
    @classmethod
    def register_technique_class(cls, name: str, technique_class: Type[BaseTechnique]):
        """
        注册新的技术类
        
        参数:
            name: 技术名称
            technique_class: 技术类
        """
        cls.TECHNIQUE_CLASSES[name] = technique_class
