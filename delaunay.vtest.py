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

def drawExplanation(app, canvas):
    text = \
        '''
        Press 1 to see if your mouse is inside the circumcircle of a triangle
        Press 2 to test the full Boyer-Watson algorithm
        '''
    canvas.create_text(
        app.width//2, app.height,
        anchor='s',
        text=text,
    )

def testPointInCircumcircle_mouseMoved(app, event):
    app.wasInCircumcircle = pointInCircumcircle(
        (event.x, event.y),
        app.testTri,
    )
    # print(f'wasInCircumcircle={app.wasInCircumcircle}')

def testPointInCircumcircle_redrawAll(app, canvas):
    color = 'green' if app.wasInCircumcircle else 'red'
    canvas.create_polygon(*app.testTri, fill=color)
    res = 10
    for x in range(0, app.width, res):
        for y in range(0, app.height, res):
            if not pointInCircumcircle((x, y), app.testTri):
                canvas.create_rectangle(
                    x, y, x + res, y + res,
                    fill='pink', width=0,
                )
    drawExplanation(app, canvas)

def testBoyerWatson_redrawAll(app, canvas):
    count = 0
    for tri in app.triangulation:
        count += 1
        for edge in edgesOf(tri):
            edge = [
                [ int(coord * 500) + 50 for coord in vert ]
                for vert in sorted(edge)
            ]
            canvas.create_line(*edge)
    # print(f'triCount = {count}')
    for pt in app.points:
        pt = [ int(coord * 500) + 50 for coord in pt ]
        canvas.create_oval(
            pt[0] - 5, pt[1] - 5, pt[0] + 5, pt[1] + 5,
            fill='red',
        )
    drawExplanation(app, canvas)

runApp(width=600, height=600)

