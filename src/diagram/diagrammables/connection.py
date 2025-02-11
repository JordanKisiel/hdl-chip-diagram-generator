from src.diagram.diagrammables.diagrammable import Diagrammable

class Connection(Diagrammable):
    def __init__(self, io_1, io_2):
        self.io_1 = io_1 
        self.io_2 = io_2 
        self.path = None

    def layout(self, path):
        self.point1 = self.io_1.get_connection_point()
        self.point2 = self.io_2.get_connection_point()
        self.path = [self.point1, *path, self.point2]

    def draw(self, canvas):
        assert(self.path != None)

        self._draw_path(canvas)

    def _draw_path(self, canvas):
        context = canvas.context
        style = canvas.style

        # TODO: also look into giving this rounded corners?
        context.line(self.path, 
                     fill=style["fg"], 
                     width=style["stroke_width"])

    def _draw_straight_line(self, canvas):
        context = canvas.context
        style = canvas.style

        context.line([self.point1, self.point2],
                     fill=style["fg"],
                     width=style["stroke_width"])