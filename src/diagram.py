from src.grid import Grid
from PIL import Image, ImageDraw, ImageFont
from abc import ABC, abstractmethod

class Diagram:
    def __init__(self,
                 grid=Grid(800, 600, 12, 12),
                 style={
                     "bg": (255, 255, 255),
                     "fg": (0, 0, 0),
                     "font": "FreeMono.ttf",
                     "base_font_size": 32,
                     "stroke_width": 2,
                     "box_radius_factor": 0.05
                 }):
        self.grid = grid
        self.style = style 
        self.out = Image.new("RGB",
                             (self.grid.width, self.grid.height),
                             self.style["bg"])
        self.draw_context = ImageDraw.Draw(self.out)
        self.elements = []

    def add(self, diagrammable):
        self.elements.append(diagrammable)
        diagrammable.add_to_diagram(self)

    def draw(self):
        for element in self.elements:
            element.draw()

    def write(self, file_path):
        self.out.save(file_path)

    def draw_grid(self):
        self.grid.draw(self.draw_context)

        
class Diagrammable(ABC):
    @abstractmethod
    def __init__(self):
        pass 

    @abstractmethod
    def draw(self):
        pass

    def add_to_diagram(self, diagram):
        self.diagram = diagram 


class Title(Diagrammable):
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.diagram = None
    
    def draw(self):
        title_font = ImageFont.truetype(self.diagram.style["font"],
                                        self.diagram.style["base_font_size"])
        self.diagram.draw_context.text(self.position,
                                       self.text,
                                       fill=self.diagram.style["fg"],
                                       font=title_font,
                                       anchor="mt")
    

class Box(Diagrammable):
    def __init__(self, bounds, text=None):
        self.bounds = bounds
        self.width = abs(bounds[0][0] - bounds[1][0])
        self.height= abs(bounds[0][1] - bounds[1][1])
        self.center_x = bounds[0][0] + self.width / 2
        self.center_y = bounds[0][1] + self.height / 2
        self.text = text
        self.diagram = None

    def draw(self):
        min_dimension = min(self.width, self.height)
        corner_radius = min_dimension * self.diagram.style["box_radius_factor"]
        self.diagram.draw_context.rounded_rectangle(self.bounds,
                                                    radius=corner_radius,
                                                    fill=None,
                                                    outline=self.diagram.style["fg"],
                                                    width=self.diagram.style["stroke_width"])
        
        if self.text != None:
            limiting_dimension = min(self.width, self.height)
            text_width = len(self.text) * self.diagram.style["base_font_size"]
            scaling_factor = limiting_dimension / 3 / text_width
            font_size = text_width * scaling_factor 
            if font_size > self.diagram.style["base_font_size"]:
                font_size = self.diagram.style["base_font_size"]
            box_font = ImageFont.truetype(self.diagram.style["font"],
                                          font_size)

            optical_center_adj = self.height * -0.1 
            self.diagram.draw_context.text((self.center_x, 
                                            self.center_y + optical_center_adj),
                                           self.text,
                                           fill=self.diagram.style["fg"],
                                           font=box_font,
                                           anchor="mt")                               