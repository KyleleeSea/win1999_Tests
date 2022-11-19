from cmu_112_graphics import *
from maze import *
from player import *

def appStarted(app):
    app.timerDelay = 200
    app.margin = min(app.width, app.height)//15
    app.maze = Maze()
    app.player = Player(app, app.maze)

def mouseMoved(app, event):
    app.player.mouseMoved(app, event)

def keyPressed(app, event):
    app.player.keyPressed(app, event)

def redrawAll(app, canvas):
    app.maze.redraw(app, canvas)
    app.player.redraw(app, canvas)

runApp(width=1500, height=600)
