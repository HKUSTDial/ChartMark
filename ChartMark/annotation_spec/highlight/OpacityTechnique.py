from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique
from ChartMark.annotation_ast_genetic.target_node.DataItemTargetNode import DataItemsTargetNode
from ChartMark.annotation_ast_genetic.marker_node.MarkerNode import MarkerNode
from typing import Dict, Optional
from ChartMark.vegalite_ast.ChartNode import Chart
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType
from ChartMark.vegalite_ast.TransformNode import Transform
from ChartMark.vegalite_ast.EncodingNode import Encoding
from ChartMark.vegalite_ast.LayerItemNode import LayerItem
from ChartMark.vegalite_ast.MarkNode import Mark

class OpacityTechnique(BaseTechnique):
    """
    透明度高亮技术类，用于在图表中为数据项添加透明度高亮
    name固定为"opacity"
    target必须是DataItemsTargetNode类型
    marker必须包含opacity属性
    """
    def __init__(self, target: DataItemsTargetNode, selected: float = 1.0, other: float = 0.5):
        """
        初始化透明度高亮技术
        
        参数:
            target: DataItemsTargetNode实例，指定要高亮的数据项
            selected: 选中项的透明度，默认为1.0（完全不透明）
            other: 其他项的透明度，默认为0.5（半透明）
        """
        # 验证透明度参数
        if not (0 <= selected <= 1):
            raise ValueError("selected透明度必须在0到1之间")
        if not (0 <= other <= 1):
            raise ValueError("other透明度必须在0到1之间")
            
        # 创建只包含opacity的MarkerNode
        marker = MarkerNode()
        marker.add_opacity_marker(selected=selected, other=other)
        
        # 调用父类初始化方法
        super().__init__(name="opacity", target=target, marker=marker)
        
        # 验证target类型
        if not isinstance(target, DataItemsTargetNode):
            raise ValueError("target必须是DataItemsTargetNode实例")
    
    def validate(self) -> bool:
        """
        验证透明度高亮技术是否有效
        规则：
        1. name必须是"opacity"
        2. target必须是DataItemsTargetNode实例
        3. marker必须包含opacity属性
        4. selected和other值必须在0到1之间
        """
        # 调用父类验证
        if not super().validate():
            return False
        
        # 检查name是否为"opacity"
        if self.name != "opacity":
            return False
        
        # 检查target是否为DataItemsTargetNode实例
        if not isinstance(self.target, DataItemsTargetNode):
            return False
        
        # 检查marker是否包含opacity属性
        if not self.marker or not self.marker.opacity:
            return False
        
        # 检查透明度值是否在有效范围内
        if not hasattr(self.marker.opacity, 'selected') or not (0 <= self.marker.opacity.selected <= 1):
            return False
        if not hasattr(self.marker.opacity, 'other') or not (0 <= self.marker.opacity.other <= 1):
            return False
        
        return True
    
    def get_selected_opacity(self) -> float:
        """获取选中项的透明度"""
        if self.marker and self.marker.opacity:
            return self.marker.opacity.selected
        return 1.0
    
    def get_other_opacity(self) -> float:
        """获取其他项的透明度"""
        if self.marker and self.marker.opacity:
            return self.marker.opacity.other
        return 0.5
    
    def set_selected_opacity(self, opacity: float) -> bool:
        """
        设置选中项的透明度
        
        参数:
            opacity: 透明度值（0-1之间）
            
        返回:
            设置是否成功
        """
        if not isinstance(opacity, (int, float)) or not (0 <= opacity <= 1):
            return False
        
        if self.marker and self.marker.opacity:
            self.marker.opacity.selected = opacity
            return True
        else:
            # 如果没有marker或opacity，创建一个
            marker = MarkerNode()
            marker.add_opacity_marker(selected=opacity, other=0.5)
            self.marker = marker
            return True
    
    def set_other_opacity(self, opacity: float) -> bool:
        """
        设置其他项的透明度
        
        参数:
            opacity: 透明度值（0-1之间）
            
        返回:
            设置是否成功
        """
        if not isinstance(opacity, (int, float)) or not (0 <= opacity <= 1):
            return False
        
        if self.marker and self.marker.opacity:
            self.marker.opacity.other = opacity
            return True
        else:
            # 如果没有marker或opacity，创建一个
            marker = MarkerNode()
            marker.add_opacity_marker(selected=1.0, other=opacity)
            self.marker = marker
            return True
    
    # 各种图表类型转化
    def _base_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        field_info = original_vegalite_node.extract_chart_field_info()
        vegalite_filter = self.target.to_vegalite_filter(field_info)
        
        original_vegalite_node.get_layer(0).encoding.set_value_with_condition(
            "opacity",
            vegalite_filter,
            self.get_selected_opacity(),
            self.get_other_opacity()
        )
        return original_vegalite_node.to_dict()
    
    def _add_new_layer_parse_to_vegalite(self, original_vegalite_node: Chart, is_group: bool = False) -> Dict:
        original_vegalite_node.get_layer(0).encoding.set_value(
            "opacity", self.get_other_opacity()
        )
        field_info = original_vegalite_node.extract_chart_field_info()
        vegalite_filter = self.target.to_vegalite_filter(field_info)
        
        transform = Transform()
        transform.add_filter(vegalite_filter)
        
        mark_obj = Mark(
            mark_type="line",
            point = True
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
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'OpacityTechnique':
        """
        从字典创建OpacityHighlight实例
        
        参数:
            data: 包含技术配置的字典
            
        返回:
            OpacityHighlight实例
        """
        # 验证name是否为opacity
        name = data.get("name")
        if name != "opacity":
            raise ValueError("name必须是'opacity'")
        
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
        
        # 验证marker是否包含opacity
        opacity_data = marker_data.get("opacity")
        if not opacity_data or not isinstance(opacity_data, dict):
            raise ValueError("marker必须包含opacity字段")
        
        # 获取opacity值
        selected = opacity_data.get("selected", 1.0)
        other = opacity_data.get("other", 0.5)
        
        # 验证opacity值
        if not isinstance(selected, (int, float)) or not (0 <= selected <= 1):
            raise ValueError("selected透明度必须是0到1之间的数值")
        if not isinstance(other, (int, float)) or not (0 <= other <= 1):
            raise ValueError("other透明度必须是0到1之间的数值")
        
        # 创建OpacityHighlight实例
        return cls(target=target, selected=selected, other=other)
