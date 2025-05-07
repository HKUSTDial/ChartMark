from ChartMark.vegalite_ast.ast_base import BaseNode

class Mark(BaseNode):
  def __init__(self, mark_type, **kwargs):
      self.mark_type = mark_type
      self.properties = kwargs
  
  def get_mark_type(self):
    return self.mark_type
  
  def to_dict(self):
      mark_dict = {"type": self.mark_type}
      if self.properties:
          mark_dict.update(self.properties)
      return mark_dict