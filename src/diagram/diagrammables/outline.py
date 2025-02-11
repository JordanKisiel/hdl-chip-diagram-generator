from src.diagram.diagrammables.diagrammable import Diagrammable

class Outline(Diagrammable):
    def __init__(self):
        self.bounds = None
        self.corner_radius = 0

    def layout(self, bounds):
        self.bounds = bounds
        
    def draw(self, canvas):
        context = canvas.context
        style = canvas.style

        self.corner_radius = (self.bounds.min_dimension 
                              * style["box_radius_factor"])

        context.rounded_rectangle(self.bounds.full_bounds,
                                  radius=self.corner_radius,
                                  fill=None,
                                  outline=style["fg"],
                                  width=style["stroke_width"])