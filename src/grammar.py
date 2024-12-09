from abc import ABC, abstractmethod

class Grammar_Rule(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def accept(self, visitor):
        self.visitor = visitor

class Vistor(ABC):
    @abstractmethod
    def visit_chip_spec(grammar_rule):
        pass

    @abstractmethod
    def visit_header(grammar_rule):
        pass

    @abstractmethod
    def visit_chip_io(grammar_rule):
        pass

    @abstractmethod
    def visit_bus(grammar_rule):
        pass

    @abstractmethod
    def visit_body(grammar_rule):
        pass

    @abstractmethod
    def visit_part(grammar_rule):
        pass

    @abstractmethod
    def visit_connections_list(grammar_rule):
        pass

    @abstractmethod
    def visit_connection(grammar_rule):
        pass

    @abstractmethod
    def visit_sub_bus(grammar_rule):
        pass

    @abstractmethod
    def visit_range(grammar_rule):
        pass


class Chip_Spec(Grammar_Rule):
    def __init__(self,
                 chip_token,
                 ident_token,
                 left_brace_token,
                 header, 
                 body,
                 right_brace_token):
        self.chip_token = chip_token
        self.ident_token = ident_token
        self.left_brace_token = left_brace_token
        self.header = header
        self.body = body
        self.right_brace_token = right_brace_token

    def accept(self, visitor):
        return visitor.visit_chip_spec(self)

class Header(Grammar_Rule):
    def __init__(self,
                 in_token,
                 chip_io_1,
                 semi_token_1,
                 out_token,
                 chip_io_2,
                 semi_token_2):
        self.in_token = in_token
        self.chip_io_1 = chip_io_1
        self.semi_token_1 = semi_token_1
        self.out_token = out_token
        self.chip_io_2 = chip_io_2
        self.semi_token_2 = semi_token_2

    def accept(self, visitor):
        return visitor.visit_header(self)

class Chip_IO(Grammar_Rule):
    def __init__(self, ident_or_bus, extra_io = []):
        self.ident_or_bus = ident_or_bus
        self.extra_io = extra_io 

    def accept(self, visitor):
        return visitor.visit_chip_io(self)

class Extra_IO(Grammar_Rule):
    def __init__(self, comma_token, ident_or_bus):
        self.comma_token = comma_token 
        self.ident_or_bus = ident_or_bus 

    def accept(self, visitor):
        return visitor.visit_extra_io(self)

class Bus(Grammar_Rule):
    def __init__(self,
                 ident_token,
                 left_bracket_token,
                 number_token,
                 right_bracket_token):
        self.ident_token = ident_token
        self.left_bracket_token = left_bracket_token
        self.number_token = number_token
        self.right_bracket_token = right_bracket_token

    def accept(self, visitor):
        return visitor.visit_bus(self)

class Body(Grammar_Rule):
    def __init__(self,
                 parts_token,
                 colon_token,
                 parts_list = []):
        self.parts_token = parts_token
        self.colon_token = colon_token
        self.parts_list = parts_list
         
    def accept(self, visitor):
        return visitor.visit_body(self)

class Part(Grammar_Rule):
    def __init__(self,
                 ident_token,
                 left_paren_token,
                 connections_list,
                 right_paren_token,
                 semi_token):
        self.ident_token = ident_token
        self.left_paren_token = left_paren_token
        self.connections_list = connections_list
        self.right_paren_token = right_paren_token
        self.semi_token= semi_token 

    def accept(self, visitor):
        return visitor.visit_part(self)

class Connections_List(Grammar_Rule):
    def __init__(self,
                 connect_1,
                 comma_token,
                 connect_2,
                 extra_connections = []):
        self.connect_1 = connect_1
        self.comma_token = comma_token
        self.connect_2 = connect_2
        self.extra_connections = extra_connections 

    def accept(self, visitor):
        return visitor.visit_connections_list(self)

class Connection(Grammar_Rule):
    def __init__(self,
                 ident_or_sub_bus,
                 equal_token,
                 ident_or_binary_val):
        self.ident_or_sub_bus = ident_or_sub_bus
        self.equal_token = equal_token
        self.ident_or_binary_val = ident_or_binary_val

    def accept(self, visitor):
        return visitor.visit_connection(self)
    
class Extra_Connection(Grammar_Rule):
    def __init__(self,
                 comma_token,
                 connection):
        self.comma_token = comma_token
        self.connection = connection

    def accept(self, visitor):
        return visitor.visit_extra_connection(self)

class Sub_Bus(Grammar_Rule):
    def __init__(self,
                 ident_token,
                 left_bracket_token,
                 number_or_range,
                 right_bracket_token):
        self.ident_token = ident_token
        self.left_bracket_token = left_bracket_token
        self.number_or_range = number_or_range
        self.right_bracket_token = right_bracket_token 

    def accept(self, visitor):
        return visitor.visit_sub_bus(self)

class Range(Grammar_Rule):
    def __init__(self,
                 number_token_1,
                 double_dot_token,
                 number_token_2):
        self.number_token_1 = number_token_1 
        self.double_dot_token = double_dot_token
        self.number_token_2 = number_token_2 

    def accept(self, visitor):
        return visitor.visit_range(self)