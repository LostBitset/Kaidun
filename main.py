# Kaidun (by HktOverload)

import time

from cmu_112_graphics import ImageTk, runApp

import mglw_main
import scoring

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
    print('!! mglw_main.main is finished !!')
    reenterHook(app)

def reenterHook(app):
    updateScores(app)

def appStarted(app):
    # See citation for mglwCenterTkWindow function
    app._root.eval('tk::PlaceWindow . center')
    app.mode = 'splashScreen'
    updateScores(app)

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
    drawScoreInfo(app, canvas)

def drawScoreInfo(app, canvas):
    text = '\n'.join([
        f'Latest Score: {app.latestScore}',
        f'Best Score: {app.bestScore}',
    ])
    canvas.create_text(
        app.width - 15, app.height - 15, anchor='se',
        text=text, font='Monospace 40 bold',
        fill='white',
    )

def maxSafe(L):
    if len(L) == 0:
        return None
    return max(L)

def updateScores(app):
    scores = scoring.readSavefile()['scores']
    highestScore = maxSafe(scores.values())
    if highestScore != None:
        highestScore = int(highestScore * 10)
    else:
        highestScore = 0
    latestTimestamp = maxSafe(scores.keys())
    if latestTimestamp == None:
        latestScore = 0
    else:
        latestScore = int(scores[latestTimestamp] * 10)
    app.latestScore = latestScore
    app.bestScore = highestScore

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
