
from ChartMark.annotation_ast_genetic.target_node.DataItemTargetNode import DataItemsTargetNode
from ChartMark.annotation_ast_genetic.marker_node.MarkerNode import MarkerNode
from ChartMark.annotation_ast_genetic.data_node.ExternalDataNode import ExternalDataNode
from typing import Dict, Optional, Union
from ChartMark.vegalite_ast.ChartNode import Chart
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType
from ChartMark.vegalite_ast.TransformNode import Transform
from ChartMark.vegalite_ast.EncodingNode import Encoding
from ChartMark.vegalite_ast.LayerItemNode import LayerItem
from ChartMark.annotation_spec.description.utils import calculate_texts_width_and_height
from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique

class InPlotTechnique(BaseTechnique):
    """
    图内注释技术类，用于在图表内部添加注释
    name固定为"in_plot"
    target必须是DataItemsTargetNode类型
    marker可同时包含stroke、text和rect属性
    data必须是ExternalDataNode类型，用于提供外部数据
    """
    def __init__(self, target: DataItemsTargetNode, 
                 stroke_width: int = 2, stroke_color: str = "black",
                 text_field: Optional[str] = None, text_color: Optional[str] = "black",
                 rect_color: Optional[str] = None, rect_opacity: Optional[float] = 0.5, 
                 rect_stroke: Optional[str] = "gray", rect_stroke_width: Optional[int] = 2, 
                 rect_corner_radius: Optional[int] = 4,
                 data: Optional[ExternalDataNode] = None):
        """
        初始化图内注释技术
        
        参数:
            target: DataItemsTargetNode实例，指定要注释的数据项
            stroke_color: 描边颜色，默认为黑色，设为None则不添加描边
            stroke_width: 描边宽度，默认为2
            text_field: 文本字段，可选参数，如果为None则不添加文本
            text_color: 文本颜色，默认为黑色
            rect_color: 矩形颜色，可选参数，如果为None则不添加矩形
            rect_opacity: 矩形透明度，默认为0.5
            rect_stroke: 矩形描边颜色，默认为灰色
            rect_stroke_width: 矩形描边宽度，默认为2
            rect_corner_radius: 矩形圆角半径，默认为4
            data: ExternalDataNode实例，提供外部数据，可选参数
        """
        # 创建MarkerNode
        marker = MarkerNode()
        
        # 添加描边标记（如果指定）
        if stroke_color is not None:
            marker.add_stroke_marker(line_width=stroke_width, color=stroke_color)
        
        # 添加文本标记（如果指定）
        if text_field is not None:
            marker.add_text_marker(field=text_field, color=text_color)
        
        # 添加矩形标记（如果指定）
        if rect_color is not None:
            marker.add_rect_marker(
                color=rect_color, 
                opacity=rect_opacity, 
                stroke=rect_stroke, 
                stroke_width=rect_stroke_width, 
                corner_radius=rect_corner_radius
            )
        
        # 确保至少有一种标记
        if not (stroke_color or text_field or rect_color):
            raise ValueError("必须至少指定一种标记（描边、文本或矩形）")
        
        # 调用父类初始化方法
        super().__init__(name="in_plot", target=target, marker=marker)
        
        # 验证target类型
        if not isinstance(target, DataItemsTargetNode):
            raise ValueError("target必须是DataItemsTargetNode实例")
            
        # 存储和验证外部数据
        self.external_data = data
        if data is not None and not isinstance(data, ExternalDataNode):
            raise ValueError("data必须是ExternalDataNode实例")
    
    def validate(self) -> bool:
        """
        验证图内注释技术是否有效
        规则：
        1. name必须是"in_plot"
        2. target必须是DataItemsTargetNode实例
        3. marker必须至少包含stroke、text或rect中的一种
        4. 如果提供了data，必须是ExternalDataNode实例
        """
        # 调用父类验证
        if not super().validate():
            return False
        
        # 检查name是否为"in_plot"
        if self.name != "in_plot":
            return False
        
        # 检查target是否为DataItemsTargetNode实例
        if not isinstance(self.target, DataItemsTargetNode):
            return False
        
        # 检查marker是否至少包含stroke、text或rect中的一种
        if not self.marker or not (self.marker.stroke or self.marker.text or self.marker.rect):
            return False
            
        # 检查data是否为ExternalDataNode实例（如果提供）
        if hasattr(self, 'external_data') and self.external_data is not None and not isinstance(self.external_data, ExternalDataNode):
            return False
        
        return True
    
    # External Data相关方法
    def has_external_data(self) -> bool:
        """检查是否有外部数据"""
        return hasattr(self, 'external_data') and self.external_data is not None
    
    def get_external_data(self) -> Optional[ExternalDataNode]:
        """获取外部数据节点，如果没有则返回None"""
        if hasattr(self, 'external_data'):
            return self.external_data
        return None
    
    def set_external_data(self, data: ExternalDataNode) -> bool:
        """
        设置外部数据节点
        
        参数:
            data: ExternalDataNode实例
            
        返回:
            设置是否成功
        """
        if not isinstance(data, ExternalDataNode):
            return False
        
        self.external_data = data
        return True
    
    def remove_external_data(self) -> bool:
        """
        移除外部数据节点
        
        返回:
            移除是否成功
        """
        if hasattr(self, 'external_data') and self.external_data is not None:
            self.external_data = None
            return True
        return False
    
    # Stroke相关方法
    def has_stroke(self) -> bool:
        """检查是否有描边标记"""
        return self.marker and self.marker.stroke is not None
    
    def get_stroke_color(self) -> Optional[str]:
        """获取描边颜色，如果没有则返回None"""
        if self.marker and self.marker.stroke:
            return self.marker.stroke.color
        return None
    
    def get_stroke_width(self) -> Optional[int]:
        """获取描边宽度，如果没有则返回None"""
        if self.marker and self.marker.stroke:
            return self.marker.stroke.width
        return None
    
    def set_stroke(self, color: str = "black", width: int = 2) -> bool:
        """
        设置描边标记
        
        参数:
            color: 描边颜色
            width: 描边宽度
            
        返回:
            设置是否成功
        """
        if not color or not isinstance(color, str):
            return False
        if not isinstance(width, int) or width <= 0:
            return False
        
        if self.marker:
            self.marker.add_stroke_marker(line_width=width, color=color)
            return True
        return False
    
    def remove_stroke(self) -> bool:
        """
        移除描边标记
        
        返回:
            移除是否成功
        """
        if self.marker and self.marker.stroke:
            self.marker.stroke = None
            return True
        return False
    
    # Text相关方法
    def has_text(self) -> bool:
        """检查是否有文本标记"""
        return self.marker and self.marker.text is not None
    
    def get_text_field(self) -> Optional[str]:
        """获取文本字段，如果没有则返回None"""
        if self.marker and self.marker.text:
            return self.marker.text.field
        return None
    
    def get_text_color(self) -> Optional[str]:
        """获取文本颜色，如果没有则返回None"""
        if self.marker and self.marker.text:
            return self.marker.text.color
        return None
    
    def set_text(self, field: str, color: str = "black") -> bool:
        """
        设置文本标记
        
        参数:
            field: 文本字段名
            color: 文本颜色
            
        返回:
            设置是否成功
        """
        if not field or not isinstance(field, str):
            return False
        if not color or not isinstance(color, str):
            return False
        
        if self.marker:
            self.marker.add_text_marker(field=field, color=color)
            return True
        return False
    
    def remove_text(self) -> bool:
        """
        移除文本标记
        
        返回:
            移除是否成功
        """
        if self.marker and self.marker.text:
            self.marker.text = None
            return True
        return False
    
    # Rect相关方法
    def has_rect(self) -> bool:
        """检查是否有矩形标记"""
        return self.marker and self.marker.rect is not None
    
    def get_rect_color(self) -> Optional[str]:
        """获取矩形颜色，如果没有则返回None"""
        if self.marker and self.marker.rect:
            return self.marker.rect.color
        return None
    
    def get_rect_opacity(self) -> Optional[float]:
        """获取矩形透明度，如果没有则返回None"""
        if self.marker and self.marker.rect:
            return self.marker.rect.opacity
        return None
    
    def get_rect_stroke(self) -> Optional[str]:
        """获取矩形描边颜色，如果没有则返回None"""
        if self.marker and self.marker.rect:
            return self.marker.rect.stroke
        return None
    
    def get_rect_stroke_width(self) -> Optional[int]:
        """获取矩形描边宽度，如果没有则返回None"""
        if self.marker and self.marker.rect:
            return self.marker.rect.strokeWidth
        return None
    
    def get_rect_corner_radius(self) -> Optional[int]:
        """获取矩形圆角半径，如果没有则返回None"""
        if self.marker and self.marker.rect:
            return self.marker.rect.cornerRadius
        return None
    
    def set_rect(self, color: str = "red", opacity: float = 0.5, 
                stroke: str = "gray", stroke_width: int = 2, 
                corner_radius: int = 4) -> bool:
        """
        设置矩形标记
        
        参数:
            color: 矩形颜色
            opacity: 矩形透明度
            stroke: 矩形描边颜色
            stroke_width: 矩形描边宽度
            corner_radius: 矩形圆角半径
            
        返回:
            设置是否成功
        """
        if not color or not isinstance(color, str):
            return False
        if not isinstance(opacity, (int, float)) or not 0 <= opacity <= 1:
            return False
        if not stroke or not isinstance(stroke, str):
            return False
        if not isinstance(stroke_width, int) or stroke_width < 0:
            return False
        if not isinstance(corner_radius, int) or corner_radius < 0:
            return False
        
        if self.marker:
            self.marker.add_rect_marker(
                color=color, 
                opacity=opacity, 
                stroke=stroke, 
                stroke_width=stroke_width, 
                corner_radius=corner_radius
            )
            return True
        return False
    
    def remove_rect(self) -> bool:
        """
        移除矩形标记
        
        返回:
            移除是否成功
        """
        if self.marker and self.marker.rect:
            self.marker.rect = None
            return True
        return False
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'InPlotTechnique':
        """
        从字典创建InPlotTechnique实例
        
        参数:
            data: 包含技术配置的字典
            
        返回:
            InPlotTechnique实例
        """
        # 验证name是否为in_plot
        name = data.get("name")
        if name != "in_plot":
            raise ValueError("name必须是'in_plot'")
        
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
        
        # 初始化参数
        stroke_color = None
        stroke_width = 2
        text_field = None
        text_color = "black"
        rect_color = None
        rect_opacity = 0.5
        rect_stroke = "gray"
        rect_stroke_width = 2
        rect_corner_radius = 4
        
        # 解析stroke数据（可选）
        stroke_data = marker_data.get("stroke")
        if stroke_data and isinstance(stroke_data, dict):
            stroke_color = stroke_data.get("color", "black")
            if not isinstance(stroke_color, str):
                raise ValueError("stroke颜色必须是字符串")
                
            stroke_width = stroke_data.get("width", 2)
            if not isinstance(stroke_width, int) or stroke_width <= 0:
                raise ValueError("stroke宽度必须是正整数")
        
        # 解析text数据（可选）
        text_data = marker_data.get("text")
        if text_data and isinstance(text_data, dict):
            text_field = text_data.get("field")
            if not text_field or not isinstance(text_field, str):
                raise ValueError("text字段必须包含有效的field")
                
            text_color = text_data.get("color", "black")
            if not isinstance(text_color, str):
                raise ValueError("text颜色必须是字符串")
        
        # 解析rect数据（可选）
        rect_data = marker_data.get("rect")
        if rect_data and isinstance(rect_data, dict):
            rect_color = rect_data.get("color", "red")
            if not isinstance(rect_color, str):
                raise ValueError("rect颜色必须是字符串")
                
            rect_opacity = rect_data.get("opacity", 0.5)
            if not isinstance(rect_opacity, (int, float)) or not 0 <= rect_opacity <= 1:
                raise ValueError("rect透明度必须是0到1之间的数值")
                
            rect_stroke = rect_data.get("stroke", "gray")
            if not isinstance(rect_stroke, str):
                raise ValueError("rect描边颜色必须是字符串")
                
            rect_stroke_width = rect_data.get("strokeWidth", 2)
            if not isinstance(rect_stroke_width, int) or rect_stroke_width < 0:
                raise ValueError("rect描边宽度必须是非负整数")
                
            rect_corner_radius = rect_data.get("cornerRadius", 4)
            if not isinstance(rect_corner_radius, int) or rect_corner_radius < 0:
                raise ValueError("rect圆角半径必须是非负整数")
        
        # 确保至少有一种标记
        if not (stroke_color or text_field or rect_color):
            raise ValueError("必须至少有一种标记（stroke、text或rect）")
            
        # 解析data字段（可选）
        external_data = None
        data_obj = data.get("data")
        if data_obj and isinstance(data_obj, dict):
            try:
                external_data = ExternalDataNode(data_obj)
            except ValueError as e:
                raise ValueError(f"创建ExternalDataNode失败: {str(e)}")
        
        # 创建InPlotTechnique实例
        return cls(
            target=target, 
            stroke_color=stroke_color, 
            stroke_width=stroke_width,
            text_field=text_field,
            text_color=text_color,
            rect_color=rect_color,
            rect_opacity=rect_opacity,
            rect_stroke=rect_stroke,
            rect_stroke_width=rect_stroke_width,
            rect_corner_radius=rect_corner_radius,
            data=external_data
        )

    def _render_background_rect(
        self, original_vegalite_node: Chart, width, height
    ):
        mark_type = "rect"
        # default_cornerRadius = 4
        # default_opacity = 0.5
        # default_strokeWidth = 2
        default_baseline = "bottom"
        # default_stroke = "gray"
        # default_color = "lightgray"
        default_y = -8
        mark_obj = {
            "type": mark_type,
            "width": width + 10,
            "height": height + 2,
            "cornerRadius": self.get_rect_corner_radius(),
            "baseline": default_baseline,
            "stroke": self.get_rect_stroke(),
            "strokeWidth": self.get_rect_stroke_width(),
            "color": self.get_rect_color(),
            "opacity": self.get_rect_opacity()
        }
        
        default_adjusted_alias = "adjusted_y"
        
        field_info = original_vegalite_node.extract_chart_field_info()
        vegalite_filter = self.target.to_vegalite_filter(field_info)

        encoding_init_x_y = {
            "x": original_vegalite_node.get_x_or_y_axis_info_obj("x"),
            # "y": original_vegalite_node.get_x_or_y_axis_info_obj("y"),
        }
        
        if original_vegalite_node.get_x_or_y_axis_info_obj("color"):
            encoding_init_x_y["color"] = original_vegalite_node.get_x_or_y_axis_info_obj("color")
        if original_vegalite_node.get_x_or_y_axis_info_obj("xOffset"):
            encoding_init_x_y["xOffset"] = original_vegalite_node.get_x_or_y_axis_info_obj("xOffset")
        
        encoding = Encoding.from_dict(encoding_init_x_y) 
        
        encoding.set_field("y", default_adjusted_alias, "quantitative")
        
        new_layer = LayerItem(mark_obj, encoding)

        transform = Transform()
        transform = Transform()
        transform.add_filter(vegalite_filter)
        
        field_y_name = original_vegalite_node.get_x_or_y_axis_info_obj("y")["field"]
        transform.add_max_and_adjusted_value(field_y_name, 20.0)
        transform.add_rank_window(field_y_name, order="descending", rank_alias="rank")
        transform.add_filter("datum.rank == 1")
        new_layer.set_property(transform=transform.to_dict())

        original_vegalite_node.add_layer(new_layer)
        
        return original_vegalite_node
      
    def _render_text(self, original_vegalite_node: Chart, text_content_list, height):
        field_info = original_vegalite_node.extract_chart_field_info()
        vegalite_filter = self.target.to_vegalite_filter(field_info)

        mark_type = "text"
        default_baseline = "top"
        default_lineHeight = 12
        mark_obj = {
            "type": mark_type,
            "baseline": default_baseline,
            "dy": -height,
            "lineHeight": default_lineHeight,
            "color": self.get_text_color(),
        }
        default_adjusted_alias = "adjusted_y"
        encoding_init_x_y = {
            **original_vegalite_node.get_field_and_type("x"),
            # **self.get_field_and_type("y"),
        }
        
        # if original_vegalite_node.get_x_or_y_axis_info_obj("color"):
        #     encoding_init_x_y["color"] = original_vegalite_node.get_x_or_y_axis_info_obj("color")
        if original_vegalite_node.get_x_or_y_axis_info_obj("xOffset"):
            encoding_init_x_y["xOffset"] = original_vegalite_node.get_x_or_y_axis_info_obj("xOffset")
        
        encoding = Encoding.from_dict(encoding_init_x_y)
        encoding.set_field("y", default_adjusted_alias, "quantitative")
        encoding.set_value("text", text_content_list)

        text_layer = LayerItem(mark_obj, encoding)

        transform = Transform()
        transform.add_filter(vegalite_filter)
        field_y_name = original_vegalite_node.get_x_or_y_axis_info_obj("y")["field"]
        transform.add_max_and_adjusted_value(field_y_name, 20.0)
        transform.add_rank_window(field_y_name, order="descending", rank_alias="rank")
        transform.add_filter("datum.rank == 1")
        text_layer.set_property(transform=transform.to_dict())

        original_vegalite_node.add_layer(text_layer)
        return original_vegalite_node
 
    def _render_pie_text(self, original_vegalite_node: Chart, text_content_list, height):
        field_info = original_vegalite_node.extract_chart_field_info()
        vegalite_filter = self.target.to_vegalite_filter(field_info)
        
        mark_type = "text"
        default_radius_offset = 12 * (len(text_content_list)//2)
        default_radius = 80
        default_stroke_color = "black"
        default_stroke_width = 0.1
        # default_font_weight = "bold"

        axis_name = original_vegalite_node.get_x_or_y_axis_info_obj("theta")["field"]
        color_name = original_vegalite_node.get_x_or_y_axis_info_obj("color")["field"]

        mark_obj = {
            "type": mark_type,
            "radiusOffset": default_radius_offset,
            "radius": default_radius,
            "stroke": default_stroke_color,
            "color": self.get_text_color(),
            "strokeWidth": default_stroke_width,      
        }
        encoding = Encoding()
        encoding.set_field("theta", axis_name, "quantitative", stack=True)
        encoding.set_field("color", color_name, "nominal")
        encoding.set_value_with_condition("text", vegalite_filter, text_content_list, [])
        text_layer = LayerItem(mark_obj, encoding)

        original_vegalite_node.add_layer(text_layer)
        return original_vegalite_node
        
    def _get_text_content(self):
        text_content = self.get_external_data().get_text_content()
        return text_content
      
    def _add_new_stroke_layer_parse_to_vegalite(self, original_vegalite_node: Chart, is_group: bool = False) -> Chart:
        field_info = original_vegalite_node.extract_chart_field_info()
        vegalite_filter = self.target.to_vegalite_filter(field_info)
        
        transform = Transform()
        # transform.add_filter(vegalite_filter)
        
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
        encoding.set_value_with_condition("stroke", vegalite_filter, self.get_stroke_color(), None)
        encoding.set_value_with_condition("strokeOpacity", vegalite_filter, 1, 0)
        encoding.set_value_with_condition("strokeWidth", vegalite_filter, self.get_stroke_width(), 0)
        encoding.set_value("fillOpacity", 0)
        
        new_layer = LayerItem(mark_obj, encoding)
        new_layer.set_property(transform=transform.to_dict())

        original_vegalite_node.add_layer(new_layer)
        
        return original_vegalite_node


    def _add_new_pie_stroke_layer_parse_to_vegalite(self, original_vegalite_node: Chart) -> Chart:
        field_info = original_vegalite_node.extract_chart_field_info()
        vegalite_filter = self.target.to_vegalite_filter(field_info)
        
        transform = Transform()
        # transform.add_filter(vegalite_filter)
        
        original_mark_obj = original_vegalite_node.get_layer(0).mark
        
        mark_obj = original_mark_obj
        
        encoding_init_dict = {
            "theta": original_vegalite_node.get_x_or_y_axis_info_obj("theta"),
            "color": original_vegalite_node.get_x_or_y_axis_info_obj("color")
        }
                
        encoding = Encoding.from_dict(encoding_init_dict)
        encoding.set_value_with_condition("stroke", vegalite_filter, self.get_stroke_color(), None)
        encoding.set_value_with_condition("strokeOpacity", vegalite_filter, 1, 0)
        encoding.set_value_with_condition("strokeWidth", vegalite_filter, self.get_stroke_width(), 0)
        encoding.set_value("fillOpacity", 0)
        
        new_layer = LayerItem(mark_obj, encoding)
        new_layer.set_property(transform=transform.to_dict())

        original_vegalite_node.add_layer(new_layer)
        
        return original_vegalite_node
        

    def _base_render(self, original_vegalite_node: Chart, is_group: bool = False):
        text_content = self._get_text_content()
        text_list,width,height  = calculate_texts_width_and_height(text_content)
        current_vegalite_node = self._render_background_rect(original_vegalite_node, width, height)
        current_vegalite_node = self._render_text(current_vegalite_node, text_list, height)
        current_vegalite_node = self._add_new_stroke_layer_parse_to_vegalite(current_vegalite_node, is_group)
        
        return current_vegalite_node.to_dict()

    def _pie_render(self, original_vegalite_node: Chart) -> Dict:
        text_content = self._get_text_content()
        text_list,width,height  = calculate_texts_width_and_height(text_content)
        current_vegalite_node = self._render_pie_text(original_vegalite_node, text_list, height)
        current_vegalite_node = self._add_new_pie_stroke_layer_parse_to_vegalite(current_vegalite_node)
        return current_vegalite_node.to_dict()

    # 各种图表类型转化
    def _pie_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._pie_render(original_vegalite_node)
    
    def _bar_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._base_render(original_vegalite_node)

    def _line_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._base_render(original_vegalite_node)
    
    def _scatter_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._base_render(original_vegalite_node)
    
    def _group_line_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._base_render(original_vegalite_node, is_group=True)
    
    def _group_bar_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._base_render(original_vegalite_node, is_group=True)
    
    def _group_scatter_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._base_render(original_vegalite_node, is_group=True)

       
    def parse_to_vegalite(self, original_vegalite_node: Chart, chart_type: ChartType) -> Dict:
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
