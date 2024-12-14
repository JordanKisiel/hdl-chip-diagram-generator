import sys, os
sys.path.append(os.path.abspath(os.path.join(".")))

from src.lexer import Lexer
from src.parser import Parser

from src.chip_diagram import Chip_Diagram
from src.grid import Grid

grid = Grid(800, 600, 12, 12)

chip_diagram = Chip_Diagram()


