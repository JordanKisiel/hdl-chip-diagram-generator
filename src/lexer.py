import re
from src.hdl_token import Token
from src.token_types import TokenType, token_types
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
            # probably don't need the start pointer
            self.start = self.current
            self.scan_token()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

        return self.tokens 

    def scan_token(self):
        source = self.source[self.current:]

        for type in token_types["single_chars"]:
            if(self.match_single_chars(type, source)):
                return
            
        for type in token_types["double_chars"]:
            if(self.match_double_chars(type, source)):
                return
            
        for type in token_types["skipped_text"]:
            if(self.match_skipped_text(type, source)):
                return
            
        for type in token_types["newline"]:
            if(self.match_newline(type, source)):
                return
            
        for type in token_types["number"]:
            if(self.match_number(type, source)):
                return

        # for identifiers, first must check to see if matching
        # text is a keyword
        ident_match = re.match(token_types["identifier"][TokenType.IDENTIFIER], source)
        if ident_match:
            if ident_match.group(0) in list(token_types["keywords"].values()):
                for type in token_types["keywords"]:
                    if(self.match_keyword(type, source)):
                        return
                
            self.match_identifier(TokenType.IDENTIFIER, source) 
            return

        HDLError.error(self.line, "Unexpected character.") 
    
    def is_at_end(self):
         return self.current >= len(self.source)
    
    def match_single_chars(self, token_type, source):
        matched = False
        match = re.match(token_types["single_chars"][token_type], source)
        if match:
            self.add_token(token_type, match.group(0))
            self.current += 1
            matched = True

        return matched
    
    def match_double_chars(self, token_type, source):
        matched = False
        match = re.match(token_types["double_chars"][token_type], source)
        if match:
            self.add_token(token_type, match.group(0))
            self.current += 2 
            matched = True

        return matched

    def match_skipped_text(self, token_type, source):
        matched = False
        match = re.match(token_types["skipped_text"][token_type], source)
        if match:
            self.current += len(match.group(0)) 
            matched = True

        return matched

    def match_newline(self, token_type, source):
        matched = False
        match = re.match(token_types["newline"][token_type], source)
        if match:
            self.current += 1
            self.line += 1
            matched = True

        return matched
    
    def match_number(self, token_type, source):
        matched = False
        match = re.match(token_types["number"][token_type], source)
        if match:
            self.add_token(token_type, match.group(0))
            self.current += len(match.group(0)) 
            matched = True

        return matched
    
    def match_identifier(self, token_type, source):
        matched = False
        match = re.match(token_types["indentifier"][token_type], source)
        if match:
            self.add_token(token_type, match.group(0))
            self.current += len(match.group(0)) 
            matched = True

        return matched

    def match_keyword(self, token_type, source):
        matched = False
        match = re.match(token_types["keywords"][token_type], source)
        if match:
            self.add_token(token_type, match.group(0))
            self.current += len(match.group(0)) 
            matched = True

        return matched

    def add_token(self, token_type, text, literal=None):
        self.tokens.append(Token(token_type, text, literal, self.line))

