from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique
from ChartMark.annotation_ast_genetic.target_node.CoordinateTargetNode import CoordinateTargetNode
from ChartMark.annotation_ast_genetic.marker_node.MarkerNode import MarkerNode
from typing import Dict, Optional, Tuple, Union, Literal, Any
from ChartMark.vegalite_ast.MarkNode import Mark
from ChartMark.vegalite_ast.EncodingNode import Encoding
from ChartMark.vegalite_ast.LayerItemNode import LayerItem
from ChartMark.vegalite_ast.TransformNode import Transform
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType
from ChartMark.vegalite_ast.ChartNode import Chart

class ShadowTechnique(BaseTechnique):
    """
    阴影技术类，用于在图表中添加具有阴影效果的范围标注
    name固定为"shadow"
    target必须是CoordinateTargetNode类型
    坐标必须同时包含(x,x1)或(y,y1)范围
    marker只包含rect标记，且rect只需要color和opacity属性
    """
    def __init__(self, target: CoordinateTargetNode, 
                 rect_color: str = "red", rect_opacity: float = 0.5):
        """
        初始化阴影技术
        
        参数:
            target: CoordinateTargetNode实例，指定阴影范围的坐标
            rect_color: 矩形颜色，默认为红色
            rect_opacity: 矩形透明度，默认为0.5
        """
        # 创建MarkerNode，只包含rect
        marker = MarkerNode()
        
        # 添加矩形标记
        marker.add_rect_marker(
            color=rect_color, 
            opacity=rect_opacity, 
            stroke=None, 
            stroke_width=0, 
            corner_radius=0
        )
        
        # 调用父类初始化方法
        super().__init__(name="shadow", target=target, marker=marker)
        
        # 验证target类型
        if not isinstance(target, CoordinateTargetNode):
            raise ValueError("target必须是CoordinateTargetNode实例")
        
        # 验证坐标设置正确
        self._validate_coordinate()
    
    def _is_valid_date_format(self, value: Any) -> bool:
        """
        验证是否为有效的日期格式
        
        参数:
            value: 要验证的值
            
        返回:
            是否为有效的日期格式
        """
        if not isinstance(value, dict):
            return False
            
        # 检查是否包含必要的日期字段
        has_year = 'year' in value and isinstance(value['year'], int)
        
        # 月份可以是字符串(如"jan")或数字(如1)
        has_month = 'month' in value and (isinstance(value['month'], str) or 
                                          isinstance(value['month'], int))
        
        # 日期字段可选
        has_date = 'date' not in value or isinstance(value['date'], int)
        
        return has_year and has_month and has_date
    
    def _compare_dates(self, date1: Dict[str, Any], date2: Dict[str, Any]) -> int:
        """
        比较两个日期格式的大小
        
        参数:
            date1: 第一个日期
            date2: 第二个日期
            
        返回:
            -1: date1 < date2
             0: date1 == date2
             1: date1 > date2
        """
        # 月份名称到数字的映射
        month_map = {
            "jan": 1, "january": 1,
            "feb": 2, "february": 2,
            "mar": 3, "march": 3,
            "apr": 4, "april": 4,
            "may": 5,
            "jun": 6, "june": 6,
            "jul": 7, "july": 7,
            "aug": 8, "august": 8,
            "sep": 9, "september": 9,
            "oct": 10, "october": 10,
            "nov": 11, "november": 11,
            "dec": 12, "december": 12
        }
        
        # 获取年份
        year1 = date1['year']
        year2 = date2['year']
        
        if year1 != year2:
            return -1 if year1 < year2 else 1
        
        # 获取月份并转换为数字
        month1 = date1['month']
        month2 = date2['month']
        
        if isinstance(month1, str):
            month1 = month_map.get(month1.lower(), 0)
        if isinstance(month2, str):
            month2 = month_map.get(month2.lower(), 0)
        
        if month1 != month2:
            return -1 if month1 < month2 else 1
        
        # 获取日期(如果存在)
        date1_val = date1.get('date', 1)
        date2_val = date2.get('date', 1)
        
        if date1_val != date2_val:
            return -1 if date1_val < date2_val else 1
        
        return 0
    
    def _validate_coordinate(self):
        """
        验证坐标设置是否正确，确保同时包含(x,x1)或(y,y1)范围，或在极坐标中同时包含theta和theta2
        支持数值坐标和日期格式坐标
        """
        # 检查是否有坐标信息
        has_xy = (hasattr(self.target, 'xyCoordinate') and 
                 self.target.xyCoordinate is not None and 
                 isinstance(self.target.xyCoordinate, dict))
        
        has_polar = (hasattr(self.target, 'polarCoordinate') and 
                    self.target.polarCoordinate is not None and 
                    isinstance(self.target.polarCoordinate, dict))
        
        if not (has_xy or has_polar):
            raise ValueError("target必须包含有效的坐标信息")
        
        # 如果是xy坐标，检查是否同时包含(x,x1)或(y,y1)范围
        if has_xy:
            has_x_range = ('x' in self.target.xyCoordinate and 'x1' in self.target.xyCoordinate)
            has_y_range = ('y' in self.target.xyCoordinate and 'y1' in self.target.xyCoordinate)
            
            if not (has_x_range or has_y_range):
                raise ValueError("xyCoordinate必须同时包含(x,x1)或(y,y1)范围")
            
            # 验证x和x1
            if has_x_range:
                x = self.target.xyCoordinate['x']
                x1 = self.target.xyCoordinate['x1']
                
                if isinstance(x, (int, float)) and isinstance(x1, (int, float)):
                    # 数值类型，直接比较
                    if x >= x1:
                        raise ValueError("x1必须大于x")
                elif self._is_valid_date_format(x) and self._is_valid_date_format(x1):
                    # 日期格式，使用特殊比较方法
                    if self._compare_dates(x, x1) >= 0:  # x >= x1
                        raise ValueError("x1必须表示晚于x的日期")
                else:
                    # 类型不匹配或无效
                    raise ValueError("x和x1必须同时是数值类型或有效的日期格式")
            
            # 验证y和y1
            if has_y_range:
                y = self.target.xyCoordinate['y']
                y1 = self.target.xyCoordinate['y1']
                
                if isinstance(y, (int, float)) and isinstance(y1, (int, float)):
                    # 数值类型，直接比较
                    if y >= y1:
                        raise ValueError("y1必须大于y")
                elif self._is_valid_date_format(y) and self._is_valid_date_format(y1):
                    # 日期格式，使用特殊比较方法
                    if self._compare_dates(y, y1) >= 0:  # y >= y1
                        raise ValueError("y1必须表示晚于y的日期")
                else:
                    # 类型不匹配或无效
                    raise ValueError("y和y1必须同时是数值类型或有效的日期格式")
        
        # 如果是极坐标，检查是否同时包含theta和theta2
        if has_polar:
            has_theta = 'theta' in self.target.polarCoordinate
            has_theta2 = 'theta2' in self.target.polarCoordinate
            
            if not (has_theta and has_theta2):
                raise ValueError("polarCoordinate必须同时包含theta和theta2")
            
            # 检查值的有效性
            theta = self.target.polarCoordinate['theta']
            theta2 = self.target.polarCoordinate['theta2']
            if not (isinstance(theta, (int, float)) and isinstance(theta2, (int, float))):
                raise ValueError("theta和theta2必须是数值类型")
            if theta >= theta2:
                raise ValueError("theta2必须大于theta")
    
    def validate(self) -> bool:
        """
        验证阴影技术是否有效
        规则：
        1. name必须是"shadow"
        2. target必须是CoordinateTargetNode实例
        3. target必须同时包含(x,x1)或(y,y1)范围
        4. marker必须包含rect标记
        """
        # 调用父类验证
        if not super().validate():
            return False
        
        # 检查name是否为"shadow"
        if self.name != "shadow":
            return False
        
        # 检查target是否为CoordinateTargetNode实例
        if not isinstance(self.target, CoordinateTargetNode):
            return False
        
        # 检查marker是否包含rect
        if not self.marker or not self.marker.rect:
            return False
        
        # 验证坐标
        try:
            self._validate_coordinate()
        except ValueError:
            return False
        
        return True
    
    # Range类型相关方法
    def get_range_type(self) -> Optional[Literal["x", "y", "both", "polar"]]:
        """
        获取范围类型
        
        返回:
            "x": 仅有x范围
            "y": 仅有y范围
            "both": 同时有x和y范围
            "polar": 极坐标范围
            None: 没有有效范围
        """
        # 检查是否有极坐标范围
        if self.has_polar_range():
            return "polar"
            
        # 检查笛卡尔坐标范围
        if not hasattr(self.target, 'xyCoordinate') or not self.target.xyCoordinate:
            return None
            
        has_x_range = ('x' in self.target.xyCoordinate and 'x1' in self.target.xyCoordinate)
        has_y_range = ('y' in self.target.xyCoordinate and 'y1' in self.target.xyCoordinate)
        
        if has_x_range and has_y_range:
            return "both"
        elif has_x_range:
            return "x"
        elif has_y_range:
            return "y"
        else:
            return None
    
    def has_x_range(self) -> bool:
        """检查是否有X范围"""
        if not hasattr(self.target, 'xyCoordinate') or not self.target.xyCoordinate:
            return False
        return 'x' in self.target.xyCoordinate and 'x1' in self.target.xyCoordinate
    
    def has_y_range(self) -> bool:
        """检查是否有Y范围"""
        if not hasattr(self.target, 'xyCoordinate') or not self.target.xyCoordinate:
            return False
        return 'y' in self.target.xyCoordinate and 'y1' in self.target.xyCoordinate
    
    def get_x_range(self) -> Optional[Tuple[Union[float, Dict], Union[float, Dict]]]:
        """
        获取X范围
        
        返回:
            (x, x1)元组，如果没有则返回None
            坐标可以是数值或日期格式
        """
        if self.has_x_range():
            return (self.target.xyCoordinate['x'], self.target.xyCoordinate['x1'])
        return None
    
    def get_y_range(self) -> Optional[Tuple[Union[float, Dict], Union[float, Dict]]]:
        """
        获取Y范围
        
        返回:
            (y, y1)元组，如果没有则返回None
            坐标可以是数值或日期格式
        """
        if self.has_y_range():
            return (self.target.xyCoordinate['y'], self.target.xyCoordinate['y1'])
        return None
    
    def set_x_range(self, start: Union[float, Dict], end: Union[float, Dict]) -> bool:
        """
        设置X范围
        
        参数:
            start: 起始X坐标(数值或日期格式)
            end: 结束X坐标(数值或日期格式)
            
        返回:
            设置是否成功
        """
        # 临时保存旧坐标
        old_coords = None
        if hasattr(self.target, 'xyCoordinate') and self.target.xyCoordinate:
            old_coords = self.target.xyCoordinate.copy()
        
        # 确保坐标字典存在
        if not hasattr(self.target, 'xyCoordinate') or self.target.xyCoordinate is None:
            self.target.xyCoordinate = {}
        
        # 设置新坐标
        self.target.xyCoordinate['x'] = start
        self.target.xyCoordinate['x1'] = end
        
        # 验证坐标
        try:
            self._validate_coordinate()
            return True
        except ValueError:
            # 恢复旧坐标
            if old_coords:
                self.target.xyCoordinate = old_coords
            return False
    
    def set_y_range(self, start: Union[float, Dict], end: Union[float, Dict]) -> bool:
        """
        设置Y范围
        
        参数:
            start: 起始Y坐标(数值或日期格式)
            end: 结束Y坐标(数值或日期格式)
            
        返回:
            设置是否成功
        """
        # 临时保存旧坐标
        old_coords = None
        if hasattr(self.target, 'xyCoordinate') and self.target.xyCoordinate:
            old_coords = self.target.xyCoordinate.copy()
        
        # 确保坐标字典存在
        if not hasattr(self.target, 'xyCoordinate') or self.target.xyCoordinate is None:
            self.target.xyCoordinate = {}
        
        # 设置新坐标
        self.target.xyCoordinate['y'] = start
        self.target.xyCoordinate['y1'] = end
        
        # 验证坐标
        try:
            self._validate_coordinate()
            return True
        except ValueError:
            # 恢复旧坐标
            if old_coords:
                self.target.xyCoordinate = old_coords
            return False
    
    def clear_x_range(self) -> bool:
        """
        清除X范围
        
        返回:
            清除是否成功
        """
        if not hasattr(self.target, 'xyCoordinate') or self.target.xyCoordinate is None:
            return True
        
        if 'x' in self.target.xyCoordinate:
            del self.target.xyCoordinate['x']
        if 'x1' in self.target.xyCoordinate:
            del self.target.xyCoordinate['x1']
        
        # 确保至少还有一个范围
        if not self.has_y_range():
            return False
        
        return True
    
    def clear_y_range(self) -> bool:
        """
        清除Y范围
        
        返回:
            清除是否成功
        """
        if not hasattr(self.target, 'xyCoordinate') or self.target.xyCoordinate is None:
            return True
        
        if 'y' in self.target.xyCoordinate:
            del self.target.xyCoordinate['y']
        if 'y1' in self.target.xyCoordinate:
            del self.target.xyCoordinate['y1']
        
        # 确保至少还有一个范围
        if not self.has_x_range():
            return False
        
        return True
    
    def has_polar_range(self) -> bool:
        """检查是否有极坐标范围"""
        if not hasattr(self.target, 'polarCoordinate') or not self.target.polarCoordinate:
            return False
        return 'theta' in self.target.polarCoordinate and 'theta2' in self.target.polarCoordinate
    
    def get_theta_range(self) -> Optional[Tuple[float, float]]:
        """
        获取极坐标角度范围
        
        返回:
            (theta, theta2)元组，如果没有则返回None
        """
        if self.has_polar_range():
            return (self.target.polarCoordinate['theta'], self.target.polarCoordinate['theta2'])
        return None
    
    def set_theta_range(self, start: float, end: float) -> bool:
        """
        设置极坐标角度范围
        
        参数:
            start: 起始角度
            end: 结束角度
            
        返回:
            设置是否成功
        """
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            return False
        if start >= end:
            return False
        
        if not hasattr(self.target, 'polarCoordinate') or self.target.polarCoordinate is None:
            self.target.polarCoordinate = {}
        
        self.target.polarCoordinate['theta'] = float(start)
        self.target.polarCoordinate['theta2'] = float(end)
        return True
    
    def clear_theta_range(self) -> bool:
        """
        清除极坐标角度范围
        
        返回:
            清除是否成功
        """
        if not hasattr(self.target, 'polarCoordinate') or self.target.polarCoordinate is None:
            return True
        
        if 'theta' in self.target.polarCoordinate:
            del self.target.polarCoordinate['theta']
        if 'theta2' in self.target.polarCoordinate:
            del self.target.polarCoordinate['theta2']
        
        # 确保还有笛卡尔坐标范围
        if not (self.has_x_range() or self.has_y_range()):
            return False
        
        return True
    
    # Rect相关方法
    def get_rect_color(self) -> str:
        """获取矩形颜色"""
        if self.marker and self.marker.rect:
            return self.marker.rect.color
        return "red"  # 默认颜色
    
    def get_rect_opacity(self) -> float:
        """获取矩形透明度"""
        if self.marker and self.marker.rect:
            return self.marker.rect.opacity
        return 0.5  # 默认透明度
    
    def set_rect_color(self, color: str) -> bool:
        """
        设置矩形颜色
        
        参数:
            color: 矩形颜色
            
        返回:
            设置是否成功
        """
        if not color or not isinstance(color, str):
            return False
        
        if self.marker and self.marker.rect:
            self.marker.rect.color = color
            return True
        return False
    
    def set_rect_opacity(self, opacity: float) -> bool:
        """
        设置矩形透明度
        
        参数:
            opacity: 矩形透明度，0到1之间
            
        返回:
            设置是否成功
        """
        if not isinstance(opacity, (int, float)) or not 0 <= opacity <= 1:
            return False
        
        if self.marker and self.marker.rect:
            self.marker.rect.opacity = opacity
            return True
        return False
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ShadowTechnique':
        """
        从字典创建ShadowTechnique实例
        
        参数:
            data: 包含技术配置的字典
            
        返回:
            ShadowTechnique实例
        """
        # 验证name是否为shadow
        name = data.get("name")
        if name != "shadow":
            raise ValueError("name必须是'shadow'")
        
        # 获取target数据
        target_data = data.get("target")
        if not target_data or not isinstance(target_data, dict):
            raise ValueError("target字段必须是有效的字典")
        
        # 验证target类型
        target_type = target_data.get("type")
        if target_type != "coordinate":
            raise ValueError("target类型必须是'coordinate'")
        
        # 创建CoordinateTargetNode
        target = CoordinateTargetNode(target_data)
        
        # 获取marker数据
        marker_data = data.get("marker")
        if not marker_data or not isinstance(marker_data, dict):
            raise ValueError("marker字段必须是有效的字典")
        
        # 验证marker是否包含rect
        rect_data = marker_data.get("rect")
        if not rect_data or not isinstance(rect_data, dict):
            raise ValueError("marker必须包含rect字段")
        
        # 获取rect的color和opacity
        rect_color = rect_data.get("color", "red")
        if not isinstance(rect_color, str):
            raise ValueError("rect颜色必须是字符串")
            
        rect_opacity = rect_data.get("opacity", 0.5)
        if not isinstance(rect_opacity, (int, float)) or not 0 <= rect_opacity <= 1:
            raise ValueError("rect透明度必须是0到1之间的数值")
        
        # 创建ShadowTechnique实例
        return cls(
            target=target, 
            rect_color=rect_color, 
            rect_opacity=rect_opacity
        )

    def _render_xy_area_rect(self, original_vegalite_node: Chart) -> Chart:
        encoding = Encoding()
        if self.has_y_range():
          encoding.set_datum("y", self.target.xyCoordinate["y"])
          encoding.set_datum("y2", self.target.xyCoordinate["y1"])
        elif self.has_x_range():
          encoding.set_datum("x", self.target.xyCoordinate["x"])
          encoding.set_datum("x2", self.target.xyCoordinate["x1"])

        mark_type = "rect"
        rule_layer = LayerItem(mark_type, encoding)

        rule_layer.set_mark_property("color", self.get_rect_color())
        rule_layer.set_mark_property("opacity", self.get_rect_opacity())

        original_vegalite_node.add_layer(rule_layer)
        return original_vegalite_node

    def _render_polar_area_rect(self, original_vegalite_node: Chart) -> Chart:
        encoding = Encoding()
        encoding.set_datum("theta", self.target.polarCoordinate["theta"])
        encoding.set_datum("theta2", self.target.polarCoordinate["theta2"])

        mark_type = "arc"
        rule_layer = LayerItem(mark_type, encoding)

        rule_layer.set_mark_property("innerRadius", 1)
        rule_layer.set_mark_property("outerRadius", 90)
        # rule_layer.set_mark_property("stroke", "black")
        # rule_layer.set_mark_property("strokeWidth", 3)
        rule_layer.set_mark_property("fillOpacity", self.get_rect_opacity())
        rule_layer.set_mark_property("color", self.get_rect_color())

        original_vegalite_node.add_layer(rule_layer)
        return original_vegalite_node

    def _pie_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_polar_area_rect(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _bar_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict: 
        current_vegalite_node = self._render_xy_area_rect(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _line_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_xy_area_rect(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _scatter_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_xy_area_rect(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _group_line_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_xy_area_rect(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _group_bar_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_xy_area_rect(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _group_scatter_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_xy_area_rect(original_vegalite_node)
        return current_vegalite_node.to_dict()     
        
    def parse_to_vegalite(self, original_vegalite_node: Chart, chart_type: ChartType, sub_type: str) -> Dict:
        """
        将技术节点转换为vegalite字典
        
        参数:
            original_vegalite_node: 原始vegalite节点实例
        """
        if chart_type == "pie":
            return self._pie_parse_to_vegalite(original_vegalite_node, sub_type)
        elif chart_type == "bar":
            return self._bar_parse_to_vegalite(original_vegalite_node, sub_type)
        elif chart_type == "line":
            return self._line_parse_to_vegalite(original_vegalite_node, sub_type)
        elif chart_type == "scatter":
            return self._scatter_parse_to_vegalite(original_vegalite_node, sub_type)
        elif chart_type == "group_line":
            return self._group_line_parse_to_vegalite(original_vegalite_node, sub_type)
        elif chart_type == "group_bar":
            return self._group_bar_parse_to_vegalite(original_vegalite_node, sub_type)
        elif chart_type == "group_scatter":
            return self._group_scatter_parse_to_vegalite(original_vegalite_node, sub_type)

