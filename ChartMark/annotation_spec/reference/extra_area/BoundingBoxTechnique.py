from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique
from ChartMark.annotation_ast_genetic.target_node.CoordinateTargetNode import CoordinateTargetNode
from ChartMark.annotation_ast_genetic.marker_node.MarkerNode import MarkerNode
from typing import Dict, Optional, Tuple, Any, Union
from ChartMark.vegalite_ast.ChartNode import Chart
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType
from ChartMark.vegalite_ast.EncodingNode import Encoding
from ChartMark.vegalite_ast.LayerItemNode import LayerItem
from ChartMark.vegalite_ast.TransformNode import Transform

class BoundingBoxTechnique(BaseTechnique):
    """
    边界框技术类，用于在图表中添加矩形边界框
    name固定为"bounding_box"
    target必须是CoordinateTargetNode类型
    坐标必须同时包含x、x1、y、y1所有四个点
    marker只包含rect中的stroke和strokeWidth属性
    """
    def __init__(self, target: CoordinateTargetNode, 
                 stroke: str = "gray", stroke_width: int = 2):
        """
        初始化边界框技术
        
        参数:
            target: CoordinateTargetNode实例，指定边界框的坐标
            stroke: 边框颜色，默认为灰色
            stroke_width: 边框宽度，默认为2
        """
        # 创建MarkerNode，只包含rect
        marker = MarkerNode()
        
        # 添加矩形标记
        marker.add_rect_marker(
            color="transparent", 
            opacity=0, 
            stroke=stroke, 
            stroke_width=stroke_width, 
            corner_radius=0
        )
        
        # 调用父类初始化方法
        super().__init__(name="bounding_box", target=target, marker=marker)
        
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
        验证坐标设置是否正确，确保同时包含x、x1、y、y1所有四个点
        支持数值坐标和日期格式坐标
        """
        # 检查是否有坐标信息
        has_xy = (hasattr(self.target, 'xyCoordinate') and 
                 self.target.xyCoordinate is not None and 
                 isinstance(self.target.xyCoordinate, dict))
        
        if not has_xy:
            raise ValueError("target必须包含有效的xyCoordinate")
        
        # 检查是否同时包含x、x1、y、y1所有四个点
        has_x = 'x' in self.target.xyCoordinate
        has_x1 = 'x1' in self.target.xyCoordinate
        has_y = 'y' in self.target.xyCoordinate
        has_y1 = 'y1' in self.target.xyCoordinate
        
        if not (has_x and has_x1 and has_y and has_y1):
            raise ValueError("xyCoordinate必须同时包含x、x1、y、y1所有四个点")
        
        # 获取坐标值
        x = self.target.xyCoordinate['x']
        x1 = self.target.xyCoordinate['x1']
        y = self.target.xyCoordinate['y']
        y1 = self.target.xyCoordinate['y1']
        
        # 验证x和x1
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
    
    def validate(self) -> bool:
        """
        验证边界框技术是否有效
        规则：
        1. name必须是"bounding_box"
        2. target必须是CoordinateTargetNode实例
        3. target必须同时包含x、x1、y、y1所有四个点
        4. marker必须包含rect标记
        """
        # 调用父类验证
        if not super().validate():
            return False
        
        # 检查name是否为"bounding_box"
        if self.name != "bounding_box":
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
    
    # 边界框坐标相关方法
    def get_box_coordinates(self) -> Tuple[Union[float, Dict], Union[float, Dict], Union[float, Dict], Union[float, Dict]]:
        """
        获取边界框坐标
        
        返回:
            (x, x1, y, y1)元组，表示边界框的左上角和右下角坐标
            坐标可以是数值或日期格式
        """
        if not hasattr(self.target, 'xyCoordinate') or not self.target.xyCoordinate:
            return (0, 0, 0, 0)
            
        x = self.target.xyCoordinate.get('x', 0)
        x1 = self.target.xyCoordinate.get('x1', 0)
        y = self.target.xyCoordinate.get('y', 0)
        y1 = self.target.xyCoordinate.get('y1', 0)
        
        return (x, x1, y, y1)
    
    def get_width(self) -> Optional[float]:
        """
        获取边界框宽度，只有当x和x1都是数值时才有意义
        
        返回:
            边界框宽度，如果x或x1不是数值则返回None
        """
        x, x1, _, _ = self.get_box_coordinates()
        if isinstance(x, (int, float)) and isinstance(x1, (int, float)):
            return x1 - x
        return None
    
    def get_height(self) -> Optional[float]:
        """
        获取边界框高度，只有当y和y1都是数值时才有意义
        
        返回:
            边界框高度，如果y或y1不是数值则返回None
        """
        _, _, y, y1 = self.get_box_coordinates()
        if isinstance(y, (int, float)) and isinstance(y1, (int, float)):
            return y1 - y
        return None
    
    def set_box_coordinates(self, x: Union[float, Dict], x1: Union[float, Dict], 
                          y: Union[float, Dict], y1: Union[float, Dict]) -> bool:
        """
        设置边界框坐标
        
        参数:
            x: 左上角x坐标(数值或日期格式)
            x1: 右下角x坐标(数值或日期格式)
            y: 左上角y坐标(数值或日期格式)
            y1: 右下角y坐标(数值或日期格式)
            
        返回:
            设置是否成功
        """
        # 临时存储新坐标
        new_coords = {
            'x': x,
            'x1': x1,
            'y': y,
            'y1': y1
        }
        
        # 备份原坐标
        old_coords = None
        if hasattr(self.target, 'xyCoordinate') and self.target.xyCoordinate:
            old_coords = self.target.xyCoordinate.copy()
        
        # 设置新坐标
        self.target.xyCoordinate = new_coords
        
        # 验证新坐标是否有效
        try:
            self._validate_coordinate()
            return True
        except ValueError:
            # 恢复原坐标
            if old_coords:
                self.target.xyCoordinate = old_coords
            return False
    
    # 边框样式相关方法
    def get_stroke(self) -> str:
        """获取边框颜色"""
        if self.marker and self.marker.rect:
            return self.marker.rect.stroke
        return "gray"  # 默认颜色
    
    def get_stroke_width(self) -> int:
        """获取边框宽度"""
        if self.marker and self.marker.rect:
            return self.marker.rect.strokeWidth
        return 2  # 默认宽度
    
    def set_stroke(self, color: str) -> bool:
        """
        设置边框颜色
        
        参数:
            color: 边框颜色
            
        返回:
            设置是否成功
        """
        if not color or not isinstance(color, str):
            return False
        
        if self.marker and self.marker.rect:
            self.marker.rect.stroke = color
            return True
        return False
    
    def set_stroke_width(self, width: int) -> bool:
        """
        设置边框宽度
        
        参数:
            width: 边框宽度
            
        返回:
            设置是否成功
        """
        if not isinstance(width, int) or width < 0:
            return False
        
        if self.marker and self.marker.rect:
            self.marker.rect.strokeWidth = width
            return True
        return False
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BoundingBoxTechnique':
        """
        从字典创建BoundingBoxTechnique实例
        
        参数:
            data: 包含技术配置的字典
            
        返回:
            BoundingBoxTechnique实例
        """
        # 验证name是否为bounding_box
        name = data.get("name")
        if name != "bounding_box":
            raise ValueError("name必须是'bounding_box'")
        
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
        
        # 获取rect的stroke和strokeWidth
        stroke = rect_data.get("stroke", "gray")
        if not isinstance(stroke, str):
            raise ValueError("stroke必须是字符串")
            
        stroke_width = rect_data.get("strokeWidth", 2)
        if not isinstance(stroke_width, int) or stroke_width < 0:
            raise ValueError("strokeWidth必须是非负整数")
        
        # 创建BoundingBoxTechnique实例
        return cls(
            target=target, 
            stroke=stroke, 
            stroke_width=stroke_width
        )

    def _render_xy_area_rect(self, original_vegalite_node: Chart) -> Chart:
        encoding = Encoding()
        encoding.set_datum("y", self.target.xyCoordinate["y"])
        encoding.set_datum("y2", self.target.xyCoordinate["y1"])
        encoding.set_datum("x", self.target.xyCoordinate["x"])
        encoding.set_datum("x2", self.target.xyCoordinate["x1"])

        mark_type = "rect"
        rule_layer = LayerItem(mark_type, encoding)

        rule_layer.set_mark_property("fillOpacity", 0)
        rule_layer.set_mark_property("stroke", self.get_stroke())
        rule_layer.set_mark_property("strokeWidth", self.get_stroke_width())

        original_vegalite_node.add_layer(rule_layer)
        return original_vegalite_node

    def _line_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_xy_area_rect(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _scatter_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_xy_area_rect(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _group_line_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
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
        if chart_type == "line":
            return self._line_parse_to_vegalite(original_vegalite_node, sub_type)
        elif chart_type == "scatter":
            return self._scatter_parse_to_vegalite(original_vegalite_node, sub_type)
        elif chart_type == "group_line":
            return self._group_line_parse_to_vegalite(original_vegalite_node, sub_type)
        elif chart_type == "group_scatter":
            return self._group_scatter_parse_to_vegalite(original_vegalite_node, sub_type)

