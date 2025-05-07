from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique
from ChartMark.annotation_ast_genetic.target_node.DataItemTargetNode import DataItemsTargetNode
from ChartMark.annotation_ast_genetic.marker_node.MarkerNode import MarkerNode
from typing import Dict, Optional
from ChartMark.vegalite_ast.TransformNode import Transform
from ChartMark.vegalite_ast.EncodingNode import Encoding
from ChartMark.vegalite_ast.LayerItemNode import LayerItem
from ChartMark.vegalite_ast.MarkNode import Mark
from ChartMark.vegalite_ast.ChartNode import Chart
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType


class LineTechnique(BaseTechnique):
    """
    线条技术类，用于在图表中为数据项添加线条标记
    name固定为"line"
    target必须是DataItemsTargetNode类型
    marker必须包含line属性，可选包含text属性
    """
    def __init__(self, target: DataItemsTargetNode, line_color: str = "red", line_size: int = 2, 
                 text_field: Optional[str] = None, text_color: str = "black"):
        """
        初始化线条技术
        
        参数:
            target: DataItemsTargetNode实例，指定要标记的数据项
            line_color: 线条颜色，默认为红色
            line_size: 线条大小，默认为2
            text_field: 文本字段，可选参数，如果提供则添加文本标记
            text_color: 文本颜色，默认为黑色
        """
        # 创建包含line的MarkerNode，可选包含text
        marker = MarkerNode()
        marker.add_line_marker(color=line_color, size=line_size)
        
        # 如果提供了text_field，添加文本标记
        if text_field:
            marker.add_text_marker(field=text_field, color=text_color)
        
        # 调用父类初始化方法
        super().__init__(name="line", target=target, marker=marker)
        
        # 验证target类型
        if not isinstance(target, DataItemsTargetNode):
            raise ValueError("target必须是DataItemsTargetNode实例")
    
    def validate(self) -> bool:
        """
        验证线条技术是否有效
        规则：
        1. name必须是"label_line"
        2. target必须是DataItemsTargetNode实例
        3. marker必须包含line属性
        """
        # 调用父类验证
        if not super().validate():
            return False
        
        # 检查name是否为"label_line"
        if self.name != "label_line":
            return False
        
        # 检查target是否为DataItemsTargetNode实例
        if not isinstance(self.target, DataItemsTargetNode):
            return False
        
        # 检查marker是否包含line属性
        if not self.marker or not self.marker.line:
            return False
        
        return True
    
    def get_line_color(self) -> str:
        """获取线条颜色"""
        if self.marker and self.marker.line:
            return self.marker.line.color
        return "red"
    
    def get_line_size(self) -> int:
        """获取线条大小"""
        if self.marker and self.marker.line:
            return self.marker.line.size
        return 2
    
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
        return "black"
    
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

    def _render_summary_arc(self, original_vegalite_node: Chart, summary_type: str) -> Chart:
      axis_type = "theta"
      
      transform = Transform()
      summary_item_name = f"{summary_type}_{axis_type}"
      axis_name = original_vegalite_node.get_x_or_y_axis_info_obj(axis_type)["field"]
      transform.add_aggregate(summary_type, axis_name, summary_item_name)
      
      mark_type = "arc"
      default_innerRadius = 85
      # default_outerRadius = 100
      # default_color = "red"
      default_opacity = 0.7
      default_corner_radius = 2
      mark_obj = {
        "type": mark_type,
        "innerRadius": default_innerRadius,
        "outerRadius": default_innerRadius + self.get_line_size(),
        "color": self.get_line_color(),
        "opacity": default_opacity,
        "cornerRadius": default_corner_radius
      }
      
      encoding = Encoding()
      encoding.set_field(axis_type, summary_item_name, "quantitative")
      
      new_layer = LayerItem(mark_obj, encoding)
      new_layer.set_property(transform=transform.to_dict())
    
      original_vegalite_node.add_layer(new_layer)
      return original_vegalite_node

    def _render_summary_arc_text(self, original_vegalite_node: Chart, summary_type: str) -> Chart:
      axis_type = "theta"
      
      transform = Transform()
      summary_item_name = f"{summary_type}_{axis_type}"
      axis_name = original_vegalite_node.get_x_or_y_axis_info_obj(axis_type)["field"]
      transform.add_aggregate(summary_type, axis_name, summary_item_name)
      
      summary_calculate_string = f"'{summary_type}:' + format(datum['{summary_item_name}'], '.2f')"
      summary_calculate_text_name = f"{summary_type}_label"
      transform.add_calculate(summary_calculate_string, summary_calculate_text_name)

      mark_type = "text"
      default_radius = 100
      default_radius_offset = 10
      mark_obj = {
        "type": mark_type,
        "radius": default_radius,
        "radiusOffset": default_radius_offset,
        "color": self.get_text_color()
      }
      
      encoding = Encoding()
      encoding.set_field("theta", summary_item_name, "quantitative", stack = True)
      encoding.set_field('text', summary_calculate_text_name, "nominal")
      
      rule_layer = LayerItem(mark_obj, encoding)
      rule_layer.set_property(transform=transform.to_dict())
    
      original_vegalite_node.add_layer(rule_layer)
      return original_vegalite_node
    
    def _render_summary_rule_with_condition(self, original_vegalite_node: Chart, summary_type: str, axis_type: str) -> Chart:
      field_info = original_vegalite_node.extract_chart_field_info()
      vegalite_filter = self.target.to_vegalite_filter(field_info)

      transform = Transform()
      if vegalite_filter and vegalite_filter!= {}:
        transform.add_filter(vegalite_filter)
      summary_item_name = f"{summary_type}_{axis_type}"
      axis_name = original_vegalite_node.get_x_or_y_axis_info_obj(axis_type)["field"]
      transform.add_aggregate(summary_type, axis_name, summary_item_name)
      
      mark_type = "rule"
      mark_obj = {
        "type": mark_type,
        "color": self.get_line_color(),
        "size": self.get_line_size(),
      }
      
      encoding = Encoding()
      encoding.set_field(axis_type, summary_item_name, "quantitative")
      
      rule_layer = LayerItem(mark_obj, encoding)
      rule_layer.set_property(transform=transform.to_dict())
      
      original_vegalite_node.add_layer(rule_layer)
      return original_vegalite_node
    
    def _render_summary_text_with_condition(self, original_vegalite_node: Chart, summary_type:str, axis_type: str) -> Chart:
      field_info = original_vegalite_node.extract_chart_field_info()
      vegalite_filter = self.target.to_vegalite_filter(field_info)
      
      transform = Transform()
      if vegalite_filter and vegalite_filter!= {}:
        transform.add_filter(vegalite_filter)
      # summary_item_name = f"{summary_type}_{axis_type}"
      summary_item_name = f"{summary_type}_{axis_type}"
      axis_name = original_vegalite_node.get_x_or_y_axis_info_obj(axis_type)["field"]
      transform.add_aggregate(summary_type, axis_name, summary_item_name)
      
      mark_type = "text"
      default_color = self.get_text_color()
      default_baseline = "middle"
      default_align = "left"
      default_dx_or_dy = 3
      
      dx_or_dy = "dx" if axis_type == "y" else "dy"
      dx_or_dy_value = default_dx_or_dy if axis_type == "y" else -default_dx_or_dy
      other_axis_type = "x" if axis_type == "y" else "y"
      other_axis_value = "width" if other_axis_type == "x" else 0
      
      
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
      encoding.set_field(axis_type, summary_item_name, "quantitative")
      encoding.set_value("text", summary_type)
      encoding.set_value(other_axis_type, other_axis_value)
      
      rule_layer = LayerItem(mark_obj, encoding)
      rule_layer.set_property(transform=transform.to_dict())
      
      original_vegalite_node.add_layer(rule_layer)
      return original_vegalite_node


    def _pie_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_summary_arc(original_vegalite_node, sub_type)
        current_vegalite_node = self._render_summary_arc_text(current_vegalite_node, sub_type)   
        return current_vegalite_node.to_dict()
    
    def _bar_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict: 
        current_vegalite_node = self._render_summary_rule_with_condition(original_vegalite_node, sub_type, "y")
        current_vegalite_node = self._render_summary_text_with_condition(current_vegalite_node, sub_type, "y")
        return current_vegalite_node.to_dict()
    
    def _line_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_summary_rule_with_condition(original_vegalite_node, sub_type, "y")
        current_vegalite_node = self._render_summary_text_with_condition(current_vegalite_node, sub_type, "y")
        return current_vegalite_node.to_dict()
    
    def _scatter_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_summary_rule_with_condition(original_vegalite_node, sub_type, "x")
        current_vegalite_node = self._render_summary_text_with_condition(current_vegalite_node, sub_type, "x")
        current_vegalite_node = self._render_summary_rule_with_condition(original_vegalite_node, sub_type, "y")
        current_vegalite_node = self._render_summary_text_with_condition(current_vegalite_node, sub_type, "y")
        return current_vegalite_node.to_dict()
    
    def _group_line_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_summary_rule_with_condition(original_vegalite_node, sub_type, "y")
        current_vegalite_node = self._render_summary_text_with_condition(current_vegalite_node, sub_type, "y")
        return current_vegalite_node.to_dict()
    
    def _group_bar_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_summary_rule_with_condition(original_vegalite_node, sub_type, "y")
        current_vegalite_node = self._render_summary_text_with_condition(current_vegalite_node, sub_type, "y")
        return current_vegalite_node.to_dict()
    
    def _group_scatter_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_summary_rule_with_condition(original_vegalite_node, sub_type, "x")
        current_vegalite_node = self._render_summary_text_with_condition(current_vegalite_node, sub_type, "x")
        current_vegalite_node = self._render_summary_rule_with_condition(original_vegalite_node, sub_type, "y")
        current_vegalite_node = self._render_summary_text_with_condition(current_vegalite_node, sub_type, "y")
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

    
    @classmethod
    def from_dict(cls, data: Dict) -> 'LineTechnique':
        """
        从字典创建LineTechnique实例
        
        参数:
            data: 包含技术配置的字典
            
        返回:
            LineTechnique实例
        """
        # 验证name是否为line
        name = data.get("name")
        if name != "label_line":
            raise ValueError("name必须是'label_line'")
        
        # 获取target数据
        target_data = data.get("target")
        if not target_data or not isinstance(target_data, dict):
            raise ValueError("target字段必须是有效的字典")
        
        # 验证target类型
        target_type = target_data.get("type")
        if target_type != "data_items":
            raise ValueError("target类型必须是'data_items'")
        
        # 创建DataItemsTargetNode
        target = DataItemsTargetNode(target_data)
        
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
        
        # 创建LineTechnique实例
        return cls(
            target=target, 
            line_color=line_color, 
            line_size=line_size,
            text_field=text_field,
            text_color=text_color
        )
