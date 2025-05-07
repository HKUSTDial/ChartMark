from ChartMark.annotation_ast_genetic.ast_base import BaseNode
from typing import Dict

class LineMarker(BaseNode):
    """线条标记"""
    def __init__(self, marker_data: Dict = None):
        self.color: str = "red"
        self.size: int = 2
        
        if marker_data:
            self._parse_marker_data(marker_data)
    
    def _parse_marker_data(self, marker_data: Dict):
        """解析线条标记数据"""
        self.color = marker_data.get("color", "red")
        self.size = marker_data.get("size", 2)
        
        # 字段验证
        if not isinstance(self.size, (int, float)) or self.size <= 0:
            raise ValueError("线条标记的size必须是正数")
    
    def to_dict(self) -> Dict:
        """将标记转换为字典格式"""
        return {
            "color": self.color,
            "size": self.size
        }