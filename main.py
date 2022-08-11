# Kaidun (by HktOverload)

import time

from cmu_112_graphics import ImageTk, runApp

import mglw_main

# Center the window given a WindowConfig object
# This must be a tkinter window
# This is Tcl code found here:
# [: Citation https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter :]
# The actual Tcl procedure was linked in the answer and can be found here:
# [: Citation https://github.com/tcltk/tk/blob/master/library/tk.tcl#L72 :]
def mglwCenterTkWindow(cfg):
    cfg.wnd._tk.eval('tk::PlaceWindow . center')

def mglwRootFrameCallback(app):
    app.mglwRedrawTime = time.time()

def mglwRootLoadHook(app, wincls):
    wincls.init_callback = mglwCenterTkWindow
    wincls.frame_callback = \
        lambda: mglwRootFrameCallback(app)
    wincls.title = app._title

def startMGLWRoot(app, maxTimeWithoutGLRoot=0.1):
    app.mglwRedrawTime = time.time()
    app.maxTimeWithoutGLRoot = maxTimeWithoutGLRoot
    app._hideRootWindow()
    mglw_main.main(
        load_hook=(
            lambda wincls: mglwRootLoadHook(app, wincls)
        ),
    )

def appStarted(app):
    # See citation for mglwCenterTkWindow function
    app._root.eval('tk::PlaceWindow . center')
    app.mode = 'splashScreen'

def splashScreen_keyPressed(app, event):
    if event.key == 'Enter':
        deferToGL(app)
    elif event.key == 'Space':
        app.mode = 'intentToQuit'
        deferToGL(app)

def splashScreen_timerFired(app):
    if not hasattr(app, 'splashScreenImage'):
        # [: Citation (course notes) https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html ]
        app.splashScreenImage = ImageTk.PhotoImage(
            app.loadImage('splash.png')
        )

def splashScreen_redrawAll(app, canvas):
    canvas.create_rectangle(
        0, 0, app.width, app.height,
        fill='#000',
    )
    if hasattr(app, 'splashScreenImage'):
        # [: Citation (course notes) https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html ]
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
        app.mode = app.mglwReturnMode
        app._showRootWindow()
        # See citation for mglwCenterTkWindow function
        app._root.eval('tk::PlaceWindow . center')

def altRootMGLW_timerFired(app):
    checkNoGLRoot(app)

def altRootMGLW_redrawAll(app, *_):
    showGL(app)

def intentToQuit_timerFired(app):
    print('*** Quitting cmu_112_graphics tk root (mode=intentToQuit)... ***')
    app.quit()

if __name__ == '__main__':
    runApp(
        width=3840//3, height=2160//3,
        title='Game Window',
    )
