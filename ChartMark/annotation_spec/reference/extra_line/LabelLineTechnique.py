
from ChartMark.annotation_ast_genetic.target_node.CoordinateTargetNode import CoordinateTargetNode
from ChartMark.annotation_ast_genetic.marker_node.MarkerNode import MarkerNode
from typing import Dict, Optional, Union
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType
from ChartMark.vegalite_ast.ChartNode import Chart
from ChartMark.vegalite_ast.EncodingNode import Encoding
from ChartMark.vegalite_ast.LayerItemNode import LayerItem
from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique

class LabelLineTechnique(BaseTechnique):
    """
    标签线技术类，用于在图表中添加带标签的指示线
    name固定为"label_line"
    target必须是CoordinateTargetNode类型
    marker必须包含line属性，可选包含text属性
    """
    def __init__(self, target: CoordinateTargetNode, 
                 line_color: str = "red", line_size: int = 2, 
                 text_field: Optional[str] = None, text_color: str = "black"):
        """
        初始化标签线技术
        
        参数:
            target: CoordinateTargetNode实例，指定线条的坐标位置
            line_color: 线条颜色，默认为红色
            line_size: 线条大小，默认为2
            text_field: 文本字段，可选参数，如果提供则添加文本标签
            text_color: 文本颜色，默认为黑色
        """
        # 创建包含line的MarkerNode，可选包含text
        marker = MarkerNode()
        marker.add_line_marker(color=line_color, size=line_size)
        
        # 如果提供了text_field，添加文本标记
        if text_field:
            marker.add_text_marker(field=text_field, color=text_color)
        
        # 调用父类初始化方法
        super().__init__(name="label_line", target=target, marker=marker)
        
        # 验证target类型
        if not isinstance(target, CoordinateTargetNode):
            raise ValueError("target必须是CoordinateTargetNode实例")
        
        # 验证坐标设置正确
        self._validate_coordinate()
    
    def _validate_coordinate(self):
        """验证坐标设置是否正确，确保x和y只存在一个，或在极坐标中存在theta"""
        # 检查是否有坐标信息
        has_xy = (hasattr(self.target, 'xyCoordinate') and 
                 self.target.xyCoordinate is not None and 
                 isinstance(self.target.xyCoordinate, dict))
        
        has_polar = (hasattr(self.target, 'polarCoordinate') and 
                    self.target.polarCoordinate is not None and 
                    isinstance(self.target.polarCoordinate, dict))
        
        if not (has_xy or has_polar):
            raise ValueError("target必须包含有效的坐标信息")
        
        # 如果是xy坐标，检查x和y是否只存在一个
        if has_xy:
            has_x = 'x' in self.target.xyCoordinate
            has_y = 'y' in self.target.xyCoordinate
            
            if has_x and has_y:
                raise ValueError("xyCoordinate中x和y只能存在一个")
            
            if not (has_x or has_y):
                raise ValueError("xyCoordinate中必须包含x或y")
                
        # 如果是极坐标，检查是否有theta
        if has_polar:
            has_theta = 'theta' in self.target.polarCoordinate
            
            if not has_theta:
                raise ValueError("polarCoordinate中必须包含theta")
    
    def validate(self) -> bool:
        """
        验证标签线技术是否有效
        规则：
        1. name必须是"label_line"
        2. target必须是CoordinateTargetNode实例
        3. marker必须包含line属性
        """
        # 调用父类验证
        if not super().validate():
            return False
        
        # 检查name是否为"label_line"
        if self.name != "label_line":
            return False
        
        # 检查target是否为CoordinateTargetNode实例
        if not isinstance(self.target, CoordinateTargetNode):
            return False
        
        # 检查marker是否包含line属性
        if not self.marker or not self.marker.line:
            return False
        
        # 验证坐标
        try:
            self._validate_coordinate()
        except ValueError:
            return False
        
        return True
    
    def get_line_color(self) -> str:
        """获取线条颜色"""
        if self.marker and self.marker.line:
            return self.marker.line.color
        return "red"  # 默认颜色
    
    def get_line_size(self) -> int:
        """获取线条大小"""
        if self.marker and self.marker.line:
            return self.marker.line.size
        return 2  # 默认大小
    
    def has_text(self) -> bool:
        """检查是否有文本标记"""
        return self.marker and self.marker.text is not None
    
    def get_text_field(self) -> Optional[str]:
        """获取文本字段，如果没有则返回None"""
        if self.marker and self.marker.text:
            return self.marker.text.field
        return None
    
    def get_text_color(self) -> str:
        """获取文本颜色，如果没有则返回默认值"""
        if self.marker and self.marker.text:
            return self.marker.text.color
        return "black"  # 默认颜色
    
    def set_line_color(self, color: str) -> bool:
        """
        设置线条颜色
        
        参数:
            color: 线条颜色
            
        返回:
            设置是否成功
        """
        if not color or not isinstance(color, str):
            return False
        
        if self.marker and self.marker.line:
            self.marker.line.color = color
            return True
        else:
            # 如果没有marker或line，创建一个
            marker = MarkerNode()
            marker.add_line_marker(color=color, size=2)
            
            # 如果原来有text标记，保留它
            if self.marker and self.marker.text:
                marker.add_text_marker(field=self.marker.text.field, color=self.marker.text.color)
                
            self.marker = marker
            return True
    
    def set_line_size(self, size: int) -> bool:
        """
        设置线条大小
        
        参数:
            size: 线条大小
            
        返回:
            设置是否成功
        """
        if not isinstance(size, int) or size <= 0:
            return False
        
        if self.marker and self.marker.line:
            self.marker.line.size = size
            return True
        else:
            # 如果没有marker或line，创建一个
            marker = MarkerNode()
            marker.add_line_marker(color="red", size=size)
            
            # 如果原来有text标记，保留它
            if self.marker and self.marker.text:
                marker.add_text_marker(field=self.marker.text.field, color=self.marker.text.color)
                
            self.marker = marker
            return True
    
    def set_text_field(self, field: Optional[str]) -> bool:
        """
        设置文本字段，如果传入None则移除文本标记
        
        参数:
            field: 文本字段名或None
            
        返回:
            设置是否成功
        """
        if field is None:
            # 移除文本标记
            if self.marker:
                self.marker.text = None
            return True
        
        if not isinstance(field, str):
            return False
        
        if self.marker:
            if self.marker.text:
                # 更新现有文本标记
                self.marker.text.field = field
            else:
                # 添加新的文本标记
                self.marker.add_text_marker(field=field, color="black")
            return True
        return False
    
    def set_text_color(self, color: str) -> bool:
        """
        设置文本颜色
        
        参数:
            color: 文本颜色
            
        返回:
            设置是否成功
        """
        if not color or not isinstance(color, str):
            return False
        
        if self.marker and self.marker.text:
            self.marker.text.color = color
            return True
        return False
    
    def has_x_coordinate(self) -> bool:
        """检查是否有X坐标"""
        return (self.target.xyCoordinate is not None and 
                isinstance(self.target.xyCoordinate, dict) and 
                'x' in self.target.xyCoordinate)
    
    def has_y_coordinate(self) -> bool:
        """检查是否有Y坐标"""
        return (self.target.xyCoordinate is not None and 
                isinstance(self.target.xyCoordinate, dict) and 
                'y' in self.target.xyCoordinate)
    
    def get_x_coordinate(self) -> Optional[float]:
        """获取X坐标值，如果没有则返回None"""
        if self.has_x_coordinate():
            return self.target.xyCoordinate['x']
        return None
    
    def get_y_coordinate(self) -> Optional[float]:
        """获取Y坐标值，如果没有则返回None"""
        if self.has_y_coordinate():
            return self.target.xyCoordinate['y']
        return None
    
    def set_x_coordinate(self, value: float) -> bool:
        """
        设置X坐标值（并清除Y坐标）
        
        参数:
            value: X坐标值
            
        返回:
            设置是否成功
        """
        if not isinstance(value, (int, float)):
            return False
        
        if not hasattr(self.target, 'xyCoordinate') or self.target.xyCoordinate is None:
            self.target.xyCoordinate = {}
        
        # 清除Y坐标，因为x和y只能存在一个
        if 'y' in self.target.xyCoordinate:
            del self.target.xyCoordinate['y']
            
        self.target.xyCoordinate['x'] = float(value)
        return True
    
    def set_y_coordinate(self, value: float) -> bool:
        """
        设置Y坐标值（并清除X坐标）
        
        参数:
            value: Y坐标值
            
        返回:
            设置是否成功
        """
        if not isinstance(value, (int, float)):
            return False
        
        if not hasattr(self.target, 'xyCoordinate') or self.target.xyCoordinate is None:
            self.target.xyCoordinate = {}
        
        # 清除X坐标，因为x和y只能存在一个
        if 'x' in self.target.xyCoordinate:
            del self.target.xyCoordinate['x']
            
        self.target.xyCoordinate['y'] = float(value)
        return True
    
    def has_polar_coordinate(self) -> bool:
        """检查是否有极坐标"""
        return (hasattr(self.target, 'polarCoordinate') and
                self.target.polarCoordinate is not None and
                isinstance(self.target.polarCoordinate, dict))
    
    def has_theta(self) -> bool:
        """检查是否有theta角度"""
        return (self.has_polar_coordinate() and
                'theta' in self.target.polarCoordinate)
    
    def get_theta(self) -> Optional[float]:
        """获取theta角度值，如果没有则返回None"""
        if self.has_theta():
            return self.target.polarCoordinate['theta']
        return None
    
    def set_theta(self, value: float) -> bool:
        """
        设置theta角度值
        
        参数:
            value: theta角度值
            
        返回:
            设置是否成功
        """
        if not isinstance(value, (int, float)):
            return False
        
        if not hasattr(self.target, 'polarCoordinate') or self.target.polarCoordinate is None:
            self.target.polarCoordinate = {}
            
        self.target.polarCoordinate['theta'] = float(value)
        return True
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'LabelLineTechnique':
        """
        从字典创建LabelLineTechnique实例
        
        参数:
            data: 包含技术配置的字典
            
        返回:
            LabelLineTechnique实例
        """
        # 验证name是否为label_line
        name = data.get("name")
        if name != "label_line":
            raise ValueError("name必须是'label_line'")
        
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
        
        # 验证marker是否包含line
        line_data = marker_data.get("line")
        if not line_data or not isinstance(line_data, dict):
            raise ValueError("marker必须包含line字段")
        
        # 获取line颜色和大小
        line_color = line_data.get("color", "red")
        if not isinstance(line_color, str):
            raise ValueError("line颜色必须是字符串")
            
        line_size = line_data.get("size", 2)
        if not isinstance(line_size, int) or line_size <= 0:
            raise ValueError("line大小必须是正整数")
        
        # 获取可选的text数据
        text_field = None
        text_color = "black"
        
        text_data = marker_data.get("text")
        if text_data and isinstance(text_data, dict):
            text_field = text_data.get("field")
            if not text_field or not isinstance(text_field, str):
                raise ValueError("text字段必须包含有效的field")
            
            text_color = text_data.get("color", "black")
            if not isinstance(text_color, str):
                raise ValueError("text颜色必须是字符串")
        
        # 创建LabelLineTechnique实例
        return cls(
            target=target, 
            line_color=line_color, 
            line_size=line_size,
            text_field=text_field,
            text_color=text_color
        )

    def _render_x_or_y_rule_with_value(
        self, original_vegalite_node: Chart, axis_type, value: Union[int, float]
    ):
        encoding = Encoding()
        encoding.set_datum(axis_type, value)

        mark_type = "rule"
        rule_layer = LayerItem(mark_type, encoding)

        rule_layer.set_mark_property("color", self.get_line_color())
        rule_layer.set_mark_property("size", self.get_line_size())

        original_vegalite_node.add_layer(rule_layer)
   
    def _render_x_or_y_text_with_value(
        self,
        original_vegalite_node: Chart,
        axis_type,
        value: Union[int, float],
        text_content: str
    ):
        mark_type = "text"
        default_color = "red"
        default_baseline = "middle"
        default_align = "left"
        default_dx_or_dy = 3
        
        dx_or_dy = "dx" if axis_type == "y" else "dy"
        dx_or_dy_value = default_dx_or_dy if axis_type == "y" else -default_dx_or_dy
        mark_obj = {
            "type": mark_type,
            "color": default_color,
            "baseline": default_baseline,
            "align": default_align,
            dx_or_dy: dx_or_dy_value
        }
        
        if axis_type == "x":
            mark_obj["angle"] = 300
        
        encoding = Encoding()
        encoding.set_value("text", text_content)
        if axis_type == "y":
            encoding.set_datum("y", value)
            encoding.set_value("x", "width")
        elif axis_type == "x":
            encoding.set_datum("x", value)
            encoding.set_value("y", 0)

        rule_layer = LayerItem(mark_obj, encoding)
            
        original_vegalite_node.add_layer(rule_layer)
        return original_vegalite_node

    def _format_date(self, date_obj: dict) -> str:
        """
        将日期对象字典转换为ISO格式的日期字符串
        
        参数:
            date_obj: 包含year、month和date的字典
            
        返回:
            格式为"YYYY-MM-DD"的日期字符串
        """
        # 月份名称到数字的映射
        month_map = {
            "jan": "01", "feb": "02", "mar": "03", "apr": "04",
            "may": "05", "jun": "06", "jul": "07", "aug": "08",
            "sep": "09", "oct": "10", "nov": "11", "dec": "12"
        }
        
        # 获取年份
        year = str(date_obj.get("year", ""))
        
        # 获取月份并转换为数字
        month_str = date_obj.get("month", "").lower()
        month = month_map.get(month_str, "01")  # 默认为01月
        
        # 获取日期并确保是两位数
        date = str(date_obj.get("date", 1)).zfill(2)
        
        # 返回YYYY-MM-DD格式的日期字符串
        return f"{year}-{month}-{date}"

    def _base_render_xy(self, original_vegalite_node: Chart) -> Chart:
        if self.has_x_coordinate():
            self._render_x_or_y_rule_with_value(original_vegalite_node, "x", self.get_x_coordinate())
            text_content = str(self.get_x_coordinate()) if isinstance(self.get_x_coordinate(), (int, float)) else self._format_date(self.get_x_coordinate())
            self._render_x_or_y_text_with_value(original_vegalite_node, "x", self.get_x_coordinate(), str(text_content))
        if self.has_y_coordinate():
            self._render_x_or_y_rule_with_value(original_vegalite_node, "y", self.get_y_coordinate())
            text_content = str(self.get_y_coordinate()) if isinstance(self.get_y_coordinate(), (int, float)) else self._format_date(self.get_y_coordinate())
            self._render_x_or_y_text_with_value(original_vegalite_node, "y", self.get_y_coordinate(), str(text_content))
        return original_vegalite_node

    def _render_pie_rule(self, original_vegalite_node: Chart, angle_axis: float):
        encoding = Encoding()

        encoding.set_datum("theta", angle_axis)

        mark_type = "arc"
        rule_layer = LayerItem(mark_type, encoding)

        rule_layer.set_mark_property("innerRadius", 1)
        rule_layer.set_mark_property("outerRadius", 80)
        rule_layer.set_mark_property("stroke", self.get_line_color())
        rule_layer.set_mark_property("strokeWidth", self.get_line_size())
        rule_layer.set_mark_property("fillOpacity", 0)    
        

        original_vegalite_node.add_layer(rule_layer)
        return original_vegalite_node
      
    def _render_pie_text(self, original_vegalite_node: Chart, angle_axis: float, text_content: str):
        encoding = Encoding()

        encoding.set_datum("theta", angle_axis)
        encoding.set_value("text", text_content)

        mark_type = "text"
        rule_layer = LayerItem(mark_type, encoding)

        
        rule_layer.set_mark_property("radius", 80)
        rule_layer.set_mark_property("radiusOffset", 12)
        rule_layer.set_mark_property("color", self.get_text_color())
        # rule_layer.set_mark_property("stroke", self.get_line_color())
        # rule_layer.set_mark_property("strokeWidth", self.get_line_size())

        original_vegalite_node.add_layer(rule_layer)
        return original_vegalite_node

    def _base_render_polar(self, original_vegalite_node: Chart) -> Chart:
        if self.has_theta():
            self._render_pie_rule(original_vegalite_node, self.get_theta())
            self._render_pie_text(original_vegalite_node, self.get_theta(), str(self.get_theta()))
        return original_vegalite_node

    def _pie_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        current_vegalite_node = self._base_render_polar(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _bar_parse_to_vegalite(self, original_vegalite_node: Chart)-> Dict: 
        current_vegalite_node = self._base_render_xy(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _line_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        current_vegalite_node = self._base_render_xy(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _scatter_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        current_vegalite_node = self._base_render_xy(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _group_line_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        current_vegalite_node = self._base_render_xy(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _group_bar_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        current_vegalite_node = self._base_render_xy(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _group_scatter_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        current_vegalite_node = self._base_render_xy(original_vegalite_node)
        return current_vegalite_node.to_dict()    


    def parse_to_vegalite(self, original_vegalite_node: Chart, chart_type: ChartType, sub_type: str) -> Dict:
        """
        将技术节点转换为vegalite字典
        
        参数:
            original_vegalite_node: 原始vegalite节点实例
        """
        if chart_type == "pie":
            return self._pie_parse_to_vegalite(original_vegalite_node)
        elif chart_type == "bar":
            return self._bar_parse_to_vegalite(original_vegalite_node)
        elif chart_type == "line":
            return self._line_parse_to_vegalite(original_vegalite_node)
        elif chart_type == "scatter":
            return self._scatter_parse_to_vegalite(original_vegalite_node)
        elif chart_type == "group_line":
            return self._group_line_parse_to_vegalite(original_vegalite_node)
        elif chart_type == "group_bar":
            return self._group_bar_parse_to_vegalite(original_vegalite_node)
        elif chart_type == "group_scatter":
            return self._group_scatter_parse_to_vegalite(original_vegalite_node)

 