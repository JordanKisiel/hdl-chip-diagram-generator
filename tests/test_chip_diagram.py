import sys, os
sys.path.append(os.path.abspath(os.path.join(".")))

from src.chip_diagram import Chip_Diagram


chip_diagram = Chip_Diagram(chip_name="Foo")

chip_diagram.draw_grid()

chip_diagram.write()

