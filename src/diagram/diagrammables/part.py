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
        # the amount to adjust the y pos of the name by
        # so that it looks centered optically
        # (relative to height)
        self.optical_center_adj = -0.1
        self.name_y_pos = 0
        self.input_names = input_names 
        self.output_names = output_names 
        self.inputs = self._create_io(self.input_names,
                                      is_inputs=True, 
                                      connect_left=True)
        self.outputs = self._create_io(self.output_names, 
                                       is_inputs=False,
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

    def get_io(self, name):
        io_lst = self.inputs + self.outputs
        matching_io = filter(lambda x: x.name == name, io_lst)
        matching_io = list(matching_io)

        assert(len(matching_io) == 1)

        return matching_io[0]

    def _layout_name(self, bounds):
        self.name_y_pos = (bounds.center_y + 
                           (self.optical_center_adj * bounds.height))  

    def _create_io(self, io_list, is_inputs=True, connect_left=True):
        lst = []
        for io_name in io_list:
            lst.append(IO(io_name, is_inputs, connect_left))

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
        name_size = self.bounds.width / 3
                    
        canvas.text((self.bounds.center_x, self.name_y_pos),
                    self.name,
                    font_size=name_size)