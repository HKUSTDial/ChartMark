from typing import Dict, List
from .BaseNonGroupNode import BaseNonGroupNode


class ScatterChartNode(BaseNonGroupNode):
    
    ORIGINAL_CHART_TEMPLATE = """
        {{
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "title": "{title}",
            "data": {{
                "values": {metadata_list}
            }},
            "layer": [
                {{
                "mark": {{
                    "type": "point",
                    "filled": true,
                    "size": 80
                }},
                "encoding": {{
                    "x": {{
                    "field": "{x_name}",
                    "type": "quantitative",
                    "title": "{x_name}",
                    "axis": {{ "grid": false}}
                    }},
                    "y": {{
                    "field": "{y_name}",
                    "type": "quantitative",
                    "title": "{y_name}",
                    "axis": {{ "grid": false}}
                    }}
                }}
                }}
            ]
        }}
    """
    
    """
    散点图节点，包含数据属性
    - x_data: 一维数值数组，表示x坐标
    - y_data: 一维数值数组，表示y坐标
    两个数组长度应相等
    """
    def __init__(self, chart_obj: Dict = None):
        super().__init__(chart_obj)
        
        if chart_obj:
            self._parse_data_properties(chart_obj)
            # 确保类型设置为scatter
            self.type = "scatter"
    
    def _parse_data_properties(self, chart_obj: Dict):
        """
        解析数据属性并确保数据格式正确
        - x_data应为一维数值数组
        - y_data应为一维数值数组
        - 两个数组长度应相等
        """
        # 获取数据
        x_data_raw = chart_obj.get("x_data", [])
        y_data_raw = chart_obj.get("y_data", [])
        
        # 将x_data转换为浮点数列表
        if isinstance(x_data_raw, list):
            self.x_data = [float(x) if isinstance(x, (int, float)) else 0.0 for x in x_data_raw]
        else:
            self.x_data = []
        
        # 将y_data转换为浮点数列表
        if isinstance(y_data_raw, list):
            self.y_data = [float(y) if isinstance(y, (int, float)) else 0.0 for y in y_data_raw]
        else:
            self.y_data = []
        
        # 确保x_data和y_data长度一致
        target_length = max(len(self.x_data), len(self.y_data))
        
        # 调整x_data长度
        if len(self.x_data) < target_length:
            # 用0.0补充x_data
            self.x_data.extend([0.0] * (target_length - len(self.x_data)))
        elif len(self.x_data) > target_length and target_length > 0:
            # 截取x_data
            self.x_data = self.x_data[:target_length]
        
        # 调整y_data长度
        if len(self.y_data) < target_length:
            # 用0.0补充y_data
            self.y_data.extend([0.0] * (target_length - len(self.y_data)))
        elif len(self.y_data) > target_length and target_length > 0:
            # 截取y_data
            self.y_data = self.y_data[:target_length]
    
    def validate(self) -> bool:
        """
        验证散点图的数据是否有效
        规则：
        1. x_data和y_data必须是非空的一维数组
        2. x_data和y_data的长度必须相同
        3. x_data的元素必须是数值
        4. y_data的元素必须是数值
        """
        # 检查x_data和y_data是否为非空一维数组
        if not self.x_data or not self.y_data:
            return False
        
        # 检查x_data和y_data长度是否相同
        if len(self.x_data) != len(self.y_data):
            return False
        
        # 检查x_data的元素是否全部是数值
        if not all(isinstance(x, (int, float)) for x in self.x_data):
            return False
        
        # 检查y_data的元素是否全部是数值
        if not all(isinstance(y, (int, float)) for y in self.y_data):
            return False
        
        return True
    
    def set_data(self, x_data: List[float], y_data: List[float]) -> bool:
        """
        设置图表数据
        
        参数:
            x_data: 一维数值数组，表示x坐标
            y_data: 一维数值数组，表示y坐标
            
        返回:
            设置是否成功
        """
        # 参数验证
        if not x_data or not y_data:
            return False
        
        # 检查x_data和y_data长度是否相同
        if len(x_data) != len(y_data):
            return False
        
        # 检查是否全部是预期类型
        try:
            # 转换x_data为浮点数数组
            x_float_data = [float(x) for x in x_data]
            # 转换y_data为浮点数数组
            y_float_data = [float(y) for y in y_data]
            
            # 设置数据
            self.x_data = x_float_data
            self.y_data = y_float_data
            
            return True
        except (ValueError, TypeError):
            return False
