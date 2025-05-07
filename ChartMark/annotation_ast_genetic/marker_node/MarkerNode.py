from ChartMark.annotation_ast_genetic.ast_base import BaseNode
from typing import Dict, List, Literal, Optional, Union, Type, Any
from dataclasses import dataclass, field
from ChartMark.annotation_ast_genetic.marker_node.SubTextNode import TextMarker
from ChartMark.annotation_ast_genetic.marker_node.SubLineNode import LineMarker
from ChartMark.annotation_ast_genetic.marker_node.SubRectNode import RectMarker
from ChartMark.annotation_ast_genetic.marker_node.SubStrokeNode import StrokeMarker
from ChartMark.annotation_ast_genetic.marker_node.SubOpacityNode import OpacityMarker

# 标记类型
MarkerType = Literal["text", "line", "rect", "stroke", "opacity"]


class MarkerNode(BaseNode):
    """
    标记节点，可以包含多种类型的标记（文本、线条、矩形、描边、透明度）
    以及自定义的键值对
    """
    def __init__(self, marker_obj: Dict = None):
        super().__init__()
        self.text: Optional[TextMarker] = None
        self.line: Optional[LineMarker] = None
        self.rect: Optional[RectMarker] = None
        self.stroke: Optional[StrokeMarker] = None
        self.opacity: Optional[OpacityMarker] = None
        self._custom_attributes: Dict[str, Any] = {}
        
        if marker_obj:
            self._parse_marker_obj(marker_obj)
    
    def _parse_marker_obj(self, marker_obj: Dict):
        """解析标记对象"""
        if not isinstance(marker_obj, dict):
            raise ValueError("标记对象必须是字典类型")
        
        # 解析各种类型的标记
        if "text" in marker_obj:
            text_data = marker_obj.get("text")
            if isinstance(text_data, dict):
                self.text = TextMarker(text_data)
            else:
                raise ValueError("text标记必须是字典类型")
        
        if "line" in marker_obj:
            line_data = marker_obj.get("line")
            if isinstance(line_data, dict):
                self.line = LineMarker(line_data)
            else:
                raise ValueError("line标记必须是字典类型")
        
        if "rect" in marker_obj:
            rect_data = marker_obj.get("rect")
            if isinstance(rect_data, dict):
                self.rect = RectMarker(rect_data)
            else:
                raise ValueError("rect标记必须是字典类型")
        
        if "stroke" in marker_obj:
            stroke_data = marker_obj.get("stroke")
            if isinstance(stroke_data, dict):
                self.stroke = StrokeMarker(stroke_data)
            else:
                raise ValueError("stroke标记必须是字典类型")
        
        if "opacity" in marker_obj:
            opacity_data = marker_obj.get("opacity")
            if isinstance(opacity_data, dict):
                self.opacity = OpacityMarker(opacity_data)
            else:
                raise ValueError("opacity标记必须是字典类型")
        
        # 解析自定义属性（排除已知的标记类型）
        known_marker_types = {"text", "line", "rect", "stroke", "opacity"}
        for key, value in marker_obj.items():
            if key not in known_marker_types:
                self._custom_attributes[key] = value
        
        # 至少需要一种标记或自定义属性
        if not (self.text or self.line or self.rect or self.stroke or self.opacity or self._custom_attributes):
            raise ValueError("标记节点必须包含至少一种标记类型或自定义属性")
    
    def to_dict(self) -> Dict:
        """将节点转换为字典格式"""
        result = {}
        
        if self.text:
            result["text"] = self.text.to_dict()
        
        if self.line:
            result["line"] = self.line.to_dict()
        
        if self.rect:
            result["rect"] = self.rect.to_dict()
        
        if self.stroke:
            result["stroke"] = self.stroke.to_dict()
        
        if self.opacity:
            result["opacity"] = self.opacity.to_dict()
        
        # 添加自定义属性
        for key, value in self._custom_attributes.items():
            result[key] = value
        
        return result
    
    def add_text_marker(self, field: str, color: str = "black"):
        """添加文本标记"""
        self.text = TextMarker({"field": field, "color": color})
    
    def add_line_marker(self, color: str = "red", size: int = 2):
        """添加线条标记"""
        self.line = LineMarker({"color": color, "size": size})
    
    def add_rect_marker(self, color: str = "red", opacity: float = 0.5, 
                      stroke: str = "gray", stroke_width: int = 2, corner_radius: int = 4):
        """添加矩形标记"""
        self.rect = RectMarker({
            "color": color,
            "opacity": opacity,
            "stroke": stroke,
            "strokeWidth": stroke_width,
            "cornerRadius": corner_radius
        })
    
    def add_stroke_marker(self, line_width: int = 2, color: str = "black"):
        """添加描边标记"""
        self.stroke = StrokeMarker({
            "lineWidth": line_width,
            "color": color
        })
    
    def add_opacity_marker(self, selected: float = 1.0, other: float = 0.5):
        """添加透明度标记"""
        self.opacity = OpacityMarker({
            "selected": selected,
            "other": other
        })
    
    def set_attribute(self, key: str, value: Any):
        """
        设置自定义属性
        
        参数:
            key: 属性名
            value: 属性值
        """
        self._custom_attributes[key] = value
    
    def get_attribute(self, key: str, default: Any = None) -> Any:
        """
        获取自定义属性
        
        参数:
            key: 属性名
            default: 如果属性不存在，返回的默认值
            
        返回:
            属性值，如果不存在则返回默认值
        """
        return self._custom_attributes.get(key, default)
    
    def has_attribute(self, key: str) -> bool:
        """
        检查是否存在指定的自定义属性
        
        参数:
            key: 属性名
            
        返回:
            如果属性存在返回True，否则返回False
        """
        return key in self._custom_attributes
    
    def remove_attribute(self, key: str) -> bool:
        """
        移除指定的自定义属性
        
        参数:
            key: 属性名
            
        返回:
            如果属性存在并被成功移除返回True，否则返回False
        """
        if key in self._custom_attributes:
            del self._custom_attributes[key]
            return True
        return False
    
    def get_all_attributes(self) -> Dict[str, Any]:
        """
        获取所有自定义属性
        
        返回:
            包含所有自定义属性的字典
        """
        return self._custom_attributes.copy()
