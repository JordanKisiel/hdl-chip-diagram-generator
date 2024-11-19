from src.hdl_token import Token
from src.token_types import TokenType
from src.hdl_error import HDLError

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self.is_at_end():
            # at beginning of token
            self.start = self.current
            self.scan_token()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

        return self.tokens 

    def scan_token(self):
        char = self.advance()

        match char:
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')': self.add_token(TokenType.RIGHT_PAREN)
            case '{': self.add_token(TokenType.LEFT_BRACE)
            case '}': self.add_token(TokenType.RIGHT_BRACE)
            case '[': self.add_token(TokenType.LEFT_BRACKET)
            case ']': self.add_token(TokenType.RIGHT_BRACKET)
            case ',': self.add_token(TokenType.COMMA)
            case ';': self.add_token(TokenType.SEMICOLON)
            case '=': self.add_token(TokenType.EQUAL)

            # default invalid char 
            case _: HDLError.error(self.line, "Unexpected character.") 
    
    def is_at_end(self):
         return self.current >= len(self.source)
    
    def advance(self):
        char = self.source[self.current]
        self.current += 1
        return char 
    
    def add_token(self, token_type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))