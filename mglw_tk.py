import threading

import mglw_main

def startTk():
    load_hook = mglwTkLoadHook
    target = lambda: \
        mglw_main.main(load_hook=load_hook)
    thread = threading.Thread(target=target, args=())
    thread.start()

