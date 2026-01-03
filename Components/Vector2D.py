import math

class Vector2D:
    def __init__(self, x:float, y:float):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    def __add__(self, otherVector2D):
        return Vector2D(self.x + otherVector2D.x, self.y + otherVector2D.y)
    
    def __sub__(self, otherVector2D):
        return Vector2D(self.x - otherVector2D.x, self.y - otherVector2D.y)
    
    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        if scalar == 0:
            raise ValueError("Деление на НУЛЬ невозможно!")
        return Vector2D(self.x / scalar, self.y / scalar)
    
    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self):
        length = self.length()
        if length == 0:
            return Vector2D(0, 0)
        return self / length