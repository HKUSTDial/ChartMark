# chart_ast_generic/ast_base.py
from abc import ABC, abstractmethod

class BaseNode(ABC):
    """
    所有 AST 节点的抽象基类
    """
    @abstractmethod
    def to_dict(self):
        """
        序列化节点为字典
        """
        pass