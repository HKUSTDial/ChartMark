from typing import Dict
from .BaseDataNode import BaseDataNode
class SimpleDataNode(BaseDataNode):
    """
    简单数据节点，只包含源类型属性
    """
    def __init__(self, data_obj: Dict = None):
        super().__init__(data_obj)
        
        # 确保非external类型的数据不包含value字段
        if data_obj and self.source != "external" and "value" in data_obj:
            raise ValueError(f"{self.source}类型的数据不应包含value字段")
