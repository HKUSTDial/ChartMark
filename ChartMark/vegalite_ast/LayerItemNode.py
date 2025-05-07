from typing import Dict, Union
from ChartMark.vegalite_ast.EncodingNode import Encoding
from ChartMark.vegalite_ast.ast_base import BaseNode

class LayerItem(BaseNode):
    def __init__(self, mark_type_or_obj: Union[str,dict], encoding: Encoding, **kwargs) -> None:
        """
        初始化 LayerItem 对象，管理每一层的 mark 类型、encoding 和附加属性。
        :param mark_type: 标记类型，bar、line、point 等
        :param encoding: Encoding 对象，用于管理 encoding 字段
        :param kwargs: 根据不同标记类型，传递额外的参数（如 size, radius 等）
        """
        self.mark = {"type": mark_type_or_obj}  if isinstance(mark_type_or_obj, str) else mark_type_or_obj# mark 属性初始化为字典
        self.encoding = encoding
        self.additional_properties = kwargs  # 用于存储每种 mark 特定的属性
    
    def set_mark_property(self, key: str, value: Union[str, Dict]) -> None:
        """
        设置 mark 类型的额外属性
        :param key: 属性名，如 "align"、"size" 等
        :param value: 属性值，可以是字符串或字典
        """
        self.mark[key] = value

    def set_encoding(self, encoding: Encoding) -> None:
        """
        设置新的 encoding 对象
        :param encoding: Encoding 对象
        """
        self.encoding = encoding
    
    def set_property(self, **kwargs) -> None:
        """
        设置额外的属性（如 size, opacity, radius 等）
        :param kwargs: 属性设置
        """
        self.additional_properties.update(kwargs)

    def to_dict(self) -> Dict:
        """
        转换为字典格式
        :return: dict 格式的 Vega-Lite 配置
        """
        layer_dict = {"mark": self.mark}
        if self.encoding:
            layer_dict["encoding"] = self.encoding.to_dict()
        layer_dict.update(self.additional_properties)
        return layer_dict

    def __repr__(self) -> str:
        return f"LayerItem(mark={self.mark}, encoding={self.encoding}, additional_properties={self.additional_properties})"