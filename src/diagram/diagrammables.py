from abc import ABC, abstractmethod
from PIL import ImageFont
from src.diagram.bounds import Bounds
from src.diagram.chip_layout import Chip_Layout

class Diagrammable(ABC):
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def layout(self):
        pass

class Title(Diagrammable):
    def __init__(self, diagram, text):
        self.diagram = diagram 
        self.text = text
        self.bounds = None

    def layout(self, bounds):
        self.bounds = bounds
        
    def draw(self):
        assert(self.bounds != None)

        context = self.diagram.canvas.context
        style = self.diagram.canvas.style

        title_font = ImageFont.truetype(style["font"],
                                        style["base_font_size"])
        context.text((self.bounds.center_x, self.bounds.top),
                     self.text,
                     fill=style["fg"],
                     font=title_font,
                     anchor="mt")

class Outline(Diagrammable):
    def __init__(self, diagram):
        self.diagram = diagram 
        self.bounds = None
        self.corner_radius = 0

    def layout(self, bounds):
        style = self.diagram.canvas.style

        self.bounds = bounds
        self.corner_radius = (self.bounds.min_dimension 
                              * style["box_radius_factor"])
    
    def draw(self):
        context = self.diagram.canvas.context
        style = self.diagram.canvas.style


        context.rounded_rectangle(self.bounds.full_bounds,
                                  radius=self.corner_radius,
                                  fill=None,
                                  outline=style["fg"],
                                  width=style["stroke_width"])
        
class IO(Diagrammable):
    def __init__(self, diagram, name, connect_left=True):
        self.diagram = diagram
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

    def draw(self):
        style = self.diagram.canvas.style
        context = self.diagram.canvas.context

        # draw text
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

class Part(Diagrammable):
    def __init__(self, diagram, name, input_names, output_names):
        self.diagram = diagram
        self.name = name
        self.font_size = 0
        # the amount to adjust the y pos of the name by
        # so that it looks centered optically
        # (relative to height)
        self.optical_center_adj = -0.1
        self.name_y_pos = 0
        self.input_names = input_names 
        self.output_names = output_names 
        self.inputs = self._create_io(self.input_names, connect_left=True)
        self.outputs = self._create_io(self.output_names, connect_left=False)
        self.outline = Outline(self.diagram)
        self.bounds = None

    def layout(self, bounds):
        self.bounds = bounds

        self._layout_name(bounds) 

        self.outline.layout(bounds)

        self._layout_io(bounds)

    def draw(self):
        assert(self.bounds != None)

        self.outline.draw()

        for input in self.inputs:
            input.draw()
        for output in self.outputs:
            output.draw()

        self._draw_name()

    def _layout_name(self, bounds):
        style = self.diagram.canvas.style

        self.name_y_pos = (bounds.center_y + 
                           (self.optical_center_adj * bounds.height))  
        name_width = len(self.name) * style["base_font_size"]
        scaling_factor = bounds.min_dimension / 3 / name_width
        self.font_size = name_width * scaling_factor
        if self.font_size > style["base_font_size"]:
            self.font_size = style["base_font_size"]

    def _create_io(self, io_list, connect_left=True):
        lst = []
        for io_name in io_list:
            lst.append(IO(self.diagram, io_name, connect_left))

        return lst

    def _layout_io(self, bounds):
        input_left = bounds.left - (bounds.width / 3)
        input_right = bounds.left
        input_group_bounds = Bounds(bounds.top, 
                                    input_left, 
                                    bounds.bottom, 
                                    input_right)
        output_left = bounds.right
        output_right = bounds.right + (bounds.width / 3)
        output_group_bounds = Bounds(bounds.top,
                                     output_left,
                                     bounds.bottom,
                                     output_right)
        
        Chip_Layout.distribute_io(input_group_bounds, self.inputs)
        Chip_Layout.distribute_io(output_group_bounds, self.outputs)

    def _draw_name(self):
        context = self.diagram.canvas.context
        style = self.diagram.canvas.style

        name_font = ImageFont.truetype(style["font"],
                                       self.font_size)
        
        context.text((self.bounds.center_x, self.name_y_pos),
                     self.name,
                     fill=style["fg"],
                     font=name_font,
                     anchor="mt")

class Connection(Diagrammable):
    def __init__(self, diagram):
        self.diagram = diagram
        self.point1 = None
        self.point2 = None
        self.center_x = None

    def layout(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.center_x = abs(point1[0] - point2[0]) / 2

    def draw(self):
        assert(self.point1 != None)
        assert(self.point2 != None)

        context = self.diagram.canvas.context
        style = self.diagram.canvas.style

        context.line([self.point1, 
                      (self.center_x, self.point1[1])],
                     fill=style["fg"],
                     width=style["stroke_width"])
        context.line([(self.center_x, self.point1[1]), 
                      (self.center_x, self.point2[1])],
                     fill=style["fg"],
                     width=style["stroke_width"])
        context.line([(self.center_x, self.point2[1]), 
                      self.point2],
                     fill=style["fg"],
                     width=style["stroke_width"])