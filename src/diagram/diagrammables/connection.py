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
        canvas.path(self.path)