from typing import Dict, Optional, Literal
from ChartMark.annotation_ast_genetic.target_node.BaseTargetNode import BaseTargetNode, TargetType
from ChartMark.annotation_ast_genetic.target_node.filter_node.FilterNode import ChartType, FilterNode, FilterCondition
from dataclasses import dataclass, field
from ChartMark.vegalite_ast.ChartNode import ChartFieldInfo


@dataclass
class DataItemsTarget:
    """数据项目标类型"""
    type: Literal["data_items"] = "data_items"
    filter: Optional[FilterCondition] = None


class DataItemsTargetNode(BaseTargetNode):
    """数据项目标节点"""
    TARGET_TYPE: TargetType = "data_items"
    
    def __init__(self, target_obj: Dict = None, chart_type: Optional[ChartType] = None):
        self.filter_node = None
        super().__init__(target_obj, chart_type)
    
    def _parse_target_obj(self, target_obj: Dict):
        """解析数据项目标"""
        # 检查是否存在filter字段，如果存在则解析
        if "filter" in target_obj:
            filter_obj = target_obj.get("filter", {})
            if filter_obj is not None and not isinstance(filter_obj, dict):
                raise ValueError("filter字段必须是字典类型或为None")
            
            # 只有在filter_obj存在且非空时才创建FilterNode
            if filter_obj:
                # 使用FilterNode类处理过滤条件，传入图表类型
                self.filter_node = FilterNode(filter_obj, self.chart_type)
                if not self.filter_node.validate():
                    raise ValueError("过滤条件验证失败")
    
    def to_vegalite_filter(self, chart_field_info: ChartFieldInfo) -> Dict:
        """将过滤条件转换为VegaLite的filter格式"""
        if self.filter_node:
            return self.filter_node.to_vegalite_filter(chart_field_info)
        return {}
    
    def to_dict(self) -> Dict:
        """将节点转换为字典格式"""
        result = super().to_dict()
        
        # 只有在filter_node存在时才添加filter字段
        if self.filter_node:
            result["filter"] = self.filter_node.to_dict()
        
        return result
