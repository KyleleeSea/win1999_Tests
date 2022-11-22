from cmu_112_graphics import *
from helpers import *
import math

class Raycaster:
    def __init__(self, app, maze):
        self.maze = maze.maze
        (self.cellWidth, self.cellHeight) = getCellSpecs(app, self.maze)
        self.FOV = 60
        self.wallHeight = (3/4)*app.height
        self.playerHeight = self.wallHeight/2

        self.numRays = 320
        self.angleBetweenRays = self.FOV/self.numRays


    def castRays(self, app, canvas):
        print(app.player.angle)
        angle = app.player.angle - 30
        for i in range(self.numRays):
            angle += self.angleBetweenRays
            self.getRay(app, angle, canvas)
        

# https://permadi.com/1996/05/ray-casting-tutorial-7/
# Conversation with Stephen Mao, discussed how to calculate height of a
# triangle. stmao@andrew.cmu.edu
    def getRay(self, app, angle, canvas):
        if angle >= 90 and angle <= 270:
            distHor = self.horizontalUpRay(app, angle, canvas)
        else:
            distHor = self.horizontalDownRay(app, angle, canvas)
        if angle >= 0 and angle <= 180:
            distVer = self.verticalRightRay(app, angle, canvas)
        else:
            distVer = self.verticalLeftRay(app, angle, canvas)
        # print(min(distHor, distVer))
        if distHor[2] < distVer[2]:
            canvas.create_line(app.player.xPos, app.player.yPos, distHor[0], distHor[1], fill="green")        
        else:
            canvas.create_line(app.player.xPos, app.player.yPos, distVer[0], distVer[1], fill="orange")        

    def checkFirstIntersection(self, app, px, py):
        (intersectionRow, intersectionCol) = getCell(app, px, py, self.maze)
        # Only check if point on map
        if (intersectionRow >= 0 and intersectionRow < len(self.maze) and 
        intersectionCol >= 0 and intersectionCol < len(self.maze)):
            if self.maze[intersectionRow][intersectionCol] == 1:
                return (True, getDistance(app.player.xPos, app.player.yPos, 
                px, py))
        return (False, 0)

    def checkOtherIntersections(self, app, px, py):
        (intersectionRow, intersectionCol) = getCell(app, px, py, self.maze)
        if (intersectionRow >= 0 and intersectionRow < len(self.maze) and 
            intersectionCol >= 0 and intersectionCol < len(self.maze)):
            if self.maze[intersectionRow][intersectionCol] == 1:
                return (True, getDistance(app.player.xPos, app.player.yPos, px, 
                py))
            # If point off map, just return a giant number 
        else:
            return (True, 10000000000000)
        return (False, 0)
    
    def verticalRightRay(self, app, angle, canvas):
    # end variable first arg: True or False condition. second arg: distance
    # value. 
        end = (False, 0)
        px = self.cellWidth*(app.player.col+1)
        py = (app.player.yPos - 
        math.tan(math.radians(angle-90))*(px-app.player.xPos))

        end = self.checkFirstIntersection(app, px, py)

        while end[0] != True:
            Ya = self.cellWidth*(math.tan(math.radians(angle-90)))
            px = px+self.cellWidth
            py = py-Ya
            end = self.checkOtherIntersections(app, px, py)

        return (px, py, end[1])
        # return end[1]
        # canvas.create_line(app.player.xPos, app.player.yPos, px, py, fill="green")        

    def verticalLeftRay(self, app, angle, canvas):
        end = (False, 0)
        #3.5*app.margin is a trivial fix to a bug that exists without the
        #3.5* multiplier. Revisit here if future bugs.
        px = self.cellWidth*(app.player.col - 1) + (3.5*app.margin)
        # print(cellWidth)
        py = (app.player.yPos - 
        math.tan(math.radians(angle - 90))*(px-app.player.xPos))

        end = self.checkFirstIntersection(app, px, py)

        while end[0] != True:
            Ya = self.cellWidth*(math.tan(math.radians(angle-90)))
            px = px-self.cellWidth
            py = py+Ya
            end = self.checkOtherIntersections(app, px, py)
        # Test other intersections until hit wall

        return (px, py, end[1])
        # return end[1]
        # print(end[1])
        # canvas.create_line(app.player.xPos, app.player.yPos, px, py, fill="green")        

    def horizontalDownRay(self, app, angle, canvas):
        end = (False, 0)
        # Horizontal
        # First intersection
        py = self.cellHeight*(app.player.row + 1)
        #0.0001 added to avoid div by 0 error
        px = (app.player.xPos + 
        (app.player.yPos - py)/(math.tan(math.radians(angle-90))
        +0.0001))

        end = self.checkFirstIntersection(app, px, py)

        while end[0] != True:
            Xa = self.cellHeight/((math.tan(math.radians(angle-90))
            +0.0001))
            px = px-Xa
            py = py+self.cellHeight
            end = self.checkOtherIntersections(app, px, py)

        return (px, py, end[1])
        # return end[1]
        # canvas.create_line(app.player.xPos, app.player.yPos, px, py, fill="orange")        

    def horizontalUpRay(self, app, angle, canvas):
        end = (False, 0)

        #1.2*app.margin is a trivial fix to a bug that exists without the
        #Revisit here if future bugs.
        py = self.cellHeight*(app.player.row - 1) + (1.2*app.margin)
        #0.0001 added to avoid div by 0 error
        px = (app.player.xPos + 
        (app.player.yPos - py)/(math.tan(math.radians(angle-90))
        +0.0001))

        end = self.checkFirstIntersection(app, px, py)

        # Test other intersections until hit wall
        while end[0] != True:
            Xa = (self.cellHeight/(math.tan(math.radians(angle-90))
            +0.0001))
            px = px+Xa
            py = py-self.cellHeight
            end = self.checkOtherIntersections(app, px, py)

        return (px, py, end[1])
        # return end[1]
        # canvas.create_oval(px-5,py-5,px+5,py+5,fill='green')
        # canvas.create_line(app.player.xPos, app.player.yPos, px, py, fill="orange")        

    def redraw(self, app, canvas):
        self.castRays(app, canvas)