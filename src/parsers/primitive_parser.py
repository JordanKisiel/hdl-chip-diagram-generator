from src.lexer.token_types import *
from src.parsers.primitive_grammar import *

class Primitive_Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0 
    
    def parse(self):
        return self.chip_spec()
    
    def chip_spec(self):
        chip_token = self.match(TokenType.CHIP) 
        ident_token = self.match(TokenType.IDENTIFIER) 
        left_brace_token = self.match(TokenType.LEFT_BRACE) 
        interface = self.interface()
        right_brace_token = self.match(TokenType.RIGHT_BRACE)

        return Chip_Spec(chip_token,
                         ident_token,
                         left_brace_token,
                         interface,
                         right_brace_token)

    def interface(self):
        inputs = self.inputs()
        outputs = self.outputs()

        return Interface(inputs,
                         outputs)

    def inputs(self):
        in_token = self.match(TokenType.IN)
        chip_io = self.chip_io()
        semi_token = self.match(TokenType.SEMICOLON)

        return Inputs(in_token,
                      chip_io,
                      semi_token)   

    def outputs(self):
        out_token = self.match(TokenType.OUT)
        chip_io = self.chip_io()
        semi_token = self.match(TokenType.SEMICOLON)

        return Outputs(out_token,
                       chip_io,
                       semi_token)

    def chip_io(self):
        ident_token = self.match(TokenType.IDENTIFIER) 
        
        extra_io = []
        # io list is terminated by semi colon
        while not self.check(TokenType.SEMICOLON):
            extra_io.append(self.extra_io())

        return Chip_IO(ident_token, extra_io)

    def extra_io(self):
        comma_token = self.match(TokenType.COMMA) 

        ident_token = self.match(TokenType.IDENTIFIER) 

        return Extra_IO(comma_token, ident_token)

    # helper methods --------------------------------
    def match(self, token_type):
        if self.check(token_type):
            return self.advance()
        else:
            self.error = True
        
    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().token_type == token_type
    
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def is_at_end(self):
        return self.peek().token_type == TokenType.EOF
    
    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current - 1]

