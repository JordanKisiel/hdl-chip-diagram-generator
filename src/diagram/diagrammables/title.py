from src.diagram.diagrammables.diagrammable import Diagrammable
from PIL import ImageFont

class Title(Diagrammable):
    def __init__(self, text):
        self.text = text
        self.bounds = None

    def layout(self, bounds):
        self.bounds = bounds
        
    def draw(self, canvas):
        assert(self.bounds != None)

        context = canvas.context
        style = canvas.style

        title_font = ImageFont.truetype(style["font"],
                                        style["base_font_size"])
        context.text((self.bounds.center_x, self.bounds.top),
                     self.text,
                     fill=style["fg"],
                     font=title_font,
                     anchor="mt")