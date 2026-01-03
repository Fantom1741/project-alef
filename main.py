from tkinter import *

from Components.Vector2D import Vector2D

from Canvas.Physics.PhysicsSystem import PhysicsSystem

from Canvas.SpaceObject import SpaceObject, Shape

canvas = None

physicsSystem = None

def main():
    global canvas
    
    root = Tk()
    root.title("Project Alef")
    root.geometry("1200x1000")

    canvas = Canvas(root, bg ="black", width=1200, height=1000)
    canvas.pack()

    Start()
    
    def gameStep():
        Update(1)
        root.after(16, gameStep)
    
    gameStep()
    root.mainloop()

def Start():
    global canvas, physicsSystem
    
    physicsSystem = PhysicsSystem(200)
    
    CreateSpace()

def CreateSpace():
    global canvas, physicsSystem

    sun = SpaceObject(canvas, Vector2D(600,500), Vector2D(0,0), 15000, 30, Shape.Circle, "yellow")
    
    planet = SpaceObject(canvas, Vector2D(300,500), Vector2D(0,2), 50, 20, Shape.Square, "white")
    
    planet1 = SpaceObject(canvas, Vector2D(400,500), Vector2D(0,3), 20, 16, Shape.Rhomb, "Cyan")
    
    planet2 = SpaceObject(canvas, Vector2D(500,500), Vector2D(0,3.9), 10, 10, Shape.Triangle, "lime")

    physicsSystem.AddObjects([sun, planet, planet1, planet2])
    physicsSystem.AddMassiveObject(sun)

    #CreateAsteroids()
    
def CreateAsteroids():
    global canvas, physicsSystem
    n = 1
    for i in range(30):
        asteroid = SpaceObject(canvas, Vector2D(30*i+1, 100-n), Vector2D(i*0.01, 5), 2*n, i+1, None, "red")
        
        if i < 15:
            n *= 2
        else:
            n /= 2
        
        physicsSystem.AddObject(asteroid)

def Update(totalTime:int):
    global physicsSystem
    
    physicsSystem.Update(totalTime)

if __name__ == "__main__":
    main()