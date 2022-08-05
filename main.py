# Kaidun (by HktOverload)

import time

from cmu_112_graphics import *

import mglw_main

def mglwCenterTkWindow(cfg):
    cfg.wnd._tk.eval('tk::PlaceWindow . center')

def mglwRootFrameCallback(app):
    app.mglwRedrawTime = time.time()

def mglwRootLoadHook(app, wincls):
    wincls.init_callback = mglwCenterTkWindow
    wincls.frame_callback = \
        lambda: \
            mglwRootFrameCallback(app)
    wincls.title = app._title

def startMGLWRoot(app, maxTimeWithoutGLRoot=0.1):
    app.mglwRedrawTime = time.time()
    app.maxTimeWithoutGLRoot = maxTimeWithoutGLRoot
    mglw_main.main(
        load_hook=(
            lambda wincls: \
                mglwRootLoadHook(app, wincls)
        ),
    )

def appStarted(app):
    app._root.eval('tk::PlaceWindow . center')
    app.mode = 'splashScreen'

def splashScreen_keyPressed(app, event):
    if event.key == 'Enter':
        deferToGL(app)

def splashScreen_timerFired(app):
    if not hasattr(app, 'splashScreenImage'):
        app.splashScreenImage = ImageTk.PhotoImage(
            app.loadImage('splash.png')
        )

def splashScreen_redrawAll(app, canvas):
    canvas.create_rectangle(
        0, 0, app.width, app.height,
        fill='#000',
    )
    if hasattr(app, 'splashScreenImage'):
        canvas.create_image(
            app.width//2,
            app.height//2,
            image=app.splashScreenImage,
        )

def deferToGL(app):
    app.mglwReturnMode = app.mode
    app.mode = 'altRootMGLW'
    startMGLWRoot(app)

def showGL(app):
    try:
        time.sleep(0.2)
        app._hideRootWindow()
    except:
        pass

def checkNoGLRoot(app):
    delta = time.time() - app.mglwRedrawTime
    if delta > app.maxTimeWithoutGLRoot:
        print('*** No response from mglw render_callback ***')
        print('*** (Assuming that mglw tk root no longer exists) ***')
        #- print('*** Quitting cmu_112_graphics tk root... ***')
        app.mode = app.mglwReturnMode
        app._showRootWindow()
        app._root.eval('tk::PlaceWindow . center')

def altRootMGLW_timerFired(app):
    checkNoGLRoot(app)

def altRootMGLW_redrawAll(app, *_):
    showGL(app)

if __name__ == '__main__':
    runApp(
        width=3840//3, height=2160//3,
        title='Game Window',
    )
