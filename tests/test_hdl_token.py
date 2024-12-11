import unittest
from src.hdl_token import Token
from src.token_types import TokenType 

class TestToken(unittest.TestCase):
    def test_to_string(self):
        token = Token(TokenType.LEFT_BRACE, "{", "{", 10)

        self.assertEqual(
            "TokenType.LEFT_BRACE { {",
            str(token)
        )
    
