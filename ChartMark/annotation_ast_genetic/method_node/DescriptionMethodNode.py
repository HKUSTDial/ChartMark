from typing import Dict, Literal, Optional
from .BaseMethodNode import BaseMethodNode, MethodType

# Description子类型
DescriptionSubType = Literal["global_note", "local_note"]

class DescriptionMethodNode(BaseMethodNode):
    """描述方法"""
    def __init__(self, method_data: Dict = None):
        super().__init__()
        self.type: MethodType = "description"
        self.subtype: Optional[DescriptionSubType] = None
        
        if method_data:
            self._parse_method_data(method_data)
    
    def _parse_method_data(self, method_data: Dict):
        """解析描述方法数据"""
        subtype = method_data.get("subType")
        if subtype:
            if subtype not in ["global_note", "local_note"]:
                raise ValueError("描述方法的subType必须是'global_note'或'local_note'")
            self.subtype = subtype
        else:
            raise ValueError("描述方法必须指定subType字段")
    
    def to_dict(self) -> Dict:
        """将方法转换为字典格式"""
        result = super().to_dict()
        if self.subtype:
            result["subType"] = self.subtype
        return result
