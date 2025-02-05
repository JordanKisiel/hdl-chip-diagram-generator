from src.diagram.bounds import *
import math

# TODO:
# -make grid a diagrammable by adding a layout
# method
# -test drawing with fractional values for points
#  to see if it makes a visual difference
#   -this might change how how do the math with grid, etc
class Grid:
    def __init__(self, 
                 width, 
                 height, 
                 x_divisions, 
                 y_divisions):
        self.width = width
        self.height = height
        self.bounds = Bounds(0, 0, height, width)
        self.x_divisions = x_divisions
        self.y_divisions = y_divisions
        self.column_width = self.width / x_divisions
        self.row_height = self.height / y_divisions
        self.color = (255, 220, 220)
        self.on_grid_threshold = 0.001
        self.grid = self._construct_grid()
        assert(width > 0)
        assert(height > 0)
        assert(x_divisions > 0)
        assert(y_divisions > 0)

    def _construct_grid(self):
        grid = []
        for i in range(self.x_divisions + 1):
            row = []
            for j in range(self.y_divisions + 1):
               x_value = self.column_width * i
               y_value = self.row_height * j
               row.append((x_value, y_value))
            grid.append(row)

        return grid

    def get(self, x_coord, y_coord):
        assert(x_coord >= 0)
        assert(y_coord >= 0)
        assert(x_coord <= self.x_divisions + 1)
        assert(y_coord <= self.y_divisions + 1)

        return self.grid[x_coord][y_coord]
    
    def draw(self, canvas, position=(0, 0)):
        context = canvas.context
        x_offset = position[0]
        y_offset = position[1]

        # draw horizontal lines
        for n in range(0, self.y_divisions + 1):
            y_value = self.grid[0][n][1]
            context.line([(0 + x_offset, y_value + y_offset),
                          (self.width + x_offset, y_value + y_offset)],
                          self.color,
                          width=2)

        # draw vertical lines
        for n in range(0, self.x_divisions + 1):
            x_value = self.grid[n][0][0]
            context.line([(x_value + x_offset, 0 + y_offset),
                          (x_value + x_offset, self.height + y_offset)],
                          self.color,
                          width=2)