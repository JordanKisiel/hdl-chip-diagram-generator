from src.grammar import *
from src.diagram import *
from PIL import Image, ImageDraw, ImageFont

class Chip_Diagramer(Vistor):
    def __init__(self, chip_spec, diagram):
        self.chip_spec = chip_spec 
        self.diagram = diagram
        self.outline_top = 4
        self.outline_right = -4
        self.outline_bottom = -4
        self.outline_left = 4
        self.parts_top = 8
        self.parts_right = -8
        self.parts_bottom = -8
        self.parts_left = 8
        self.part_aspect = 16 / 9
        
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
        parts_section_height = bottom - top
        parts_section_width = right - left
        parts_margin = self.diagram.grid.y(1) / len(parts_list) 

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

            part_top = top + index * parts_section_height / len(parts_list) + top_margin
            part_bottom = top + (index + 1) * parts_section_height / len(parts_list) - bottom_margin
            part_height = part_bottom - part_top
            part_width = part_height * self.part_aspect
            #TODO:
            #  -figure out how to round this width to the nearest width
            #  divisible by grid divisions
            part_left = left + parts_section_width / 2 - part_width / 2 
            part_right = left + parts_section_width / 2 + part_width / 2
            part = Part([(part_left, part_top), (part_right, part_bottom)], part_name)
            self.diagram.add(part)

        #TODO:
        # -draw inputs and outputs of parts
        #   -possible problem: in the connections list I don't distinguish
        #   the inputs and outputs
        #     -in order to know which connection is an input and output, I would
        #     have to peek inside the part's chip definition header
        #       -add primitive chip definition files (which ones?)
        #       -start thinking about a chip decomposition tree or chip lookup table



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


class Chip_IO(Diagrammable):
    def __init__(self, name, x_bounds, y_position):
        self.name = name
        self.x_bounds = x_bounds 
        self.y_position = y_position
        self.diagram = None

    def draw(self):
        # draw text
        input_font = ImageFont.truetype(self.diagram.style["font"],
                                        self.diagram.style["base_font_size"] * 0.75)
        name_pos_x = (abs(self.x_bounds[0] - self.x_bounds[1]) / 2) + self.x_bounds[0]
        name_pos_y = self.y_position - self.diagram.grid.x(1) * 0.75  
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
    def __init__(self, bounds, text):
        self.bounds = bounds
        self.text = text
        self.box = Box(bounds, text)
        self.diagram = None

    def draw(self):
        self.box.draw()

    def add_to_diagram(self, diagram):
        self.diagram = diagram
        self.box.diagram = diagram 