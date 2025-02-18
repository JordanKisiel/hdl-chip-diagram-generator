class Bounds:
    def __init__(self, top, left, bottom, right):
        self.left= left 
        self.top= top 
        self.right = right 
        self.bottom = bottom
        self._calculate_properties() 
        self._check_bounds() 
        
    def draw(self, canvas):
        canvas.rectangle(self.point_bounds)
        
    def expand(self, amount):
        self.left -= amount
        self.top -= amount
        self.right += amount
        self.bottom += amount
        self._calculate_properties()
        self._check_bounds()

    def is_inside(self, point):
        return (self.is_inside_x(point) and
                self.is_inside_y(point)) 
    
    def is_inside_x(self, point):
        is_inside_left = point[0] >= self.left
        is_inside_right = point[0] <= self.right

        return (is_inside_left and
                is_inside_right)

    def is_inside_y(self, point):
        is_inside_top = point[1] >= self.top
        is_inside_bottom = point[1] <= self.bottom

        return (is_inside_top and
                is_inside_bottom)

    def _calculate_properties(self):
        self.width = self.right - self.left
        self.height = self.bottom - self.top
        self.center_x = self.width / 2 + self.left
        self.center_y = self.height / 2 + self.top
        self.center = (self.center_x, self.center_y)
        self.min_dimension = min(self.width, self.height)
        self.top_left = (self.left, self.top)
        self.bottom_left = (self.left, self.bottom)
        self.top_right= (self.right, self.top)
        self.bottom_right= (self.right, self.bottom)
        self.point_bounds = [self.top_left, self.bottom_right]

    def _check_bounds(self):
        # TODO:
        # the display of this error should probably be delegated to
        # an error class
        if self.top > self.bottom:
            error_message = (
                f"Top edge (top: {self.top}) of boundary cannot be below "
                f"bottom edge (bottom: {self.bottom})."
            )
            raise Exception(error_message)
        if self.left > self.right:
            error_message = (
                f"Left edge (left: {self.left}) of boundary cannot be to "
                f"to the right of the right edge (right: {self.right})."
            )
            raise Exception(error_message)