from typing import Dict, Optional, Literal
from ChartMark.annotation_ast_genetic.ast_base import BaseNode
from .filter_node.FilterNode import ChartType

TargetType = Literal["data_items", "coordinate", "chart_element", "annotation"]


class BaseTargetNode(BaseNode):
    """
    目标节点基类，为不同类型的目标提供通用功能
    """
    TARGET_TYPE: TargetType = ""
    
    def __init__(self, target_obj: Dict = None, chart_type: Optional[ChartType] = None):
        super().__init__()
        self.type: TargetType = self.__class__.TARGET_TYPE
        self.chart_type = chart_type
        
        if target_obj:
            self._validate_target_type(target_obj)
            self._parse_target_obj(target_obj)
    
    def _validate_target_type(self, target_obj: Dict):
        """验证目标类型是否与节点类型匹配"""
        if not isinstance(target_obj, dict):
            raise ValueError("目标对象必须是字典类型")
        
        target_type = target_obj.get("type")
        if not target_type:
            raise ValueError("目标对象必须指定type字段")
        
        if target_type != self.__class__.TARGET_TYPE:
            raise ValueError(f"目标类型不匹配，期望{self.__class__.TARGET_TYPE}，实际为{target_type}")
    
    def _parse_target_obj(self, target_obj: Dict):
        """解析目标对象，由子类实现"""
        pass
    
    def to_dict(self) -> Dict:
        """将节点转换为字典格式，由子类实现"""
        return {"type": self.type}
    
    # @classmethod
    # def create(cls, target_obj: Dict, chart_type: Optional[ChartType] = None) -> 'TargetNode':
    #     """
    #     工厂方法，根据目标类型创建相应的目标节点对象
    #     """
    #     if not isinstance(target_obj, dict):
    #         raise ValueError("目标对象必须是字典类型")
        
    #     target_type = target_obj.get("type")
    #     if not target_type:
    #         raise ValueError("目标对象必须指定type字段")
        
    #     # 根据目标类型选择合适的节点类
    #     if target_type == "data_items":
    #         return DataItemsTargetNode(target_obj, chart_type)
    #     elif target_type == "coordinate":
    #         return CoordinateTargetNode(target_obj, chart_type)
    #     elif target_type == "chart_element":
    #         return ChartElementTargetNode(target_obj, chart_type)
    #     elif target_type == "annotation":
    #         return AnnotationTargetNode(target_obj, chart_type)
    #     else:
    #         raise ValueError(f"无效的目标类型: {target_type}")
