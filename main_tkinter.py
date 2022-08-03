import time

from cmu_112_graphics import *

import tkinter
from OpenGL import GL
from pyopengltk import OpenGLFrame

class GameGLFrame(OpenGLFrame):

    def initgl(self):
        global appRef
        GL.glViewport(0, 0, appRef.width, appRef.height)
        GL.glClearColor(0.0, 1.0, 0.0, 0.0)
        print('In initgl')
    
    def redraw(self):
        global appRef
        redrawAll(appRef, canvas=None, glctx='yes')
        appRef.gltkRedrawTime = time.time()

def appStarted(app):
    global appRef
    appRef = app
    setupGLWindow(app)
    runGLFrame(app)
    showGL(app)

def setupGLWindow(app, maxTimeWithoutGLRoot=0.25):
    app.glWindowRoot = tkinter.Tk()
    app.glFrame = GameGLFrame(
        app.glWindowRoot,
        width=app.width, height=app.height,
    )
    app.gltkRedrawTime = time.time()
    app.maxTimeWithoutGLRoot = maxTimeWithoutGLRoot

def runGLFrame(app):
    app.glFrame.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    app.glFrame.animate = 1
    app.glFrame.after(100, app.glFrame.printContext)

def showGL(app):
    try:
        app._hideRootWindow()
        app.glWindowRoot.focus()
        app.glWindowRoot.focus_force()
        app.glWindowRoot.focus_set()
    except:
        pass

def checkNoGLRoot(app):
    delta = time.time() - app.gltkRedrawTime
    if delta > app.maxTimeWithoutGLRoot:
        print('***** KILLING MAIN TK ROOT *****')
        app.quit()

def timerFired(app):
    checkNoGLRoot(app)

def redrawAll(app, canvas, glctx=None):
    if glctx != None:
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        showGL(app)
    else:
        pass

if __name__ == '__main__':
    runApp(
        width=3840//3, height=2160//3,
        title='Game Window',
    )
