from ChartMark.annotation_ast_genetic.ast_base import BaseNode
from typing import Dict

class StrokeMarker(BaseNode):
    """描边标记"""
    def __init__(self, marker_data: Dict = None):
        self.width: int = 2
        self.color: str = "black"
        
        if marker_data:
            self._parse_marker_data(marker_data)
    
    def _parse_marker_data(self, marker_data: Dict):
        """解析描边标记数据"""
        self.width = marker_data.get("width", 2)
        self.color = marker_data.get("color", "black")
        
        # 字段验证
        if not isinstance(self.width, (int, float)) or self.width <= 0:
            raise ValueError("描边标记的lineWidth必须是正数")
    
    def to_dict(self) -> Dict:
        """将标记转换为字典格式"""
        return {
            "width": self.width,
            "color": self.color
        }