from typing import Dict, Type

# 导入图表相关类
from ChartMark.annotation_ast_genetic.chart_node.non_group.BarChartNode import BarChartNode
from ChartMark.annotation_ast_genetic.chart_node.non_group.ScatterChartNode import ScatterChartNode
from ChartMark.annotation_ast_genetic.chart_node.non_group.LineChartNode import LineChartNode
from ChartMark.annotation_ast_genetic.chart_node.non_group.PieChartNode import PieChartNode
from ChartMark.annotation_ast_genetic.chart_node.group.GroupBarChartNode import GroupBarChartNode
from ChartMark.annotation_ast_genetic.chart_node.group.GroupLineChartNode import GroupLineChartNode
from ChartMark.annotation_ast_genetic.chart_node.group.GroupScatterChartNode import GroupScatterChartNode

# 图表类型到图表类的映射
CHART_ROUTER: Dict[str, Type] = {
    # 非分组图表
    "bar": BarChartNode,
    "scatter": ScatterChartNode,
    "line": LineChartNode,
    "pie": PieChartNode,
    
    # 分组图表
    "group_bar": GroupBarChartNode,
    "group_line": GroupLineChartNode,
    "group_scatter": GroupScatterChartNode,
    
    # 可以在这里添加更多图表类型
}

def get_chart_class(chart_type: str) -> Type:
    """
    根据图表类型获取对应的图表类
    
    参数:
        chart_type: 图表类型
        
    返回:
        对应的图表类
        
    异常:
        ValueError: 不支持的图表类型
    """
    chart_class = CHART_ROUTER.get(chart_type)
    if not chart_class:
        raise ValueError(f"不支持的图表类型: {chart_type}")
    return chart_class

def register_chart_type(chart_type: str, chart_class: Type) -> None:
    """
    注册新的图表类型
    
    参数:
        chart_type: 图表类型
        chart_class: 图表类
        
    异常:
        ValueError: 图表类型已存在
    """
    if chart_type in CHART_ROUTER:
        raise ValueError(f"图表类型已存在: {chart_type}")
    CHART_ROUTER[chart_type] = chart_class

def get_supported_chart_types() -> list:
    """
    获取支持的图表类型列表
    
    返回:
        支持的图表类型列表
    """
    return list(CHART_ROUTER.keys()) 