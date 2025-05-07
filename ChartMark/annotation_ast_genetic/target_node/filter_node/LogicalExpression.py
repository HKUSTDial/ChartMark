from typing import Dict, List, Literal, Optional, Union, Any
from dataclasses import dataclass, field
from ChartMark.vegalite_ast.ChartNode import ChartFieldInfo

# ===== 轴类型 =====
AxisType = Literal["category", "quantity", "group", "temporal", "x_quantity", "y_quantity"]

# ===== 图表类型 =====
ChartType = Literal["line", "bar", "scatter", "pie", "group_bar", "group_line", "group_scatter"]

# ===== 逻辑运算符 =====
LogicOperator = Literal["and", "or", "not"]

@dataclass
class CategoryFilter:
    """分类轴过滤条件"""
    axisType: Literal["category"] = "category"
    oneOf: List[str] = field(default_factory=list)
    
    def validate(self):
        """验证分类轴过滤条件"""
        if not isinstance(self.oneOf, list):
            raise ValueError("category过滤条件的oneOf必须是字符串列表")
        
        if not all(isinstance(item, str) for item in self.oneOf):
            raise ValueError("category过滤条件的oneOf必须只包含字符串")
        
        if not self.oneOf:
            raise ValueError("category过滤条件的oneOf不能为空")

@dataclass
class QuantityFilter:
    """数量轴过滤条件"""
    axisType: Literal["quantity", "x_quantity", "y_quantity"] = "quantity"
    range: Optional[List[float]] = None
    equal: Optional[float] = None
    lt: Optional[float] = None
    lte: Optional[float] = None
    gt: Optional[float] = None
    gte: Optional[float] = None
    
    def validate(self):
        """验证数量轴过滤条件"""
        if self.range is not None:
            if not isinstance(self.range, list) or len(self.range) != 2:
                raise ValueError(f"{self.axisType}过滤条件的range必须是包含两个数字的列表")
            
            if not all(isinstance(item, (int, float)) for item in self.range):
                raise ValueError(f"{self.axisType}过滤条件的range必须只包含数字")
            
            if self.range[0] >= self.range[1]:
                raise ValueError(f"{self.axisType}过滤条件的range必须是升序的[最小值, 最大值]")
        
        if self.equal is not None and not isinstance(self.equal, (int, float)):
            raise ValueError(f"{self.axisType}过滤条件的equal必须是数字")
        
        if self.lt is not None and not isinstance(self.lt, (int, float)):
            raise ValueError(f"{self.axisType}过滤条件的lt必须是数字")
        
        if self.lte is not None and not isinstance(self.lte, (int, float)):
            raise ValueError(f"{self.axisType}过滤条件的lte必须是数字")
        
        if self.gt is not None and not isinstance(self.gt, (int, float)):
            raise ValueError(f"{self.axisType}过滤条件的gt必须是数字")
        
        if self.gte is not None and not isinstance(self.gte, (int, float)):
            raise ValueError(f"{self.axisType}过滤条件的gte必须是数字")
        
        # 确保至少有一个条件
        if self.range is None and self.equal is None and self.lt is None and self.lte is None and self.gt is None and self.gte is None:
            raise ValueError(f"{self.axisType}过滤条件必须至少指定一个条件(range/equal/lt/lte/gt/gte)")
        
        # 检查逻辑一致性
        if self.equal is not None:
            if self.lt is not None and self.equal >= self.lt:
                raise ValueError(f"{self.axisType}过滤条件的equal必须小于lt")
            
            if self.lte is not None and self.equal > self.lte:
                raise ValueError(f"{self.axisType}过滤条件的equal必须小于等于lte")
            
            if self.gt is not None and self.equal <= self.gt:
                raise ValueError(f"{self.axisType}过滤条件的equal必须大于gt")
            
            if self.gte is not None and self.equal < self.gte:
                raise ValueError(f"{self.axisType}过滤条件的equal必须大于等于gte")
        
        if self.lt is not None and self.gt is not None and self.lt <= self.gt:
            raise ValueError(f"{self.axisType}过滤条件的lt必须大于gt")
        
        if self.lte is not None and self.gte is not None and self.lte < self.gte:
            raise ValueError(f"{self.axisType}过滤条件的lte必须大于等于gte")

@dataclass
class GroupFilter:
    """分组轴过滤条件"""
    axisType: Literal["group"] = "group"
    oneOf: List[str] = field(default_factory=list)
    
    def validate(self):
        """验证分组轴过滤条件"""
        if not isinstance(self.oneOf, list):
            raise ValueError("group过滤条件的oneOf必须是字符串列表")
        
        if not all(isinstance(item, str) for item in self.oneOf):
            raise ValueError("group过滤条件的oneOf必须只包含字符串")
        
        if not self.oneOf:
            raise ValueError("group过滤条件的oneOf不能为空")

