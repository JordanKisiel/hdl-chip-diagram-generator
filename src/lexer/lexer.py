import re
from src.lexer.hdl_token import Token
from src.lexer.token_types import TokenType, token_types
from src.hdl_error import HDLError

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self.is_at_end():
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
            keywords = [keyword[1:-1] for keyword in list(token_types["keywords"].values())]
            if ident_match.group(0) in keywords: 
                for type in token_types["keywords"]:
                    if(self.match_keyword(type, source)):
                        return
                
            self.match_identifier(TokenType.IDENTIFIER, source) 
            return

        HDLError.error(self.line, "Unexpected character.") 
        self.current += 1
    
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
            if token_type == TokenType.SINGLE_LINE_COMMENT:
                self.line += 1
            if token_type == TokenType.MULTI_LINE_COMMENT:
                new_line_matches = re.findall(r"\n", match.group(0))
                self.line += len(new_line_matches)

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
        match = re.match(token_types["identifier"][token_type], source)
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

