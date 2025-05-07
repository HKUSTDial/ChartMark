from typing import Dict, Literal

# 方法类型
MethodType = Literal["reference", "highlight", "encoding", "summary", "description"]


class BaseMethodNode:
    """方法的基类"""
    def __init__(self):
        self.type: MethodType = ""
    
    def to_dict(self) -> Dict:
        """将方法转换为字典格式"""
        return {"type": self.type}