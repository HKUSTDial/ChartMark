from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique
from ChartMark.annotation_ast_genetic.target_node.DataItemTargetNode import DataItemsTargetNode
from ChartMark.annotation_ast_genetic.marker_node.MarkerNode import MarkerNode
from typing import Dict, Optional
from ChartMark.annotation_ast_genetic.marker_node.SubTextNode import TextMarker
from ChartMark.vegalite_ast.ChartNode import Chart
from ChartMark.vegalite_ast.EncodingNode import Encoding
from ChartMark.vegalite_ast.LayerItemNode import LayerItem
from ChartMark.vegalite_ast.TransformNode import Transform
from ChartMark.vegalite_ast.MarkNode import Mark
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType

class LabelTechnique(BaseTechnique):
    """
    标签技术类，用于在图表中为数据项添加标签
    name固定为"label"
    target必须是DataItemsTargetNode类型
    marker必须包含text属性
    """
    def __init__(self, target: DataItemsTargetNode, text_field: str, text_color: str = "black"):
        """
        初始化标签技术
        
        参数:
            target: DataItemsTargetNode实例，指定要标记的数据项
            text_field: 标签文本字段
            text_color: 标签文本颜色，默认为黑色
        """
        # 创建只包含text的MarkerNode
        marker = MarkerNode()
        marker.add_text_marker(field=text_field, color=text_color)
        
        # 调用父类初始化方法
        super().__init__(name="label", target=target, marker=marker)
        
        # 验证target类型
        if not isinstance(target, DataItemsTargetNode):
            raise ValueError("target必须是DataItemsTargetNode实例")
    
    def validate(self) -> bool:
        """
        验证标签技术是否有效
        规则：
        1. name必须是"label"
        2. target必须是DataItemsTargetNode实例
        3. marker必须包含text属性
        """
        # 调用父类验证
        if not super().validate():
            return False
        
        # 检查name是否为"label"
        if self.name != "label":
            return False
        
        # 检查target是否为DataItemsTargetNode实例
        if not isinstance(self.target, DataItemsTargetNode):
            return False
        
        # 检查marker是否包含text属性
        if not self.marker or not self.marker.text:
            return False
        
        return True
    
    def get_text_field(self) -> str:
        """获取标签文本字段"""
        if self.marker and self.marker.text:
            return self.marker.text.field
        return ""
    
    def get_text_color(self) -> str:
        """获取标签文本颜色"""
        if self.marker and self.marker.text:
            return self.marker.text.color
        return "black"
    
    def set_text_field(self, field: str) -> bool:
        """
        设置标签文本字段
        
        参数:
            field: 文本字段名
            
        返回:
            设置是否成功
        """
        if not field or not isinstance(field, str):
            return False
        
        if self.marker and self.marker.text:
            self.marker.text.field = field
            return True
        else:
            # 如果没有marker或text，创建一个
            marker = MarkerNode()
            marker.add_text_marker(field=field)
            self.marker = marker
            return True
    
    def set_text_color(self, color: str) -> bool:
        """
        设置标签文本颜色
        
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
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'LabelTechnique':
        """
        从字典创建LabelTechnique实例
        
        参数:
            data: 包含技术配置的字典
            
        返回:
            LabelTechnique实例
        """
        # 验证name是否为label
        name = data.get("name")
        if name != "label":
            raise ValueError("name必须是'label'")
        
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
        
        # 验证marker是否包含text
        text_data = marker_data.get("text")
        if not text_data or not isinstance(text_data, dict):
            raise ValueError("marker必须包含text字段")
        
        # 获取text字段和颜色
        text_field = text_data.get("field")
        if not text_field:
            raise ValueError("text必须包含field字段")
        
        text_color = text_data.get("color", "black")
        
        # 创建LabelTechnique实例
        return cls(target=target, text_field=text_field, text_color=text_color)

    def _y_text_with_condition(self, original_vegalite_node: Chart, is_group: bool = False) -> Dict:
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
        y_field_and_type_obj = original_vegalite_node.get_field_and_type("y")["y"]
        encoding.set_field("text", field_name=y_field_and_type_obj["field"], field_type=y_field_and_type_obj["type"])

        
        text_layer = LayerItem(mark_obj, encoding)
        
        if vegalite_filter:
            transform = Transform()
            transform.add_filter(vegalite_filter)
            text_layer.set_property(transform=transform.to_dict())
        
        original_vegalite_node.add_layer(text_layer)
        
        return original_vegalite_node.to_dict()
    
    def _xy_text_with_condition(self, original_vegalite_node: Chart, is_group: bool = False) -> Dict:
        y_field_and_type_obj = original_vegalite_node.get_field_and_type("y")["y"]
        x_field_and_type_obj = original_vegalite_node.get_field_and_type("x")["x"]
        
        transform = Transform()
        x_name = x_field_and_type_obj["field"]
        y_name = y_field_and_type_obj["field"]
        temporal_str = f"'(' + datum['{x_name}'] + ', ' + datum['{y_name}'] + ')'"
        temporal_value_name = "xy"
        transform.add_calculate(temporal_str, temporal_value_name)
        
        
        field_info = original_vegalite_node.extract_chart_field_info()
        vegalite_filter = self.target.to_vegalite_filter(field_info)
        if vegalite_filter:
          transform.add_filter(vegalite_filter)
      
        encoding_init_x_y = {
            "x": original_vegalite_node.get_x_or_y_axis_info_obj("x"),
            "y": original_vegalite_node.get_x_or_y_axis_info_obj("y"),
        }
        if is_group:
            encoding_init_x_y["color"] = original_vegalite_node.get_x_or_y_axis_info_obj("color")

        encoding = Encoding.from_dict(encoding_init_x_y)
        encoding.set_field("text", temporal_value_name, "nominal" )
        
        mark_type = "text"
        default_baseline = "line-top"
        
        mark_obj = Mark(
            mark_type= mark_type,
            baseline = default_baseline
        ).to_dict() 
        

        rule_layer = LayerItem(mark_obj, encoding)
        rule_layer.set_property(transform=transform.to_dict())

        original_vegalite_node.add_layer(rule_layer)

        return original_vegalite_node.to_dict()
    
    def _pie_text_with_condition(self, original_vegalite_node: Chart) -> Dict:
        field_info = original_vegalite_node.extract_chart_field_info()
        vegalite_filter = self.target.to_vegalite_filter(field_info)
      
        mark_type = "text"
        default_radius = 90
        
        mark_obj = Mark(
            mark_type= mark_type,
            radius = default_radius
        ).to_dict() 
      

        encoding_init = {
            "theta": original_vegalite_node.get_x_or_y_axis_info_obj("theta"),
            "color": original_vegalite_node.get_x_or_y_axis_info_obj("color"),
        }
        encoding = Encoding.from_dict(encoding_init)
      
        text_base_obj = original_vegalite_node.get_field_and_type("theta")["theta"]
      
        if not vegalite_filter or vegalite_filter == {}:
            encoding.set_field("text", text_base_obj["field"], text_base_obj["type"])
        else:
            field_name = text_base_obj["field"]
            field_type = text_base_obj["type"]
            encoding.set_field_with_condition("text", field_name, field_type, vegalite_filter, [])

        rule_layer = LayerItem(mark_obj, encoding)
        
        original_vegalite_node.add_layer(rule_layer)

        return original_vegalite_node.to_dict()

    def _pie_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._pie_text_with_condition(original_vegalite_node)
    
    def _bar_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._y_text_with_condition(original_vegalite_node)
    
    def _line_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._y_text_with_condition(original_vegalite_node)
    
    def _scatter_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._xy_text_with_condition(original_vegalite_node)
    
    def _group_line_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._y_text_with_condition(original_vegalite_node, is_group=True)
    
    def _group_bar_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._y_text_with_condition(original_vegalite_node, is_group=True)
    
    def _group_scatter_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._xy_text_with_condition(original_vegalite_node, is_group=True)
    
    
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
