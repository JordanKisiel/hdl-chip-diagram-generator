from src.diagram.diagrammables.diagrammable import Diagrammable
from src.diagram.diagrammables.outline import Outline
from src.diagram.diagrammables.io import IO
from src.diagram.bounds import Bounds
from src.diagram.chip_layout import Chip_Layout
from PIL import ImageFont

class Part(Diagrammable):
    def __init__(self, name, id, input_names, output_names):
        self.name = name
        self.id = id
        self.font_size = 0
        # the amount to adjust the y pos of the name by
        # so that it looks centered optically
        # (relative to height)
        self.optical_center_adj = -0.1
        self.name_y_pos = 0
        self.input_names = input_names 
        self.output_names = output_names 
        self.inputs = self._create_io(self.input_names, 
                                      connect_left=True)
        self.outputs = self._create_io(self.output_names, 
                                       connect_left=False)
        self.outline = Outline()
        self.bounds = None

    def layout(self, bounds):
        self.bounds = bounds

        self._layout_name(bounds) 

        self.outline.layout(bounds)

        self._layout_io(bounds)

    def draw(self, canvas):
        assert(self.bounds != None)

        self.outline.draw(canvas)

        for input in self.inputs:
            input.draw(canvas)
        for output in self.outputs:
            output.draw(canvas)

        self._draw_name(canvas)

    def _layout_name(self, bounds):
        self.name_y_pos = (bounds.center_y + 
                           (self.optical_center_adj * bounds.height))  

    def _create_io(self, io_list, connect_left=True):
        lst = []
        for io_name in io_list:
            lst.append(IO(io_name, connect_left))

        return lst

    def _layout_io(self, bounds):
        input_left = bounds.left - (bounds.width / 4)
        input_right = bounds.left
        input_group_bounds = Bounds(bounds.top, 
                                    input_left, 
                                    bounds.bottom, 
                                    input_right)
        output_left = bounds.right
        output_right = bounds.right + (bounds.width / 4)
        output_group_bounds = Bounds(bounds.top,
                                     output_left,
                                     bounds.bottom,
                                     output_right)
        
        Chip_Layout.distribute_io(input_group_bounds, self.inputs)
        Chip_Layout.distribute_io(output_group_bounds, self.outputs)

    def _draw_name(self, canvas):
        context = canvas.context
        style = canvas.style

        name_width = len(self.name) * style["base_font_size"]
        scaling_factor = self.bounds.min_dimension / 3 / name_width
        self.font_size = name_width * scaling_factor
        if self.font_size > style["base_font_size"]:
            self.font_size = style["base_font_size"]
        # draw text
        # but only if it's big enough to see 
        if self.font_size >= 5:
            name_font = ImageFont.truetype(style["font"],
                                        self.font_size)
            
            context.text((self.bounds.center_x, self.name_y_pos),
                        self.name,
                        fill=style["fg"],
                        font=name_font,
                        anchor="mt")