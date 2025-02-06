# TODO:
# -before moving forward on grid, test out grid_new code
# with canvas to draw it out
from src.diagram.diagrammables import Grid
from src.diagram.bounds import *
from src.diagram.canvas_new import *

def main():
   canvas = Canvas(1024, 768) 
   grid = Grid(800, 600, 5, 2)
   grid.layout(Bounds(30, 0, 400, 300))
   grid.draw(canvas)
   grid.layout(Bounds(200, 400, 400, 600))
   grid.draw(canvas)
   canvas.save("grid_test.png")


main()