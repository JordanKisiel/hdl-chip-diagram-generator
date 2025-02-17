import sys
from src.parsers.grammar import *
from src.visitors.ast_printer import *
from src.hdl_error import HDLError
from src.diagram.chip_diagram import *
from src.visitors.chip_data import Chip_Data
from src.diagram.canvas import Canvas
from src.chip_loader import Chip_Loader

def main():
    # incorrect number of args
    # must equal 3 because first arg is always the name of this script
    if len(sys.argv) != 3:
        print("Must provide source and destination files. Usage: python3 main.py <hdl source> <hdl dest>")
        sys.exit(64)
    else:
        compile(sys.argv[1], sys.argv[2])


def compile(source_path, dest_filename):
    chip_loader = Chip_Loader()
    chip = chip_loader.load_chip(source_path)
    chip_loader.load_chip_folder("src/chip_defs/primitive", is_primitives=True)
    chip_loader.load_chip_folder("src/chip_defs/custom", is_primitives=False)
    generated_hdl = AST_Printer().print(chip)

    # if there was an error, don't do anything
    # except report errors 
    if HDLError.had_error:
        sys.exit(65)   

    diagram(chip, chip_loader.primitives, chip_loader.chips)
    # write out what should be the original hdl code
    # to help with debugging
    with open(f"compiled_files/{dest_filename}", "w") as dest_file:
        dest_file.write(generated_hdl)


def diagram(chip, primitive_chips, custom_chips):
    canvas = Canvas(800, 600)
    canvas.set_style({
        "bg": (50,50,50),
        "fg": (220, 220, 220)
        })
    chip_data = Chip_Data(primitive_chips, custom_chips)
    chip_diagram = Chip_Diagram(canvas, chip_data)
    chip_diagram.diagram(chip)

    chip_diagram.write()


if __name__ == "__main__":
    main()