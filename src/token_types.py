from enum import Enum

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

                 # two char tokens
                 "DOUBLE_SLASH",
                 "SLASH_STAR",
                 "STAR_SLASH",
                 "DOUBLE_DOT"

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