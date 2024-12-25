from src.lexer.token_types import *
from src.parsers.grammar import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0 
        self.error = False
    
    def parse(self):
        return self.chip_spec()
    
    def chip_spec(self):
        chip_token = self.match(TokenType.CHIP) 
        ident_token = self.match(TokenType.IDENTIFIER) 
        left_brace_token = self.match(TokenType.LEFT_BRACE) 
        header = self.header()
        body = self.body()
        right_brace_token = self.match(TokenType.RIGHT_BRACE)

        return Chip_Spec(chip_token,
                         ident_token,
                         left_brace_token,
                         header,
                         body,
                         right_brace_token)

    def header(self):
        in_token= self.match(TokenType.IN) 
        chip_io_1 = self.chip_io()
        semi_token_1 = self.match(TokenType.SEMICOLON)
        out_token= self.match(TokenType.OUT) 
        chip_io_2 = self.chip_io()
        semi_token_2 = self.match(TokenType.SEMICOLON)

        return Header(in_token,
                      chip_io_1,
                      semi_token_1,
                      out_token,
                      chip_io_2,
                      semi_token_2)
    
    def chip_io(self):
        ident_or_bus = None
        if self.check(TokenType.IDENTIFIER):
            ident_or_bus = self.match(TokenType.IDENTIFIER)
        else:
            ident_or_bus = self.bus()
        
        extra_io = []
        # io list is terminated by semi colon
        while not self.check(TokenType.SEMICOLON):
            extra_io.append(self.extra_io())

        return Chip_IO(ident_or_bus, extra_io)

    def body(self):
        parts_token = self.match(TokenType.PARTS)
        colon_token = self.match(TokenType.COLON)

        parts_list = []

        # the right brace is a unique char in a valid
        # chip spec and effectively ends the body
        # which the parts list is the last part of 
        while not self.check(TokenType.RIGHT_BRACE):
            parts_list.append(self.part())

        return Body(parts_token, colon_token, parts_list)


    def part(self):
        ident_token = self.match(TokenType.IDENTIFIER)
        left_paren_token = self.match(TokenType.LEFT_PAREN)
        connections_list = self.connections_list()
        right_paren_token = self.match(TokenType.RIGHT_PAREN)
        semi_token = self.match(TokenType.SEMICOLON)

        return Part(ident_token, 
                    left_paren_token, 
                    connections_list, 
                    right_paren_token, 
                    semi_token)

    def connections_list(self):
        connect_1 = self.connection()
        comma_token = self.match(TokenType.COMMA)
        connect_2 = self.connection()
        extra_connections = []
        
        # connections list is ended by a right paren
        while not self.check(TokenType.RIGHT_PAREN):
            extra_connections.append(self.extra_connection())

        return Connections_List(connect_1,
                                comma_token, 
                                connect_2, 
                                extra_connections)

    def connection(self):
        ident_or_sub_bus = None
        if self.check(TokenType.IDENTIFIER):
            ident_or_sub_bus = self.match(TokenType.IDENTIFIER)
        else:
            ident_or_sub_bus = self.sub_bus()

        equal_token = self.match(TokenType.EQUAL)

        ident_or_binary_val = None 
        if self.check(TokenType.IDENTIFIER):
            ident_or_binary_val = self.match(TokenType.IDENTIFIER)
        else:
            ident_or_binary_val = self.match(TokenType.NUMBER)
        
        return Connection(ident_or_sub_bus, equal_token, ident_or_binary_val)

    def extra_connection(self):
        comma_token = self.match(TokenType.COMMA)
        connection = self.connection()

        return Extra_Connection(comma_token, connection)

    def bus(self):
        ident_token = self.match(TokenType.IDENTIFIER)
        left_bracket_token = self.match(TokenType.LEFT_BRACKET)
        number_token = self.match(TokenType.NUMBER)
        right_bracket_token = self.match(TokenType.RIGHT_BRACKET)

        return Bus(ident_token, 
                   left_bracket_token, 
                   number_token, 
                   right_bracket_token)

    def sub_bus(self):
        ident_token = self.match(TokenType.IDENTIFIER)
        left_bracket_token = self.match(TokenType.LEFT_BRACKET)

        number_or_range = None
        if self.check(TokenType.NUMBER):
            self.match(TokenType.NUMBER)
        else:
            self.range()

        right_bracket_token = self.match(TokenType.RIGHT_BRACKET)

        return Sub_Bus(ident_token,
                       left_bracket_token,
                       number_or_range,
                       right_bracket_token)

    def extra_io(self):
        comma_token = self.match(TokenType.COMMA) 

        ident_or_bus = None
        if self.check(TokenType.IDENTIFIER):
            ident_or_bus = self.match(TokenType.IDENTIFIER)
        else:
            ident_or_bus = self.bus()

        return Extra_IO(comma_token, ident_or_bus)

    def range(self):
        number_token_1 = self.match(TokenType.NUMBER) 
        double_dot_token = self.match(TokenType.DOUBLE_DOT)
        number_token_2 = self.match(TokenType.NUMBER) 

        return Range(number_token_1, double_dot_token, number_token_2)

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

