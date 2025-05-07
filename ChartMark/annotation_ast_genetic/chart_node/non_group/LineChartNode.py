from typing import Dict, List
from .BaseNonGroupNode import BaseNonGroupNode
import re
from datetime import datetime


class LineChartNode(BaseNonGroupNode):
    
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
                        }},
                        "scale": {{
                            "nice": true 
                        }}
                    }},
                    "y": {{ 
                        "field": "{y_name}", 
                        "type": "quantitative", 
                        "title": "{y_name}",
                        "axis": {{"grid": false}}
                    }}
                }}
            }}
        ]
    }}
    """
    
    
    """
    折线图节点，包含数据属性
    - x_data: 一维日期字符串数组，格式如 "2023-01-01"
    - y_data: 一维数值数组，表示对应的数值
    两个数组长度应相等
    """
    def __init__(self, chart_obj: Dict = None):
        super().__init__(chart_obj)
        
        if chart_obj:
            self._parse_data_properties(chart_obj)
            # 确保类型设置为line
            self.type = "line"
    
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
        - y_data应为一维数值数组
        - 两个数组长度应相等
        """
        # 获取数据
        x_data_raw = chart_obj.get("x_data", [])
        y_data_raw = chart_obj.get("y_data", [])
        
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
        
        # 将y_data转换为浮点数列表
        if isinstance(y_data_raw, list):
            self.y_data = [float(y) if isinstance(y, (int, float)) else 0.0 for y in y_data_raw]
        else:
            self.y_data = []
        
        # 确保x_data和y_data长度一致
        target_length = max(len(self.x_data), len(self.y_data))
        
        # 调整x_data长度
        if len(self.x_data) < target_length:
            # 如果x_data为空，用默认日期补充
            if not self.x_data:
                self.x_data = ["1970-01-01"] * target_length
            else:
                # 复制最后一个日期，递增一天
                last_date = self.x_data[-1]
                for i in range(target_length - len(self.x_data)):
                    try:
                        # 尝试解析日期并递增
                        dt = datetime.strptime(last_date, '%Y-%m-%d')
                        dt = dt.replace(day=dt.day + 1)
                        new_date = dt.strftime('%Y-%m-%d')
                        self.x_data.append(new_date)
                        last_date = new_date
                    except (ValueError, TypeError):
                        # 无法解析，使用默认值
                        self.x_data.append("1970-01-01")
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
        验证折线图的数据是否有效
        规则：
        1. x_data和y_data必须是非空的一维数组
        2. x_data和y_data的长度必须相同
        3. x_data的元素应该是日期格式的字符串
        4. y_data的元素必须是数值
        """
        # 检查x_data和y_data是否为非空一维数组
        if not self.x_data or not self.y_data:
            return False
        
        # 检查x_data和y_data长度是否相同
        if len(self.x_data) != len(self.y_data):
            return False
        
        # 检查x_data的元素是否是日期格式
        # 这里只要求部分元素符合日期格式（至少一个），以提高容错性
        if not any(self._is_date_format(x) for x in self.x_data):
            return False
        
        # 检查y_data的元素是否全部是数值
        if not all(isinstance(y, (int, float)) for y in self.y_data):
            return False
        
        return True
    
    def set_data(self, x_data: List[str], y_data: List[float]) -> bool:
        """
        设置图表数据
        
        参数:
            x_data: 一维日期字符串数组，格式如 "2023-01-01"
            y_data: 一维数值数组，表示对应的数值
            
        返回:
            设置是否成功
        """
        # 参数验证
        if not x_data or not y_data:
            return False
        
        # 检查x_data和y_data长度是否相同
        if len(x_data) != len(y_data):
            return False
        
        # 检查x_data中是否至少有一些元素符合日期格式
        if not any(self._is_date_format(x) for x in x_data):
            return False
        
        # 检查是否全部是预期类型
        try:
            # 转换x_data为日期格式字符串数组
            x_date_data = [self._format_date(x) for x in x_data]
            # 转换y_data为浮点数数组
            y_float_data = [float(y) for y in y_data]
            
            # 设置数据
            self.x_data = x_date_data
            self.y_data = y_float_data
            
            return True
        except (ValueError, TypeError):
            return False
