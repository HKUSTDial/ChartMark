from ChartMark.annotation_ast_genetic.ast_base import BaseNode
from typing import Dict

class TextMarker(BaseNode):
    """文本标记"""
    def __init__(self, marker_data: Dict = None):
        self.field: str = ""
        self.color: str = "black"
        
        if marker_data:
            self._parse_marker_data(marker_data)
    
    def _parse_marker_data(self, marker_data: Dict):
        """解析文本标记数据"""
        self.field = marker_data.get("field", "")
        self.color = marker_data.get("color", "black")
        
        # 字段验证
        if not self.field:
            raise ValueError("文本标记必须指定field字段")
    
    def to_dict(self) -> Dict:
        """将标记转换为字典格式"""
        return {
            "field": self.field,
            "color": self.color
        }