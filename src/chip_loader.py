import os
from src.lexer.lexer import *
from src.parsers.parser import *
from src.parsers.primitive_parser import *
from src.lexer.token_types import *

class Chip_Loader:
    def __init__(self):
        self.chips = {}
        self.primitives = {}

    def load_chip(self, file_path):
        file_name = file_path.split('/')[-1]
        chip_name = file_name.split('.')[0]
        with open(file_path, 'r') as chip_source:
            chip = self.source_to_chip(chip_source) 
            self.chips[chip_name] = chip
            return chip 

    def load_chips(self, file_paths):
        for file_path in file_paths:
            self.load_chip(file_path)

    def load_chip_folder(self, chips_file_path, is_primitives=False):
        # load in every file ending with .hdl in
        # the provided file path 
        listing = os.listdir(chips_file_path)
        for file in listing:
            extension = file.split('.')[1]
            is_hdl = extension == "hdl"
            file_path = f"{chips_file_path}/{file}"
            if os.path.isfile(file_path) and is_hdl:
                chip_name = file.split('.')[0]
                with open(file_path, 'r') as chip_source:
                    chip = None
                    if is_primitives:
                        chip = self.source_to_primitive(chip_source)
                        self.primitives[chip_name] = chip
                    else:
                        chip = self.source_to_chip(chip_source)
                        self.chips[chip_name] = chip

    def source_to_chip(self, chip_source):
        source = chip_source.read()
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        parser = Parser(tokens)
        chip = parser.parse()
        return chip

    def source_to_primitive(self, chip_source):
        source = chip_source.read()
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        parser = Primitive_Parser(tokens)
        primitive = parser.parse()
        return primitive
        
        