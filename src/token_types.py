from enum import Enum
from src.hdl_token import Token

TokenType = Enum("TokenType",
             [
                 # single char tokens
                 "LEFT_PAREN",
                 "RIGHT_PAREN",
                 "LEFT_BRACE",
                 "RIGHT_BRACE",
                 "LEFT_BRACKET",
                 "RIGHT_BRACKET",
                 "COMMA",
                 "SEMICOLON",
                 "EQUAL",
                 "COLON",

                 # two char tokens
                 "DOUBLE_DOT",

                 "SINGLE_LINE_COMMENT",
                 "MULTI_LINE_COMMENT",
                 "NON_NEWLINE_SPACE",

                 "NEWLINE",

                 # literals
                 "IDENTIFIER",
                 "NUMBER",

                 # keywords
                 "CHIP",
                 "PARTS",
                 "IN",
                 "OUT",
                 "BUILTIN",
                 "CLOCKED",

                 "EOF"
             ] 

)

# mapping token type to
# regex pattern
token_types = {
    "single_chars": {
        TokenType.LEFT_PAREN: r"([(])",
        TokenType.RIGHT_PAREN: r"([)])",
        TokenType.LEFT_BRACE: r"([{])",
        TokenType.RIGHT_BRACE: r"([}])",
        TokenType.LEFT_BRACKET: r"([[])",
        TokenType.RIGHT_BRACKET: r"([]])",
        TokenType.COMMA: r"([,])",
        TokenType.SEMICOLON: r"([;])",
        TokenType.EQUAL: r"([=])",
        TokenType.COLON: r"([:])"
    },

    "double_chars": {
        TokenType.DOUBLE_DOT: r"([.]{2})"
    },

    "skipped_text": {
        TokenType.SINGLE_LINE_COMMENT: r"([/]{2,}.*[\n])",
        TokenType.MULTI_LINE_COMMENT: r"(\/\*(.|\n)*\*\/)",
        TokenType.NON_NEWLINE_SPACE: r"([\t ]+)"
    },

    "newline": {
        TokenType.NEWLINE: r"([\r\n]{1})"
    },
    
    "number": {
        TokenType.NUMBER: r"(\d+)"
    },

    "identifier": {
        TokenType.IDENTIFIER: r"([a-zA-Z][a-zA-Z\d]*)"
    },

    "keywords": {
        TokenType.CHIP: r"(CHIP)",
        TokenType.PARTS: r"(PARTS)",
        TokenType.IN: r"(IN)",
        TokenType.OUT: r"(OUT)",
        TokenType.BUILTIN: r"(BUILTIN)",
        TokenType.CLOCKED: r"(CLOCKED)"
    },

    TokenType.EOF: None
}


