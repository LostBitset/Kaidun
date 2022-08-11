# Kaidun (by HktOverload)

'''
This is just a simple visual test for the Boyer-Watson
implementation found in delaunay.py
Look there for citations
'''

from cmu_112_graphics import *

from delaunay import boyerWatson

import random

numVerts = 10

unitSuperTri = [(-1, 1), (1, -1), (1, 1)]

def randUnit2():
    return (random.random(), random.random())

def appStarted(app):
    points = [ randUnit2() for _ in range(numVerts) ]
    triangulation = boyerWatson(points, unitSuperTri)
    app.points = points
    app.triangulation = triangulation

def redrawAll(app, canvas):
    for pt in app.points:
        pt = [ int(coord * 500) + 50 for coord in pt ]
        canvas.create_oval(
            pt[0] - 5, pt[1] - 5, pt[0] + 5, pt[1] + 5,
            fill='red',
        )

runApp(width=600, height=600)

