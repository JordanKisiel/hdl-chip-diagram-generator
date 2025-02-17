from src.diagram.diagrammables.diagrammable import Diagrammable
from PIL import ImageFont

class IO(Diagrammable):
    def __init__(self, name, is_input=True, connect_left=True):
        self.name = name
        self.is_input = is_input
        self.bounds = None
        self.name_pos = (0, 0)
        self.font_size = 0
        self._minimum_font_size = 5
        self.connect_left = connect_left

    def get_connection_point(self):
        assert(self.bounds != None)

        if self.connect_left:
            return self.bounds.bottom_left
        else:
            return self.bounds.bottom_right

    def layout(self, bounds):
        self.bounds = bounds 
        self.font_size = self.bounds.width / 4
        if self.connect_left:
            self.name_pos = (self.bounds.center_x + self.font_size / 2, 
                             self.bounds.bottom - self.font_size)
        else:
            self.name_pos = (self.bounds.center_x - self.font_size / 2,
                             self.bounds.bottom - self.font_size)

    def draw(self, canvas):
        canvas.text(self.name_pos,
                    self.name,
                    font_size=self.font_size)
        
        canvas.line([self.bounds.bottom_left,
                     self.bounds.bottom_right]) 