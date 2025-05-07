from ChartMark.annotation_ast_genetic.ast_base import BaseNode
from typing import Dict, List, Optional, Any
from ChartMark.annotation_ast_genetic.method_node.BaseMethodNode import BaseMethodNode
from ChartMark.annotation_ast_genetic.data_node.BaseDataNode import BaseDataNode
from ChartMark.annotation_ast_genetic.technique_node.BaseTechnique import BaseTechnique


class BaseAnnotationNode(BaseNode):
    """
    注释节点基类，用于处理注释相关的配置
    包含基本属性：id、method、data和techniques
    """
    def __init__(self, id: str, method: BaseMethodNode, data: BaseDataNode, techniques: List[BaseTechnique]):
        super().__init__()
        
        if not isinstance(id, str):
            raise ValueError("id必须是字符串类型")
        
        if not method or not isinstance(method, BaseMethodNode):
            raise ValueError("method必须是BaseMethodNode实例")
            
        if not data or not isinstance(data, BaseDataNode):
            raise ValueError("data必须是BaseDataNode实例")
            
        if not techniques or not isinstance(techniques, list) or len(techniques) == 0:
            raise ValueError("techniques必须是非空的BaseTechnique列表")
            
        for technique in techniques:
            if not isinstance(technique, BaseTechnique):
                raise ValueError("techniques列表中的所有元素必须是BaseTechnique实例")
        
        self.id: str = id
        self.method: BaseMethodNode = method  # BaseMethodNode类型，必需的
        self.data: BaseDataNode = data  # BaseDataNode类型，必需的
        self.techniques: List[BaseTechnique] = techniques  # BaseTechnique类型的列表，必需的
    
    def to_dict(self) -> Dict:
        """将节点转换为字典格式"""
        result = {
            "id": self.id,
            "method": self.method.to_dict(),
            "data": self.data.to_dict(),
            "techniques": [technique.to_dict() for technique in self.techniques]
        }
        
        return result
    
    def validate(self) -> bool:
        """
        验证注释节点的数据是否有效
        规则：
        1. method必须存在且有效
        2. data必须存在且有效
        3. 必须至少有一个technique且所有technique都有效
        """
        # 检查method是否存在且有效
        if not self.method or not isinstance(self.method, BaseMethodNode):
            return False
        
        # 检查data是否存在且有效
        if not self.data or not isinstance(self.data, BaseDataNode):
            return False
        
        # 检查是否至少有一个technique且所有technique都有效
        if not self.techniques:
            return False
        
        for technique in self.techniques:
            if not isinstance(technique, BaseTechnique) or not technique.validate():
                return False
        
        return True
    
    def add_technique(self, technique: BaseTechnique) -> bool:
        """
        添加技术节点
        
        参数:
            technique: BaseTechnique实例
            
        返回:
            添加是否成功
        """
        if not technique or not isinstance(technique, BaseTechnique):
            return False
        
        self.techniques.append(technique)
        return True
    
    def set_method(self, method: BaseMethodNode) -> bool:
        """
        设置方法节点
        
        参数:
            method: BaseMethodNode实例
            
        返回:
            设置是否成功
        """
        if not method or not isinstance(method, BaseMethodNode):
            return False
        
        self.method = method
        return True
    
    def set_data(self, data: BaseDataNode) -> bool:
        """
        设置数据节点
        
        参数:
            data: BaseDataNode实例
            
        返回:
            设置是否成功
        """
        if not data or not isinstance(data, BaseDataNode):
            return False
        
        self.data = data
        return True
        
    def set_id(self, id: str) -> bool:
        """
        设置注释ID
        
        参数:
            id: 字符串ID
            
        返回:
            设置是否成功
        """
        if not isinstance(id, str):
            return False
            
        self.id = id
        return True
