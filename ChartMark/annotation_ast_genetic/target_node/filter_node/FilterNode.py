from typing import Dict, Optional, List
from ChartMark.annotation_ast_genetic.ast_base import BaseNode
from .LogicalExpression import LogicalExpression, ChartType, CategoryFilter, QuantityFilter, GroupFilter, TemporalFilter, FilterItem
from dataclasses import dataclass, field
from ChartMark.vegalite_ast.ChartNode import ChartFieldInfo

@dataclass
class FilterCondition:
    """过滤条件组合"""
    and_: Optional[List[FilterItem]] = field(default_factory=list),
    not_: Optional[List[FilterItem]] = field(default_factory=list),
    or_: Optional[List[FilterItem]] = field(default_factory=list)



class FilterNode(BaseNode):
    """
    过滤条件节点，用于管理和验证不同类型的过滤条件
    """
    def __init__(self, filter_obj: Dict = None, chart_type: Optional[ChartType] = None):
        super().__init__()
        self.logic_expr: Optional[LogicalExpression] = None
        self.chart_type = chart_type
        
        if filter_obj:
            self._parse_filter(filter_obj)
    
    def _parse_filter(self, filter_obj: Dict):
        """解析过滤条件"""
        if not isinstance(filter_obj, dict):
            raise ValueError("过滤条件必须是字典类型")
        
        # 检查是否包含逻辑操作符
        logic_operators = [op for op in filter_obj.keys() if op in ["and", "or", "not"]]
        
        if not logic_operators:
            raise ValueError("过滤条件必须包含逻辑操作符(and/or/not)")
        
        if len(logic_operators) > 1:
            raise ValueError("过滤条件只能包含一个顶级逻辑操作符")
        
        operator = logic_operators[0]
        operands = filter_obj[operator]
        
        if not isinstance(operands, list):
            if operator == "not":
                operands = [operands]  # not操作符可以只有一个操作数
            else:
                raise ValueError(f"{operator}逻辑操作符的值必须是列表")
        
        # 递归解析操作数
        parsed_operands = []
        for operand in operands:
            if isinstance(operand, dict):
                # 检查是否是嵌套的逻辑表达式
                nested_operators = [op for op in operand.keys() if op in ["and", "or", "not"]]
                
                if nested_operators:
                    # 递归解析嵌套的逻辑表达式
                    nested_filter = FilterNode(operand, self.chart_type)
                    parsed_operands.append(nested_filter.logic_expr)
                else:
                    # 是过滤条件项
                    axis_type = operand.get("axisType")
                    if not axis_type:
                        raise ValueError("过滤条件必须指定axisType字段")
                    
                    if axis_type == "category":
                        filter_item = CategoryFilter(
                            oneOf=operand.get("oneOf", [])
                        )
                    elif axis_type == "quantity":
                        filter_item = QuantityFilter(
                            range=operand.get("range"),
                            equal=operand.get("equal"),
                            lt=operand.get("lt"),
                            lte=operand.get("lte"),
                            gt=operand.get("gt"),
                            gte=operand.get("gte")
                        )
                    elif axis_type == "x_quantity" or axis_type == "y_quantity":
                        filter_item = QuantityFilter(
                            axisType=axis_type,
                            range=operand.get("range"),
                            equal=operand.get("equal"),
                            lt=operand.get("lt"),
                            lte=operand.get("lte"),
                            gt=operand.get("gt"),
                            gte=operand.get("gte")
                        )
                    elif axis_type == "group":
                        filter_item = GroupFilter(
                            oneOf=operand.get("oneOf", [])
                        )
                    elif axis_type == "temporal":
                        filter_item = TemporalFilter(
                            range=operand.get("range"),
                            equal=operand.get("equal"),
                            lt=operand.get("lt"),
                            lte=operand.get("lte"),
                            gt=operand.get("gt"),
                            gte=operand.get("gte")
                        )
                    else:
                        raise ValueError(f"无效的轴类型: {axis_type}")
                    
                    parsed_operands.append(filter_item)
            else:
                raise ValueError("过滤条件的操作数必须是字典类型")
        
        # 创建逻辑表达式
        self.logic_expr = LogicalExpression(operator, parsed_operands)
    
    def to_vegalite_filter(self, chart_field_info: ChartFieldInfo) -> Dict:
        """将过滤条件转换为vegalite的filter格式"""
        if not self.logic_expr:
            return {}
        
        return self.logic_expr.to_vegalite_filter(chart_field_info)
    
    
    def validate(self) -> bool:
        """验证过滤条件的有效性"""
        if not self.logic_expr:
            return False
        
        try:
            self.logic_expr.validate(self.chart_type)
            return True
        except ValueError:
            return False
    
    def to_dict(self) -> Dict:
        """将过滤条件转换为字典格式"""
        if not self.logic_expr:
            return {}
        
        return self.logic_expr.to_dict() 