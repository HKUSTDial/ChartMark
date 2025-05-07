from typing import Literal, Dict

from ChartMark.vegalite_ast.ast_base import BaseNode
from typing import Dict, Union

# 定义三种编码字段的类型
FieldEncoding = Dict[str, Union[str, Dict]]
DatumEncoding = Dict[str, Union[int, float, str]]
ValueEncoding = Dict[str, Union[str, int, float]]

# axis_key_type 限制值为 color, x, y, x2, y2
axis_key_type = Literal["color", "x", "y", "x2", "y2"]


from typing import Union, Dict


class Encoding(BaseNode):
    def __init__(self) -> None:
        """
        初始化 Encoding 对象，管理所有的 encoding 字段（如 x, y, color 等）。
        """
        self.encoding_obj = {}

    def set_field(self, encoding_key: str, field_name: str, field_type: str, **kwargs) -> None:
        """
        设置 field 类型的 encoding 字段
        :param field_name: 字段名称
        :param field_type: 字段类型，如 'quantitative', 'nominal'
        :param kwargs: 其他附加字段
        """
        self.encoding_obj[encoding_key] = {
            "field": field_name,
            "type": field_type,
            **kwargs
        }

    def set_datum(self, encoding_key: str,  datum_value: Union[int, float, str]) -> None:
        """
        设置 datum 类型的 encoding 字段
        :param field_name: 字段名称
        :param datum_value: datum 值
        """
        self.encoding_obj[encoding_key] = {
            "datum": datum_value
        }

    def set_value(self, encoding_key: str, value: Union[str, int, float]) -> None:
        """
        设置 value 类型的 encoding 字段
        :param field_name: 字段名称
        :param value: value 值
        """
        self.encoding_obj[encoding_key] = {
            "value": value
        }
        
    def set_value_with_condition(self, encoding_key: str, filter_obj: Union[dict, str], condition_value, default_value) -> None:
      
        condition_obj = {
          "test": filter_obj,
          "value": condition_value
        }
        self.encoding_obj[encoding_key] = {
          "condition": condition_obj,
          "value": default_value
        }
        
    def set_field_with_condition(self, encoding_key: str, field_name:str, field_type:str, filter_obj: Union[dict, str], default_value) -> None:
      
        condition_obj = {
          "test": filter_obj,
          "field": field_name,
          "type": field_type
        }
          
        self.encoding_obj[encoding_key] = {
          "condition": condition_obj,
          "value": default_value
        }
        
    def set_value_default_field_with_condition(self, encoding_key: str, field_name:str, field_type:str, filter_obj: Union[dict, str], selected_value) -> None:
        condition_obj = {
          "test": filter_obj,
          "value": selected_value
        }
          
        self.encoding_obj[encoding_key] = {
          "condition": condition_obj,
          "field": field_name,
          "type": field_type
        }
      
    def get_subcontent_obj(self, encoding_key: str):
        subcontent_obj = self.encoding_obj.get(encoding_key, None)
        # if field_obj is None:
            # print(f"Warning: Field '{field_key}' not found in fields.")
        return subcontent_obj

    def update_subcontent_obj(self, encoding_key: str, **kwargs) -> None:
      """
      更新已存在的 encoding 字段，合并属性而非完全覆盖
      :param field_name: 字段名称
      :param kwargs: 要更新的字段内容
      """
      if encoding_key in self.encoding_obj:
          # 如果字段中已有 'axis' 属性，合并新属性
          for key, value in kwargs.items():
              if key == 'axis' and 'axis' in self.encoding_obj[encoding_key]:
                  self.encoding_obj[encoding_key][key].update(value)  # 合并 axis 配置
              else:
                  self.encoding_obj[encoding_key].update({key: value})
    
    def to_dict(self) -> Dict[str, Union[Dict, str]]:
        """
        获取 encoding 字段的字典形式
        :return: encoding 字典
        """
        return self.encoding_obj
                  
    @classmethod
    def from_dict(cls, encoding_dict: Dict) -> "Encoding":
        """
        从字典解析创建 Encoding 对象
        :param encoding_dict: 包含字段的字典
        :return: 一个 Encoding 实例
        """
        encoding = cls()

        for field_key, field_value in encoding_dict.items():
            if "field" in field_value:  # 类型为 field
                encoding.set_field(field_key, field_value["field"], field_value["type"], **{k: v for k, v in field_value.items() if k != "type"})
            elif "datum" in field_value:  # 类型为 datum
                encoding.set_datum(field_key, field_value["datum"])
            elif "value" in field_value:  # 类型为 value
                encoding.set_value(field_key, field_value["value"])

        return encoding