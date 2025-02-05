from src.diagram.bounds import *
import math

class Grid:
    def __init__(self, width, height, divisions_x, divisions_y):
        self.width = width
        self.height = height
        self.bounds = Bounds(0, 0, height, width)
        self.divisions_x = divisions_x
        self.divisions_y = divisions_y
        self.column_width = self.width / divisions_y
        self.row_height = self.height / divisions_x
        self.color = (255, 220, 220)
        self.on_grid_threshold = 0.001

    def x(self, division_x):
        if division_x < 0:
            division_x += self.divisions_x
        return self.width / self.divisions_x * division_x

    def y(self, division_y):
        if division_y < 0:
            division_y += self.divisions_y
        return self.height / self.divisions_y * division_y

    def point(self, division_x, division_y):
        return (self.x(division_x), self.y(division_y))
    
    def center_x(self):
        return self.width / 2
    
    def center_y(self):
        return self.height / 2
    
    def center(self):
        return (self.center_x(), self.center_y()) 
    
    def is_grid_point(self, point):
        return (self.is_on_grid_x(point) and 
                self.is_on_grid_y(point))
    
    def is_on_grid_x(self, point):
        fractional, _ = math.modf(point[0] / self.column_width)
        is_x_on_grid = (fractional < self.on_grid_threshold or
                        1 - fractional < self.on_grid_threshold)

        return is_x_on_grid

    def is_on_grid_y(self, point):
        fractional, _ = math.modf(point[1] / self.row_height)
        is_y_on_grid = (fractional < self.on_grid_threshold or
                        1 - fractional < self.on_grid_threshold)
        
        return is_y_on_grid
    
    def get_closest_on_grid_x(self, point, to_left=True):
        x = point[0]
        fractional, _ = math.modf(x / self.column_width)

        if to_left:
            if fractional > self.on_grid_threshold:
                x = x - ((x % self.column_width))
            else:
                x = x - self.column_width
        else:
            if fractional > self.on_grid_threshold:
                x = (x + (self.column_width - 
                          (x % self.column_width)))
            else:
                x = x + self.column_width

        return (x, point[1])
    
    def get_closest_on_grid_y(self, point, to_up=True):
        y = point[1]
        fractional, _ = math.modf(y / self.row_height)

        if to_up:
            if fractional > self.on_grid_threshold:
                y = y - ((y % self.row_height))
            else:
                y = y - self.row_height
        else:
            if fractional > self.on_grid_threshold:
                y = (y + (self.row_height - 
                          (y % self.row_height)))
            else:
                y = y + self.row_height

        return (point[0], y)

    def get_grid_neighbors(self, point):
        neighbors = []

        # look left and right
        if self.is_on_grid_x(point):
            x_left = point[0] - self.column_width
            x_right = point[0] + self.column_width

            if self.bounds.is_inside_x((x_left, point[1])):
                neighbors.append((x_left, point[1]))
            if self.bounds.is_inside_x((x_right, point[1])):
                neighbors.append((x_right, point[1]))

        # look top and bottom
        if self.is_on_grid_y(point):
            y_top = point[1] - self.row_height
            y_bottom = point[1] + self.row_height

            if self.bounds.is_inside_y((point[0], y_top)):
                neighbors.append((point[0], y_top))
            if self.bounds.is_inside_y((point[0], y_bottom)):
                neighbors.append((point[0], y_bottom))  
    
        return neighbors
    