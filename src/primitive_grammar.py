from abc import ABC, abstractmethod
from src.grammar import Grammar_Rule

class Chip_Spec(Grammar_Rule):
    def __init__(self,
                 chip_token,
                 ident_token,
                 left_brace_token,
                 interface, 
                 right_brace_token):
        self.chip_token = chip_token
        self.ident_token = ident_token
        self.left_brace_token = left_brace_token
        self.interface = interface
        self.right_brace_token = right_brace_token

    def accept(self, visitor):
        return visitor.visit_chip_spec(self)
    
class Interface(Grammar_Rule):
    def __init__(self,
                 inputs,
                 outputs):
        self.inputs = inputs
        self.outputs = outputs
    
    def accept(self, visitor):
        return visitor.visit_interface(self) 

class Inputs(Grammar_Rule):
    def __init__(self,
                 in_token,
                 chip_io,
                 semi_token):
        self.in_token = in_token
        self.chip_io = chip_io 
        self.semi_token = semi_token 

    def accept(self, visitor):
        return visitor.visit_inputs(self) 
    
class Outputs(Grammar_Rule):
    def __init__(self,
                 out_token,
                 chip_io,
                 semi_token):
        self.out_token = out_token 
        self.chip_io = chip_io 
        self.semi_token = semi_token 

    def accept(self, visitor):
        return visitor.visit_outputs(self) 
    
class Chip_IO(Grammar_Rule):
    def __init__(self, ident_token, extra_io = []):
        self.ident_token = ident_token
        self.extra_io = extra_io 

    def accept(self, visitor):
        return visitor.visit_chip_io(self)
    
class Extra_IO(Grammar_Rule):
    def __init__(self, comma_token, ident_token):
        self.comma_token = comma_token 
        self.ident_token = ident_token

    def accept(self, visitor):
        return visitor.visit_extra_io(self)