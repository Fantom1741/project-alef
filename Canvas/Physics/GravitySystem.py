from Canvas.SpaceObject import SpaceObject

class GravitySystem:
    Gravity = 0.1
    Softening = 10
    def __init__(self):
        self._massiveObjects = []

    @property
    def massiveObjects(self):
        return self._massiveObjects
        
    def AddMassiveObject(self, spaceObject:SpaceObject):
        if spaceObject not in self._massiveObjects:
            self._massiveObjects.append(spaceObject)

    def RemoveMassiveObject(self, spaceObject:SpaceObject):
        if spaceObject in self._massiveObjects:
            self._massiveObjects.remove(spaceObject)

    def ApplyForce(self, spaceSubject, otherSpaceObject):
        if spaceSubject == otherSpaceObject:
            return
        
        differential = otherSpaceObject.position - spaceSubject.position
        distance = differential.length()
        
        if distance < max(spaceSubject.size, otherSpaceObject.size) * 2:
            distance = max(spaceSubject.size, otherSpaceObject.size) * 2
        
        acceleration_magnitude = self.Gravity * otherSpaceObject.mass / (distance**2 + self.Softening)

        acceleration = differential.normalize() * acceleration_magnitude
        spaceSubject.AddVelocity(acceleration.x, acceleration.y)