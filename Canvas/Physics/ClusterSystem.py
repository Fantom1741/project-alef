from collections import defaultdict

from Components.Vector2D import Vector2D

from Canvas.SpaceObject import SpaceObject

class ClusterSystem:
    def __init__(self, cellSize:int):
        self._cellSize = cellSize
        self._grid = defaultdict(list)
    
    def BuildGrid(self, spaceObjects):
        self._grid.clear()

        for spaceObject in spaceObjects:
            self._grid[self.GetCellCoords(spaceObject.position)].append(spaceObject)

    def GetCellCoords(self, position:Vector2D):
        return (int(position.x // self._cellSize),int(position.y // self._cellSize))
    
    def GetNeighbors(self, spaceObject:SpaceObject):
        x, y = self.GetCellCoords(spaceObject.position)
        neighbors = []

        for deltaX in [-1, 0, 1]:
            for deltaY in [-1, 0, 1]:
                neighborKey = (x + deltaX, y + deltaY)

                if neighborKey in self._grid:
                    neighbors.extend(self._grid[neighborKey])
                    
        return neighbors