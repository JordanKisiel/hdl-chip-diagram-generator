from src.diagram.diagrammables import Grid
from src.diagram.bounds import *
from src.diagram.canvas import *

def main():
   canvas = Canvas(1024, 768) 
   canvas.set_style({"bg": (45, 45, 45)})
   grid = Grid(800, 600, 16, 6)
   # grid.layout(Bounds(200, 400, 400, 600))
   grid.draw(canvas)
   canvas.save("grid_test.png")


main()