from typing import Dict, Literal, Optional
from .BaseMethodNode import BaseMethodNode, MethodType

# Summary子类型
SummarySubType = Literal["max", "min", "med", "mean"]


class SummaryMethodNode(BaseMethodNode):
    """汇总方法"""
    def __init__(self, method_data: Dict = None):
        super().__init__()
        self.type: MethodType = "summary"
        self.subtype: Optional[SummarySubType] = None
        
        if method_data:
            self._parse_method_data(method_data)
    
    def _parse_method_data(self, method_data: Dict):
        """解析汇总方法数据"""
        subtype = method_data.get("subType")
        if subtype:
            if subtype not in ["max", "min", "median", "mean"]:
                raise ValueError("汇总方法的subtype必须是'max'、'min'、'median'或'mean'")
            self.subtype = subtype
        else:
            raise ValueError("汇总方法必须指定subtype字段")
    
    def to_dict(self) -> Dict:
        """将方法转换为字典格式"""
        result = super().to_dict()
        if self.subtype:
            result["subtype"] = self.subtype
        return result
