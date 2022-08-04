import threading

import mglw_main

class MglwTkSingleton(object):
    mglwSingletonRoot = None

def mglwTkInitCallback(cfg):
    MglwTkSingleton.mglwSingletonRoot = cfg.wnd._tk

def mglwTkLoadHook(wincls):
    wincls.init_callback = mglwTkInitCallback

def startTk():
    load_hook = mglwTkLoadHook
    target = lambda: \
        mglw_main.main(load_hook=load_hook)
    thread = threading.Thread(target=target, args=())
    thread.start()
    while MglwTkSingleton.mglwSingletonRoot == None:
        pass
    return MglwTkSingleton.mglwSingletonRoot
