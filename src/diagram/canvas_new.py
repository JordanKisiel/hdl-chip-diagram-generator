from PIL import Image, ImageDraw
from src.diagram.bounds import *

class Canvas:
   def __init__(self,
                width,
                height,
                style={
                     "bg": (255, 255, 255),
                     "fg": (0, 0, 0),
                     "font": "FreeMono.ttf",
                     "base_font_size": 32,
                     "stroke_width": 2,
                     "box_radius_factor": 0.05
                }):
      self.width = width
      self.height = height
      self.bounds = Bounds(0, 0, height, width)
      self.style = style
      self.out = Image.new("RGB", 
                           (self.width, self.height),
                           self.style["bg"])
      self.context = ImageDraw.Draw(self.out)

   def save(self, file_name):
      self.out.save(file_name)