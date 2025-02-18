from PIL import Image, ImageDraw, ImageFont
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
                     "min_font_size": 5,
                     "max_font_size": 32,
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

   def set_style(self, style):
      self.style = {
         **self.style,
         **style
      }

      self.out = Image.new("RGB",
                           (self.width, self.height),
                           self.style["bg"])
      
      self.context = ImageDraw.Draw(self.out)

   def get_style(self):
      return self.style

   def path(self, path, color=None, stroke_width=None):
      if color == None:
         color = self.style["fg"]
      if stroke_width == None:
         stroke_width = self.style["stroke_width"]
      # TODO: also look into giving this rounded corners?
      self.context.line(path, color, stroke_width)
      
   def line(self, points, color=None, stroke_width=None):
      if color == None:
         color = self.style["fg"]
      if stroke_width == None:
         stroke_width = self.style["stroke_width"]

      self.context.line(points, color, stroke_width) 

   def text(self, position, text, color=None, font_size=None):
      if color == None:
         color = self.style["fg"]
      if font_size == None:
         font_size = self.style["base_font_size"]

      if font_size < self.style["min_font_size"]:
         # TODO:
         # consider having the display of these warning messages being
         # delegated to the warning class
         warning_message = (f"Warning: text '{text}' could not be drawn due "
                             "to font size being below the minimum font size "
                            f"of {self.style['min_font_size']}")
         print(warning_message)
         return
      if font_size > self.style["max_font_size"]:
         warning_message = f'''Warning: text {text} drawn at 
                               {self.style["max_font_size"]} due to given size
                               exceeding max.'''
         print(warning_message)

      font = ImageFont.truetype(self.style["font"], font_size)
      
      self.context.text(position, text, color, font, anchor="mt")

   def rectangle(self, 
                 bounds, 
                 radius=0, 
                 color=None, 
                 stroke_width=None):
      if radius != 0:
         radius = self.style["box_radius_factor"] * radius
      if color == None:
         color = self.style["fg"]
      if stroke_width == None:
         stroke_width = self.style["stroke_width"]

      self.context.rounded_rectangle(bounds,
                                     radius,
                                     fill=None,
                                     outline=color,
                                     width=stroke_width)

   def save(self, file_name):
      self.out.save(file_name)