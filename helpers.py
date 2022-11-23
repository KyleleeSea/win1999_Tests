# View Helpers
def getCellSpecs(app, maze):
    width = app.width
    height = app.height
    (numRows, numCols) = (len(maze), len(maze[0]))
    cellWidth = width//numRows
    cellHeight = height//numCols
    return (cellWidth, cellHeight)

def getCellBounds(row, col, maze, app):
    (cellWidth, cellHeight) = getCellSpecs(app, maze)
    (x0, y0, x1, y1) = (col*cellWidth, row*cellHeight, (col+1)*cellWidth,
    (row+1)*cellHeight)
    return (x0, y0, x1, y1)

# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCell(app, x, y, maze):
    gridWidth  = app.width
    gridHeight = app.height
    cellWidth  = gridWidth / len(maze[0])
    cellHeight = gridHeight / len(maze)

    row = int((y) / cellHeight)
    col = int((x) / cellWidth)

    return (row, col)

# Dynamic audio helpers

def getDistance(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y1-y0)**2)**(1/2)