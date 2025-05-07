from typing import Dict, List
from .BaseGroupNode import BaseGroupNode


class GroupScatterChartNode(BaseGroupNode):

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
    分组散点图节点，除了基本属性和分组属性外，还包含数据
    - x_data: 二维数值数组，表示每个点的x坐标，外层长度与classify长度相同
    - y_data: 二维数值数组，表示每个点的y坐标，外层长度与classify长度相同，每个内层数组长度应与对应的x_data内层数组相同
    """

    def __init__(self, chart_obj: Dict = None):
        super().__init__(chart_obj)

        if chart_obj:
            self._parse_data_properties(chart_obj)
            # 确保类型设置为group_scatter
            self.type = "group_scatter"

    def _parse_data_properties(self, chart_obj: Dict):
        """
        解析数据属性并确保数据格式正确
        - x_data应为二维数值数组
        - y_data应为二维数值数组
        - x_data和y_data的外层长度应与classify长度相同
        - 每对x_data和y_data内层数组的长度应相同
        """
        # 获取数据
        x_data_raw = chart_obj.get("x_data", [])
        y_data_raw = chart_obj.get("y_data", [])
        
        self.classify = chart_obj.get("classify", [])

        # 解析x_data为二维数值数组
        if isinstance(x_data_raw, list):
            self.x_data = []

            # 处理x_data，确保为二维数组
            if x_data_raw and all(
                isinstance(item, (int, float)) for item in x_data_raw
            ):
                # 如果是一维数值数组，转换为单一系列的二维数组
                numeric_series = [float(x) for x in x_data_raw]
                self.x_data = [numeric_series]
            else:
                # 处理二维数组情况
                for series in x_data_raw:
                    if isinstance(series, list):
                        # 将内层数组转换为浮点数
                        numeric_series = [
                            float(x) if isinstance(x, (int, float)) else 0.0
                            for x in series
                        ]
                        self.x_data.append(numeric_series)
                    elif isinstance(series, (int, float)):
                        # 如果元素是数值，添加为长度为1的数组
                        self.x_data.append([float(series)])
                    else:
                        # 其他情况添加空数组
                        self.x_data.append([])

        # 解析y_data为二维数值数组
        if isinstance(y_data_raw, list):
            self.y_data = []

            # 处理y_data，确保为二维数组
            if y_data_raw and all(
                isinstance(item, (int, float)) for item in y_data_raw
            ):
                # 如果是一维数值数组，转换为单一系列的二维数组
                numeric_series = [float(y) for y in y_data_raw]
                self.y_data = [numeric_series]
            else:
                # 处理二维数组情况
                for series in y_data_raw:
                    if isinstance(series, list):
                        # 将内层数组转换为浮点数
                        numeric_series = [
                            float(y) if isinstance(y, (int, float)) else 0.0
                            for y in series
                        ]
                        self.y_data.append(numeric_series)
                    elif isinstance(series, (int, float)):
                        # 如果元素是数值，添加为长度为1的数组
                        self.y_data.append([float(series)])
                    else:
                        # 其他情况添加空数组
                        self.y_data.append([])

        # 确保x_data和y_data外层长度与classify长度一致
        expected_outer_length = (
            len(self.classify) if self.classify else max(len(self.x_data), len(self.y_data))
        )

        # 处理x_data长度
        if len(self.x_data) < expected_outer_length:
            # 如果x_data比预期短，用空数组补足
            self.x_data.extend(
                [[] for _ in range(expected_outer_length - len(self.x_data))]
            )
        elif len(self.x_data) > expected_outer_length and expected_outer_length > 0:
            # 如果x_data比预期长，截取
            self.x_data = self.x_data[:expected_outer_length]

        # 处理y_data长度
        if len(self.y_data) < expected_outer_length:
            # 如果y_data比预期短，用空数组补足
            self.y_data.extend(
                [[] for _ in range(expected_outer_length - len(self.y_data))]
            )
        elif len(self.y_data) > expected_outer_length and expected_outer_length > 0:
            # 如果y_data比预期长，截取
            self.y_data = self.y_data[:expected_outer_length]

        # 确保每对x_data和y_data内层数组长度一致
        for i in range(len(self.x_data)):
            x_series = self.x_data[i]
            y_series = self.y_data[i] if i < len(self.y_data) else []

            # 取较大的长度作为统一长度
            target_length = max(len(x_series), len(y_series))

            # 调整x_series长度
            if len(x_series) < target_length:
                x_series.extend([0.0] * (target_length - len(x_series)))
            elif len(x_series) > target_length and target_length > 0:
                x_series = x_series[:target_length]

            # 调整y_series长度
            if len(y_series) < target_length:
                y_series.extend([0.0] * (target_length - len(y_series)))
            elif len(y_series) > target_length and target_length > 0:
                y_series = y_series[:target_length]

            # 更新调整后的数据
            self.x_data[i] = x_series
            if i < len(self.y_data):
                self.y_data[i] = y_series

    def validate(self) -> bool:
        """
        验证分组散点图的数据是否有效
        规则：
        1. x_data和y_data必须是非空的二维数组
        2. x_data和y_data的外层长度必须与classify长度相同
        3. 每对x_data和y_data内层数组的长度必须相同
        4. x_data和y_data的元素必须是数值
        """
        # 检查x_data和y_data是否为非空二维数组
        if not self.x_data or not self.y_data:
            return False

        if not all(isinstance(series, list) for series in self.x_data) or not all(
            isinstance(series, list) for series in self.y_data
        ):
            return False

        # 检查x_data和y_data外层长度是否与classify长度相同
        if len(self.x_data) != len(self.classify) or len(self.y_data) != len(
            self.classify
        ):
            return False

        # 检查每对x_data和y_data内层数组的长度是否相同
        if not all(
            len(self.x_data[i]) == len(self.y_data[i]) for i in range(len(self.x_data))
        ):
            return False

        # 检查x_data和y_data的元素是否全部是数值
        if not all(
            all(isinstance(x, (int, float)) for x in series) for series in self.x_data
        ):
            return False

        if not all(
            all(isinstance(y, (int, float)) for y in series) for series in self.y_data
        ):
            return False

        return True

    def set_data(
        self, x_data: List[List[float]], y_data: List[List[float]], classify: List[str]
    ) -> bool:
        """
        设置图表数据

        参数:
            x_data: 二维数值数组，表示每个点的x坐标
            y_data: 二维数值数组，表示每个点的y坐标
            classify: 分类名称列表

        返回:
            设置是否成功
        """
        # 参数验证
        if not x_data or not y_data or not classify:
            return False

        if len(x_data) != len(classify) or len(y_data) != len(classify):
            return False

        # 检查每对x_data和y_data内层数组的长度是否相同
        if not all(len(x_data[i]) == len(y_data[i]) for i in range(len(x_data))):
            return False

        # 检查是否全部是数值
        try:
            # 转换x_data为二维浮点数数组
            x_float_data = [[float(x) for x in series] for series in x_data]
            # 转换y_data为二维浮点数数组
            y_float_data = [[float(y) for y in series] for series in y_data]

            # 设置数据
            self.x_data = x_float_data
            self.y_data = y_float_data
            self.classify = classify

            return True
        except (ValueError, TypeError):
            return False

