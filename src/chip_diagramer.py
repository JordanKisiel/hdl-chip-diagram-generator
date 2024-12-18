from src.grammar import *
from src.primitive_grammar import *
from src.diagram import *
from PIL import Image, ImageDraw, ImageFont

class Chip_Diagramer(Vistor):
    def __init__(self, chip_spec, diagram, primitive_chips):
        self.chip_spec = chip_spec 
        self.diagram = diagram
        self.primitive_chips = primitive_chips
        self.outline_top = 4
        self.outline_right = -4
        self.outline_bottom = -4
        self.outline_left = 4
        self.parts_top = 8
        self.parts_right = -8
        self.parts_bottom = -8
        self.parts_left = 8
        self.part_aspect = 4 / 3 
        
    def write(self):
        self.diagram.write(f"{self.chip_spec.ident_token.lexeme}_diagram.png") 

    def draw(self):
        self.diagram.draw_grid()
        self.visit_chip_spec(self.chip_spec)
        self.diagram.draw()

    def add_chip_io(self, input_list, output_list):
        top = self.diagram.grid.y(self.outline_top)
        bottom = self.diagram.grid.y(self.outline_bottom)
        for index, input_name in enumerate(input_list):
            y_pos = ((index + 1) * abs(top - bottom) / (len(input_list) + 1)) + top
            input = Chip_IO(input_name,
                            (self.diagram.grid.x(1), self.diagram.grid.x(self.outline_left)),
                            y_pos)
            self.diagram.add(input)

        for index, output_name in enumerate(output_list):
            y_pos = ((index + 1) * abs(top - bottom) / (len(output_list) + 1)) + top
            output = Chip_IO(output_name,
                            (self.diagram.grid.x(self.outline_right), self.diagram.grid.x(-1)),
                            y_pos)
            self.diagram.add(output)

    def add_parts(self, parts_list):
        top = self.diagram.grid.y(self.parts_top)
        right = self.diagram.grid.x(self.parts_right)
        bottom = self.diagram.grid.y(self.parts_bottom)
        left = self.diagram.grid.x(self.parts_left)
        parts_margin = self.diagram.grid.y(1) / len(parts_list) 
        part_height = (bottom - top) / len(parts_list) - (2 * parts_margin)
        part_width = part_height * self.part_aspect

        for index, part_name in enumerate(parts_list):
            if index == 0:
                top_margin = 0
                bottom_margin = parts_margin * 2
            elif index < len(parts_list) - 1:
                top_margin = parts_margin
                bottom_margin = parts_margin
            else:
                top_margin = parts_margin * 2
                bottom_margin = 0

            if len(parts_list) == 1:
                bottom_margin = 0

            part_top = top + index * (bottom - top) / len(parts_list) + top_margin
            part_bottom = top + (index + 1) * (bottom - top) / len(parts_list) - bottom_margin
            part_left = left + (right - left) / 2 - part_width / 2 
            part_left = self._snap(part_left, self.diagram.grid.x(1), snap_lower=True)
            part_right = left + (right - left) / 2 + part_width / 2
            part_right = self._snap(part_right, self.diagram.grid.x(1), snap_lower=False)

            io = {
                "inputs": [],
                "outputs": []
            } 

            if part_name.lower() in self.primitive_chips:
                io = self._get_primitive_io(part_name.lower())
            part = Part([(part_left, part_top), (part_right, part_bottom)], part_name, io["inputs"], io["outputs"])
            self.diagram.add(part)



    # Visitor methods
    # ----------------------------------------------------------------------
    def visit_chip_spec(self, rule):
        title = Title(rule.ident_token.lexeme, 
                      (self.diagram.grid.center_x(), self.diagram.grid.y(2)))
        self.diagram.add(title)
        rule.header.accept(self)
        rule.body.accept(self)

    def visit_header(self, rule):
        chip_outline = Box([self.diagram.grid.point(self.outline_left,
                                                    self.outline_top),
                            self.diagram.grid.point(self.outline_right,
                                                    self.outline_bottom)])
        self.diagram.add(chip_outline)

        input_list = rule.chip_io_1.accept(self)
        output_list = rule.chip_io_2.accept(self)

        self.add_chip_io(input_list, output_list)

    def visit_chip_io(self, rule):
        io_list = []
        if isinstance(rule.ident_or_bus, Bus):
            io_list.append(rule.ident_or_bus.accept(self))
        else:
            io_list.append(rule.ident_or_bus.lexeme)

        for io in rule.extra_io:
            io_list.append(io.accept(self))

        return io_list 

    def visit_extra_io(self, rule):
        if isinstance(rule.ident_or_bus, Bus):
            return rule.ident_or_bus.accept(self)
        else:
            return rule.ident_or_bus.lexeme

    def visit_bus(self, rule):
        return f"{rule.ident_token}[{rule.number_token}]" 

    def visit_body(self, rule):
        parts = []
        for part in rule.parts_list:
            parts.append(part.accept(self))
        
        self.add_parts(parts)

    def visit_part(self, rule):
        return rule.ident_token.lexeme

    def visit_connections_list(self, rule):
        pass

    def visit_connection(self, rule):
        pass

    def visit_extra_connection(self, rule):
        pass

    def visit_sub_bus(self, rule):
        pass

    def visit_range(self, rule):
        pass

    # helper methods
    # --------------------------------------------

    def _snap(self, value, div_value, snap_lower):
        threshold = 0.001
        divisions = value / div_value 
        fractional = divisions % 1
        if fractional < threshold:
            return value
        if 1 - fractional < threshold:
            return value
        
        if snap_lower:
            rounding = value % div_value 
            return value - rounding
        else:
            rounding = 1 - (value % div_value)
            return value + rounding
        
    def _get_primitive_io(self, primitive_name):
        io = {}
        inputs = []
        outputs = []

        prim = self.primitive_chips[primitive_name]

        inputs.append(prim.interface.inputs.chip_io.ident_token.lexeme)
        for item in prim.interface.inputs.chip_io.extra_io:
            inputs.append(item.ident_token.lexeme)
        outputs.append(prim.interface.outputs.chip_io.ident_token.lexeme)
        for item in prim.interface.outputs.chip_io.extra_io:
            outputs.append(item.ident_token.lexeme)

        io["inputs"] = inputs
        io["outputs"] = outputs 

        return io



