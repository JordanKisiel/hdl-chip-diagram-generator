from src.parsers.grammar import *
from src.diagram.bounds import Bounds
from src.diagram.diagrammables import *
from src.diagram.chip_layout import Chip_Layout
from src.visitors.interface_getter import *
from src.utils import Autoincrementer

class Chip_Diagram(Vistor):
    def __init__(self, canvas, primitive_chips, custom_chips):
        self.canvas = canvas
        self.primitive_chips = primitive_chips
        self.custom_chips = custom_chips
        # TODO:
        # change the code to use chip components
        # instead of member variables
        self.chip_data = {
            "title_text": None,
            "input_names": [],
            "output_names": [],
            "parts_data": [],
            "connection_data": [],
            "internal_wires": {}
        }

        self.components = {
            "title": None,
            "outline": None,
            "inputs": [],
            "outputs": [],
            "parts": [],
            "connections": []
        }

        self.margin = 4
        self.title_margin = 1.5
        self.io_width = 3
        self.part_id_generator = Autoincrementer()

    def diagram(self, chip_ast):
        chip_ast.accept(self)
        self.generate()
        self.layout()
        self.draw()

    def generate(self):
        self.components["title"] = Title(self, self.chip_data["title_text"])
        self.components["outline"] = Outline(self)
        self.components["inputs"]= [IO(self, input_name, connect_left=False) 
                       for input_name in self.chip_data["input_names"]]
        self.components["outputs"] = [IO(self, output_name, connect_left=True) 
                        for output_name in self.chip_data["output_names"]]
        self.components["parts"] = [Part(self, 
                           part["name"], 
                           part["id"], 
                           part["inputs"], 
                           part["outputs"]) 
                      for part in self.chip_data["parts_data"]]

        self._generate_internal_wire_associations()
        
        for connection in self.chip_data["connection_data"]:
            part = self._get_part_by_id(connection["part_id"])
            io_1 = self._get_part_io_by_name(part, connection["part_pin"])
            io_2 = None
            
            if connection["other_pin"] in self.chip_data["internal_wires"]:
                pin_data = self.chip_data["internal_wires"][connection["other_pin"]]
                other_pin_part = self._get_part_by_id(pin_data["part_id"])
                io_2 = self._get_part_io_by_name(other_pin_part, pin_data["output_pin"]) 
            elif connection["other_pin"] in (self.chip_data["input_names"] + 
                                             self.chip_data["output_names"]):
                io_2 = self._get_chip_io_by_name(connection["other_pin"])

            # connection lines only draw correctly if drawn
            # left to right, so swap io objects if necessary
            if io_1.connect_left:
                temp = io_1
                io_1 = io_2
                io_2 = temp

            self.components["connections"].append(Connection(self, io_1, io_2))


    def layout(self):
        assert(self.components["title"] != None)
        assert(self.components["outline"] != None)

        min_parts_margin = self.margin + 2
        dynamic_parts_margin = self.margin + 6 - len(self.components["parts"])
        parts_margin = max(min_parts_margin, dynamic_parts_margin)

        grid = self.canvas.grid
        
        self.components["title"].layout(Bounds(grid.y(self.title_margin), 
                                 0, 
                                 self.canvas.height, 
                                 self.canvas.width))
        
        self.components["outline"].layout(Bounds(grid.y(self.margin),
                                   grid.x(self.margin),
                                   grid.y(-self.margin),
                                   grid.x(-self.margin)))

        # inputs
        Chip_Layout.distribute_io(Bounds(self.components["outline"].bounds.top,
                                         self.components["outline"].bounds.left -
                                          grid.x(self.io_width),
                                         self.components["outline"].bounds.bottom,
                                         self.components["outline"].bounds.left),
                                  self.components["inputs"])
        # outputs
        Chip_Layout.distribute_io(Bounds(self.components["outline"].bounds.top,
                                         self.components["outline"].bounds.right,
                                         self.components["outline"].bounds.bottom,
                                         self.components["outline"].bounds.right + 
                                          grid.x(self.io_width)),
                                  self.components["outputs"])
        
        Chip_Layout.distribute_parts(Bounds(grid.y(parts_margin),
                                            grid.x(parts_margin),
                                            grid.y(-parts_margin),
                                            grid.x(-parts_margin)),
                                    self.components["parts"],
                                    grid.y(1),
                                    grid.x(1))
        
        Chip_Layout.distribute_connections(self.components["connections"]) 


    def draw(self):
        self.canvas.draw_grid()
        
        self.components["title"].draw()
        self.components["outline"].draw()
        for input in self.components["inputs"]:
            input.draw()
        for output in self.components["outputs"]:
            output.draw()
        for part in self.components["parts"]:
            part.draw()
        for connection in self.components["connections"]:
            connection.draw()

    def write(self):
        assert(self.components["title"] != None)
        self.canvas.out.save(f"{self.chip_data['title_text']}_Chip.png")

    def _get_chip_io_by_name(self, name):
        io_lst = self.components["inputs"] + self.components["outputs"]
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
    
    def _get_part_by_id(self, id):
        matching_part = filter(lambda x: x.id == id, self.components["parts"])
        matching_part = list(matching_part)

        # asserting that exactly 1 result
        # should be retrieved
        assert(len(matching_part) == 1)

        return matching_part[0]

    def _generate_internal_wire_associations(self):
        internal_wire_references = []
        chip_io_names = (self.chip_data["input_names"] + 
                         self.chip_data["output_names"])
        for connect_data in self.chip_data["connection_data"]:
            if connect_data["other_pin"] not in chip_io_names:
                internal_wire_references.append(connect_data)

        for reference in internal_wire_references:
            part = self._get_part_by_id(reference["part_id"])
            if reference["part_pin"] in part.output_names:
                wire_name = reference["other_pin"]
                part_id = reference["part_id"]
                output_pin = reference["part_pin"]

                assert(wire_name not in self.chip_data["internal_wires"])

                self.chip_data["internal_wires"][wire_name] = {
                    "part_id": part_id, 
                    "output_pin": output_pin
                    }




    # Visitor Methods
    # ---------------------------------------------------
    def visit_chip_spec(self, rule):
        self.chip_data["title_text"] = rule.ident_token.lexeme
        rule.header.accept(self)
        rule.body.accept(self)

    def visit_header(self, rule):
        self.chip_data["input_names"] = rule.chip_io_1.accept(self)
        self.chip_data["output_names"] = rule.chip_io_2.accept(self)

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
            self.chip_data["parts_data"].append(part.accept(self))
        
    def visit_part(self, rule):
        part_name = rule.ident_token.lexeme

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

        part_id = self.part_id_generator.get_id()

        part = {
            "name": part_name,
            "id": part_id,
            "inputs": io["inputs"],
            "outputs": io["outputs"]
        }

        connections = rule.connections_list.accept(self)

        for connection in connections:
            self.chip_data["connection_data"].append({"part_id": part_id,
                                         "part_pin": connection["pin_1"],
                                         "other_pin": connection["pin_2"]})


        # for connection in connections:
        #     # if I enounter an internal wire (meaning the right side of the
        #     # connection isn't found in the chip interface) then I need to
        #     # check if the internal wire has been defined in the
        #     # self.internal_wires dict
        #     # if it has not, add it as for example:
        #     # "w1" => reference to io object
        #     # and don't add a connection
        #     # if it has, retrieve the io object and use it as one of the
        #     # io object in the Connection object constructor
        #     io_1 = self._get_chip_io_by_name(connection["chip_connect"])
        #     io_2 = self._get_part_io_by_name(part, connection["part_connect"])


        #     # if the chip connection is an output (and therefore
        #     # connects left) then swap the order of the args
        #     # to prevent drawing error that occurs if the
        #     # connections aren't drawn from a consistent direction
        #     if io_1.connect_left:
        #         temp = io_1
        #         io_1 = io_2
        #         io_2 = temp

        #     self.connections.append(Connection(self, io_1, io_2))

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
            "pin_1": ident_or_sub_bus, 
            "pin_2": rule.ident_or_binary_val.lexeme
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
