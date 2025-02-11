from src.diagram.bounds import Bounds
from src.diagram.diagrammables.grid import Grid
from src.diagram.diagrammables.title import Title
from src.diagram.diagrammables.outline import Outline
from src.diagram.diagrammables.io import IO
from src.diagram.diagrammables.part import Part
from src.diagram.diagrammables.connection import Connection
from src.diagram.chip_layout import Chip_Layout

class Chip_Diagram:
    def __init__(self, canvas, chip_data):
        self.canvas = canvas
        self.grid = Grid(canvas.width, canvas.height, 32, 32)
        self.chip_data = chip_data
        self.title = None
        self.outline = None
        self.inputs = []
        self.outputs = []
        self.parts = []
        self.connections = []

        self.measurements = {
            "margin": 5,
            "title_margin": 2,
            "io_width": 3
        }

    def diagram(self, chip_ast):
        self.chip_data.get_data(chip_ast)
        self.generate()
        self.layout()
        self.draw()

    def generate(self):
        self.title = Title(self.chip_data.title_text)
        self.outline = Outline()
        self.inputs = [IO(input_name, connect_left=False) 
                       for input_name in self.chip_data.input_names]
        self.outputs = [IO(output_name, connect_left=True) 
                        for output_name in self.chip_data.output_names]
        self.parts = [Part(part["name"], 
                           part["id"], 
                           part["inputs"], 
                           part["outputs"]) 
                      for part in self.chip_data.parts_data]

        for connection in self.chip_data.connections_data:
            part = self._get_part_by_id(connection["part_id"])
            io_1 = self._get_part_io_by_name(part, connection["part_pin"])
            io_2 = None
            
            if connection["other_pin"] in self.chip_data.internal_wires:
                pin_data = self.chip_data.internal_wires[connection["other_pin"]]
                other_pin_part = self._get_part_by_id(pin_data["part_id"])
                io_2 = self._get_part_io_by_name(other_pin_part, pin_data["output_pin"]) 
            elif connection["other_pin"] in (self.chip_data.input_names + 
                                             self.chip_data.output_names):
                io_2 = self._get_chip_io_by_name(connection["other_pin"])

            # connection lines only draw correctly if drawn
            # left to right, so swap io objects if necessary
            if io_1.connect_left:
                temp = io_1
                io_1 = io_2
                io_2 = temp

            self.connections.append(Connection(io_1, io_2))


    def layout(self):
        assert(self.title != None)
        assert(self.outline != None)

        min_parts_margin = self.measurements["margin"] + 2
        dynamic_parts_margin = (self.measurements["margin"] + 
                                6 - 
                                len(self.parts))
        parts_margin = max(min_parts_margin, dynamic_parts_margin)
        
        self.title.layout(Bounds(self.grid.div_y(self.measurements["title_margin"]), 
                                 0, 
                                 self.canvas.height, 
                                 self.canvas.width))

        self.outline.layout(Bounds(self.grid.div_y(self.measurements["margin"]),
                                   self.grid.div_x(self.measurements["margin"]),
                                   self.grid.div_y(self.grid.y_divisions - 
                                               self.measurements["margin"]),
                                   self.grid.div_x(self.grid.x_divisions - 
                                               self.measurements["margin"])))

        # inputs
        Chip_Layout.distribute_io(Bounds(self.outline.bounds.top,
                                         self.outline.bounds.left -
                                          self.grid.div_x(self.measurements["io_width"]),
                                         self.outline.bounds.bottom,
                                         self.outline.bounds.left),
                                  self.inputs)
        # outputs
        Chip_Layout.distribute_io(Bounds(self.outline.bounds.top,
                                         self.outline.bounds.right,
                                         self.outline.bounds.bottom,
                                         self.outline.bounds.right + 
                                          self.grid.div_x(self.measurements["io_width"])),
                                  self.outputs)

        Chip_Layout.distribute_parts(Bounds(self.grid.div_y(parts_margin),
                                            self.grid.div_x(parts_margin),
                                            self.grid.div_y(self.grid.y_divisions - 
                                                            parts_margin),
                                            self.grid.div_x(self.grid.x_divisions - 
                                                            parts_margin)),
                                    self.parts,
                                    self.chip_data.connections_data,
                                    self.chip_data.internal_wires,
                                    self.grid.div_y(1),
                                    self.grid.div_x(1))
        
        Chip_Layout.distribute_connections(self.connections, self.grid) 


    def draw(self):
        self.grid.draw(self.canvas)
        
        self.title.draw(self.canvas)
        self.outline.draw(self.canvas)
        for input in self.inputs:
            input.draw(self.canvas)
        for output in self.outputs:
            output.draw(self.canvas)
        for part in self.parts:
            part.draw(self.canvas)
        for connection in self.connections:
            connection.draw(self.canvas)

    def write(self):
        assert(self.title != None)
        self.canvas.out.save(f"{self.chip_data.title_text}_Chip.png")

    def _get_chip_io_by_name(self, name):
        io_lst = self.inputs + self.outputs
        matching_io = filter(lambda x: x.name == name, io_lst)
        matching_io = list(matching_io)
        # asserting that io names should be unique
        # and that we're searching for name that should match something
        assert(len(matching_io) == 1)

        return matching_io[0]
    
    def _get_part_io_by_name(self, part, name):
        io_lst = part.inputs + part.outputs
        matching_io = filter(lambda x: x.name == name, io_lst)
        matching_io = list(matching_io)
        # asserting that io names should be unique
        # and that we're searching for name that should match something
        assert(len(matching_io) == 1)

        return matching_io[0] 
    
    def _get_part_by_id(self, id):
        matching_part = filter(lambda x: x.id == id, self.parts)
        matching_part = list(matching_part)

        # asserting that exactly 1 result
        # should be retrieved
        assert(len(matching_part) == 1)

        return matching_part[0]