from typing import Dict
from .BaseMethodNode import BaseMethodNode, MethodType


class HighlightMethodNode(BaseMethodNode):
    """高亮方法"""
    def __init__(self, method_data: Dict = None):
        super().__init__()
        self.type: MethodType = "highlight"
        
        if method_data:
            self._parse_method_data(method_data)
    
    def _parse_method_data(self, method_data: Dict):
        """解析高亮方法数据"""
        # 高亮方法目前没有额外字段需要解析
        pass