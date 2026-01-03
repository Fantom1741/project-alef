class CollisionSystem:
    def CheckCollision(self, spaceSubject, otherSpaceObject):
        if spaceSubject == otherSpaceObject:
            return False
        
        distance = (spaceSubject.position - otherSpaceObject.position).length()
        
        if distance < (spaceSubject.size + otherSpaceObject.size):
            return True
        return False