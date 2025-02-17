from src.diagram.diagrammables.diagrammable import Diagrammable

class Outline(Diagrammable):
    def __init__(self):
        self.bounds = None
        self.corner_radius = 0

    def layout(self, bounds):
        self.bounds = bounds
        
    def draw(self, canvas):
        canvas.rectangle(self.bounds.full_bounds,
                         radius=self.bounds.min_dimension)