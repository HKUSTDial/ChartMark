from typing import Dict, List, Any, Optional, ClassVar, Tuple, Union, Callable, Type, Protocol, cast, Set, TypeVar, Generic, AbstractSet, Mapping, Sequence, MutableMapping, MutableSequence, Iterable
from abc import ABC, abstractmethod
from ..BaseChartNode import BaseChartNode

class BaseNonGroupNode(BaseChartNode, ABC):
    """
    非分组图表节点基类，继承基础图表节点
    利用父类的x_name和y_name属性，并添加x_data和y_data属性
    要求子类必须实现_process_data方法来设置x_data和y_data
    """
    def __init__(self, chart_obj: Dict = None):
        """
        初始化非分组图表节点
        
        参数:
            chart_obj: 图表数据字典
        """
        # 先调用父类初始化方法，处理基本属性（包括x_name和y_name）
        super().__init__(chart_obj)
        
        # 初始化数据属性
        self.x_data: List[Any] = []
        self.y_data: List[Any] = []
        
    
    def get_x_data(self) -> List[Any]:
        """
        获取X轴数据
        
        返回:
            X轴数据列表
        """
        return self.x_data
    
    def get_y_data(self) -> List[Any]:
        """
        获取Y轴数据
        
        返回:
            Y轴数据列表
        """
        return self.y_data
        
    def _parse_to_metadata(self) -> List[Dict[str, Any]]:
        """
        将x_data和y_data转换为格式化的元数据列表
        例如: 将x_data=["A", "B"], y_data=[1, 2], x_name="类别", y_name="值"
        转换为: [{"类别": "A", "值": 1}, {"类别": "B", "值": 2}]
        
        返回:
            包含x_name和y_name作为键的字典列表
        """
        # 确保x_name和y_name存在
        if not self.x_name or not self.y_name:
            raise ValueError("x_name和y_name必须存在才能生成元数据")
            
        # 确保x_data和y_data非空且长度一致
        if not self.x_data or not self.y_data or len(self.x_data) != len(self.y_data):
            raise ValueError("x_data和y_data必须非空且长度一致")
            
        # 生成元数据列表
        metadata_list = []
        for i in range(len(self.x_data)):
            metadata = {
                self.x_name: self.x_data[i],
                self.y_name: self.y_data[i]
            }
            metadata_list.append(metadata)
            
        return metadata_list

    def to_dict(self) -> Dict:
        """
        将节点转换为字典格式，包含所有属性
        """
        return {
            "title": self.title,
            "type": self.type,
            "x_name": self.x_name,
            "y_name": self.y_name,
            "x_data": self.x_data,
            "y_data": self.y_data
        }
        
    def to_vegalite_chart(self) -> str:
        """
        将图表转换为VegaLite图表规范字符串
        使用子类定义的ORIGINAL_CHART_TEMPLATE模板
        填充title、x_name、y_name以及metadata_list
        
        返回:
            VegaLite图表规范的字符串
        """
        # 检查子类是否定义了图表模板
        if not hasattr(self.__class__, 'ORIGINAL_CHART_TEMPLATE'):
            raise NotImplementedError(f"{self.__class__.__name__}未定义ORIGINAL_CHART_TEMPLATE")
            
        # 获取模板
        template = self.__class__.ORIGINAL_CHART_TEMPLATE
        
        # 确保有必要的数据
        if not self.title or not self.x_name or not self.y_name:
            raise ValueError("生成图表需要title、x_name和y_name")
            
        # 生成元数据列表并转为JSON字符串
        try:
            metadata_list = self._parse_to_metadata()
            
            # 导入json处理元数据
            import json
            metadata_json = json.dumps(metadata_list)
            
            # 填充模板
            chart_spec = template.format(
                title=self.title,
                x_name=self.x_name,
                y_name=self.y_name,
                metadata_list=metadata_json
            )
            
            return chart_spec
            
        except Exception as e:
            raise ValueError(f"生成VegaLite图表失败: {str(e)}")