import sys
from src.lexer import Lexer
from src.parser import Parser
from src.grammar import *
from src.ast_printer import *
from src.hdl_error import HDLError
from src.chip_diagramer import Chip_Diagramer
from src.diagram import Diagram
from src.grid import Grid
from src.chip_loader import Chip_Loader

def main():
    # incorrect number of args
    # must equal 3 because first arg is always the name of this script
    if len(sys.argv) != 3:
        print("Must provide source and destination files. Usage: python3 main.py <hdl source> <python dest>")
        sys.exit(64)
    else:
        compile(sys.argv[1], sys.argv[2])


def compile(source_path, dest_filename):
    chip_loader = Chip_Loader()
    chip = chip_loader.load_chip(source_path)
    chip_loader.load_primitives("src/primitive_chips")
    generated_hdl = AST_Printer().print(chip)

    # if there was an error, don't compile the file
    if HDLError.had_error:
        sys.exit(65)   

    diagram(chip, chip_loader.primitives)
    with open(f"compiled_files/{dest_filename}", "w") as dest_file:
        dest_file.write(generated_hdl)


def diagram(chip, primitive_chips):
    grid = Grid(800, 600, 30, 30)
    diagram = Diagram(grid)
 
    chip_diagramer = Chip_Diagramer(chip, diagram, primitive_chips)
    chip_diagramer.draw()
    chip_diagramer.write()


if __name__ == "__main__":
    main()