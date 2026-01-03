from enum import Enum
from tkinter import *

from Components.Vector2D import Vector2D

class Shape(Enum):
    Square      = 1
    Rhomb       = 2
    Circle      = 3
    Triangle    = 4
    TriangleDown= 5

class SpaceObject:
    def __init__(self, canvas:Canvas, position:Vector2D, velocity:Vector2D, mass:float, size:float, shape:Shape, color:StringVar):
        self._position = position

        self._velocity = velocity

        self._mass = mass
        self._size = size

        self._shape = shape
        self._color = color
        
        self._canvas = canvas
        self._canvasId = self.CreateShapeOnCanvas()

        self._trail = Trail(canvas, self._canvasId, color)
        
    @property
    def position(self):
        return self._position
    @property
    def velocity(self):
        return self._velocity
    @property
    def mass(self):
        return self._mass
    @property
    def size(self):
        return self._size
    @property
    def shape(self):
        return self._shape
    @property
    def density(self):
        return self._mass / self._size
        
    def GetPoints(self):
        if self._shape == Shape.Square:
            x1 = self._position.x-self._size
            y1 = self._position.y-self._size
            
            x2 = self._position.x+self._size
            y2 = self._position.y+self._size
            
            return [x1, y1, x2, y2]
        elif self._shape == Shape.Rhomb:
            x1 = self._position.x
            y1 = self._position.y-self._size
            
            x2 = self._position.x+self._size
            y2 = self._position.y
            
            x3 = self._position.x
            y3 = self._position.y+self._size
            
            x4 = self._position.x-self._size
            y4 = self._position.y
            
            return [x1, y1, x2, y2, x3, y3, x4, y4]
        elif self._shape == Shape.Circle:
            x1 = self._position.x-self._size
            y1 = self._position.y-self._size
            
            x2 = self._position.x+self._size
            y2 = self._position.y+self._size
            
            return [x1, y1, x2, y2]
        elif self._shape == Shape.Triangle:
            x1 = self._position.x
            y1 = self._position.y-self._size
            
            x2 = self._position.x+self._size
            y2 = self._position.y+self._size
            
            x3 = self._position.x-self._size
            y3 = self._position.y+self._size
            
            return [x1, y1, x2, y2, x3, y3]
        elif self._shape == Shape.TriangleDown:
            x1 = self._position.x-self._size
            y1 = self._position.y-self._size
            
            x2 = self._position.x+self._size
            y2 = self._position.y-self._size
            
            x3 = self._position.x
            y3 = self._position.y+self._size
            
            return [x1, y1, x2, y2, x3, y3]
        else:
            x1 = self._position.x-self._size
            y1 = self._position.y+self._size
            
            x2 = self._position.x+self._size
            y2 = self._position.y-self._size
            
            x3 = self._position.x+self._size
            y3 = self._position.y+self._size
            
            return [x1, y1, x2, y2, x3, y3]

    def Grow(self, value):
        if value <= 0:
            return
        self._mass += value
        self._size += (value ** 0.3) * 0.6

    def Decrease(self, value):
        if value <= 0:
            return
        self._mass -= value
        self._size -= (value ** 0.3) * 0.6

    def CreateShapeOnCanvas(self):
        if self._shape == Shape.Square:
            return self._canvas.create_rectangle(*self.GetPoints(), fill=self._color)
        elif self._shape == Shape.Circle:
            return self._canvas.create_oval(*self.GetPoints(), fill=self._color)
        else:
            return self._canvas.create_polygon(*self.GetPoints(), fill=self._color)
        

    def AddVelocity(self, velocityX, velocityY):
        self._velocity += Vector2D(velocityX, velocityY)
        
    def UpdatePosition(self, deltaTime:int):
        if deltaTime < 1:
            deltaTime = 1

        self._position += self._velocity * deltaTime

    def UpdateDraw(self):
        self._canvas.coords(self._canvasId, *self.GetPoints())

        if self._trail is not None:
            self._trail.UpdateDraw(self._position)

    def Destroy(self):
        self._canvas.delete(self._canvasId)

        if self._trail is not None:
            self._trail.Destroy()

class Trail:
    def __init__(self, canvas, parentID, color):
        self._trail = []
        self._maxTrailLength = 500

        self._canvas = canvas
        self._canvasID = None

        self._parentID = parentID

        self._color = color

    def Destroy(self):
        self._canvas.delete(self._canvasID)

    def UpdateDraw(self, position):
        self._trail.append(position.x)
        self._trail.append(position.y)

        if len(self._trail) > self._maxTrailLength * 2:
            self._trail.pop(0)
            self._trail.pop(0)

        if len(self._trail) > 4:
            if self._canvasID is not None:
                self._canvas.coords(self._canvasID, *self._trail)
                self._canvas.tag_lower(self._canvasID, self._parentID)
            else:
                self._canvasID = self._canvas.create_line(*self._trail, fill=self._color, width=1)