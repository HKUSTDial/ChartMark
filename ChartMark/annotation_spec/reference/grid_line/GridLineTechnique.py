from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique
from ChartMark.annotation_ast_genetic.target_node.ChartElementTargetNode import ChartElementTargetNode
from typing import Dict, Optional
from ChartMark.vegalite_ast.ChartNode import Chart
from ChartMark.annotation_ast_genetic.chart_node.BaseChartNode import ChartType
from ChartMark.vegalite_ast.EncodingNode import Encoding
from ChartMark.vegalite_ast.LayerItemNode import LayerItem

class GridLineTechnique(BaseTechnique):
    """
    网格线技术类，用于在图表中添加网格线
    name固定为"grid_line"
    target必须是ChartElementTargetNode类型
    """
    def __init__(self, target: ChartElementTargetNode):
        """
        初始化网格线技术
        
        参数:
            target: ChartElementTargetNode实例，指定要添加网格线的坐标轴
        """
        # 调用父类初始化方法
        super().__init__(name="grid_line", target=target, marker=None)
        
        # 验证target类型
        if not isinstance(target, ChartElementTargetNode):
            raise ValueError("target必须是ChartElementTargetNode实例")
        
        # 验证target至少包含一个轴的网格配置
        if not self._has_valid_grid_config():
            raise ValueError("target必须至少包含一个轴的网格配置")
    
    def _has_valid_grid_config(self) -> bool:
        """检查是否有有效的网格配置"""
        # 检查x轴网格
        has_x_grid = (self.target.xAxis is not None and 
                      isinstance(self.target.xAxis, dict) and
                      self.target.xAxis.get("grid") == True)
        
        # 检查y轴网格
        has_y_grid = (self.target.yAxis is not None and 
                      isinstance(self.target.yAxis, dict) and
                      self.target.yAxis.get("grid") == True)
        
        # 检查theta轴网格
        has_theta_grid = (self.target.thetaAxis is not None and 
                          isinstance(self.target.thetaAxis, dict) and
                          self.target.thetaAxis.get("grid") == True)
        
        return has_x_grid or has_y_grid or has_theta_grid
    
    def validate(self) -> bool:
        """
        验证网格线技术是否有效
        规则：
        1. name必须是"grid_line"
        2. target必须是ChartElementTargetNode实例
        3. target必须至少包含一个轴的网格配置
        """
        # 调用父类验证
        if not super().validate():
            return False
        
        # 检查name是否为"grid_line"
        if self.name != "grid_line":
            return False
        
        # 检查target是否为ChartElementTargetNode实例
        if not isinstance(self.target, ChartElementTargetNode):
            return False
        
        # 检查是否有有效的网格配置
        if not self._has_valid_grid_config():
            return False
        
        return True
    
    def has_x_grid(self) -> bool:
        """检查是否有x轴网格"""
        return (self.target.xAxis is not None and 
                isinstance(self.target.xAxis, dict) and
                self.target.xAxis.get("grid") == True)
    
    def has_y_grid(self) -> bool:
        """检查是否有y轴网格"""
        return (self.target.yAxis is not None and 
                isinstance(self.target.yAxis, dict) and
                self.target.yAxis.get("grid") == True)
    
    def has_theta_grid(self) -> bool:
        """检查是否有theta轴网格"""
        return (self.target.thetaAxis is not None and 
                isinstance(self.target.thetaAxis, dict) and
                self.target.thetaAxis.get("grid") == True)
    
    def get_x_interval(self) -> Optional[float]:
        """获取x轴网格间隔，如果没有则返回None"""
        if self.has_x_grid() and "interval" in self.target.xAxis:
            return self.target.xAxis["interval"]
        return None
    
    def get_y_interval(self) -> Optional[float]:
        """获取y轴网格间隔，如果没有则返回None"""
        if self.has_y_grid() and "interval" in self.target.yAxis:
            return self.target.yAxis["interval"]
        return None
    
    def get_theta_interval(self) -> Optional[float]:
        """获取theta轴网格间隔，如果没有则返回None"""
        if self.has_theta_grid() and "interval" in self.target.thetaAxis:
            return self.target.thetaAxis["interval"]
        return None
    
    def get_x_tick_count(self) -> Optional[int]:
        """获取x轴刻度数量，如果没有则返回None"""
        if self.has_x_grid() and "tickCount" in self.target.xAxis:
            return self.target.xAxis["tickCount"]
        return None
    
    def get_y_tick_count(self) -> Optional[int]:
        """获取y轴刻度数量，如果没有则返回None"""
        if self.has_y_grid() and "tickCount" in self.target.yAxis:
            return self.target.yAxis["tickCount"]
        return None
    
    def get_theta_tick_count(self) -> Optional[int]:
        """获取theta轴刻度数量，如果没有则返回None"""
        if self.has_theta_grid() and "tickCount" in self.target.thetaAxis:
            return self.target.thetaAxis["tickCount"]
        return None
    
    def set_x_grid(self, enabled: bool = True, interval: Optional[float] = None, tick_count: Optional[int] = None) -> bool:
        """
        设置x轴网格
        
        参数:
            enabled: 是否启用网格
            interval: 网格间隔
            tick_count: 刻度数量
            
        返回:
            设置是否成功
        """
        if not hasattr(self.target, 'xAxis') or self.target.xAxis is None:
            self.target.xAxis = {}
            
        self.target.xAxis["grid"] = enabled
        
        if interval is not None:
            if not isinstance(interval, (int, float)) or interval <= 0:
                return False
            self.target.xAxis["interval"] = interval
            
        if tick_count is not None:
            if not isinstance(tick_count, int) or tick_count <= 0:
                return False
            self.target.xAxis["tickCount"] = tick_count
            
        return True
    
    def set_y_grid(self, enabled: bool = True, interval: Optional[float] = None, tick_count: Optional[int] = None) -> bool:
        """
        设置y轴网格
        
        参数:
            enabled: 是否启用网格
            interval: 网格间隔
            tick_count: 刻度数量
            
        返回:
            设置是否成功
        """
        if not hasattr(self.target, 'yAxis') or self.target.yAxis is None:
            self.target.yAxis = {}
            
        self.target.yAxis["grid"] = enabled
        
        if interval is not None:
            if not isinstance(interval, (int, float)) or interval <= 0:
                return False
            self.target.yAxis["interval"] = interval
            
        if tick_count is not None:
            if not isinstance(tick_count, int) or tick_count <= 0:
                return False
            self.target.yAxis["tickCount"] = tick_count
            
        return True
    
    def set_theta_grid(self, enabled: bool = True, interval: Optional[float] = None, tick_count: Optional[int] = None) -> bool:
        """
        设置theta轴网格
        
        参数:
            enabled: 是否启用网格
            interval: 网格间隔
            tick_count: 刻度数量
            
        返回:
            设置是否成功
        """
        if not hasattr(self.target, 'thetaAxis') or self.target.thetaAxis is None:
            self.target.thetaAxis = {}
            
        self.target.thetaAxis["grid"] = enabled
        
        if interval is not None:
            if not isinstance(interval, (int, float)) or interval <= 0:
                return False
            self.target.thetaAxis["interval"] = interval
            
        if tick_count is not None:
            if not isinstance(tick_count, int) or tick_count <= 0:
                return False
            self.target.thetaAxis["tickCount"] = tick_count
            
        return True
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GridLineTechnique':
        """
        从字典创建GridLineTechnique实例
        
        参数:
            data: 包含技术配置的字典
            
        返回:
            GridLineTechnique实例
        """
        # 验证name是否为grid_line
        name = data.get("name")
        if name != "grid_line":
            raise ValueError("name必须是'grid_line'")
        
        # 获取target数据
        target_data = data.get("target")
        if not target_data or not isinstance(target_data, dict):
            raise ValueError("target字段必须是有效的字典")
        
        # 验证target类型
        target_type = target_data.get("type")
        if target_type != "chart_element":
            raise ValueError("target类型必须是'chart_element'")
        
        # 创建ChartElementTargetNode
        target = ChartElementTargetNode(target_data)
        
        # 创建GridLineTechnique实例
        return cls(target=target)

    def _set_axis_gridline_state(self, original_vegalite_node: Chart, field_key: str, state: bool = True):
        original_vegalite_node.get_layer(0).encoding.update_subcontent_obj(field_key, axis={"grid": state})
        return original_vegalite_node
      
    def _set_axis_gridline_tick_count(self, original_vegalite_node: Chart, field_key: str, tick_count: int):
        original_vegalite_node.get_layer(0).encoding.update_subcontent_obj(field_key, axis={"tickCount": tick_count})
        return original_vegalite_node

    def _get_max_value(self, original_vegalite_node: Chart, field_name: str):
        values = original_vegalite_node.data["values"]
        filed_value_list = [item[field_name] for item in values]
        
        return max(filed_value_list)

    def set_axis_gridline_values(self, original_vegalite_node: Chart, field_key: str, interval: float) -> None:

        values = []
        
        field_name = original_vegalite_node.get_layer(0).encoding.get_subcontent_obj(field_key)["field"]
        max_value = self._get_max_value(original_vegalite_node, field_name)
        
        # 生成间隔的值，直到第一个值超过 max_value
        current_value = 0
        while current_value <= max_value:
            values.append(current_value)
            current_value += interval

        original_vegalite_node.get_layer(0).encoding.update_field(field_key, axis={"values": values})

        return original_vegalite_node
      
      
    def _xy_gridline(self, original_vegalite_node: Chart) -> Chart:
        if self.has_x_grid():
            self._set_axis_gridline_state(original_vegalite_node, "x", True)
            if self.get_x_tick_count() is not None:
                self._set_axis_gridline_tick_count(original_vegalite_node, "x", self.get_x_tick_count())
            if self.get_x_interval() is not None:
                self.set_axis_gridline_values(original_vegalite_node, "x", self.get_x_interval())
            
        if self.has_y_grid():
            self._set_axis_gridline_state(original_vegalite_node, "y", True)
            if self.get_y_tick_count() is not None:
                self._set_axis_gridline_tick_count(original_vegalite_node, "y", self.get_y_tick_count())
            if self.get_y_interval() is not None:
                self.set_axis_gridline_values(original_vegalite_node, "y", self.get_y_interval())
            
        return original_vegalite_node

    def _sum_data(self, original_vegalite_node: Chart):
        theta_name = original_vegalite_node.get_x_or_y_axis_info_obj("theta")["field"]
        data_list = [ value[theta_name] for value in  original_vegalite_node.data["values"]]
        return sum(data_list)

    def _pie_grid_line(self, original_vegalite_node: Chart, sum: float, start_value: float = None, color: str = "black"):
      
        encoding = Encoding()

        encoding.set_field("theta", "interval", "quantitative")

        mark_type = "arc"
        rule_layer = LayerItem(mark_type, encoding)

        rule_layer.set_mark_property("innerRadius", 1)
        rule_layer.set_mark_property("outerRadius", 80)
        rule_layer.set_mark_property("stroke", "black")
        rule_layer.set_mark_property("strokeWidth", 3)
        rule_layer.set_mark_property("fillOpacity", 0)
        rule_layer.set_mark_property("color", color)
        
        cnt = 6
        if self.has_theta_grid():
            if self.get_theta_tick_count() is not None:
                cnt = self.get_theta_tick_count()
            
        interval = sum/cnt
            
        if self.get_theta_interval() is not None:
                interval = self.get_theta_interval()
        
        value_list = [{"interval": interval} for _ in range(cnt)]
        
        if(start_value):
          value_list.insert(0, {"name": "start", "interval": start_value})
          encoding.set_value_with_condition("strokeOpacity", "datum.name == 'start'", 0, 1)

        data = {
          "values": value_list
        }
        
        rule_layer.set_property(data = data)

        original_vegalite_node.add_layer(rule_layer)
        return original_vegalite_node

    def _pie_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        sum_data = self._sum_data(original_vegalite_node)
        current_vegalite_node = self._pie_grid_line(original_vegalite_node, sum_data)
        return current_vegalite_node.to_dict()
    
    def _bar_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict: 
        current_vegalite_node = self._xy_gridline(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _line_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._xy_gridline(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _scatter_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._xy_gridline(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _group_line_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._xy_gridline(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _group_bar_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._xy_gridline(original_vegalite_node)
        return current_vegalite_node.to_dict()
    
    def _group_scatter_parse_to_vegalite(self, original_vegalite_node: Chart, sub_type: str) -> Dict:
        current_vegalite_node = self._xy_gridline(original_vegalite_node)
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