class Chip_IO(Diagrammable):
    def __init__(self, name, x_bounds, y_position):
        self.name = name
        self.x_bounds = x_bounds 
        self.y_position = y_position
        self.diagram = None

    def draw(self):
        # draw text
        input_width = abs(self.x_bounds[0] - self.x_bounds[1])
        text_width = len(self.name) * self.diagram.style["base_font_size"]
        scaling_factor = input_width / 4 / text_width
        font_size = text_width * scaling_factor 
        input_font = ImageFont.truetype(self.diagram.style["font"],
                                        font_size)
        name_pos_x = input_width / 2 + self.x_bounds[0]
        name_pos_y = self.y_position - font_size  
        self.diagram.draw_context.text((name_pos_x, name_pos_y),
                                       self.name,
                                       fill=self.diagram.style["fg"],
                                       font=input_font,
                                       anchor="mt")
        # draw line
        self.diagram.draw_context.line([(self.x_bounds[0], 
                                        self.y_position),
                                        (self.x_bounds[1],
                                         self.y_position)],
                                         fill=self.diagram.style["fg"],
                                         width=self.diagram.style["stroke_width"])
        
class Part(Diagrammable):
    def __init__(self, bounds, text, input_names, output_names):
        self.bounds = bounds
        self.text = text
        self.box = Box(bounds, text)
        self.input_names = input_names 
        self.output_names = output_names
        self.inputs = []
        self.outputs = []
        self.diagram = None

    def draw(self):
        self.box.draw()

        for input in self.inputs:
            input.draw()

        for output in self.outputs:
            output.draw()
        
    def add_to_diagram(self, diagram):
        self.diagram = diagram
        self.box.diagram = diagram 

        left = self.bounds[0][0]
        top = self.bounds[0][1]
        right = self.bounds[1][0]
        bottom = self.bounds[1][1]
        for index, input_name in enumerate(self.input_names):
            y_pos = ((index + 1) * abs(top - bottom) / (len(self.input_names) + 1)) + top
            io_input = (Chip_IO(input_name,
                                (left - self.diagram.grid.x(2), 
                                 left),
                                y_pos))
            io_input.diagram = diagram
            self.inputs.append(io_input) 

        for index, output_name in enumerate(self.output_names):
            y_pos = ((index + 1) * abs(top - bottom) / (len(self.output_names) + 1)) + top
            io_output = (Chip_IO(output_name,
                                (right, 
                                 right + self.diagram.grid.x(2)),
                                y_pos))
            io_output.diagram = diagram
            self.outputs.append(io_output) 

        