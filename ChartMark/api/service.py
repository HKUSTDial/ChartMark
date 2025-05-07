import json
import os
from typing import Dict, Any, Optional, List, Type

# 导入图表路由
from ChartMark.router.chart_router import get_chart_class, get_supported_chart_types
# 导入Chart类和注释路由
from ChartMark.vegalite_ast.ChartNode import Chart
from ChartMark.router.annotation_router import get_annotation_class

class ChartMark:
    """
    ChartMark服务类，提供加载JSON和渲染图表的功能
    作为对外暴露的API接口
    
    在Jupyter Notebook中使用示例:
    ```python
    from api.service import ChartMark
    
    # 创建ChartMark实例
    chart_mark = ChartMark()
    
    # 从JSON文件加载数据并渲染图表
    vegalite_spec = chart_mark.process_file("path/to/chart.json")
    
    # 显示图表
    chart_mark.display_vegalite(vegalite_spec)
    ```
    """
    
    def __init__(self):
        """初始化图表服务"""
        pass
    
    def load_json(self, file_path: str) -> Dict[str, Any]:
        """
        加载JSON文件并返回解析后的字典
        
        参数:
            file_path: JSON文件路径
            
        返回:
            解析后的字典
            
        异常:
            FileNotFoundError: 文件不存在
            json.JSONDecodeError: JSON格式错误
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"JSON格式错误: {str(e)}", e.doc, e.pos)
    
    def display_vegalite(self, vegalite_spec: str, width: int = 600, height: int = 400) -> None:
        """
        在Jupyter Notebook中显示VegaLite图表
        
        参数:
            vegalite_spec: VegaLite规范字符串
            width: 图表宽度（像素）
            height: 图表高度（像素）
            
        返回:
            无返回值，直接在Notebook中显示图表
            
        异常:
            ImportError: 缺少必要的依赖库
            ValueError: VegaLite规范无效
        """
        try:
            # 尝试使用IPython.display
            from IPython.display import display, HTML
            
            # 尝试使用不同的可视化库
            try:
                # 优先尝试使用altair（更常用）
                import altair as alt
                from altair import Chart as AltChart
                
                # 解析VegaLite规范
                if isinstance(vegalite_spec, str):
                    vegalite_dict = json.loads(vegalite_spec)
                else:
                    vegalite_dict = vegalite_spec
                
                # 设置宽度和高度
                if "width" not in vegalite_dict:
                    vegalite_dict["width"] = width
                if "height" not in vegalite_dict:
                    vegalite_dict["height"] = height
                
                # 创建图表并显示
                chart = AltChart.from_dict(vegalite_dict)
                display(chart)
                return
            except ImportError:
                # 如果没有altair，尝试使用vegaplot
                try:
                    import vegaplot
                    
                    # 使用vegaplot显示
                    vegaplot.plot(vegalite_spec, width=width, height=height)
                    return
                except ImportError:
                    # 如果两个库都没有，尝试使用vega_datasets和vega
                    try:
                        import vega
                        
                        # 如果是字符串，解析为字典
                        if isinstance(vegalite_spec, str):
                            spec_dict = json.loads(vegalite_spec)
                        else:
                            spec_dict = vegalite_spec
                        
                        # 显示图表
                        vega.VegaLite(spec_dict, width=width, height=height).display()
                        return
                    except ImportError:
                        # 如果所有库都不可用，尝试使用HTML直接渲染
                        if isinstance(vegalite_spec, str):
                            spec_json = vegalite_spec
                        else:
                            spec_json = json.dumps(vegalite_spec)
                        
                        # 创建内嵌Vega-Lite的HTML
                        vega_html = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                          <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
                          <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
                          <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
                        </head>
                        <body>
                          <div id="vis" style="width: {width}px; height: {height}px;"></div>
                          <script type="text/javascript">
                            var spec = {spec_json};
                            vegaEmbed('#vis', spec);
                          </script>
                        </body>
                        </html>
                        """
                        display(HTML(vega_html))
                        return
        
        except ImportError:
            # 如果IPython不可用，说明不在Jupyter环境中
            print("警告: 无法显示图表。请确保在Jupyter Notebook环境中运行，并安装以下库之一: altair, vegaplot, vega")
            print("可以运行: pip install altair 或 pip install vegaplot")
            print("图表规范:", vegalite_spec[:200] + "..." if len(vegalite_spec) > 200 else vegalite_spec)
        except Exception as e:
            print(f"显示图表时出错: {str(e)}")
            print("图表规范:", vegalite_spec[:200] + "..." if len(vegalite_spec) > 200 else vegalite_spec)
    
    def render_original_chart(self, data: Dict[str, Any]) -> str:
        """
        渲染原始图表，生成VegaLite图表规范
        
        参数:
            data: 包含图表数据的字典
            
        返回:
            VegaLite图表规范字符串
            
        异常:
            ValueError: 图表数据无效或不支持的图表类型
        """
        # 提取chart字段
        chart_data = data.get("chart")
        if not chart_data or not isinstance(chart_data, dict):
            raise ValueError("数据中缺少有效的chart字段")
        
        # 获取图表类型
        chart_type = chart_data.get("type")
        if not chart_type or not isinstance(chart_type, str):
            raise ValueError("chart中缺少有效的type字段")
        
        try:
            # 从路由获取对应的图表类
            chart_class = get_chart_class(chart_type)
            
            # 实例化图表对象
            chart_instance = chart_class(chart_data)
            
            # 调用to_vegalite_chart生成图表规范
            vegalite_spec = chart_instance.to_vegalite_chart()
            
            return vegalite_spec
            
        except ValueError as e:
            # 处理图表类型不支持的错误
            raise ValueError(f"图表类型错误: {str(e)}")
        except Exception as e:
            # 处理其他渲染错误
            raise ValueError(f"渲染图表失败: {str(e)}")
    
    def render_annotations(self, data: Dict[str, Any]) -> str:
        """
        处理基于原始图表的注释添加，实现注释的叠加渲染
        
        处理流程：
        1. 调用render_original_chart获取原始VegaLite规范
        2. 实例化为Chart对象
        3. 读取data中的annotations字段，获取注释字典列表
        4. 遍历注释列表，根据注释类型进行处理
        5. 依次应用每个注释到图表上，形成注释叠加效果
        
        参数:
            data: 包含图表和注释数据的字典
            
        返回:
            应用了注释的VegaLite图表规范字符串
            
        异常:
            ValueError: 数据无效或处理过程中的错误
        """
        # 确保数据包含annotations字段
        annotations_data = data.get("annotations")
        if annotations_data is None:
            # 如果没有annotations字段，直接返回原始图表
            return self.render_original_chart(data)
        
        if not isinstance(annotations_data, list):
            raise ValueError("annotations字段必须是数组类型")
        
        # 获取chart类型
        chart_data = data.get("chart")
        if not chart_data or not isinstance(chart_data, dict):
            raise ValueError("数据中缺少有效的chart字段")
        
        chart_type = chart_data.get("type")
        if not chart_type or not isinstance(chart_type, str):
            raise ValueError("chart中缺少有效的type字段")
        
        try:
            # 获取原始VegaLite规范
            vegalite_spec = self.render_original_chart(data)
            
            # 解析VegaLite规范为JSON
            vegalite_dict = json.loads(vegalite_spec)
            
            # 创建Chart实例
            current_chart = Chart(vegalite_dict)
            
            # 遍历annotations列表
            for annotation in annotations_data:
                if not isinstance(annotation, dict):
                    print(f"警告：跳过非字典类型的注释: {annotation}")
                    continue
                
                # 获取注释的method和type
                method = annotation.get("method", {})
                if not isinstance(method, dict):
                    print(f"警告：跳过缺少有效method字段的注释: {annotation}")
                    continue
                
                annotation_type = method.get("type")
                if not annotation_type or not isinstance(annotation_type, str):
                    print(f"警告：跳过缺少有效类型的注释: {annotation}")
                    continue
                
                try:
                    # 获取对应的注释类
                    annotation_class = get_annotation_class(annotation_type)
                    
                    # 实例化注释对象
                    annotation_instance = annotation_class(annotation)
                    
                    # 调用parse_techniques_to_vegalite方法应用注释
                    new_vegalite_dict = annotation_instance.parse_techniques_to_vegalite(current_chart, chart_type)
                    
                    # 使用新的vegalite_dict创建新的Chart实例，用于下一个注释处理
                    current_chart = Chart(new_vegalite_dict)
                except Exception as e:
                    print(f"应用注释 {annotation_type} 时出错: {str(e)}")
            
            # 返回最终处理结果的JSON字符串
            return json.dumps(current_chart.to_dict(), indent=2)
            
        except Exception as e:
            raise ValueError(f"渲染注释失败: {str(e)}")
    
    def save_vegalite_spec(self, spec: str, output_path: str) -> None:
        """
        保存VegaLite规范到文件
        
        参数:
            spec: VegaLite规范字符串
            output_path: 输出文件路径
        """
        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(spec)
        except Exception as e:
            raise IOError(f"保存VegaLite规范失败: {str(e)}")
    
    def process_file(self, input_path: str, output_path: Optional[str] = None, with_annotations: bool = False) -> str:
        """
        处理单个文件：加载JSON并渲染图表
        
        参数:
            input_path: 输入JSON文件路径
            output_path: 输出VegaLite规范文件路径，如果为None则不保存
            with_annotations: 是否处理注释，默认为False
            
        返回:
            VegaLite图表规范字符串
        """
        # 加载JSON
        data = self.load_json(input_path)
        
        # 根据是否处理注释选择渲染方法
        if with_annotations:
            vegalite_spec = self.render_annotations(data)
        else:
            vegalite_spec = self.render_original_chart(data)
        
        # 如果指定了输出路径，保存规范
        if output_path:
            self.save_vegalite_spec(vegalite_spec, output_path)
        
        return vegalite_spec
    
    def batch_process(self, input_dir: str, output_dir: str, with_annotations: bool = False) -> List[str]:
        """
        批量处理目录中的所有JSON文件
        
        参数:
            input_dir: 输入目录路径
            output_dir: 输出目录路径
            with_annotations: 是否处理注释，默认为False
            
        返回:
            处理成功的文件列表
        """
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        processed_files = []
        
        # 遍历输入目录中的所有JSON文件
        for filename in os.listdir(input_dir):
            if filename.endswith('.json'):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename.replace('.json', '.vl.json'))
                
                try:
                  self.process_file(input_path, output_path, with_annotations=with_annotations)
                  processed_files.append(filename)
                except Exception as e:
                    print(f"处理文件 {filename} 失败: {str(e)}")
        
        return processed_files
    
    def get_supported_chart_types(self) -> List[str]:
        """
        获取支持的图表类型列表
        
        返回:
            支持的图表类型列表
        """
        return get_supported_chart_types()


# 使用示例
if __name__ == "__main__":
    service = ChartMark()
    
    # 示例1：处理单个文件（不包含注释）
    try:
        vegalite_spec = service.process_file("examples/bar_chart.json", "output/bar_chart.vl.json")
        print("原始图表VegaLite规范生成成功")
    except Exception as e:
        print(f"处理失败: {str(e)}")
    
    # 示例2：处理单个文件（包含注释）
    try:
        vegalite_spec = service.process_file("examples/bar_chart.json", "output/bar_chart_with_annotations.vl.json", with_annotations=True)
        print("带注释的图表VegaLite规范生成成功")
    except Exception as e:
        print(f"处理失败: {str(e)}")
    
    # 示例3：批量处理目录
    try:
        processed_files = service.batch_process("examples", "output")
        print(f"成功处理 {len(processed_files)} 个文件")
    except Exception as e:
        print(f"批量处理失败: {str(e)}")
    
    # 示例4：查看支持的图表类型
    chart_types = service.get_supported_chart_types()
    print(f"支持的图表类型: {', '.join(chart_types)}") 