@dataclass
class TemporalFilter:
    """时间轴过滤条件"""
    axisType: Literal["temporal"] = "temporal"
    range: Optional[List[Dict[str, Any]]] = None
    equal: Optional[Dict[str, Any]] = None
    lt: Optional[Dict[str, Any]] = None
    lte: Optional[Dict[str, Any]] = None
    gt: Optional[Dict[str, Any]] = None
    gte: Optional[Dict[str, Any]] = None
    
    def validate(self):
        """验证时间轴过滤条件"""
        # 时间值只能是字典格式(如{"year": 2020, "month": "apr", "date": 1})
        
        if self.range is not None:
            if not isinstance(self.range, list) or len(self.range) != 2:
                raise ValueError("temporal过滤条件的range必须是包含两个值的列表")
            
            if not all(isinstance(item, dict) for item in self.range):
                raise ValueError("temporal过滤条件的range必须包含日期字典")
        
        if self.equal is not None and not isinstance(self.equal, dict):
            raise ValueError("temporal过滤条件的equal必须是日期字典")
        
        if self.lt is not None and not isinstance(self.lt, dict):
            raise ValueError("temporal过滤条件的lt必须是日期字典")
        
        if self.lte is not None and not isinstance(self.lte, dict):
            raise ValueError("temporal过滤条件的lte必须是日期字典")
        
        if self.gt is not None and not isinstance(self.gt, dict):
            raise ValueError("temporal过滤条件的gt必须是日期字典")
        
        if self.gte is not None and not isinstance(self.gte, dict):
            raise ValueError("temporal过滤条件的gte必须是日期字典")
        
        # 确保至少有一个条件
        if self.range is None and self.equal is None and self.lt is None and self.lte is None and self.gt is None and self.gte is None:
            raise ValueError("temporal过滤条件必须至少指定一个条件(range/equal/lt/lte/gt/gte)")

# 过滤器类型
FilterItem = Union[CategoryFilter, QuantityFilter, GroupFilter, TemporalFilter]

