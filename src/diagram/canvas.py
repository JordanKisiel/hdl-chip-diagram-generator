from PIL import Image, ImageDraw
from src.diagram.grid import Grid

class Canvas:
    def __init__(self,
                 width,
                 height,
                 style={
                    "bg": (255, 255, 255),
                    "fg": (0, 0, 0),
                    "font": "FreeMono.ttf",
                    "base_font_size": 32,
                    "stroke_width": 2,
                    "box_radius_factor": 0.05,
                    "grid_color": (255, 220, 220)
                 }):
        self.width = width
        self.height = height
        self.style = style
        self.grid = Grid(self.width, self.height, 12, 12) 
        self.out = Image.new("RGB", 
                             (self.width, self.height),
                             self.style["bg"])
        self.context = ImageDraw.Draw(self.out)


    def set_grid(self, grid):
        self.grid = grid

    def draw_grid(self):
        # draw horizontal lines
        for n in range(1, self.grid.divisions_y):
            self.context.line([(0, self.height / self.grid.divisions_y * n), 
                               (self.width, self.height / self.grid.divisions_y * n)], 
                              self.style["grid_color"],
                              width=2)
        # draw vertical lines
        for n in range(1, self.grid.divisions_x):
            self.context.line([(self.width / self.grid.divisions_x * n, 0), 
                               (self.width / self.grid.divisions_x * n, self.height)], 
                              self.style["grid_color"],
                              width=2)