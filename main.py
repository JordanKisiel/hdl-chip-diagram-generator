import sys
from src.lexer import Lexer
from src.parser import Parser
from src.grammar import *
from src.ast_printer import *
from src.hdl_error import HDLError
from src.chip_diagram import Chip_Diagram
from src.grid import Grid

def main():
    # incorrect number of args
    # must equal 3 because first arg is always the name of this script
    if len(sys.argv) != 3:
        print("Must provide source and destination files. Usage: python3 main.py <hdl source> <python dest>")
        sys.exit(64)
    else:
        compile_to_python(sys.argv[1], sys.argv[2])


def compile_to_python(source_path, dest_filename):
    with open(source_path, 'r') as source_file:
        source = source_file.read()
        generated_python = compile_file(source)
    with open(f"compiled_files/{dest_filename}", "w") as dest_file:
        dest_file.write(generated_python)


def compile_file(source_text):
    lexer = Lexer(source_text)
    tokens = lexer.scan_tokens()
    parser = Parser(tokens)
    chip = parser.parse()
    printed_chip = AST_Printer().print(chip)

    grid = Grid(800, 600, 30, 30)
    chip_diagram = Chip_Diagram(chip, grid)
    chip_diagram.draw()
    chip_diagram.write()


    # if there was an error, don't compile the file
    if HDLError.had_error:
        sys.exit(65)

    return printed_chip


if __name__ == "__main__":
    main()