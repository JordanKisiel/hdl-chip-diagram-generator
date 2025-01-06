from src.parsers.grammar import *
from src.visitors.interface_getter import *
from src.utils import Autoincrementer

class Chip_Data(Vistor):
    def __init__(self, primitive_chips, custom_chips):
        self.title_text = None
        self.input_names = []
        self.output_names = []
        self.parts_data = []
        self.connections_data = []
        self.internal_wires = {}
        self.primitive_chips = primitive_chips
        self.custom_chips = custom_chips 
        self.part_id_generator = Autoincrementer()

    def get_data(self, chip_ast):
        chip_ast.accept(self)

        self._generate_internal_wire_associations()

    def _generate_internal_wire_associations(self):
        internal_wire_references = []
        chip_io_names = (self.input_names + 
                         self.output_names)
        for connect_data in self.connections_data:
            if connect_data["other_pin"] not in chip_io_names:
                internal_wire_references.append(connect_data)

        for reference in internal_wire_references:
            part_data = self._get_part_data_by_id(reference["part_id"])
            if reference["part_pin"] in part_data["outputs"]:
                wire_name = reference["other_pin"]
                part_id = reference["part_id"]
                output_pin = reference["part_pin"]

                assert(wire_name not in self.internal_wires)

                self.internal_wires[wire_name] = {
                    "part_id": part_id, 
                    "output_pin": output_pin
                    }
                
    def _get_part_data_by_id(self, id):
        matching_data = filter(lambda x: x["id"] == id,
                               self.parts_data)
        matching_data = list(matching_data)

        # asserting that exactly 1 result
        # should be retrieved
        assert(len(matching_data) == 1)

        return matching_data[0]

    # Visitor Methods
    # ---------------------------------------------------
    def visit_chip_spec(self, rule):
        self.title_text = rule.ident_token.lexeme
        rule.header.accept(self)
        rule.body.accept(self)

    def visit_header(self, rule):
        self.input_names = rule.chip_io_1.accept(self)
        self.output_names = rule.chip_io_2.accept(self)

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
            self.parts_data.append(part.accept(self))
        
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
            self.connections_data.append({"part_id": part_id,
                                         "part_pin": connection["pin_1"],
                                         "other_pin": connection["pin_2"]})

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
