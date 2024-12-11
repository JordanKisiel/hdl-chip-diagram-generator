from PIL import Image, ImageDraw, ImageFont

class Chip_Diagram:
    def __init__(self,
                 chip_name="Chip",
                 width=800, 
                 height=600, 
                 bg=(255, 255, 255), 
                 fg=(0, 0, 0), 
                 font_path="FreeMono.ttf",
                 base_font_size=30,
                 grid_size=12):
        self.chip_name = chip_name
        self.width = width
        self.height = height
        self.bg = bg
        self.fg = fg
        self.font_path = font_path 
        self.base_font_size = base_font_size
        self.grid_size = grid_size
        self.out = Image.new("RGB", (width, height), bg)
        self.draw_context = ImageDraw.Draw(self.out)
        self.chip_font = ImageFont.truetype(font_path, 
                                            self.base_font_size)
        self.chip_io_font = ImageFont.truetype(font_path,
                                               base_font_size * 0.67)
        self.part_font = ImageFont.truetype(font_path,
                                            base_font_size * 0.67)
        self.part_io_font = ImageFont.truetype(font_path,
                                               base_font_size * 0.5)
        
        
    def write(self):
        self.out.save(f"{self.chip_name}_diagram.png")

    def _grid(self, x, y):
        if x > self.grid_size or y > self.grid_size:
            raise Exception(f"divisions cannot exceed grid size of: {self.grid_size}")
        return (self.width / self.grid_size * x, self.height / self.grid_size * y)
    
    def draw_grid(self):
        # draw horizontal lines
        for n in range(1, self.grid_size):
            self.draw_context.line([(0, self.height / self.grid_size * n), 
                                    (self.width, self.height / self.grid_size * n)], 
                                    (255, 220, 220),
                                    width=2)
        # draw vertical lines
        for n in range(1, self.grid_size):
            self.draw_context.line([(self.width / self.grid_size * n, 0), 
                                    (self.width / self.grid_size * n, self.height)], 
                                    (255, 220, 220), 
                                    width=2)