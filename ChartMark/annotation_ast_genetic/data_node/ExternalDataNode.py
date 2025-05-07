from ChartMark.annotation_ast_genetic.ast_base import BaseNode
from typing import Dict, List, Literal, Optional, Union, Type, Any
from dataclasses import dataclass, field
from ChartMark.annotation_ast_genetic.data_node.BaseDataNode import BaseDataNode

# 值类型定义
@dataclass
class TextValue:
    """文本类型值"""
    type: Literal["text"] = "text"
    content: str = ""

@dataclass
class ImageValue:
    """图片类型值"""
    type: Literal["image"] = "image"
    url: str = ""

# 值类型
ValueType = Union[TextValue, ImageValue]


class ExternalDataNode(BaseDataNode):
    """
    外部数据节点，可以包含不同类型的数据值
    """
    def __init__(self, data_obj: Dict = None):
        self.text_value: Optional[TextValue] = None
        self.image_value: Optional[ImageValue] = None
        super().__init__(data_obj)
        
        if data_obj:
            self._parse_value(data_obj)
    
    def _parse_source(self, data_obj: Dict):
        """解析数据源并确保为external类型"""
        super()._parse_source(data_obj)
        if self.source != "external":
            raise ValueError(f"ExternalDataNode必须是external类型，实际为{self.source}")
    
    def _parse_value(self, data_obj: Dict):
        """解析值对象"""
        value = data_obj.get("value")
        if not value:
            raise ValueError("external类型的数据必须包含value字段")
        
        # 支持单个值对象或值对象数组
        values = value if isinstance(value, list) else [value]
        
        for val in values:
            if not isinstance(val, dict):
                raise ValueError("value必须是字典类型或字典数组")
            
            value_type = val.get("type")
            if not value_type:
                raise ValueError("value必须指定type字段")
            
            if value_type == "text":
                if "content" not in val:
                    raise ValueError("text类型的value必须包含content字段")
                self.text_value = TextValue(content=val["content"])
            
            elif value_type == "image":
                if "url" not in val:
                    raise ValueError("image类型的value必须包含url字段")
                self.image_value = ImageValue(url=val["url"])
            
            else:
                raise ValueError(f"不支持的value类型: {value_type}")
    
    def to_dict(self) -> Dict:
        """将节点转换为字典格式"""
        result = super().to_dict()
        
        # 收集所有值
        values = []
        if self.text_value:
            values.append({
                "type": "text",
                "content": self.text_value.content
            })
        
        if self.image_value:
            values.append({
                "type": "image",
                "url": self.image_value.url
            })
        
        # 如果有值，添加到结果中
        if values:
            # 如果只有一个值，直接使用该值
            if len(values) == 1:
                result["value"] = values[0]
            else:
                result["value"] = values
        
        return result
    
    def set_text_value(self, content: str):
        """设置文本值"""
        self.text_value = TextValue(content=content)
    
    def set_image_value(self, url: str):
        """设置图片值"""
        self.image_value = ImageValue(url=url)
        
    def get_text_content(self):
        """获取文本值"""
        return self.text_value.content
    
    def get_image_url(self):
        """获取图片值"""
        return self.image_value.url
