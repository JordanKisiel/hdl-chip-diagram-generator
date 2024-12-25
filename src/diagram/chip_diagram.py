from src.parsers.grammar import *
from src.diagram.bounds import Bounds
from src.diagram.diagrammables import *
from src.diagram.chip_layout import Chip_Layout

class Chip_Diagram(Vistor):
    def __init__(self, canvas, primitive_chips):
        self.canvas = canvas
        self.primitive_chips = primitive_chips
        self.title = None
        self.outline = None
        self.inputs = []
        self.outputs = []
        self.parts = []
        self.connections = []
        self.margin = 4
        self.title_margin = 1.5
        self.parts_margin = 3 + self.margin
        self.io_width = 3

    def diagram(self, chip_ast):
        chip_ast.accept(self)
        self.layout()
        self.draw()

    def layout(self):
        assert(self.title != None)
        assert(self.outline != None)

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
        
        Chip_Layout.distribute_parts(Bounds(grid.y(self.parts_margin),
                                            grid.x(self.parts_margin),
                                            grid.y(-self.parts_margin),
                                            grid.x(-self.parts_margin)),
                                    self.parts,
                                    grid.y(1),
                                    grid.x(1))

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
        # for now we don't have connections
        # for connection in self.connections:
        #     connection.draw()

    def write(self):
        assert(self.title != None)
        self.canvas.out.save(f"{self.title.text}_Chip.png")

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

    # Visitor Methods
    # ---------------------------------------------------
    def visit_chip_spec(self, rule):
        self.title = Title(self, rule.ident_token.lexeme)
        rule.header.accept(self)
        rule.body.accept(self)

    def visit_header(self, rule):
        self.outline = Outline(self)
        
        input_list = rule.chip_io_1.accept(self)
        self.inputs = [IO(self, input_name) for input_name in input_list]
        output_list = rule.chip_io_2.accept(self)
        self.outputs = [IO(self, output_name) for output_name in output_list]

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
            io = self._get_primitive_io(part_name.lower())

        return Part(self, 
                    rule.ident_token.lexeme,
                    io["inputs"],
                    io["outputs"])
        
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
        
        return (ident_or_sub_bus, rule.ident_or_binary_val.lexeme)
         
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
