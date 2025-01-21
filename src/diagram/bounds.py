class Bounds:
    def __init__(self, top, left, bottom, right):
        self.left= left 
        self.top= top 
        self.right = right 
        self.bottom = bottom
        self.width = self.right - self.left
        self.height = self.bottom- self.top
        self.center_x = self.width / 2 + self.left
        self.center_y = self.height / 2 + self.top
        self.center = (self.center_x, self.center_y)
        self.min_dimension = min(self.width, self.height)
        self.top_left = (self.left, self.top)
        self.bottom_left = (self.left, self.bottom)
        self.top_right= (self.right, self.top)
        self.bottom_right= (self.right, self.bottom)
        self.full_bounds = [self.top_left, self.bottom_right]
        if self.top > self.bottom:
            raise Exception("Top edge of boundary cannot be below bottom edge.")
        if self.left > self.right:
            raise Exception("Left edge of boundary cannot be to the right of the right edge.")
        
    def draw(self, canvas):
        style = canvas.style
        context = canvas.context

        context.rectangle(self.full_bounds,
                          fill=None,
                          outline=style["fg"],
                          width=style["stroke_width"])