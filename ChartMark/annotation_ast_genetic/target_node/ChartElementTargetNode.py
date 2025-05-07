from typing import Dict, Optional, Literal
from .BaseTargetNode import BaseTargetNode, TargetType
from .filter_node.FilterNode import ChartType
from dataclasses import dataclass

# ===== 图表元素 (chart_element) 结构 =====
@dataclass
class AxisConfig:
    """坐标轴配置"""
    grid: bool = False
    interval: Optional[float] = None
    tickCount: Optional[int] = None

@dataclass
class ChartElementTarget:
    """图表元素目标类型"""
    type: Literal["chart_element"] = "chart_element"
    xAxis: Optional[AxisConfig] = None
    yAxis: Optional[AxisConfig] = None
    thetaAxis: Optional[AxisConfig] = None

class ChartElementTargetNode(BaseTargetNode):
    """图表元素目标节点"""
    TARGET_TYPE: TargetType = "chart_element"
    
    def __init__(self, target_obj: Dict = None, chart_type: Optional[ChartType] = None):
        self.xAxis = None
        self.yAxis = None
        self.thetaAxis = None
        super().__init__(target_obj, chart_type)
    
    def _parse_target_obj(self, target_obj: Dict):
        """解析图表元素目标"""
        x_axis = target_obj.get("xAxis")
        if x_axis and isinstance(x_axis, dict):
            self.xAxis = x_axis
        
        y_axis = target_obj.get("yAxis")
        if y_axis and isinstance(y_axis, dict):
            self.yAxis = y_axis
            
        theta_axis = target_obj.get("thetaAxis")
        if theta_axis and isinstance(theta_axis, dict):
            self.thetaAxis = theta_axis
    
    def to_dict(self) -> Dict:
        """将节点转换为字典格式"""
        result = super().to_dict()
        
        if self.xAxis:
            result["xAxis"] = self.xAxis
        if self.yAxis:
            result["yAxis"] = self.yAxis
        if self.thetaAxis:
            result["thetaAxis"] = self.thetaAxis
        
        return result
