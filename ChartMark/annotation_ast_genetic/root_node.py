from ChartMark.annotation_ast_genetic.ast_base import BaseNode
from typing import Dict, List
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import BaseChartNode
from ChartMark.annotation_ast_genetic.annotation_node.BaseAnnotationNode import BaseAnnotationNode


class BaseRootNode(BaseNode):
    """
    根节点类，作为整个注释语法树的根
    包含chart和annotations两个主要属性
    """
    def __init__(self, chart: BaseChartNode, annotations: List[BaseAnnotationNode]):
        super().__init__()
        
        if not chart or not isinstance(chart, BaseChartNode):
            raise ValueError("chart必须是BaseChartNode实例")
            
        if not isinstance(annotations, list):
            raise ValueError("annotations必须是列表类型")
            
        for annotation in annotations:
            if not isinstance(annotation, BaseAnnotationNode):
                raise ValueError("annotations列表中的所有元素必须是BaseAnnotationNode实例")
        
        self.chart: BaseChartNode = chart  # 图表节点，必需的
        self.annotations: List[BaseAnnotationNode] = annotations  # 注释节点列表
    
    def to_dict(self) -> Dict:
        """将节点转换为字典格式"""
        return {
            "chart": self.chart.to_dict(),
            "annotations": [annotation.to_dict() for annotation in self.annotations]
        }
    
    def validate(self) -> bool:
        """
        验证根节点的数据是否有效
        规则：
        1. chart必须存在且有效
        2. annotations可以为空列表，但如果有元素，所有元素必须有效
        """
        # 检查chart是否存在且有效
        if not self.chart or not isinstance(self.chart, BaseChartNode):
            return False
        
        # 检查annotations中的所有元素是否有效
        for annotation in self.annotations:
            if not isinstance(annotation, BaseAnnotationNode) or not annotation.validate():
                return False
        
        return True
    
    def add_annotation(self, annotation: BaseAnnotationNode) -> bool:
        """
        添加注释节点
        
        参数:
            annotation: BaseAnnotationNode实例
            
        返回:
            添加是否成功
        """
        if not annotation or not isinstance(annotation, BaseAnnotationNode):
            return False
        
        self.annotations.append(annotation)
        return True
    
    def set_chart(self, chart: BaseChartNode) -> bool:
        """
        设置图表节点
        
        参数:
            chart: BaseChartNode实例
            
        返回:
            设置是否成功
        """
        if not chart or not isinstance(chart, BaseChartNode):
            return False
        
        self.chart = chart
        return True
    
    def get_chart(self) -> BaseChartNode:
        """获取图表节点"""
        return self.chart
    
    def get_annotations(self) -> List[BaseAnnotationNode]:
        """获取所有注释节点"""
        return self.annotations
    
    def get_annotation_by_id(self, id: str) -> BaseAnnotationNode:
        """
        根据ID获取注释节点
        
        参数:
            id: 注释ID
            
        返回:
            找到的注释节点，如果未找到则返回None
        """
        for annotation in self.annotations:
            if annotation.id == id:
                return annotation
        return None
