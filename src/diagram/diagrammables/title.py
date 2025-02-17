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

        canvas.text((self.bounds.center_x, self.bounds.top),
                     self.text)