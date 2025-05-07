from ChartMark.annotation_ast_genetic.ast_base import BaseNode
from typing import Dict, List, Literal, Optional, Any, Union, TypeVar
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# 定义可接受的元素类型：字符串或数字
# T = TypeVar('T', str, int, float)

# 图表类型定义
ChartType = Literal["line", "bar", "scatter", "pie", "group_bar", "group_line", "group_scatter"]

@dataclass
class ChartDict:
    """
    图表数据结构定义，用作类型提示和文档
    """
    title: str = ""
    type: ChartType = ""
    x_name: str = ""
    y_name: str = ""

class BaseChartNode(BaseNode, ABC):
    """
    基础图表节点，只包含基本属性：标题、类型和轴名称
    """
    def __init__(self, chart_obj: Dict = None):
        super().__init__()
        self.title = ""
        self.type = ""
        self.x_name = ""
        self.y_name = ""
        
        if chart_obj:
            self._parse_base_properties(chart_obj)
    
    def _parse_base_properties(self, chart_obj: Dict):
        """解析基本图表属性"""
        self.title = chart_obj.get("title", "")
        self.type = chart_obj.get("type", "line")
        self.x_name = chart_obj.get("x_name", "")
        self.y_name = chart_obj.get("y_name", "")
        
    def get_chart_type(self) -> ChartType:
        """
        获取图表类型
        """
        return self.type
    
    
    @abstractmethod
    def _parse_data_properties(self, chart_obj: Dict) -> None:
        """
        处理图表数据，设置x_data和y_data，classify_data
        子类必须实现此方法来解析特定类型的图表数据
        
        参数:
            chart_obj: 图表数据字典
        """
        pass  # 子类必须实现此方法
    
    @abstractmethod
    def to_dict(self) -> Dict:
        """
        将节点转换为字典格式
        """
        pass
    
    @abstractmethod
    def _parse_to_metadata(self) -> List[Dict[str, Any]]:
        """
        将节点转换为元数据格式
        """
        pass
    
    @abstractmethod
    def to_vegalite_chart(self) -> str:
        """
        将节点转换为VegaLite图表规范字符串
        """
        pass
