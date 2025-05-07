from typing import List, Dict, Union, Optional
from ChartMark.vegalite_ast.LayerItemNode import LayerItem
from ChartMark.vegalite_ast.EncodingNode import Encoding
from dataclasses import dataclass
from datetime import datetime
from ChartMark.vegalite_ast.ast_base import BaseNode


@dataclass
class BarFieldInfo:
    category_name: str = None
    quantity_name: str = None
    group_name: Optional[str] = None

@dataclass
class PieFieldInfo:
    category_name: str = None
    quantity_name: str = None


@dataclass
class LineFieldInfo:
    temporal_name: str = None
    # time_unit: str = None
    quantity_name: str = None
    group_name: Optional[str] = None


@dataclass
class ScatterFieldInfo:
    x_quantity_name: str = None
    y_quantity_name: str = None
    group_name: Optional[str] = None


ChartFieldInfo = Union[BarFieldInfo, PieFieldInfo, LineFieldInfo, ScatterFieldInfo]


class Chart(BaseNode):
    def __init__(self, chart_dict: Dict) -> None:
        """
        从字典初始化 Chart 对象，自动解析所有字段。
        :param chart_dict: 包含 veagalite 配置的字典
        """
        self.schema:str = chart_dict.get("$schema", "")
        self.description:str = chart_dict.get("description", "")
        self.title:str = chart_dict.get("title", "")
        self.data:Dict = chart_dict.get("data", {})
        self.layers: List[LayerItem] = []

        layers_data = chart_dict.get("layer", [])

        for layer_data in layers_data:
            # mark_type = layer_data.get("mark", {}).get("type")
            mark_obj = layer_data.get("mark", {})
            encoding_data = layer_data.get("encoding", {})
            encoding = Encoding()

            for field, field_data in encoding_data.items():
                if "field" in field_data:
                    encoding.set_field(
                        field, field_data["field"], field_data["type"], **field_data
                    )
                elif "datum" in field_data:
                    encoding.set_datum(field, field_data["datum"])
                    
                elif "condition" in field_data and "value" in field_data:
                    filter_obj = field_data["condition"].get("test")
                  
                    condition_value = field_data["condition"].get("value")
                    condition_value_field_type = field_data["condition"].get("type")
                    condition_value_field_name = field_data["condition"].get("field")
                    
                    if not condition_value is None:                    # 创建一个condition_obj字典，包含condition中除了value之外的所有键值对
                      encoding.set_value_with_condition(field, filter_obj, condition_value, field_data["value"])
                    else:
                      encoding.set_field_with_condition(field, condition_value_field_name, condition_value_field_type, filter_obj, field_data["value"])
                    
                elif "value" in field_data and "condition" not in field_data:
                    encoding.set_value(field, field_data["value"])
            # 创建 LayerItem 实例
            # 去除mark和encoding字段，剩下的为layer_other_data
            layer_other_data = layer_data.copy()  # 创建字典副本
            layer_other_data.pop("mark", None)  # 删除mark字段
            layer_other_data.pop("encoding", None)  # 删除encoding字段
            layer = LayerItem(mark_obj, encoding=encoding, **layer_other_data)
            self.layers.append(layer)

    def add_layer(self, layer: LayerItem) -> None:
        """
        添加图层到 layers 数组。
        :param layer: LayerItem 对象
        """
        self.layers.append(layer)

    def get_layer(self, index: int) -> LayerItem:
        """
        获取指定索引的图层
        :param index: 图层的索引
        :return: LayerItem 对象
        """
        return self.layers[index]

    def swap_layers(self, index1: int, index2: int) -> None:
        """
        交换 layers 数组中两个图层的位置。
        :param index1: 第一个图层的索引
        :param index2: 第二个图层的索引
        """
        if 0 <= index1 < len(self.layers) and 0 <= index2 < len(self.layers):
            # 交换两个图层
            self.layers[index1], self.layers[index2] = (
                self.layers[index2],
                self.layers[index1],
            )
            print(f"Swapped layer {index1} with layer {index2}.")
        else:
            print(f"Invalid indices: {index1} or {index2}. No swap performed.")

    def print_layer_positions(self) -> None:
        """
        打印当前 layers 数组中每个图层的位置和内容。
        """
        for idx, layer in enumerate(self.layers):
            print(f"Layer {idx}: {layer.to_dict()}")

    def to_dict(self) -> Dict:
        """
        返回 Chart 对象的字典表示形式。
        :return: 字典格式的 Chart 配置
        """
        return {
            "$schema": self.schema,
            "title": self.title,
            "description": self.description,
            "data": self.data,
            "layer": [layer.to_dict() for layer in self.layers],
        }

    def extract_chart_field_info(self) -> ChartFieldInfo:
        """
        从 layer 的第一个元素中提取 encoding 中的 x, y 和 color 的 field 值，
        并根据字段类型返回格式化的信息。

        :return: 包含提取信息的字典对象
        """
        # 获取 layer 的第一个元素
        first_layer = self.get_layer(0)
        encoding = first_layer.encoding

        # 提取 x, y, 和 color 的信息
        x_info = encoding.get_subcontent_obj("x")
        y_info = encoding.get_subcontent_obj("y")
        color_info = encoding.get_subcontent_obj("color")
        theta_info = encoding.get_subcontent_obj("theta")

        # print("x_info", x_info)
        # print("y_info", y_info)
        # print("color_info", color_info)
        # print("theta_info",theta_info)

        # 根据字段类型组织返回值
        result = {}

        if color_info and color_info.get("field") and not theta_info:
            result["group_name"] = color_info.get("field")

        if x_info and y_info and x_info.get("type") == "temporal" and y_info.get("type") == "quantitative":
            result["temporal_name"] = x_info.get("field", None)
            # result["time_unit"] = x_info.get("timeUnit", None)
            result["quantity_name"] = y_info.get("field", None)
            return LineFieldInfo(**result)

        elif x_info and y_info and x_info.get("type") == "nominal" and y_info.get("type") == "quantitative":
            result["category_name"] = x_info.get("field", None)
            result["quantity_name"] = y_info.get("field", None)
            return BarFieldInfo(**result)

        elif (
            x_info and y_info and
            x_info.get("type") == "quantitative"
            and y_info.get("type") == "quantitative"
        ):
            result["x_quantity_name"] = x_info.get("field", None)
            result["y_quantity_name"] = y_info.get("field", None)
            return ScatterFieldInfo(**result)

        elif color_info and color_info.get("field") and theta_info and theta_info.get("type") == "quantitative":
            result["category_name"] = color_info.get("field", None)
            result["quantity_name"] = theta_info.get("field", None)
            # print("result", result)
            return PieFieldInfo(**result)

    #   return result

    def get_x_or_y_axis_info_obj(self, field_key):

        field_obj = self.get_layer(0).encoding.get_subcontent_obj(field_key)

        return field_obj
      
    def get_field_and_type(self, field_key):

        field_obj = self.get_layer(0).encoding.get_subcontent_obj(field_key)

        return {
            field_key: {"field": field_obj.get("field"), "type": field_obj.get("type")}
        }
        
    def get_mark_type(self):
        return self.get_layer(0).mark.get_mark_type()