# Kaidun (by HktOverload)

'''
This is just a simple visual test for the Boyer-Watson
implementation found in delaunay.py
Look there for citations
'''

from cmu_112_graphics import *

from delaunay import boyerWatson, edgesOf, pointInCircumcircle

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
    app.mode = 'testPointInCircumcircle'
    tri = (randUnit2(), randUnit2(), randUnit2())
    tri = [
        [ int(coord * 500) + 50 for coord in vert ]
        for vert in tri
    ]
    app.testTri = tri
    app.wasInCircumcircle = False

def general_keyPressed(app, event):
    if event.key == '1':
        app.mode = 'testPointInCircumcircle'
    elif event.key == '2':
        app.mode = 'testBoyerWatson'

def testPointInCircumcircle_keyPressed(app, event):
    general_keyPressed(app, event)

def testBoyerWatson_keyPressed(app, event):
    general_keyPressed(app, event)

def testPointInCircumcircle_mousePressed(app, event):
    app.wasInCircumcircle = pointInCircumcircle(
        (event.x, event.y),
        app.testTri,
    )
    print(f'wasInCircumcircle={app.wasInCircumcircle}')

def testPointInCircumcircle_redrawAll(app, canvas):
    color = 'green' if app.wasInCircumcircle else 'red'
    canvas.create_polygon(*app.testTri, fill=color)

def testBoyerWatson_redrawAll(app, canvas):
    for tri in app.triangulation:
        for edge in edgesOf(tri):
            print(sorted(edge))
            canvas.create_line(*sorted(edge))
    for pt in app.points:
        pt = [ int(coord * 500) + 50 for coord in pt ]
        canvas.create_oval(
            pt[0] - 5, pt[1] - 5, pt[0] + 5, pt[1] + 5,
            fill='red',
        )

runApp(width=600, height=600)

