from terrain_graph_utils import incenter, distToSegment
from graphs import DirectedEdgeIn2D

from cmu_112_graphics import *

import random

def appStarted(app):
    app.a, app.b, app.c = (200, 500), (300, 100), (700, 500)

def timerFired(app):
    q = 30
    r = lambda: random.randrange(-q, q)
    app.a = (app.a[0] + r(), app.a[1] + r())
    app.b = (app.b[0] + r(), app.b[1] + r())
    app.c = (app.c[0] + r(), app.c[1] + r())

def redrawAll(app, canvas):
    a, b, c = app.a, app.b, app.c
    canvas.create_polygon(a, b, c)
    [cx, cy] = incenter([a, b, c])
    r = distToSegment(DirectedEdgeIn2D(a, b), [cx, cy])
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill='blue')
    canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill='red')

runApp(width=1000,height=1000)

