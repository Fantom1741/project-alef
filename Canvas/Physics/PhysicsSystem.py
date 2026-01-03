from Canvas.Physics.ClusterSystem import ClusterSystem
from Canvas.Physics.CollisionSystem import CollisionSystem
from Canvas.Physics.GravitySystem import GravitySystem

from Canvas.SpaceObject import SpaceObject

class PhysicsSystem:
    def __init__(self, cellSize:int):
        self._clusterSystem = ClusterSystem(cellSize)
        self._gravitySystem = GravitySystem()
        self._collisionSystem = CollisionSystem()

        self._spaceObjects = []

        self._objectsToRemove = []

    @property
    def spaceObjects(self):
        return self._spaceObjects
    
    def AddObjects(self, spaceObjects):
        for spaceObjects in spaceObjects:
            self.AddObject(spaceObjects)
        
    def AddObject(self, spaceObject:SpaceObject):
        if spaceObject not in self._spaceObjects:
            self._spaceObjects.append(spaceObject)

    def AddMassiveObject(self, spaceObject:SpaceObject):
        self.AddObject(spaceObject)
        if spaceObject not in self._gravitySystem.massiveObjects:
            self._gravitySystem.AddMassiveObject(spaceObject)

    def Update(self, totalTime:int):
        self._objectsToRemove.clear()
        
        self._clusterSystem.BuildGrid(self._spaceObjects)

        processedPairs = set()

        for _ in range(totalTime):
            for spaceObject in self._spaceObjects:
                if spaceObject in self._objectsToRemove:
                    continue

                for massiveObject in self._gravitySystem.massiveObjects:
                    if spaceObject == massiveObject:
                        continue

                    self._gravitySystem.ApplyForce(spaceObject, massiveObject)
                
                neighbors = self._clusterSystem.GetNeighbors(spaceObject)
                for neighbor in neighbors:
                    if spaceObject == neighbor:
                        continue

                    if neighbor in self._objectsToRemove:
                        continue

                    pairID = tuple(sorted((id(spaceObject), id(neighbor))))
                    if pairID in processedPairs:
                        continue

                    if neighbor not in self._gravitySystem.massiveObjects:
                        self._gravitySystem.ApplyForce(spaceObject, neighbor)
                        self._gravitySystem.ApplyForce(neighbor, spaceObject)
                    
                    if self._collisionSystem.CheckCollision(spaceObject, neighbor):
                        if spaceObject.mass > neighbor.mass * 2:
                            spaceObject.Grow(neighbor.mass / 2)

                            self._objectsToRemove.append(neighbor)
                        elif spaceObject.mass * 2 < neighbor.mass:
                            neighbor.Grow(spaceObject.mass / 2)

                            self._objectsToRemove.append(spaceObject)
                        else:
                            neighbor.Decrease(neighbor.mass / 1.5)
                            spaceObject.Decrease(spaceObject.mass / 1.5)

                            if neighbor.mass <= 0:
                                self._objectsToRemove.append(neighbor)
                            if spaceObject.mass <= 0:
                                self._objectsToRemove.append(spaceObject)

                    processedPairs.add(pairID)

        for spaceObject in self._objectsToRemove:
            if spaceObject in self._spaceObjects:
                if spaceObject in self._gravitySystem.massiveObjects:
                    self._gravitySystem.RemoveMassiveObject(spaceObject)
                self._spaceObjects.remove(spaceObject)
                spaceObject.Destroy()

        for spaceObject in self._spaceObjects:
            spaceObject.UpdatePosition(1)

        
        for spaceObject in self._spaceObjects:
            spaceObject.UpdateDraw()