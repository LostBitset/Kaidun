import threading
import time

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
    time.sleep(1) # Trying to wait for it to change the value doesn't work
    return MglwTkSingleton.mglwSingletonRoot
