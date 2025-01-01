from src.parsers.grammar import *
from src.diagram.bounds import Bounds
from src.diagram.diagrammables import *
from src.diagram.chip_layout import Chip_Layout
from src.visitors.interface_getter import *

class Chip_Diagram(Vistor):
    def __init__(self, canvas, primitive_chips, custom_chips):
        self.canvas = canvas
        self.primitive_chips = primitive_chips
        self.custom_chips = custom_chips
        self.title = None
        self.outline = None
        self.inputs = []
        self.outputs = []
        self.internal_pins = []
        self.parts = []
        self.connections = []
        self.margin = 4
        self.title_margin = 1.5
        self.io_width = 3

    def diagram(self, chip_ast):
        chip_ast.accept(self)
        self.layout()
        self.draw()

    def layout(self):
        assert(self.title != None)
        assert(self.outline != None)

        min_parts_margin = self.margin + 2
        dynamic_parts_margin = self.margin + 6 - len(self.parts)
        parts_margin = max(min_parts_margin, dynamic_parts_margin)

        grid = self.canvas.grid
        
        self.title.layout(Bounds(grid.y(self.title_margin), 
                                 0, 
                                 self.canvas.height, 
                                 self.canvas.width))
        
        self.outline.layout(Bounds(grid.y(self.margin),
                                   grid.x(self.margin),
                                   grid.y(-self.margin),
                                   grid.x(-self.margin)))

        # inputs
        Chip_Layout.distribute_io(Bounds(self.outline.bounds.top,
                                         self.outline.bounds.left -
                                          grid.x(self.io_width),
                                         self.outline.bounds.bottom,
                                         self.outline.bounds.left),
                                  self.inputs)
        # outputs
        Chip_Layout.distribute_io(Bounds(self.outline.bounds.top,
                                         self.outline.bounds.right,
                                         self.outline.bounds.bottom,
                                         self.outline.bounds.right + 
                                          grid.x(self.io_width)),
                                  self.outputs)
        
        Chip_Layout.distribute_parts(Bounds(grid.y(parts_margin),
                                            grid.x(parts_margin),
                                            grid.y(-parts_margin),
                                            grid.x(-parts_margin)),
                                    self.parts,
                                    grid.y(1),
                                    grid.x(1))
        
        Chip_Layout.distribute_connections(self.connections) 


    def draw(self):
        self.canvas.draw_grid()
        
        self.title.draw()
        self.outline.draw()
        for input in self.inputs:
            input.draw()
        for output in self.outputs:
            output.draw()
        for part in self.parts:
            part.draw()
        for connection in self.connections:
            connection.draw()

    def write(self):
        assert(self.title != None)
        self.canvas.out.save(f"{self.title.text}_Chip.png")

    def _get_chip_io_by_name(self, name):
        io_lst = self.inputs + self.outputs
        matching_io = filter(lambda x: x.name == name, io_lst)
        matching_io = list(matching_io)
        # asserting that io names should be unique
        # and that we're searching for name that should match something
        assert(len(matching_io) == 1)

        return matching_io[0]
    
    def _get_part_io_by_name(self, part, name):
        io_lst = part.inputs + part.outputs
        matching_io = filter(lambda x: x.name == name, io_lst)
        matching_io = list(matching_io)
        # asserting that io names should be unique
        # and that we're searching for name that should match something
        assert(len(matching_io) == 1)

        return matching_io[0] 
    

    # Visitor Methods
    # ---------------------------------------------------
    def visit_chip_spec(self, rule):
        self.title = Title(self, rule.ident_token.lexeme)
        rule.header.accept(self)
        rule.body.accept(self)

    def visit_header(self, rule):
        self.outline = Outline(self)
        
        input_list = rule.chip_io_1.accept(self)
        self.inputs = [IO(self, input_name, connect_left=False) 
                       for input_name in input_list]
        output_list = rule.chip_io_2.accept(self)
        self.outputs = [IO(self, output_name, connect_left=True) 
                        for output_name in output_list]

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
        for part in rule.parts_list:
            self.parts.append(part.accept(self))
        
    def visit_part(self, rule):
        part_name = rule.ident_token.lexeme
        # for now we only get the io of primitive
        # chips as those are the only chips we
        # are using in the dummy hdl chip
        io = {
            "inputs": [],
            "outputs": []
        }
        
        if part_name.lower() in self.primitive_chips:
            prim_io = Primitive_IO_Getter()
            prim_chip = self.primitive_chips[part_name.lower()]
            io = prim_io.get_io(prim_chip)
        elif part_name.lower() in self.custom_chips:
            custom_io = Chip_IO_Getter()
            custom_chip = self.custom_chips[part_name.lower()]
            io = custom_io.get_io(custom_chip)

        part = Part(self, 
                    rule.ident_token.lexeme, 
                    io["inputs"], 
                    io["outputs"])

        connections = rule.connections_list.accept(self)

        for connection in connections:
            io_1 = self._get_chip_io_by_name(connection["chip_connect"])
            io_2 = self._get_part_io_by_name(part, connection["part_connect"])

            # if the chip connection is an output (and therefore
            # connects left) then swap the order of the args
            # to prevent drawing error that occurs if the
            # connections aren't drawn from a consistent direction
            if io_1.connect_left:
                temp = io_1
                io_1 = io_2
                io_2 = temp

            self.connections.append(Connection(self, io_1, io_2))

        return part
        
    def visit_connections_list(self, rule):
        connect_1 = rule.connect_1.accept(self)
        connect_2 = rule.connect_2.accept(self)
        connections = [connect_1, connect_2]

        for connection in rule.extra_connections:
            connections.append(connection.accept(self))

        return connections

    def visit_connection(self, rule):
        ident_or_sub_bus = None
        if isinstance(rule.ident_or_sub_bus, Sub_Bus):
            ident_or_sub_bus = rule.ident_or_sub_bus.accept(self)
        else:
            ident_or_sub_bus = rule.ident_or_sub_bus.lexeme

        return {
            "part_connect": ident_or_sub_bus, 
            "chip_connect": rule.ident_or_binary_val.lexeme
        }
         
    def visit_extra_connection(self, rule):
        return rule.connection.accept(self) 

    def visit_sub_bus(self, rule):
        number_or_range = None
        if isinstance(rule.number_or_range, Range):
            number_or_range = rule.number_or_range.accept(self)
        else:
            number_or_range = rule.number_or_range.lexeme

        return f"{rule.ident_token.lexeme}[{number_or_range}]" 

    def visit_range(self, rule):
        return f"{rule.number_token_1.lexeme}..{rule.number_token_2.lexeme}" 
