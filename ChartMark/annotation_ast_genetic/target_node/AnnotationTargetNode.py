from typing import Dict, Optional, Literal
from .BaseTargetNode import BaseTargetNode, TargetType
from .filter_node.FilterNode import ChartType
from dataclasses import dataclass

# ===== 注释 (annotation) 结构 =====
@dataclass
class AnnotationTarget:
    """注释目标类型"""
    type: Literal["annotation"] = "annotation"
    prior: str = ""

class AnnotationTargetNode(BaseTargetNode):
    """注释目标节点"""
    TARGET_TYPE: TargetType = "annotation"
    
    def __init__(self, target_obj: Dict = None, chart_type: Optional[ChartType] = None):
        self.prior = ""
        super().__init__(target_obj, chart_type)
    
    def _parse_target_obj(self, target_obj: Dict):
        """解析注释目标"""
        prior = target_obj.get("prior")
        if prior:
            self.prior = prior
        else:
            raise ValueError("annotation目标必须提供prior字段")
    
    def to_dict(self) -> Dict:
        """将节点转换为字典格式"""
        result = super().to_dict()
        
        if self.prior:
            result["prior"] = self.prior
        
        return result
