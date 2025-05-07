from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique
from ChartMark.annotation_ast_genetic.target_node.DataItemTargetNode import DataItemsTargetNode
from ChartMark.annotation_ast_genetic.marker_node.MarkerNode import MarkerNode
from typing import Dict, Optional
from ChartMark.vegalite_ast.ChartNode import Chart
from ChartMark.vegalite_ast.EncodingNode import Encoding
from ChartMark.vegalite_ast.LayerItemNode import LayerItem
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType
from ChartMark.vegalite_ast.TransformNode import Transform

class DataLineTechnique(BaseTechnique):
    """
    数据线技术类，用于在图表中为数据项添加连接线
    name固定为"data_line"
    target必须是DataItemsTargetNode类型
    marker必须包含line属性
    """
    def __init__(self, target: DataItemsTargetNode, line_color: str = "red", line_size: int = 2):
        """
        初始化数据线技术
        
        参数:
            target: DataItemsTargetNode实例，指定要连接的数据项
            line_color: 线条颜色，默认为红色
            line_size: 线条大小，默认为2
        """
        # 创建包含line的MarkerNode
        marker = MarkerNode()
        marker.add_line_marker(color=line_color, size=line_size)
        
        # 调用父类初始化方法
        super().__init__(name="data_line", target=target, marker=marker)
        
        # 验证target类型
        if not isinstance(target, DataItemsTargetNode):
            raise ValueError("target必须是DataItemsTargetNode实例")
    
    def validate(self) -> bool:
        """
        验证数据线技术是否有效
        规则：
        1. name必须是"data_line"
        2. target必须是DataItemsTargetNode实例
        3. marker必须包含line属性
        """
        # 调用父类验证
        if not super().validate():
            return False
        
        # 检查name是否为"data_line"
        if self.name != "data_line":
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
        return "red"  # 默认颜色
    
    def get_line_size(self) -> int:
        """获取线条大小"""
        if self.marker and self.marker.line:
            return self.marker.line.size
        return 2  # 默认大小
    
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
            self.marker = marker
            return True
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'DataLineTechnique':
        """
        从字典创建DataLineTechnique实例
        
        参数:
            data: 包含技术配置的字典
            
        返回:
            DataLineTechnique实例
        """
        # 验证name是否为data_line
        name = data.get("name")
        if name != "data_line":
            raise ValueError("name必须是'data_line'")
        
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
        
        # 创建DataLineTechnique实例
        return cls(
            target=target, 
            line_color=line_color, 
            line_size=line_size
        )

    def _render_x_or_y_rule_with_condition(
        self, original_vegalite_node: Chart, rule_type
    ) -> Chart:
        field_info = original_vegalite_node.extract_chart_field_info()
        vegalite_filter = self.target.to_vegalite_filter(field_info)

        transform = Transform()
        transform.add_filter(vegalite_filter)

        
        encoding_init_x_y = {
            "x": original_vegalite_node.get_x_or_y_axis_info_obj("x"),
            "y": original_vegalite_node.get_x_or_y_axis_info_obj("y"),
        }
        print("---------------1-----------------")
        print(encoding_init_x_y)
        encoding = Encoding.from_dict(encoding_init_x_y)
        if rule_type == "y":
            encoding.set_value("x2", 0)
        elif rule_type == "x":
            encoding.set_value("y2", "height")

        mark_type = "rule"

        rule_layer = LayerItem(mark_type, encoding)
        rule_layer.set_mark_property("color", self.get_line_color())
        rule_layer.set_mark_property("size", self.get_line_size())

        rule_layer.set_property(transform=transform.to_dict())

        original_vegalite_node.add_layer(rule_layer)
        return original_vegalite_node


    # def _pie_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
    #     current_vegalite_node = self._base_render_polar(original_vegalite_node)
    #     return current_vegalite_node.to_dict()
    
    def _bar_parse_to_vegalite(self, original_vegalite_node: Chart)-> Dict: 
        current_vegalite_node = self._render_x_or_y_rule_with_condition(original_vegalite_node, "y")
        return current_vegalite_node.to_dict()
    
    def _line_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        current_vegalite_node = self._render_x_or_y_rule_with_condition(original_vegalite_node, "y")
        current_vegalite_node = self._render_x_or_y_rule_with_condition(current_vegalite_node, "x")
        return current_vegalite_node.to_dict()
    
    def _scatter_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        current_vegalite_node = self._render_x_or_y_rule_with_condition(original_vegalite_node, "y")
        current_vegalite_node = self._render_x_or_y_rule_with_condition(current_vegalite_node, "x")
        return current_vegalite_node.to_dict()
    
    def _group_line_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        current_vegalite_node = self._render_x_or_y_rule_with_condition(original_vegalite_node, "y")
        current_vegalite_node = self._render_x_or_y_rule_with_condition(current_vegalite_node, "x")
        return current_vegalite_node.to_dict()
    
    def _group_bar_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        current_vegalite_node = self._render_x_or_y_rule_with_condition(original_vegalite_node, "y")
        return current_vegalite_node.to_dict()
    
    def _group_scatter_parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        current_vegalite_node = self._render_x_or_y_rule_with_condition(original_vegalite_node, "y")
        current_vegalite_node = self._render_x_or_y_rule_with_condition(current_vegalite_node, "x")
        return current_vegalite_node.to_dict() 


    def parse_to_vegalite(self, original_vegalite_node: Chart, chart_type: ChartType, sub_type: str) -> Dict:
        """
        将技术节点转换为vegalite字典
        
        参数:
            original_vegalite_node: 原始vegalite节点实例
        """
        # if chart_type == "pie":
        #     return self._pie_parse_to_vegalite(original_vegalite_node)
        if chart_type == "bar":
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
