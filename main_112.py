from cmu_112_graphics import *

import mglw_main

class MglwTkSingleton(object):
    mglwSingletonRoot = None

def runApp(*args, **kwargs):
    global appRef
    appRef = App(*args, **kwargs, autorun=False)
    startMglw()

def updateMglwSingletonRoot(cfg):
    MglwTkSingleton.mglwSingletonRoot = cfg.wnd._tk
    appRef.run()

def addInitCallback(wincls):
    wincls.init_callback = updateMglwSingletonRoot

def startMglw():
    mglw_main.main(load_hook=addInitCallback)

def keyPressed(app, event):
    print(f':recv_key {event.key};')

def main():
    runApp(
        width=3840//3, height=2160//3,
        title='Game Window',
    )

if __name__ == '__main__':
    main()
