from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique
from ChartMark.annotation_ast_genetic.target_node.DataItemTargetNode import DataItemsTargetNode
from ChartMark.annotation_ast_genetic.marker_node.MarkerNode import MarkerNode
from typing import Dict, Optional
from ChartMark.vegalite_ast.ChartNode import Chart
from ChartMark.vegalite_ast.MarkNode import Mark
from ChartMark.vegalite_ast.EncodingNode import Encoding
from ChartMark.vegalite_ast.LayerItemNode import LayerItem
from ChartMark.vegalite_ast.TransformNode import Transform
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType


class StrokeTechnique(BaseTechnique):
    """
    描边技术类，用于在图表中为数据项添加描边标记
    name固定为"stroke"
    target必须是DataItemsTargetNode类型
    marker必须包含stroke属性，可选包含text属性
    """
    def __init__(self, target: DataItemsTargetNode, line_width: int = 2, stroke_color: str = "black", 
                 text_field: Optional[str] = None, text_color: str = "black"):
        """
        初始化描边技术
        
        参数:
            target: DataItemsTargetNode实例，指定要标记的数据项
            line_width: 线宽，默认为2
            stroke_color: 描边颜色，默认为黑色
            text_field: 文本字段，可选参数，如果提供则添加文本标记
            text_color: 文本颜色，默认为黑色
        """
        # 创建包含stroke的MarkerNode，可选包含text
        marker = MarkerNode()
        marker.add_stroke_marker(line_width=line_width, color=stroke_color)
        
        # 如果提供了text_field，添加文本标记
        if text_field:
            marker.add_text_marker(field=text_field, color=text_color)
        
        # 调用父类初始化方法
        super().__init__(name="stroke", target=target, marker=marker)
        
        # 验证target类型
        if not isinstance(target, DataItemsTargetNode):
            raise ValueError("target必须是DataItemsTargetNode实例")
    
    def validate(self) -> bool:
        """
        验证描边技术是否有效
        规则：
        1. name必须是"stroke"
        2. target必须是DataItemsTargetNode实例
        3. marker必须包含stroke属性
        """
        # 调用父类验证
        if not super().validate():
            return False
        
        # 检查name是否为"stroke"
        if self.name != "stroke":
            return False
        
        # 检查target是否为DataItemsTargetNode实例
        if not isinstance(self.target, DataItemsTargetNode):
            return False
        
        # 检查marker是否包含stroke属性
        if not self.marker or not self.marker.stroke:
            return False
        
        return True
    
    def get_stroke_width(self) -> int:
        """获取线宽"""
        if self.marker and self.marker.stroke:
            return self.marker.stroke.width
        return 2
    
    def get_stroke_color(self) -> str:
        """获取描边颜色"""
        if self.marker and self.marker.stroke:
            return self.marker.stroke.color
        return "black"
    
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
    
    def set_stroke_width(self, width: int) -> bool:
        """
        设置线宽
        
        参数:
            width: 线宽
            
        返回:
            设置是否成功
        """
        if not isinstance(width, int) or width <= 0:
            return False
        
        if self.marker and self.marker.stroke:
            self.marker.stroke.width = width
            return True
        else:
            # 如果没有marker或stroke，创建一个
            marker = MarkerNode()
            marker.add_stroke_marker(line_width=width, color="black")
            
            # 如果原来有text标记，保留它
            if self.marker and self.marker.text:
                marker.add_text_marker(field=self.marker.text.field, color=self.marker.text.color)
                
            self.marker = marker
            return True
    
    def set_stroke_color(self, color: str) -> bool:
        """
        设置描边颜色
        
        参数:
            color: 描边颜色
            
        返回:
            设置是否成功
        """
        if not color or not isinstance(color, str):
            return False
        
        if self.marker and self.marker.stroke:
            self.marker.stroke.color = color
            return True
        else:
            # 如果没有marker或stroke，创建一个
            marker = MarkerNode()
            marker.add_stroke_marker(line_width=2, color=color)
            
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

    def _render_xy_stroke_max_min_with_condition(self, original_vegalite_node: Chart, summary_type: str, axis_type: str, is_group: bool = False) -> Chart:
        
        field_info = original_vegalite_node.extract_chart_field_info()
        vegalite_filter = self.target.to_vegalite_filter(field_info)

        # 获取y轴字段
        transform = Transform()
        if vegalite_filter and vegalite_filter!= {}:
          transform.add_filter(vegalite_filter)
          
        summary_item_name = f"{summary_type}_{axis_type}"
        axis_name = original_vegalite_node.get_x_or_y_axis_info_obj(axis_type)["field"]
        transform.add_joinaggregate(summary_type, axis_name, summary_item_name)

        filter_str = f"datum.{axis_name} == datum.{summary_item_name}"
        is_max_min_name = f"is_{summary_type}"
        transform.add_calculate(filter_str,is_max_min_name)

        original_mark_obj = original_vegalite_node.get_layer(0).mark
        
        mark_obj = original_mark_obj
        
        encoding_init_dict = {
            "x": original_vegalite_node.get_x_or_y_axis_info_obj("x"),
            "y": original_vegalite_node.get_x_or_y_axis_info_obj("y"),
        }
        
        if is_group:
            encoding_init_dict["color"] = original_vegalite_node.get_x_or_y_axis_info_obj("color")
            if original_vegalite_node.get_x_or_y_axis_info_obj("xOffset"):
                encoding_init_dict["xOffset"] = original_vegalite_node.get_x_or_y_axis_info_obj("xOffset")

                
        encoding = Encoding.from_dict(encoding_init_dict)
        
        condition_str = f"datum.{is_max_min_name}"
        encoding.set_value_with_condition("stroke", condition_str, self.get_stroke_color(), None)
        encoding.set_value_with_condition("strokeOpacity", condition_str, 1, 0)
        encoding.set_value_with_condition("strokeWidth", condition_str, self.get_stroke_width(), 0)
        encoding.set_value("fillOpacity", 0)

        layer_item = LayerItem(mark_obj, encoding)
        layer_item.set_property(transform=transform.to_dict())
        
        original_vegalite_node.add_layer(layer_item)
        
        return original_vegalite_node

    def _render_xy_text_max_min_with_condition(self, original_vegalite_node: Chart, summary_type: str, axis_type: str, is_group: bool = False) -> Chart:
        field_info = original_vegalite_node.extract_chart_field_info()
        vegalite_filter = self.target.to_vegalite_filter(field_info)

        mark_type = "text"
        default_baseline = "line-bottom"
        
        mark_obj = Mark(
            mark_type= mark_type,
            baseline = default_baseline
        ).to_dict() 

        encoding_init_x_y = {
            "x": original_vegalite_node.get_x_or_y_axis_info_obj("x"),
            "y": original_vegalite_node.get_x_or_y_axis_info_obj("y"),
        }
        if is_group:
            encoding_init_x_y["color"] = original_vegalite_node.get_x_or_y_axis_info_obj("color")
            if original_vegalite_node.get_x_or_y_axis_info_obj("xOffset"):
                encoding_init_x_y["xOffset"] = original_vegalite_node.get_x_or_y_axis_info_obj("xOffset")
            
        encoding = Encoding.from_dict(encoding_init_x_y)
        
        text_layer = LayerItem(mark_obj, encoding)
        
        transform = Transform()
        if vegalite_filter and vegalite_filter != {}:
            transform.add_filter(vegalite_filter)
            text_layer.set_property(transform=transform.to_dict())
            
        summary_item_name = f"{summary_type}_{axis_type}"
        axis_name = original_vegalite_node.get_x_or_y_axis_info_obj(axis_type)["field"]
        transform.add_joinaggregate(summary_type, axis_name, summary_item_name)

        filter_str = f"datum.{axis_name} == datum.{summary_item_name}"
        is_max_min_name = f"is_{summary_type}"
        transform.add_calculate(filter_str,is_max_min_name)

        condition_str = f"datum.{is_max_min_name}"
        encoding.set_value_with_condition("text", condition_str, summary_type, "")
        encoding.set_value("color", self.get_text_color())

        text_layer.set_property(transform=transform.to_dict())
        original_vegalite_node.add_layer(text_layer)
        
        return original_vegalite_node

    def _render_theta_stroke_max_min_with_condition(self, original_vegalite_node: Chart, summary_type: str, axis_type: str) -> Chart:

        # 获取y轴字段
        transform = Transform()
          
        summary_item_name = f"{summary_type}_{axis_type}"
        axis_name = original_vegalite_node.get_x_or_y_axis_info_obj(axis_type)["field"]
        transform.add_joinaggregate(summary_type, axis_name, summary_item_name)

        filter_str = f"datum.{axis_name} == datum.{summary_item_name}"
        is_max_min_name = f"is_{summary_type}"
        transform.add_calculate(filter_str,is_max_min_name)

        original_mark_obj = original_vegalite_node.get_layer(0).mark
        
        mark_obj = original_mark_obj
        
        encoding_init_dict = {
            "theta": original_vegalite_node.get_x_or_y_axis_info_obj("theta"),
            "color": original_vegalite_node.get_x_or_y_axis_info_obj("color"),
        }
                                
        encoding = Encoding.from_dict(encoding_init_dict)
        
        condition_str = f"datum.{is_max_min_name}"
        encoding.set_value_with_condition("stroke", condition_str, self.get_stroke_color(), None)
        encoding.set_value_with_condition("opacity", condition_str, 1, 0)
        encoding.set_value_with_condition("strokeWidth", condition_str, self.get_stroke_width(), 0)
        
        layer_item = LayerItem(mark_obj, encoding)
        layer_item.set_property(transform=transform.to_dict())
        
        original_vegalite_node.add_layer(layer_item)
        
        return original_vegalite_node

    def _render_theta_text_with_condition(self, original_vegalite_node: Chart, summary_type: str, axis_type: str) -> Chart:
      
        mark_type = "text"
        default_radius = 95
        
        mark_obj = Mark(
            mark_type= mark_type,
            radius = default_radius
        ).to_dict() 
      

        encoding_init = {
            "theta": original_vegalite_node.get_x_or_y_axis_info_obj("theta"),
            # "color": original_vegalite_node.get_x_or_y_axis_info_obj("color"),
        }
        encoding = Encoding.from_dict(encoding_init)
            
        transform = Transform()
          
        summary_item_name = f"{summary_type}_{axis_type}"
        axis_name = original_vegalite_node.get_x_or_y_axis_info_obj(axis_type)["field"]
        transform.add_joinaggregate(summary_type, axis_name, summary_item_name)

        filter_str = f"datum.{axis_name} == datum.{summary_item_name}"
        is_max_min_name = f"is_{summary_type}"
        transform.add_calculate(filter_str,is_max_min_name)

        color_name = original_vegalite_node.get_x_or_y_axis_info_obj("color")["field"]
        condition_str = f"datum.{is_max_min_name}"
        encoding.set_value_with_condition("text", condition_str, summary_type, "")
        encoding.set_value_default_field_with_condition("color", color_name, "nominal", condition_str, self.get_text_color())

        layer_item = LayerItem(mark_obj, encoding)
        layer_item.set_property(transform=transform.to_dict())

        original_vegalite_node.add_layer(layer_item)

        return original_vegalite_node


    def _pie_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_theta_stroke_max_min_with_condition(original_vegalite_node, sub_type, "theta")
        current_vegalite_node = self._render_theta_text_with_condition(current_vegalite_node, sub_type, "theta")   
        return current_vegalite_node.to_dict()
    
    def _bar_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict: 
        current_vegalite_node = self._render_xy_stroke_max_min_with_condition(original_vegalite_node, sub_type, "y")
        current_vegalite_node = self._render_xy_text_max_min_with_condition(current_vegalite_node, sub_type, "y")
        return current_vegalite_node.to_dict()
    
    def _line_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_xy_stroke_max_min_with_condition(original_vegalite_node, sub_type, "y")
        current_vegalite_node = self._render_xy_text_max_min_with_condition(current_vegalite_node, sub_type, "y")
        return current_vegalite_node.to_dict()
    
    def _scatter_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_xy_stroke_max_min_with_condition(original_vegalite_node, sub_type, "x")
        current_vegalite_node = self._render_xy_text_max_min_with_condition(current_vegalite_node, sub_type, "x")
        current_vegalite_node = self._render_xy_stroke_max_min_with_condition(original_vegalite_node, sub_type, "y")
        current_vegalite_node = self._render_xy_text_max_min_with_condition(current_vegalite_node, sub_type, "y")
        return current_vegalite_node.to_dict()
    
    def _group_line_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_xy_stroke_max_min_with_condition(original_vegalite_node, sub_type, "y", is_group=True)
        current_vegalite_node = self._render_xy_text_max_min_with_condition(current_vegalite_node, sub_type, "y", is_group=True)
        return current_vegalite_node.to_dict()
    
    def _group_bar_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_xy_stroke_max_min_with_condition(original_vegalite_node, sub_type, "y", is_group=True)
        current_vegalite_node = self._render_xy_text_max_min_with_condition(current_vegalite_node, sub_type, "y", is_group=True)
        return current_vegalite_node.to_dict()
    
    def _group_scatter_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._render_xy_stroke_max_min_with_condition(original_vegalite_node, sub_type, "x", is_group=True)
        current_vegalite_node = self._render_xy_text_max_min_with_condition(current_vegalite_node, sub_type, "x", is_group=True)
        current_vegalite_node = self._render_xy_stroke_max_min_with_condition(original_vegalite_node, sub_type, "y", is_group=True)
        current_vegalite_node = self._render_xy_text_max_min_with_condition(current_vegalite_node, sub_type, "y", is_group=True)
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
    def from_dict(cls, data: Dict) -> 'StrokeTechnique':
        """
        从字典创建StrokeTechnique实例
        
        参数:
            data: 包含技术配置的字典
            
        返回:
            StrokeTechnique实例
        """
        # 验证name是否为stroke
        name = data.get("name")
        if name != "stroke":
            raise ValueError("name必须是'stroke'")
        
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
        
        # 验证marker是否包含stroke
        stroke_data = marker_data.get("stroke")
        if not stroke_data or not isinstance(stroke_data, dict):
            raise ValueError("marker必须包含stroke字段")
        
        # 获取stroke线宽和颜色
        line_width = stroke_data.get("width", 2)
        if not isinstance(line_width, int) or line_width <= 0:
            raise ValueError("线宽必须是正整数")
            
        stroke_color = stroke_data.get("color", "black")
        if not isinstance(stroke_color, str):
            raise ValueError("描边颜色必须是字符串")
        
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
        
        # 创建StrokeTechnique实例
        return cls(
            target=target, 
            line_width=line_width, 
            stroke_color=stroke_color,
            text_field=text_field,
            text_color=text_color
        )
