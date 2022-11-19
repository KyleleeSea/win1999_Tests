from cmu_112_graphics import *
from helpers import *
import random

class Maze:
    def __init__(self):
        self.maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 1, 0, 1], [1, 0, 0, 0, 1, 0, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 1, 1, 1, 1], [1, 0, 0, 0, 0, 1, 0, 0, 0, 1], [1, 0, 0, 1, 1, 1, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1, 0, 0, 0, 1], [1, 0, 0, 1, 0, 0, 0, 1, 0, 1], [1, 0, 0, 0, 0, 1, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    def redraw(self, app, canvas):
        for rowIndex in range(len(self.maze)):
            for colIndex in range(len(self.maze[rowIndex])):
                if self.maze[rowIndex][colIndex] == 1:
                    drawWall(app, canvas, rowIndex, colIndex, self.maze)
                else:
                    drawOpen(app, canvas, rowIndex, colIndex, self.maze)
#----------------------
# Maze drawing helpers
def drawWall(app, canvas, row, col, maze):
    (x0, y0, x1, y1) = getCellBounds(row, col, maze, app)
    canvas.create_rectangle(x0, y0, x1, y1, fill='black')

def drawOpen(app, canvas, row, col, maze):
    (x0, y0, x1, y1) = getCellBounds(row, col, maze, app)
    canvas.create_rectangle(x0, y0, x1, y1, fill='white', outline='black')