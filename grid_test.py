# TODO:
# -before moving forward on grid, test out grid_new code
# with canvas to draw it out

from src.diagram.grid_new import *
from src.diagram.canvas_new import *

def main():
   canvas = Canvas(1024, 768) 
   grid = Grid(800, 600, 32, 2)
   grid.draw(canvas, (200, 0))
   canvas.save("grid_test.png")

main()