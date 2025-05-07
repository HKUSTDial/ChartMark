from typing import Dict
from .BaseMethodNode import BaseMethodNode, MethodType


class EncodingMethodNode(BaseMethodNode):
    """编码方法"""
    def __init__(self, method_data: Dict = None):
        super().__init__()
        self.type: MethodType = "encoding"
        
        if method_data:
            self._parse_method_data(method_data)
    
    def _parse_method_data(self, method_data: Dict):
        """解析编码方法数据"""
        # 编码方法目前没有额外字段需要解析
        pass