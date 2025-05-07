from ChartMark.annotation_ast_genetic.ast_base import BaseNode
from typing import Dict

class OpacityMarker(BaseNode):
    """透明度标记"""
    def __init__(self, marker_data: Dict = None):
        self.selected: float = 1.0
        self.other: float = 0.5
        
        if marker_data:
            self._parse_marker_data(marker_data)
    
    def _parse_marker_data(self, marker_data: Dict):
        """解析透明度标记数据"""
        self.selected = marker_data.get("selected", 1.0)
        self.other = marker_data.get("other", 0.5)
        
        # 字段验证
        if not isinstance(self.selected, (int, float)) or not (0 <= self.selected <= 1):
            raise ValueError("透明度标记的selected值必须在0到1之间")
        
        if not isinstance(self.other, (int, float)) or not (0 <= self.other <= 1):
            raise ValueError("透明度标记的other值必须在0到1之间")
    
    def to_dict(self) -> Dict:
        """将标记转换为字典格式"""
        return {
            "selected": self.selected,
            "other": self.other
        }
