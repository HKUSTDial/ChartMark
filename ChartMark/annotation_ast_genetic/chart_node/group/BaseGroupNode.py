from typing import Dict, List, Any
from abc import ABC, abstractmethod
from ..BaseChartNode import BaseChartNode

class BaseGroupNode(BaseChartNode, ABC):
    """
    分组图表节点基类，除了基本属性外，还包含分类相关属性
    """
    def __init__(self, chart_obj: Dict = None):
        super().__init__(chart_obj)        
        
        self.x_data: List[str] = []  # 一维字符串数组
        self.y_data: List[List[float]] = []  # 二维数值数组
        self.classify: List[str]= []
        
        self.classify_name = chart_obj.get("classify_name", "") if chart_obj is not None else ""        
    
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
            "y_data": self.y_data,
            "classify": self.classify,
            "classify_name": self.classify_name
        }

    def _parse_to_metadata(self) -> List[Dict[str, Any]]:
        """
        将分组图表数据转换为格式化的元数据列表
        
        处理两种情况:
        1. x_data为一维数组时，需要将其扩展与y_data匹配
        2. x_data为二维数组时，直接与y_data一一对应
        
        返回:
            包含x_name、y_name和classify_name作为键的字典列表
        """
        # 确保必要的属性存在
        if not self.x_name or not self.y_name or not self.classify_name:
            raise ValueError("生成元数据需要x_name、y_name和classify_name")
            
        # 确保classify、x_data和y_data非空且长度一致
        if not self.classify or not self.x_data or not self.y_data:
            raise ValueError("classify、x_data和y_data不能为空")
            
        if len(self.classify) != len(self.y_data):
            raise ValueError("classify和y_data的长度必须一致")
            
        # 判断x_data是一维还是二维数组
        is_x_data_2d = False
        if isinstance(self.x_data, list) and len(self.x_data) > 0 and isinstance(self.x_data[0], list):
            is_x_data_2d = True
            # 验证二维x_data的有效性
            if len(self.x_data) != len(self.y_data):
                raise ValueError("二维x_data的外层长度必须与y_data一致")
                
            for i in range(len(self.x_data)):
                if len(self.x_data[i]) != len(self.y_data[i]):
                    raise ValueError(f"x_data[{i}]的长度必须与y_data[{i}]一致")
        
        # 生成元数据列表
        metadata_list = []
        
        # 处理x_data为一维数组的情况
        if not is_x_data_2d:
            for group_index in range(len(self.classify)):
                group_name = self.classify[group_index]
                group_data = self.y_data[group_index]
                
                # 确保x_data长度足够
                if len(self.x_data) < len(group_data):
                    raise ValueError(f"x_data长度不足以匹配分组{group_name}的数据")
                
                # 生成该分组的元数据
                for data_index in range(len(group_data)):
                    metadata = {
                        self.x_name: self.x_data[data_index],
                        self.y_name: group_data[data_index],
                        self.classify_name: group_name
                    }
                    metadata_list.append(metadata)
        
        # 处理x_data为二维数组的情况
        else:
            for group_index in range(len(self.classify)):
                group_name = self.classify[group_index]
                group_x_data = self.x_data[group_index]
                group_y_data = self.y_data[group_index]
                
                # 生成该分组的元数据
                for data_index in range(len(group_y_data)):
                    metadata = {
                        self.x_name: group_x_data[data_index],
                        self.y_name: group_y_data[data_index],
                        self.classify_name: group_name
                    }
                    metadata_list.append(metadata)
        
        return metadata_list
        
    def to_vegalite_chart(self) -> str:
        """
        将分组图表转换为VegaLite图表规范字符串
        使用子类定义的ORIGINAL_CHART_TEMPLATE模板
        填充title、x_name、y_name、classify_name以及metadata_list
        
        返回:
            VegaLite图表规范的字符串
        """
        # 检查子类是否定义了图表模板
        if not hasattr(self.__class__, 'ORIGINAL_CHART_TEMPLATE'):
            # 如果子类没有定义模板，尝试从GroupLineChartNode获取默认模板
            from .GroupLineChartNode import GroupLineChartNode
            if hasattr(GroupLineChartNode, 'ORIGINAL_CHART_TEMPLATE'):
                template = GroupLineChartNode.ORIGINAL_CHART_TEMPLATE
            else:
                raise NotImplementedError(f"{self.__class__.__name__}未定义ORIGINAL_CHART_TEMPLATE，且无法找到默认模板")
        else:
            # 使用子类定义的模板
            template = self.__class__.ORIGINAL_CHART_TEMPLATE
        
        # 确保有必要的数据
        if not self.title or not self.x_name or not self.y_name or not self.classify_name:
            raise ValueError("生成图表需要title、x_name、y_name和classify_name")
            
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
                classify_name=self.classify_name,
                metadata_list=metadata_json
            )
            
            return chart_spec
            
        except Exception as e:
            raise ValueError(f"生成VegaLite图表失败: {str(e)}")