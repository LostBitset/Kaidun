from cmu_112_graphics import *

import tkinter

def appStarted(app):
    app.oldRoot = app._root
    app.isRootSwap = False

def timerFired(app):
    if not app.isRootSwap:
        app._hideRootWindow()
        app._root = tkinter.Tk()
        app.isRootSwap = True

def keyPressed(app, event):
    print(event.key)

if __name__ == '__main__':
    runApp(
        width=3840//3, height=2160//3,
        title='Game Window',
    )
