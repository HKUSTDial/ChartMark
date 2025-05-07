from ChartMark.annotation_ast_genetic.ast_base import BaseNode
from typing import Dict

class RectMarker(BaseNode):
    """矩形标记"""
    def __init__(self, marker_data: Dict = None):
        self.color: str = "red"
        self.opacity: float = 0.5
        self.stroke: str = "gray"
        self.strokeWidth: int = 2
        self.cornerRadius: int = 4
        
        if marker_data:
            self._parse_marker_data(marker_data)
    
    def _parse_marker_data(self, marker_data: Dict):
        """解析矩形标记数据"""
        self.color = marker_data.get("color", "red")
        self.opacity = marker_data.get("opacity", 0.5)
        self.stroke = marker_data.get("stroke", "gray")
        self.strokeWidth = marker_data.get("strokeWidth", 2)
        self.cornerRadius = marker_data.get("cornerRadius", 4)
        
        # 字段验证
        if not isinstance(self.opacity, (int, float)) or not (0 <= self.opacity <= 1):
            raise ValueError("矩形标记的opacity必须在0到1之间")
        
        if not isinstance(self.strokeWidth, (int, float)) or self.strokeWidth < 0:
            raise ValueError("矩形标记的strokeWidth必须是非负数")
        
        if not isinstance(self.cornerRadius, (int, float)) or self.cornerRadius < 0:
            raise ValueError("矩形标记的cornerRadius必须是非负数")
    
    def to_dict(self) -> Dict:
        """将标记转换为字典格式"""
        return {
            "color": self.color,
            "opacity": self.opacity,
            "stroke": self.stroke,
            "strokeWidth": self.strokeWidth,
            "cornerRadius": self.cornerRadius
        }