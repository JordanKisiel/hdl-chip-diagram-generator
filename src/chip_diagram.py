from PIL import Image, ImageDraw, ImageFont
from src.grid import Grid
from src.grammar import Vistor

class Chip_Diagram(Vistor):
    def __init__(self,
                 chip_spec,
                 grid=Grid(800, 600, 12, 12),
                 style={
                     "bg": (255, 255, 255),
                     "fg": (0, 0, 0),
                     "font": "FreeMono.ttf",
                     "base_font_size": 30
                 }):
        self.chip_spec = chip_spec 
        self.grid = grid
        self.style = style 
        self.out = Image.new("RGB", (self.grid.width, self.grid.height), self.style["bg"])
        self.draw_context = ImageDraw.Draw(self.out)
        self.chip_font = ImageFont.truetype(self.style["font"], 
                                            self.style["base_font_size"])
        self.chip_io_font = ImageFont.truetype(self.style["font"],
                                               self.style["base_font_size"] * 0.67)
        self.part_font = ImageFont.truetype(self.style["font"],
                                            self.style["base_font_size"] * 0.67)
        self.part_io_font = ImageFont.truetype(self.style["font"],
                                               self.style["base_font_size"] * 0.5)
        
        
    def write(self):
        self.out.save(f"{self.chip_spec.ident_token.lexeme}_diagram.png")

    def draw(self):
        self.grid.draw(self.draw_context)
        self.visit_chip_spec(self.chip_spec)

    def visit_chip_spec(self, rule):
        self.draw_context.text((self.grid.center_x(), self.grid.y(1)),
                               rule.ident_token.lexeme,
                               self.style["fg"],
                               self.chip_font,
                               anchor="mt")

    def visit_header(self, rule):
        # TODO: continue from here by drawing chip outline?
        pass

    def visit_chip_io(self, rule):
        pass

    def visit_extra_io(self, rule):
        pass

    def visit_bus(self, rule):
        pass

    def visit_body(self, rule):
        pass

    def visit_part(self, rule):
        pass

    def visit_connections_list(self, rule):
        pass

    def visit_connection(self, rule):
        pass

    def visit_extra_connection(self, rule):
        pass

    def visit_sub_bus(self, rule):
        pass

    def visit_range(self, rule):
        pass
