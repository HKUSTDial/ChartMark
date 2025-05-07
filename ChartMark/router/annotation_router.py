from typing import Dict, Type

# 导入注释相关类
from ChartMark.annotation_spec.description.BaseDescription import BaseDescription
from ChartMark.annotation_spec.encoding.BaseEncoding import BaseEncoding
from ChartMark.annotation_spec.highlight.BaseHighlight import BaseHighlight
from ChartMark.annotation_spec.reference.BaseReference import BaseReference
from ChartMark.annotation_spec.summary.BaseSummary import BaseSummary
from ChartMark.annotation_spec.trend.BaseTrend import BaseTrend
# 注释类型到注释类的映射
ANNOTATION_ROUTER: Dict[str, Type] = {
    # 描述类注释
    "description": BaseDescription,
    
    # 编码类注释
    "encoding": BaseEncoding,
    
    # 高亮类注释
    "highlight": BaseHighlight,
    
    # 引用类注释
    "reference": BaseReference,
    
    # 摘要类注释
    "summary": BaseSummary,
    
    # 趋势类注释
    "trend": BaseTrend,
    
    # 可以在这里添加更多注释类型
}

def get_annotation_class(annotation_type: str) -> Type:
    """
    根据注释类型获取对应的注释类
    
    参数:
        annotation_type: 注释类型
        
    返回:
        对应的注释类
        
    异常:
        ValueError: 不支持的注释类型
    """
    annotation_class = ANNOTATION_ROUTER.get(annotation_type)
    if not annotation_class:
        raise ValueError(f"不支持的注释类型: {annotation_type}")
    return annotation_class

def register_annotation_type(annotation_type: str, annotation_class: Type) -> None:
    """
    注册新的注释类型
    
    参数:
        annotation_type: 注释类型
        annotation_class: 注释类
        
    异常:
        ValueError: 注释类型已存在
    """
    if annotation_type in ANNOTATION_ROUTER:
        raise ValueError(f"注释类型已存在: {annotation_type}")
    ANNOTATION_ROUTER[annotation_type] = annotation_class

def get_supported_annotation_types() -> list:
    """
    获取支持的注释类型列表
    
    返回:
        支持的注释类型列表
    """
    return list(ANNOTATION_ROUTER.keys())
