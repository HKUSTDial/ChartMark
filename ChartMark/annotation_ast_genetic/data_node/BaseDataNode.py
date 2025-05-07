from ChartMark.annotation_ast_genetic.ast_base import BaseNode
from typing import Dict, List, Literal, Optional, Union, Type, Any
from dataclasses import dataclass, field

# 数据源类型
SourceType = Literal["external", "derived", "internal", "none"]

class BaseDataNode(BaseNode):
    """
    数据节点基类，只处理数据源属性
    """
    def __init__(self, data_obj: Dict = None):
        super().__init__()
        self.source: SourceType = "none"
        
        if data_obj:
            self._parse_source(data_obj)
    
    def _parse_source(self, data_obj: Dict):
        """解析数据源"""
        if not isinstance(data_obj, dict):
            raise ValueError("数据对象必须是字典类型")
        
        source = data_obj.get("source")
        if not source:
            raise ValueError("数据对象必须指定source字段")
        
        if source not in ["external", "derived", "internal", "none"]:
            raise ValueError(f"无效的数据源类型: {source}")
        
        self.source = source
    
    def to_dict(self) -> Dict:
        """将节点转换为字典格式"""
        return {"source": self.source}
    
    # @classmethod
    # def create(cls, data_obj: Dict) -> 'BaseDataNode':
    #     """
    #     工厂方法，根据数据源类型创建相应的数据节点对象
    #     """
    #     if not isinstance(data_obj, dict):
    #         raise ValueError("数据对象必须是字典类型")
        
    #     source = data_obj.get("source")
    #     if not source:
    #         raise ValueError("数据对象必须指定source字段")
        
    #     # 根据数据源类型选择合适的节点类
    #     if source == "external":
    #         return ExternalDataNode(data_obj)
    #     else:
    #         return SimpleDataNode(data_obj)




