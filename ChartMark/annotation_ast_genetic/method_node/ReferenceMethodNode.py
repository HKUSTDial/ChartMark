from typing import Dict, Literal, Optional
from .BaseMethodNode import BaseMethodNode, MethodType

# Reference子类型
ReferenceSubType = Literal["grid_line", "data_line", "extra_line", "extra_range", "extra_area"]

class ReferenceMethodNode(BaseMethodNode):
    """引用方法"""
    def __init__(self, method_data: Dict = None):
        super().__init__()
        self.type: MethodType = "reference"
        self.subtype: Optional[ReferenceSubType] = None
        
        if method_data:
            self._parse_method_data(method_data)
    
    def _parse_method_data(self, method_data: Dict):
        """解析引用方法数据"""
        subtype = method_data.get("subType")
        if subtype:
            if subtype not in ["grid_line", "data_line", "extra_line", "extra_range", "extra_area"]:
                raise ValueError("引用方法的subtype必须是'grid_line'、'data_line'、'extra_line'、'extra_range'或'extra_area'")
            self.subtype = subtype
        else:
            raise ValueError("引用方法必须指定subtype字段")
    
    def to_dict(self) -> Dict:
        """将方法转换为字典格式"""
        result = super().to_dict()
        if self.subtype:
            result["subtype"] = self.subtype
        return result
