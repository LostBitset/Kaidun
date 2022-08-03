import time

from cmu_112_graphics import *

import mglw_main

def mglwRootFrameCallback(app):
    app.mglwRedrawTime = time.time()

def mglwRootLoadHook(app, wincls):
    wincls.frame_callback = \
        lambda: \
            mglwRootFrameCallback(app)
    wincls.title = app._title

def startMGLWRoot(app, maxTimeWithoutGLRoot=0.5):
    app.mglwRedrawTime = time.time()
    app.maxTimeWithoutGLRoot = maxTimeWithoutGLRoot
    mglw_main.main(
        load_hook=(
            lambda wincls: \
                mglwRootLoadHook(app, wincls)
        ),
    )

def appStarted(app):
    startMGLWRoot(app)

def showGL(app):
    try:
        app._hideRootWindow()
    except:
        pass

def checkNoGLRoot(app):
    delta = time.time() - app.mglwRedrawTime
    if delta > app.maxTimeWithoutGLRoot:
        print('*** No response from mglw render_callback ***')
        print('*** (Assuming that mglw tk root no longer exists) ***')
        print('*** Quitting cmu_112_graphics tk root... ***')
        app.quit()

def timerFired(app):
    checkNoGLRoot(app)

def redrawAll(app, *_):
    showGL(app)

if __name__ == '__main__':
    runApp(
        width=3840//3, height=2160//3,
        title='Game Window',
    )
