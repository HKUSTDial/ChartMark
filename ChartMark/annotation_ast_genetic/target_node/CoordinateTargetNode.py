from typing import Dict, Optional, Literal
from .BaseTargetNode import BaseTargetNode, TargetType
from .filter_node.FilterNode import ChartType
from dataclasses import dataclass

# ===== 坐标 (coordinate) 结构 =====
@dataclass
class XYCoordinate:
    """笛卡尔坐标"""
    x: float = 0
    y: float = 0
    x1: Optional[float] = None
    y1: Optional[float] = None

@dataclass
class PolarCoordinate:
    """极坐标"""
    radius: float = 0
    radius2: Optional[float] = None
    theta: float = 0
    theta2: Optional[float] = None

@dataclass
class CoordinateTarget:
    """坐标目标类型"""
    type: Literal["coordinate"] = "coordinate"
    xyCoordinate: Optional[XYCoordinate] = None
    polarCoordinate: Optional[PolarCoordinate] = None



class CoordinateTargetNode(BaseTargetNode):
    """坐标目标节点"""
    TARGET_TYPE: TargetType = "coordinate"
    
    def __init__(self, target_obj: Dict = None, chart_type: Optional[ChartType] = None):
        self.xyCoordinate = None
        self.polarCoordinate = None
        super().__init__(target_obj, chart_type)
    
    def _parse_target_obj(self, target_obj: Dict):
        """解析坐标目标"""
        # 根据图表类型决定使用哪种坐标系统
        if self.chart_type == "pie" or target_obj.get("polarCoordinate"):
            # 饼图使用极坐标
            polar_coordinate = target_obj.get("polarCoordinate")
            if polar_coordinate and isinstance(polar_coordinate, dict):
                self.polarCoordinate = polar_coordinate
            else:
                # 饼图必须提供极坐标
                raise ValueError("饼图目标必须提供polarCoordinate")
        else:
            # 其他图表使用笛卡尔坐标
            xy_coordinate = target_obj.get("xyCoordinate")
            if xy_coordinate and isinstance(xy_coordinate, dict):
                self.xyCoordinate = xy_coordinate
            else:
                # 非饼图必须提供笛卡尔坐标
                raise ValueError(f"{self.chart_type or '未知'}图表目标必须提供xyCoordinate")
    
    def to_dict(self) -> Dict:
        """将节点转换为字典格式"""
        result = super().to_dict()
        
        if self.chart_type == "pie":
            if self.polarCoordinate:
                result["polarCoordinate"] = self.polarCoordinate
        else:
            if self.xyCoordinate:
                result["xyCoordinate"] = self.xyCoordinate
        
        return result
