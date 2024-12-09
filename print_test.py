from src.grammar import *
from src.token_types import *
from src.ast_printer import AST_Printer

def main():
    chip = Chip_Spec(Token(TokenType.CHIP, "CHIP", None, 1),
                     Token(TokenType.IDENTIFIER, "Foo", None, 1),
                     Token(TokenType.LEFT_BRACE, "{", None, 1),
                     Header(
                        Token(TokenType.IN, "IN", None, 2),
                        Chip_IO(Token(TokenType.IDENTIFIER, "in1", None, 2), 
                                [
                                    Extra_IO(Token(TokenType.COMMA, ",", None, 2), Token(TokenType.IDENTIFIER, "in2", None, 2))
                                ]),
                        Token(TokenType.SEMICOLON, ";", None, 2),
                        Token(TokenType.OUT, "OUT", None, 3),
                        Chip_IO(Token(TokenType.IDENTIFIER, "out", None, 3), []),
                        Token(TokenType.SEMICOLON, ";", None, 3),
                     ),
                     Body(
                         Token(TokenType.PARTS, "PARTS", None, 4),
                         Token(TokenType.COLON, ":", None, 4),
                         [
                             Part(
                                 Token(TokenType.IDENTIFIER, "Not", None, 5),
                                 Token(TokenType.LEFT_PAREN, "(", None, 5),
                                 Connections_List(
                                    Connection(
                                         Token(TokenType.IDENTIFIER, "a", None, 5),
                                         Token(TokenType.EQUAL, "=", None, 5),
                                         Token(TokenType.IDENTIFIER, "in", None, 5)
                                    ),
                                    Token(TokenType.COMMA, ",", None, 5),
                                    Connection(
                                         Token(TokenType.IDENTIFIER, "out", None, 5),
                                         Token(TokenType.EQUAL, "=", None, 5),
                                         Token(TokenType.IDENTIFIER, "out", None, 5)
                                    ),
                                    []
                                 ),
                                 Token(TokenType.RIGHT_PAREN, ")", None, 5),
                                 Token(TokenType.SEMICOLON, ";", None, 5)
                             )
                         ]
                     ),
                     Token(TokenType.RIGHT_BRACE, "}", None, 6))
                            

    print(AST_Printer().print(chip))

main()