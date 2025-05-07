from typing import Dict, List
from .BaseGroupNode import BaseGroupNode


class GroupBarChartNode(BaseGroupNode):
    
    ORIGINAL_CHART_TEMPLATE = """
    {{
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": "{title}",
        "data": {{
            "values": {metadata_list}
        }},
        "layer": [
            {{
                "mark": {{"type":"bar"}},
                "encoding": {{
                    "x": {{"field": "{x_name}", "type": "nominal", "title": "{x_name}", "axis": {{"labelAngle": -45}}}},
                    "xOffset": {{"field": "{classify_name}", "type": "nominal"}},
                    "y": {{"field": "{y_name}", "type": "quantitative", "title": "{y_name}", "axis": {{"grid": false}}}},
                    "color": {{ "field": "{classify_name}", "type": "nominal", "title": "{classify_name}"}}
                }}
            }}
        ]
    }}
    """
    
    """
    分组柱状图节点，除了基本属性和分组属性外，还包含数据
    - x_data: 一维字符串数组，表示类别
    - y_data: 二维数值数组，外层长度与classify长度相同，内层长度与x_data长度相同
    """
    def __init__(self, chart_obj: Dict = None):
        super().__init__(chart_obj)
        
        if chart_obj:
            self._parse_data_properties(chart_obj)
            # 确保类型设置为group_bar
            self.type = "group_bar"
    
    def _parse_data_properties(self, chart_obj: Dict):
        """
        解析数据属性并确保数据格式正确
        - x_data应为一维字符串数组
        - y_data应为二维数值数组
        - y_data外层长度应与classify长度相同
        - y_data内层长度应与x_data长度相同
        """
        # 获取数据
        x_data_raw = chart_obj.get("x_data", [])
        y_data_raw = chart_obj.get("y_data", [])
        
        self.classify = chart_obj.get("classify", [])
        
        # 将x_data转换为字符串列表
        self.x_data = [str(x) for x in x_data_raw] if isinstance(x_data_raw, list) else []
        
        # 解析y_data为二维数值数组
        if isinstance(y_data_raw, list):
            self.y_data = []
            
            # 确保y_data外层长度与classify长度相同
            # 如果classify为空，则保留原有y_data的长度
            expected_outer_length = len(self.classify) if self.classify else len(y_data_raw)
            
            # 如果y_data比classify短，用空数组补足
            if len(y_data_raw) < expected_outer_length:
                y_data_raw.extend([[] for _ in range(expected_outer_length - len(y_data_raw))])
            # 如果y_data比classify长，截取符合长度的部分
            elif len(y_data_raw) > expected_outer_length and expected_outer_length > 0:
                y_data_raw = y_data_raw[:expected_outer_length]
            
            # 处理每个系列数据
            for series in y_data_raw:
                if isinstance(series, list):
                    # 将内层数组转换为浮点数
                    numeric_series = [float(y) if isinstance(y, (int, float)) else 0.0 for y in series]
                    
                    # 确保内层长度与x_data长度相同
                    if len(numeric_series) < len(self.x_data):
                        # 如果内层数组比x_data短，补充0.0
                        numeric_series.extend([0.0] * (len(self.x_data) - len(numeric_series)))
                    elif len(numeric_series) > len(self.x_data) and self.x_data:
                        # 如果内层数组比x_data长，截取符合长度的部分
                        numeric_series = numeric_series[:len(self.x_data)]
                    
                    self.y_data.append(numeric_series)
                else:
                    # 如果不是列表，添加一个与x_data等长的空数组（填充0.0）
                    self.y_data.append([0.0] * len(self.x_data))
    
    def to_dict(self) -> Dict:
        """
        将节点转换为字典格式，包含所有属性
        """
        result = super().to_dict()
        result.update({
            "x_data": self.x_data,
            "y_data": self.y_data
        })
        return result
    
    def validate(self) -> bool:
        """
        验证分组柱状图的数据是否有效
        规则：
        1. x_data必须是非空的一维数组
        2. y_data必须是非空的二维数组
        3. y_data外层长度必须与classify长度相同
        4. y_data内层每个数组的长度必须与x_data长度相同
        5. x_data的元素必须是字符串
        6. y_data的元素必须是数值
        """
        # 检查x_data是否为非空一维数组且元素为字符串
        if not self.x_data or not all(isinstance(x, str) for x in self.x_data):
            return False
        
        # 检查y_data是否为非空二维数组
        if not self.y_data or not all(isinstance(series, list) for series in self.y_data):
            return False
        
        # 检查y_data外层长度是否与classify长度相同
        if len(self.y_data) != len(self.classify):
            return False
        
        # 检查y_data内层每个数组的长度是否与x_data长度相同
        if not all(len(series) == len(self.x_data) for series in self.y_data):
            return False
        
        # 检查y_data的元素是否全部是数值
        if not all(all(isinstance(y, (int, float)) for y in series) for series in self.y_data):
            return False
        
        return True
    
    def set_data(self, x_data: List[str], y_data: List[List[float]], classify: List[str]) -> bool:
        """
        设置图表数据
        
        参数:
            x_data: 一维字符串数组，表示类别
            y_data: 二维数值数组，对应每个分类的数据系列
            classify: 分类名称列表
            
        返回:
            设置是否成功
        """
        # 参数验证
        if not x_data or not y_data or not classify:
            return False
        
        if len(y_data) != len(classify):
            return False
        
        if not all(len(series) == len(x_data) for series in y_data):
            return False
        
        # 设置数据
        self.x_data = x_data
        self.y_data = y_data
        self.classify = classify
        
        return True
