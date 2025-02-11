from src.diagram.diagrammables.diagrammable import Diagrammable
from src.diagram.bounds import Bounds

class Grid(Diagrammable):
    def __init__(self, 
                 width, 
                 height, 
                 x_divisions, 
                 y_divisions):
        self.width = width
        self.height = height
        self.bounds = Bounds(0, 0, height, width)
        self.x_divisions = x_divisions
        self.y_divisions = y_divisions
        self.column_width = self.width / x_divisions
        self.row_height = self.height / y_divisions
        self.color = (255, 220, 220)
        self._on_grid_threshold = 1
        self.grid = self._construct_grid()
        assert(width > 0)
        assert(height > 0)
        assert(x_divisions > 0)
        assert(y_divisions > 0)

    def _construct_grid(self):
        grid = []
        for i in range(self.x_divisions + 1):
            row = []
            for j in range(self.y_divisions + 1):
               x_value = self.column_width * i + self.bounds.left
               y_value = self.row_height * j + self.bounds.top
               row.append((x_value, y_value))
            grid.append(row)

        return grid
    
    def div_x(self, div):
        assert(div >= 0)
        assert(div <= self.x_divisions)

        return self.grid[div][0][0]

    def div_y(self, div):
        assert(div >= 0)
        assert(div <= self.y_divisions)

        return self.grid[0][div][1]

    def get(self, x_coord, y_coord):
        assert(x_coord >= 0)
        assert(y_coord >= 0)
        assert(x_coord <= self.x_divisions)
        assert(y_coord <= self.y_divisions)

        return self.grid[x_coord][y_coord]
    
    def snap_x(self, point, to_left=True):
        assert(self.bounds.is_inside(point))

        x_value = point[0]
        snapped_x = x_value - (x_value % self.column_width)

        if snapped_x == x_value:
            return point

        if to_left:
            return (snapped_x, point[1])
        else:
            return (snapped_x + self.column_width, point[1]) 

    def snap_y(self, point, to_up=True):
        assert(self.bounds.is_inside(point))

        y_value = point[1]
        snapped_y = y_value - (y_value % self.row_height)

        if snapped_y == y_value:
            return point

        if to_up:
            return (point[0], snapped_y)
        else:
            return (point[0], snapped_y + self.row_height)
        
    def snap(self, point, to_left=True, to_up=True):
        assert(self.bounds.is_inside(point))

        snapped_point = self.snap_x(point, to_left)
        snapped_point = self.snap_y(snapped_point, to_up)

        return snapped_point
    
    def is_on_grid_x(self, point):
        assert(self.bounds.is_inside(point))

        for row in self.grid:
            x_range = (row[0][0] - self._on_grid_threshold,
                       row[0][0] + self._on_grid_threshold)
            in_x_range = (point[0] >= x_range[0] and 
                          point[0] <= x_range[1])
            if in_x_range:
                return True

        return False

    def is_on_grid_y(self, point):
        assert(self.bounds.is_inside(point))

        for row_point in self.grid[0]:
            y_range = (row_point[1] - self._on_grid_threshold,
                       row_point[1] + self._on_grid_threshold)
            in_y_range = (point[1] >= y_range[0] and 
                          point[1] <= y_range[1])
            if in_y_range:
                return True

        return False   
    
    def is_grid_point(self, point):
        assert(self.bounds.is_inside(point))

        return (self.is_on_grid_x(point) and
                 self.is_on_grid_y(point))
    
    def get_neighbors(self, point):
        assert(self.bounds.is_inside(point))

        neighbors = []

        if self.is_grid_point(point):
            neighbors.append((point[0] - self.column_width, point[1]))
            neighbors.append((point[0] + self.column_width, point[1]))
            neighbors.append((point[0], point[1] - self.row_height))
            neighbors.append((point[0], point[1] + self.row_height))

        else:
            if self.is_on_grid_x(point):
                neighbors.append(self.snap_y(point, to_up=True))
                neighbors.append(self.snap_y(point, to_up=False))
            if self.is_on_grid_y(point):
                neighbors.append(self.snap_x(point, to_left=True))
                neighbors.append(self.snap_x(point, to_left=False))

        neighbors = list(filter(lambda x: self.bounds.is_inside(x), 
                                neighbors))
            
        return neighbors

    def layout(self, bounds):
        self.bounds = bounds
        self.width = bounds.width
        self.height = bounds.height
        self.column_width = self.width / self.x_divisions
        self.row_height = self.height / self.y_divisions

        self.grid = self._construct_grid()

    def draw(self, canvas):
        context = canvas.context

        # draw horizontal lines
        for n in range(0, self.y_divisions + 1):
            y_value = self.grid[0][n][1]
            context.line([(self.bounds.left, y_value),
                          (self.bounds.right, y_value)],
                          self.color,
                          width=2)

        # draw vertical lines
        for n in range(0, self.x_divisions + 1):
            x_value = self.grid[n][0][0]
            context.line([(x_value, self.bounds.top),
                          (x_value, self.bounds.bottom)],
                          self.color,
                          width=2)