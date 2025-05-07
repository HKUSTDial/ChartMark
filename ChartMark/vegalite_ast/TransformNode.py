from typing import Dict, Union, List
from ChartMark.vegalite_ast.ast_base import BaseNode

class Transform(BaseNode):
    def __init__(self) -> None:
        """
        初始化 Transform 对象，管理所有的 transform 操作。
        """
        self.transforms = []

    def add_calculate(self, expression: str, alias: str) -> None:
        """
        添加一个 calculate 操作。
        :param expression: 计算表达式，如 "datetime(2017, 0, 1)"
        :param alias: 计算结果的别名，如 "x_start"
        """
        transform = {"calculate": expression, "as": alias}
        self.transforms.append(transform)

    def add_aggregate(self, op: str, field: str, alias: str) -> None:
        """
        添加一个 aggregate 操作。
        :param op: 聚合操作符，如 "mean", "sum", "count" 等。
        :param field: 要聚合的字段名，如 "y"。
        :param alias: 聚合结果的别名，如 "mean_y"。
        """
        transform = {
            "aggregate": [{"op": op, "field": field, "as": alias}]
        }
        self.transforms.append(transform)
        
    def add_joinaggregate(self, op: str, field: str, alias: str) -> None:
        """
        添加一个 joinaggregate 操作。
        :param op: 聚合操作符，如 "mean", "sum", "count" 等。
        :param field: 要聚合的字段名，如 "y"。
        :param alias: 聚合结果的别名，如 "mean_y"。
        """
        transform = {
            "joinaggregate": [{"op": op, "field": field, "as": alias}]
        }
        self.transforms.append(transform)

    def add_regression(self, target_field: str, on_field: str, group_field: str = None) -> None:
        """
        添加一个回归 (regression) 操作。
        :param target_field: 回归的目标字段，如 "gdp"。
        :param on_field: 自变量字段，如 "year"。
        :param group_field: 分组字段，如 "country"。
        """
        transform = {
            "regression": target_field,
            "on": on_field
        }
        if group_field:
            transform["groupby"] = [group_field]
        self.transforms.append(transform)

    def add_filter(self, filter_condition: Union[Dict, str]) -> None:
        """
        添加一个 filter 操作。
        :param filter_condition: 过滤条件，可以是字典形式或者字符串形式。
        """
        if isinstance(filter_condition, dict):
            self.transforms.append({"filter": filter_condition})
        elif isinstance(filter_condition, str):
            self.transforms.append({"filter": filter_condition})
        else:
            raise ValueError("Filter condition must be either a dictionary or a string.")

    def add_range_filter(self, field: str, time_unit: str, start: Dict[str, Union[int, str]], end: Dict[str, Union[int, str]]) -> None:
        """
        添加一个时间范围过滤操作。
        :param field: 要过滤的字段名
        :param time_unit: 时间单位，如 "yearmonthdate"
        :param start: 开始日期（字典格式，如 {"year": 2006, "month": "june", "date": 1}）
        :param end: 结束日期（字典格式，如 {"year": 2009, "month": "jan", "date": 20}）
        """
        range_filter = {
            "filter": {
                "timeUnit": time_unit,
                "field": field,
                "range": [start, end]
            }
        }
        self.transforms.append(range_filter)

    def update_filter(self, index: int, filter_condition: Union[Dict, str]) -> None:
        """
        更新指定索引的 filter 操作。
        :param index: 要更新的 filter 操作的索引
        :param filter_condition: 新的过滤条件
        """
        if 0 <= index < len(self.transforms):
            if isinstance(filter_condition, dict):
                self.transforms[index] = {"filter": filter_condition}
            elif isinstance(filter_condition, str):
                self.transforms[index] = {"filter": filter_condition}
            else:
                raise ValueError("Filter condition must be either a dictionary or a string.")
        else:
            raise IndexError("Invalid index for transform.")

    def remove_transform(self, index: int) -> None:
        """
        删除指定索引的 transform 操作。
        :param index: 要删除的 transform 操作的索引
        """
        if 0 <= index < len(self.transforms):
            self.transforms.pop(index)
        else:
            raise IndexError("Invalid index for transform.")

    def to_dict(self) -> List[Dict]:
        """
        返回所有 transform 操作的字典形式。
        :return: 包含所有 transform 操作的字典列表
        """
        return self.transforms

    @classmethod
    def from_dict(cls, transform_list: List[Dict]) -> "Transform":
        """
        从字典列表解析出 Transform 对象。
        :param transform_list: 包含多个 transform 操作的字典列表
        :return: Transform 对象
        """
        transform_instance = cls()
        transform_instance.transforms = transform_list
        return transform_instance

    def add_window(self, op: str, alias: str, field: str = None, params: Dict = None) -> None:
        """
        添加一个窗口 (window) 操作。
        
        Args:
            op: 窗口操作符，如 "row_number", "rank", "dense_rank", "percent_rank", 
                "cume_dist", "ntile", "lag", "lead", "first_value", "last_value", 
                "nth_value", "min", "max", "mean", "sum", "product", "count"等。
            alias: 窗口结果的别名，如 "index"。
            field: 可选，要计算的字段名，某些操作需要(如sum需要指定字段)。
            params: 可选，额外参数，如 ntile 操作的 {"param": 5}。
        """
        window_op = {"op": op, "as": alias}
        
        # 如果提供了字段，添加到操作中
        if field is not None:
            window_op["field"] = field
        
        # 如果提供了额外参数，添加到操作中
        if params is not None:
            for key, value in params.items():
                window_op[key] = value
        
        transform = {"window": [window_op]}
        self.transforms.append(transform)

    # def add_window_and_filter(self, window_op: str, window_alias: str, filter_condition: str = None, field: str = None, params: Dict = None) -> None:
    #     """
    #     添加一个窗口操作，后跟一个过滤操作。常用于行号过滤。
        
    #     Args:
    #         window_op: 窗口操作符，如 "row_number"。
    #         window_alias: 窗口结果的别名，如 "index"。
    #         filter_condition: 过滤条件，如 "datum.index == 4"。如果为None，则不添加过滤。
    #         field: 可选，要计算的字段名。
    #         params: 可选，额外参数。
    #     """
    #     # 添加窗口操作
    #     self.add_window(op=window_op, alias=window_alias, field=field, params=params)
        
    #     # 如果提供了过滤条件，添加过滤操作
    #     if filter_condition is not None:
    #         self.add_filter(filter_condition)

    def add_row_number_filter(self, index: int, alias: str = "index") -> None:
        """
        添加一个行号窗口操作，后跟一个过滤操作，只保留指定行号的数据。
        
        Args:
            index: 要保留的行号 (从1开始)
            alias: 行号的别名，默认为 "index"
        """
        self.add_window(op="row_number", alias=alias)
        self.add_filter(f"datum.{alias} == {index}")

    def add_max_window(self, field: str, alias: str = "max_value") -> None:
        """
        添加一个计算指定字段最大值的窗口操作。
        
        Args:
            field: 要计算最大值的字段名，如 "Premiere week"
            alias: 结果的别名，默认为 "max_value"
        """
        self.add_window(op="max", field=field, alias=alias)

    def add_adjusted_value_calculation(self, field: str, max_field: str = "max_value", adjustment_factor: float = 50.0, alias: str = "adjusted_y") -> None:
        """
        添加一个计算字段，将原始字段值加上最大值的一小部分作为调整。
        
        Args:
            field: 原始字段名，如 "Premiere week"
            max_field: 最大值字段名，默认为 "max_value"
            adjustment_factor: 调整因子，最大值会除以此值，默认为 50.0
            alias: 结果的别名，默认为 "adjusted_y"
        """
        expression = f"datum['{field}'] + (datum['{max_field}'] / {adjustment_factor})"
        self.add_calculate(expression=expression, alias=alias)

    def add_max_and_adjusted_value(self, field: str, adjustment_factor: float = 50.0, max_alias: str = "max_value", adjusted_alias: str = "adjusted_y") -> None:
        """
        添加一个窗口操作计算最大值，然后添加一个计算调整值的操作。
        
        Args:
            field: 字段名，如 "Premiere week"
            adjustment_factor: 调整因子，最大值会除以此值，默认为 50.0
            max_alias: 最大值的别名，默认为 "max_value"
            adjusted_alias: 调整值的别名，默认为 "adjusted_y"
        """
        # 添加计算最大值的窗口操作
        self.add_max_window(field=field, alias=max_alias)
        
        # 添加计算调整值的操作
        self.add_adjusted_value_calculation(
            field=field, 
            max_field=max_alias, 
            adjustment_factor=adjustment_factor,
            alias=adjusted_alias
        )

    def add_aggregate_operation(self, op: str, field: str, alias: str):
        """
        向现有的聚合转换中添加一个聚合操作，如果不存在则创建新的。
        
        Args:
            op: 聚合操作符，如 "min", "max", "mean", "sum", "count" 等
            field: 要聚合的字段
            alias: 聚合结果的别名
        """
        # 创建聚合操作对象
        agg_op = {"op": op, "field": field, "as": alias}
        
        # 查找现有的聚合转换
        for transform in self.transforms:
            if "aggregate" in transform:
                # 如果找到，添加操作到现有聚合
                transform["aggregate"].append(agg_op)
                return
        
        # 如果没有找到，创建新的聚合转换
        self.transforms.append({"aggregate": [agg_op]})

    def add_min_max_aggregate(self, x_field: str, y_field: str):
        """
        添加计算x和y字段最小值和最大值的聚合转换。
        
        Args:
            x_field: x轴字段名
            y_field: y轴字段名
        
        Returns:
            转换后的 Transform 对象自身，便于链式调用
        """
        # 添加聚合转换
        self.transforms.append({
            "aggregate": [
                {"op": "min", "field": x_field, "as": "x_min"},
                {"op": "max", "field": x_field, "as": "x_max"},
                {"op": "min", "field": y_field, "as": "y_min"},
                {"op": "max", "field": y_field, "as": "y_max"}
            ]
        })
        return self

    def add_center_calculations(self):
        """
        添加计算中心点的转换，基于已有的最小值和最大值。
        
        Returns:
            转换后的 Transform 对象自身，便于链式调用
        """
        self.add_calculate("(datum.x_min + datum.x_max)/2", "x_center")
        self.add_calculate("(datum.y_min + datum.y_max)/2", "y_center")
        return self

    def add_diff_calculations(self):
        """
        添加计算差异值的转换，基于已有的最小值和最大值。
        
        Returns:
            转换后的 Transform 对象自身，便于链式调用
        """
        self.add_calculate("(datum.x_max - datum.x_min)/2", "x_diff")
        self.add_calculate("(datum.y_max - datum.y_min)/2", "y_diff")
        return self

    def add_center_label_calculation(self, format_precision: str = ".2f"):
        """
        添加创建中心点和差值标签的转换。
        
        Args:
            format_precision: 格式化精度，默认为".2f"
        
        Returns:
            转换后的 Transform 对象自身，便于链式调用
        """
        # 添加标签文本计算
        label_expression = (
            f"'X: ' + format(datum.x_center, '{format_precision}') + ' ± ' + "
            f"format(datum.x_diff, '{format_precision}') + '\\nY: ' + "
            f"format(datum.y_center, '{format_precision}') + ' ± ' + "
            f"format(datum.y_diff, '{format_precision}')"
        )
        self.add_calculate(label_expression, "center_label_with_diff")
        return self

    def create_center_point_transforms(self, x_field: str, y_field: str):
        """
        一次性创建所有需要的中心点相关转换。
        
        Args:
            x_field: x轴字段名
            y_field: y轴字段名
        
        Returns:
            转换后的 Transform 对象自身，便于链式调用
        """
        return (self
                .add_min_max_aggregate(x_field, y_field)
                .add_center_calculations()
                .add_diff_calculations()
                .add_center_label_calculation())
        """
        添加一个基于指定字段排序的排名窗口操作
        
        Args:
            field: 要排序的字段名，如 "Season"
            order: 排序方式，"ascending" 或 "descending"，默认为 "descending"
            alias: 排名结果的别名，默认为 "rank"
        
        Returns:
            转换后的 Transform 对象自身，便于链式调用
        """
        # 添加排名窗口操作
        self.transforms.append({
            "window": [{"op": "rank", "as": alias}],
            "sort": [{"field": field, "order": order}]
        })
        return self
        """
        添加一组变换，用于获取趋势线的终点
        
        Args:
            x_field: x轴字段名，如 "Season"
            y_field: y轴字段名，如 "Average Points Scored per Game"
            rank_field: 用于排序的字段，默认使用x_field
            order: 排序顺序，默认为降序("descending")
        
        Returns:
            转换后的 Transform 对象自身，便于链式调用
        """
        if rank_field is None:
            rank_field = x_field
        
        # 添加回归变换
        self.add_regression_transform(y_field, x_field)
        
        # 添加排名变换
        self.add_rank_window(rank_field, order)
        
        # 添加过滤条件，只保留排名第一的点
        self.add_filter("datum.rank == 1")
        
        return self

    def add_rank_window(self, field: str,  order: str = "descending", rank_alias: str = "rank"):
        """
        添加一个基于指定字段排序并过滤指定排名的操作。
        
        Args:
            field: 要排序的字段名，如 "adjusted_y"
            rank_index: 要保留的排名，默认为1（保留排名第一的记录）
            order: 排序方式，"ascending" 或 "descending"，默认为 "descending"
            rank_alias: 排名结果的别名，默认为 "rank"
            
        Returns:
            转换后的 Transform 对象自身，便于链式调用
        """
        # 添加排名窗口操作
        self.transforms.append({
            "window": [{"op": "rank", "as": rank_alias}],
            "sort": [{"field": field, "order": order}]
        })
        
        return self