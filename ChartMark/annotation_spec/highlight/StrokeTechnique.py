from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique
from ChartMark.annotation_ast_genetic.target_node.DataItemTargetNode import DataItemsTargetNode
from ChartMark.annotation_ast_genetic.marker_node.MarkerNode import MarkerNode
from typing import Dict, Optional
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType
from ChartMark.vegalite_ast.ChartNode import Chart
from ChartMark.vegalite_ast.MarkNode import Mark
from ChartMark.vegalite_ast.EncodingNode import Encoding
from ChartMark.vegalite_ast.LayerItemNode import LayerItem
from ChartMark.vegalite_ast.TransformNode import Transform

class StrokeTechnique(BaseTechnique):
    """
    描边高亮技术类，用于在图表中为数据项添加描边高亮
    name固定为"stroke"
    target必须是DataItemsTargetNode类型
    marker必须包含stroke属性
    """
    def __init__(self, target: DataItemsTargetNode, width: int = 2, color: str = "black"):
        """
        初始化描边高亮技术
        
        参数:
            target: DataItemsTargetNode实例，指定要高亮的数据项
            width: 描边宽度，默认为2
            color: 描边颜色，默认为黑色
        """
        # 创建只包含stroke的MarkerNode
        marker = MarkerNode()
        marker.add_stroke_marker(line_width=width, color=color)
        
        # 调用父类初始化方法
        super().__init__(name="stroke", target=target, marker=marker)
        
        # 验证target类型
        if not isinstance(target, DataItemsTargetNode):
            raise ValueError("target必须是DataItemsTargetNode实例")
    
    def validate(self) -> bool:
        """
        验证描边高亮技术是否有效
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
        """获取描边宽度"""
        if self.marker and self.marker.stroke:
            return self.marker.stroke.width
        return 2
    
    def get_stroke_color(self) -> str:
        """获取描边颜色"""
        if self.marker and self.marker.stroke:
            return self.marker.stroke.color
        return "black"
    
    def set_stroke_width(self, width: int) -> bool:
        """
        设置描边宽度
        
        参数:
            width: 描边宽度
            
        返回:
            设置是否成功
        """
        if not isinstance(width, int) or width <= 0:
            return False
        
        if self.marker and self.marker.stroke:
            self.marker.stroke.lineWidth = width
            return True
        else:
            # 如果没有marker或stroke，创建一个
            marker = MarkerNode()
            marker.add_stroke_marker(line_width=width, color="black")
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
            self.marker = marker
            return True
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'StrokeTechnique':
        """
        从字典创建StrokeHighlight实例
        
        参数:
            data: 包含技术配置的字典
            
        返回:
            StrokeHighlight实例
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
        
        # 获取stroke宽度和颜色
        width = stroke_data.get("width", 2)
        if not isinstance(width, int) or width <= 0:
            raise ValueError("stroke宽度必须是正整数")
            
        color = stroke_data.get("color", "black")
        if not isinstance(color, str):
            raise ValueError("stroke颜色必须是字符串")
        
        # 创建StrokeHighlight实例
        return cls(target=target, width=width, color=color)

    
    def _base_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        field_info = original_vegalite_node.extract_chart_field_info()
        vegalite_filter = self.target.to_vegalite_filter(field_info)
        
        original_vegalite_node.get_layer(0).encoding.set_value_with_condition(
            "stroke",
            vegalite_filter,
            self.get_stroke_color(),
            None
        )
        
        original_vegalite_node.get_layer(0).encoding.set_value_with_condition(
            "strokeWidth",
            vegalite_filter,
            self.get_stroke_width(),
            0
        )
        return original_vegalite_node.to_dict()

    def _add_new_layer_parse_to_vegalite(self, original_vegalite_node: Chart, is_group: bool = False) -> Dict:
        field_info = original_vegalite_node.extract_chart_field_info()
        vegalite_filter = self.target.to_vegalite_filter(field_info)
        
        transform = Transform()
        transform.add_filter(vegalite_filter)
        
        point_obj = {
            "stroke": self.get_stroke_color(),
            "strokeWidth": self.get_stroke_width()
        }
        
        mark_obj = Mark(
            mark_type="line",
            point = point_obj
        ).to_dict()
        
        encoding_init_x_y = {
            "x": original_vegalite_node.get_x_or_y_axis_info_obj("x"),
            "y": original_vegalite_node.get_x_or_y_axis_info_obj("y"),
        }
        
        if is_group:
            encoding_init_x_y["color"] = original_vegalite_node.get_x_or_y_axis_info_obj("color")
        
        encoding = Encoding.from_dict(encoding_init_x_y)
        
        new_layer = LayerItem(mark_obj, encoding)
        
        new_layer.set_property(transform=transform.to_dict())

        original_vegalite_node.add_layer(new_layer)
        
        return original_vegalite_node.to_dict()
 

    # 各种图表类型转化
    def _pie_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._base_parse_to_vegalite(original_vegalite_node)
    
    def _bar_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._base_parse_to_vegalite(original_vegalite_node)

    def _line_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._add_new_layer_parse_to_vegalite(original_vegalite_node)
    
    def _scatter_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._base_parse_to_vegalite(original_vegalite_node)
    
    def _group_line_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._add_new_layer_parse_to_vegalite(original_vegalite_node, is_group=True)
    
    def _group_bar_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._base_parse_to_vegalite(original_vegalite_node)
    
    def _group_scatter_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        return self._base_parse_to_vegalite(original_vegalite_node)
    
    
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
