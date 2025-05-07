from typing import Dict, List, Optional
from .BaseGroupNode import BaseGroupNode
import re
from datetime import datetime


class GroupLineChartNode(BaseGroupNode):
    
    ORIGINAL_CHART_TEMPLATE = """
    {{
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": "{title}",
        "data": {{
            "values": {metadata_list}
        }},
        "layer": [
            {{
                "mark": {{"type": "line", "point": true}},
                "encoding": {{
                    "x": {{
                        "field": "{x_name}",
                        "type": "temporal",
                        "title": "{x_name}",
                        "axis": {{
                            "labelAngle": -45,
                            "labelOverlap": false,
                            "grid": false
                        }}
                    }},
                    "y": {{
                        "field": "{y_name}",
                        "type": "quantitative",
                        "title": "{y_name}",
                        "axis": {{"grid": false}}
                    }},
                    "color": {{ 
                        "field": "{classify_name}", 
                        "type": "nominal",
                        "title": "{classify_name}"
                    }}
                }}
            }}
        ]
    }}
    """
    
    """
    分组折线图节点，除了基本属性和分组属性外，还包含数据
    - x_data: 一维日期字符串数组，格式如 "2023-01-01"
    - y_data: 二维数值数组，外层长度与classify长度相同，内层长度与x_data长度相同
    """
    def __init__(self, chart_obj: Dict = None):
        super().__init__(chart_obj)
        
        if chart_obj:
            self._parse_data_properties(chart_obj)
            # 确保类型设置为group_line
            self.type = "group_line"
    
    def _is_date_format(self, date_str: str) -> bool:
        """
        检查字符串是否为有效的日期格式
        支持的格式: YYYY-MM-DD, YYYY/MM/DD
        """
        date_patterns = [
            r'^\d{4}-\d{1,2}-\d{1,2}$',  # YYYY-MM-DD
            r'^\d{4}/\d{1,2}/\d{1,2}$',  # YYYY/MM/DD
        ]
        return any(re.match(pattern, date_str) for pattern in date_patterns)
    
    def _format_date(self, date_str: str) -> str:
        """
        格式化日期字符串为标准格式
        """
        try:
            # 尝试解析日期
            if '-' in date_str:
                parts = date_str.split('-')
                if len(parts) == 3:
                    year, month, day = parts
                    dt = datetime(int(year), int(month), int(day))
                    return dt.strftime('%Y-%m-%d')
            elif '/' in date_str:
                parts = date_str.split('/')
                if len(parts) == 3:
                    year, month, day = parts
                    dt = datetime(int(year), int(month), int(day))
                    return dt.strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            pass
        
        # 如果无法解析为日期格式，返回原始字符串
        return date_str
    
    def _parse_data_properties(self, chart_obj: Dict):
        """
        解析数据属性并确保数据格式正确
        - x_data应为一维日期字符串数组
        - y_data应为二维数值数组
        - y_data外层长度应与classify长度相同
        - y_data内层长度应与x_data长度相同
        """
        # 获取数据
        x_data_raw = chart_obj.get("x_data", [])
        y_data_raw = chart_obj.get("y_data", [])
        
        self.classify = chart_obj.get("classify", [])
        
        # 将x_data转换为日期字符串列表
        if isinstance(x_data_raw, list):
            self.x_data = []
            for x in x_data_raw:
                x_str = str(x)
                # 尝试格式化为日期格式
                formatted_date = self._format_date(x_str)
                self.x_data.append(formatted_date)
        else:
            self.x_data = []
        
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
        验证分组折线图的数据是否有效
        规则：
        1. x_data必须是非空的一维数组
        2. x_data的元素应该是日期格式的字符串
        3. y_data必须是非空的二维数组
        4. y_data外层长度必须与classify长度相同
        5. y_data内层每个数组的长度必须与x_data长度相同
        6. y_data的元素必须是数值
        """
        # 检查x_data是否为非空一维数组
        if not self.x_data:
            return False
        
        # 检查x_data的元素是否是日期格式
        # 这里只要求部分元素符合日期格式（至少一个），以提高容错性
        if not any(self._is_date_format(x) for x in self.x_data):
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
            x_data: 一维日期字符串数组，格式如 "2023-01-01"
            y_data: 二维数值数组，对应每个分类的数据系列
            classify: 分类名称列表
            
        返回:
            设置是否成功
        """
        # 参数验证
        if not x_data or not y_data or not classify:
            return False
        
        # 检查x_data中是否至少有一些元素符合日期格式
        if not any(self._is_date_format(x) for x in x_data):
            return False
        
        if len(y_data) != len(classify):
            return False
        
        if not all(len(series) == len(x_data) for series in y_data):
            return False
        
        # 设置数据
        self.x_data = [self._format_date(x) for x in x_data]
        self.y_data = y_data
        self.classify = classify
        
        return True
