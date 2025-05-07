from ChartMark.annotation_ast_genetic.ast_base import BaseNode
from typing import Dict, Optional, Any
from ChartMark.annotation_ast_genetic.target_node.BaseTargetNode import BaseTargetNode
from ChartMark.annotation_ast_genetic.marker_node.MarkerNode import MarkerNode
from abc import ABC, abstractmethod
from ChartMark.vegalite_ast.ChartNode import Chart

class BaseTechnique(BaseNode, ABC):
    """
    技术节点基类，用于处理技术相关的配置
    包含基本属性：name（名称）、target（目标）和marker（标记，可选）
    """
    def __init__(self, name: str, target: BaseTargetNode, marker: MarkerNode = None):
        super().__init__()
        if not name or not isinstance(name, str):
            raise ValueError("name必须是非空字符串")
        if not target or not isinstance(target, BaseTargetNode):
            raise ValueError("target必须是BaseTargetNode实例")
        if marker and not isinstance(marker, MarkerNode):
            raise ValueError("marker必须是MarkerNode实例")
            
        self.name: str = name
        self.target: BaseTargetNode = target  # BaseTargetNode类型，必需的
        self.marker: Optional[MarkerNode] = marker  # MarkerNode类型，可选的
    
    def to_dict(self) -> Dict:
        """将节点转换为字典格式"""
        result = {
            "name": self.name,
            "target": self.target.to_dict()
        }
        
        if self.marker:
            result["marker"] = self.marker.to_dict()
        
        return result
    
    def validate(self) -> bool:
        """
        验证技术节点的数据是否有效
        规则：
        1. name必须是非空字符串
        2. target必须存在且有效
        """
        # 检查name是否为非空字符串
        if not self.name or not isinstance(self.name, str):
            return False
        
        # 检查target是否存在且有效
        if not self.target or not isinstance(self.target, BaseTargetNode):
            return False
        
        # 如果有marker，检查marker是否有效
        if self.marker and not isinstance(self.marker, MarkerNode):
            return False
        
        return True
    
    def set_marker(self, marker: MarkerNode) -> bool:
        """
        设置标记对象
        
        参数:
            marker: MarkerNode实例
            
        返回:
            设置是否成功
        """
        if not marker or not isinstance(marker, MarkerNode):
            return False
        
        self.marker = marker
        return True
    
    def set_name(self, name: str) -> bool:
        """
        设置技术名称
        
        参数:
            name: 技术名称
            
        返回:
            设置是否成功
        """
        if not name or not isinstance(name, str):
            return False
        
        self.name = name
        return True
    
    def set_target(self, target: BaseTargetNode) -> bool:
        """
        设置目标节点
        
        参数:
            target: BaseTargetNode实例
            
        返回:
            设置是否成功
        """
        if not target or not isinstance(target, BaseTargetNode):
            return False
        
        self.target = target
        return True

    @abstractmethod
    def parse_to_vegalite(self, original_vegalite_node: Chart) -> Dict:
        """
        将原始vegalite转换为技术节点
        
        参数:
            original_vegalite_node: 原始vegalite节点实例
            
        返回:
            处理后的vegalite字典
        """
        pass