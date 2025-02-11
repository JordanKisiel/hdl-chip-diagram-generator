from src.diagram.diagrammables.diagrammable import Diagrammable
from PIL import ImageFont

class IO(Diagrammable):
    def __init__(self, name, connect_left=True):
        self.name = name
        self.bounds = None
        self.name_pos = (0, 0)
        self.font_size = 0
        self.connect_left = connect_left

    def layout(self, bounds):
        self.bounds = bounds 
        self.font_size = self.bounds.width / 3 
        self.name_pos = (self.bounds.center_x, 
                         self.bounds.bottom - self.font_size)

    def draw(self, canvas):
        style = canvas.style
        context = canvas.context

        # draw text
        # but only if it's big enough to see
        if self.font_size >= 5:
            io_font = ImageFont.truetype(style["font"],
                                         self.font_size)
            context.text(self.name_pos,
                         self.name,
                         fill=style["fg"],
                         font=io_font,
                         anchor="mt")
        
        # draw line
        context.line([self.bounds.bottom_left,
                      self.bounds.bottom_right],
                     fill=style["fg"],
                     width=style["stroke_width"])
        
    def get_connection_point(self):
        assert(self.bounds != None)

        if self.connect_left:
            return self.bounds.bottom_left
        else:
            return self.bounds.bottom_right