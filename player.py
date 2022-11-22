from cmu_112_graphics import *
from helpers import *
import math

class Player:
    def __init__(self, app, maze):
        # Consider restructuring self.maze and self.exitBlock assignment
        self.lastMousePos = None
        self.mouseSensitivityDenominator = int(min(app.width, app.height)//400)
        self.maze = maze.maze
        self.angle = 90
        # self.angleVel = 10
        self.moveVel = int(min(app.width, app.height)//100)
        (startX0, startY0, startX1, startY1) = getCellBounds(1, 1, self.maze, 
        app)
        self.xPos = int((startX0 + startX1)//2)
        self.yPos = int((startY0 + startY1)//2)
        self.row = 1
        self.col = 1
        self.lastRow = 0
        self.lastCol = 0
        # playerSize temporary
        self.playerSize = int(min(app.width, app.height)//(len(maze.maze)*4))

    def adjustAngle(self, angleDiff):
        self.angle = (self.angle - angleDiff) % 360

    def movePlayer(self, app):
        # https://www.youtube.com/watch?v=rbokZWrwCJE
        # "Solve a Right Triangle Given an Angle and the Hypotenuse"
        # https://www.tutorialspoint.com/python/number_sin.htm
        # https://www.geeksforgeeks.org/degrees-and-radians-in-python/
        # Must convert to radians. Sin and cos in radians
        newX = self.xPos + self.moveVel * math.sin(math.radians(self.angle))
        newY = self.yPos + self.moveVel * math.cos(math.radians(self.angle))
        if self.checkLegalMove(newX, newY, app):
            self.xPos = newX
            self.yPos = newY
            self.row, self.col = getCell(app, newX, newY, self.maze)

    def keyPressed(self, app, event):
        if event.key == 'w':
            self.movePlayer(app)

    def mouseMoved(self, app, event):
        if self.lastMousePos == None:
            self.lastMousePos = event.x
        else:
            diff = event.x - self.lastMousePos
            self.lastMousePos = event.x
            self.adjustAngle(diff//self.mouseSensitivityDenominator)

    def checkLegalMove(self, newX, newY, app):
        (row, col) = getCell(app, newX, newY, self.maze)
        if self.maze[row][col] == 0:
            return True
        return False

    def checkExit(self, x, y, exitBlock, app):
        (row, col) = getCell(app, x, y, self.maze)
        if exitBlock.row == row and exitBlock.col == col:
            return True
        return False

    def redraw(self, app, canvas):
        canvas.create_oval(self.xPos-self.playerSize, self.yPos-self.playerSize,
        self.xPos + self.playerSize, self.yPos + self.playerSize,
        fill='orange')
        # Temporary 2D debugging line that'll show angle facing
        canvas.create_line(self.xPos, self.yPos, 
        self.xPos+(self.moveVel * math.sin(math.radians(self.angle)))*10,
        self.yPos+self.moveVel * math.cos(math.radians(self.angle))*10, 
        fill='orange')

        self.drawRay(app, canvas)


# https://permadi.com/1996/05/ray-casting-tutorial-7/
# Conversation with Stephen Mao, discussed how to calculate height of a
# triangle. stmao@andrew.cmu.edu
    def drawRay(self, app, canvas):
        if self.angle >= 90 and self.angle <= 270:
            distHor = self.horizontalUpRay(app)
        else:
            distHor = self.horizontalDownRay(app)
        # print(distHor)
        self.verticalRightRay(app, canvas)

    def checkFirstIntersection(self, app, px, py):
        (intersectionRow, intersectionCol) = getCell(app, px, py, self.maze)
        # Only check if point on map
        if (intersectionRow >= 0 and intersectionRow < len(self.maze) and 
        intersectionCol >= 0 and intersectionCol < len(self.maze)):
            if self.maze[intersectionRow][intersectionCol] == 1:
                # return getDistance(self.xPos, self.yPos, px, py)
    
    def verticalRightRay(self, app, canvas):
        isInWall = False
        (cellWidth, cellHeight) = getCellSpecs(app, self.maze)
        px = cellWidth*(self.col+1)
        py = self.yPos - math.tan(math.radians(self.angle-90))*(px-self.xPos)
        # Check if first intersection hits a wall
        (intersectionRow, intersectionCol) = getCell(app, px, py, self.maze)
        # Only check if point on map
        self.checkFirstIntersection(app, px, py)
        if (intersectionRow >= 0 and intersectionRow < len(self.maze) and 
        intersectionCol >= 0 and intersectionCol < len(self.maze)):
            if self.maze[intersectionRow][intersectionCol] == 1:
                isInWall = True
                # return getDistance(self.xPos, self.yPos, px, py)
        
        # Test other intersections until hit wall
        while isInWall != True:
            Ya = cellWidth*(math.tan(math.radians(self.angle-90)))
            px = px+cellWidth
            py = py-Ya
            (intersectionRow, intersectionCol) = getCell(app, px, py, self.maze)
            if (intersectionRow >= 0 and intersectionRow < len(self.maze) and 
            intersectionCol >= 0 and intersectionCol < len(self.maze)):
                if self.maze[intersectionRow][intersectionCol] == 1:
                    isInWall = True
                    # return getDistance(self.xPos, self.yPos, px, py)
            # If point off map, just return a giant number 
            else:
                isInWall = True
                # return 10000000000
        canvas.create_oval(px-5,py-5,px+5,py+5,fill='green')

    def horizontalDownRay(self, app):
        isInWall = False
        # Horizontal
        # First intersection
        (cellWidth, cellHeight) = getCellSpecs(app, self.maze)
        py = cellHeight*(self.row + 1)
        #0.0001 added to avoid div by 0 error
        px = self.xPos + (self.yPos - py)/(math.tan(math.radians(self.angle-90))
        +0.0001)
        # Check if first intersection hits a wall
        (intersectionRow, intersectionCol) = getCell(app, px, py, self.maze)
        # Only check if point on map
        if (intersectionRow >= 0 and intersectionRow < len(self.maze) and 
        intersectionCol >= 0 and intersectionCol < len(self.maze)):
            if self.maze[intersectionRow][intersectionCol] == 1:
                isInWall = True
                return getDistance(self.xPos, self.yPos, px, py)
        
        # Test other intersections until hit wall
        while isInWall != True:
            Xa = cellHeight/(math.tan(math.radians(self.angle-90))+0.0001)
            px = px-Xa
            py = py+cellHeight
            (intersectionRow, intersectionCol) = getCell(app, px, py, self.maze)
            if (intersectionRow >= 0 and intersectionRow < len(self.maze) and 
            intersectionCol >= 0 and intersectionCol < len(self.maze)):
                if self.maze[intersectionRow][intersectionCol] == 1:
                    isInWall = True
                    return getDistance(self.xPos, self.yPos, px, py)
            # If point off map, just return a giant number 
            else:
                isInWall = True
                return 10000000000
                
    def horizontalUpRay(self, app):
        isInWall = False
        # Horizontal
        # First intersection
        (cellWidth, cellHeight) = getCellSpecs(app, self.maze)
        py = cellHeight*(self.row - 1)
        #0.0001 added to avoid div by 0 error
        px = self.xPos + (self.yPos - py)/(math.tan(math.radians(self.angle-90))
        +0.0001)
        # Check if first intersection hits a wall
        (intersectionRow, intersectionCol) = getCell(app, px, py, self.maze)
        # Only check if point on map
        if (intersectionRow >= 0 and intersectionRow < len(self.maze) and 
        intersectionCol >= 0 and intersectionCol < len(self.maze)):
            if self.maze[intersectionRow][intersectionCol] == 1:
                isInWall = True
                return getDistance(self.xPos, self.yPos, px, py)
        
        # Test other intersections until hit wall
        while isInWall != True:
            Xa = cellHeight/(math.tan(math.radians(self.angle-90))+0.0001)
            px = px+Xa
            py = py-cellHeight
            (intersectionRow, intersectionCol) = getCell(app, px, py, self.maze)
            if (intersectionRow >= 0 and intersectionRow < len(self.maze) and 
            intersectionCol >= 0 and intersectionCol < len(self.maze)):
                if self.maze[intersectionRow][intersectionCol] == 1:
                    isInWall = True
                    return getDistance(self.xPos, self.yPos, px, py)
            # If point off map, just return a giant number 
            else:
                isInWall = True
                return 10000000000
