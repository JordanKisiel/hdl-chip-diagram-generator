from src.parsers.grammar import Vistor as Chip_Visitor
from src.parsers.grammar import Bus, Sub_Bus, Range
from src.parsers.primitive_grammar import Vistor as Primitive_Visitor

class Primitive_IO_Getter(Primitive_Visitor):
    def __init__(self):
        self.inputs = []
        self.outputs = []

    def get_io(self, rule):
        rule.accept(self)

        return {
            "inputs": self.inputs,
            "outputs": self.outputs
        } 
    
    def visit_chip_spec(self, rule):
        rule.interface.accept(self) 
    
    def visit_interface(self, rule):
        self.inputs = rule.inputs.accept(self)
        self.outputs = rule.outputs.accept(self)

    def visit_inputs(self, rule):
        return rule.chip_io.accept(self)

    def visit_outputs(self, rule):
        return rule.chip_io.accept(self)

    def visit_chip_io(self, rule):
        io_lst = [rule.ident_token.lexeme]

        for io in rule.extra_io:
            io_lst.append(io.accept(self))

        return io_lst

    def visit_extra_io(self, rule):
        return rule.ident_token.lexeme

class Chip_IO_Getter(Chip_Visitor):
    def __init__(self):
        self.inputs = []
        self.outputs = []

    def get_io(self, rule):
        rule.accept(self)

        return {
            "inputs": self.inputs,
            "outputs": self.outputs
        }
    
    def visit_chip_spec(self, rule):
        rule.header.accept(self)

    def visit_header(self, rule):
        self.inputs = rule.chip_io_1.accept(self)
        self.outputs = rule.chip_io_2.accept(self)

    def visit_chip_io(self, rule):
        io_lst = []
        io_name = None
        if isinstance(rule.ident_or_bus, Bus):
            io_name = rule.ident_or_bus.accept(self)
        else:
            io_name = rule.ident_or_bus.lexeme
        
        io_lst.append(io_name)
        
        for io in rule.extra_io:
            io_lst.append(io.accept(self))

        return io_lst

    def visit_extra_io(self, rule):
        io_name = None
        if isinstance(rule.ident_or_bus, Bus):
            io_name = rule.ident_or_bus.accept(self)
        else:
            io_name = rule.ident_or_bus.lexeme
        
        return io_name

    def visit_bus(self, rule):
        return rule.ident_token.lexeme 
     
    def visit_body(self, rule):
        pass

    def visit_connection(self, rule):
        pass 

    def visit_connections_list(self, rule):
        pass 

    def visit_extra_connection(self, rule):
        pass

    def visit_part(self, rule):
        pass 

    def visit_range(self, rule):
        pass 

    def visit_sub_bus(self, rule):
        pass 