class LogicalExpression:
    """逻辑表达式"""
    def __init__(self, operator: LogicOperator, operands: List[Union['LogicalExpression', FilterItem]]):
        self.operator = operator
        self.operands = operands
    
    def validate(self, chart_type: Optional[ChartType] = None):
        """验证逻辑表达式"""
        if not self.operands:
            raise ValueError(f"{self.operator}逻辑表达式必须至少有一个操作数")
        
        # 检查操作数类型
        for operand in self.operands:
            if isinstance(operand, LogicalExpression):
                operand.validate(chart_type)
            else:
                # 是过滤条件项
                if isinstance(operand, (CategoryFilter, QuantityFilter, GroupFilter, TemporalFilter)):
                    # 根据图表类型检查轴类型是否合法
                    if chart_type is not None:
                        self._validate_axis_type_for_chart(operand.axisType, chart_type)
                    
                    # 验证过滤条件项
                    operand.validate()
                else:
                    raise ValueError("逻辑表达式的操作数必须是逻辑表达式或过滤条件")
        
        # 对NOT操作符进行特殊检查
        if self.operator == "not" and len(self.operands) != 1:
            raise ValueError("not逻辑表达式必须只有一个操作数")
    
    def _validate_axis_type_for_chart(self, axis_type: AxisType, chart_type: ChartType):
        """根据图表类型验证轴类型是否合法"""
        if chart_type in ["bar", "pie"]:
            # bar和pie图表支持category和quantity
            if axis_type not in ["category", "quantity"]:
                raise ValueError(f"{chart_type}图表不支持{axis_type}轴类型")
        
        elif chart_type == "scatter":
            # scatter图表支持x_quantity和y_quantity
            if axis_type not in ["x_quantity", "y_quantity"]:
                raise ValueError(f"{chart_type}图表不支持{axis_type}轴类型")
        
        elif chart_type == "line":
            # line图表支持temporal
            if axis_type not in ["temporal", "quantity"]:
                raise ValueError(f"{chart_type}图表不支持{axis_type}轴类型")
        
        elif chart_type in ["group_bar", "group_line", "group_scatter"]:
            # 分组图表支持group
            if axis_type not in ["category", "quantity", "group", "temporal", "x_quantity", "y_quantity"]:
                raise ValueError(f"{chart_type}图表不支持{axis_type}轴类型")
    
    def to_dict(self) -> Dict:
        """将逻辑表达式转换为字典格式"""
        operands_dict = []
        
        for operand in self.operands:
            if isinstance(operand, LogicalExpression):
                operands_dict.append(operand.to_dict())
            else:
                # 是过滤条件项
                if isinstance(operand, CategoryFilter):
                    operands_dict.append({
                        "axisType": operand.axisType,
                        "oneOf": operand.oneOf
                    })
                elif isinstance(operand, QuantityFilter):
                    filter_dict = {"axisType": operand.axisType}
                    
                    if operand.range is not None:
                        filter_dict["range"] = operand.range
                    if operand.equal is not None:
                        filter_dict["equal"] = operand.equal
                    if operand.lt is not None:
                        filter_dict["lt"] = operand.lt
                    if operand.lte is not None:
                        filter_dict["lte"] = operand.lte
                    if operand.gt is not None:
                        filter_dict["gt"] = operand.gt
                    if operand.gte is not None:
                        filter_dict["gte"] = operand.gte
                    
                    operands_dict.append(filter_dict)
                elif isinstance(operand, GroupFilter):
                    operands_dict.append({
                        "axisType": operand.axisType,
                        "oneOf": operand.oneOf
                    })
                elif isinstance(operand, TemporalFilter):
                    filter_dict = {"axisType": operand.axisType}
                    
                    if operand.range is not None:
                        filter_dict["range"] = operand.range
                    if operand.equal is not None:
                        filter_dict["equal"] = operand.equal
                    if operand.lt is not None:
                        filter_dict["lt"] = operand.lt
                    if operand.lte is not None:
                        filter_dict["lte"] = operand.lte
                    if operand.gt is not None:
                        filter_dict["gt"] = operand.gt
                    if operand.gte is not None:
                        filter_dict["gte"] = operand.gte
                    
                    operands_dict.append(filter_dict)
        
        return {self.operator: operands_dict}

    def to_vegalite_filter(self, chart_field_info: ChartFieldInfo) -> Dict:
        """
        将逻辑表达式转换为VegaLite的filter格式
        
        参数:
            chart_field_info: 图表字段信息，包含各轴的名称
            
        返回:
            VegaLite格式的filter表达式
        """
        operands_expr = []
        
        for operand in self.operands:
            if isinstance(operand, LogicalExpression):
                # 递归处理嵌套的逻辑表达式
                operands_expr.append(operand.to_vegalite_filter(chart_field_info))
            else:
                # 处理过滤条件项
                field_name = self._get_field_name_for_axis_type(operand.axisType, chart_field_info)
                
                if field_name is None:
                    raise ValueError(f"无法找到{operand.axisType}轴类型对应的字段名")
                
                # 根据过滤条件类型转换为VegaLite格式
                if isinstance(operand, CategoryFilter) or isinstance(operand, GroupFilter):
                    # 对于分类/分组过滤，使用oneOf条件
                    operands_expr.append({
                        "field": field_name,
                        "oneOf": operand.oneOf
                    })
                elif isinstance(operand, QuantityFilter) or isinstance(operand, TemporalFilter):
                    # 对于数量/时间过滤，转换各种条件
                    filter_expr = {"field": field_name}
                    
                    if operand.range is not None:
                        filter_expr["range"] = operand.range
                    if operand.equal is not None:
                        filter_expr["equal"] = operand.equal
                    if operand.lt is not None:
                        filter_expr["lt"] = operand.lt
                    if operand.lte is not None:
                        filter_expr["lte"] = operand.lte
                    if operand.gt is not None:
                        filter_expr["gt"] = operand.gt
                    if operand.gte is not None:
                        filter_expr["gte"] = operand.gte
                    
                    operands_expr.append(filter_expr)
        
        # 如果只有一个操作数且操作符为"not"，添加"not"操作符
        if self.operator == "not" and len(operands_expr) == 1:
            return {"not": operands_expr[0]}
        # 否则返回带有操作符的表达式
        return {self.operator: operands_expr}
    
    def _get_field_name_for_axis_type(self, axis_type: AxisType, chart_field_info: ChartFieldInfo) -> Optional[str]:
        """
        根据轴类型获取对应的字段名
        
        参数:
            axis_type: 轴类型
            chart_field_info: 图表字段信息
            
        返回:
            对应的字段名，如果找不到则返回None
        """
        from ChartMark.vegalite_ast.ChartNode import BarFieldInfo, PieFieldInfo, LineFieldInfo, ScatterFieldInfo
        
        if axis_type == "category":
            if isinstance(chart_field_info, (BarFieldInfo, PieFieldInfo)):
                return chart_field_info.category_name
        elif axis_type == "quantity":
            if isinstance(chart_field_info, (BarFieldInfo, PieFieldInfo, LineFieldInfo)):
                return chart_field_info.quantity_name
        elif axis_type == "group":
            if hasattr(chart_field_info, "group_name"):
                return chart_field_info.group_name
        elif axis_type == "temporal":
            if isinstance(chart_field_info, LineFieldInfo):
                return chart_field_info.temporal_name
        elif axis_type == "x_quantity":
            if isinstance(chart_field_info, ScatterFieldInfo):
                return chart_field_info.x_quantity_name
        elif axis_type == "y_quantity":
            if isinstance(chart_field_info, ScatterFieldInfo):
                return chart_field_info.y_quantity_name
        
        return None
