import mglw_main

import inspect
import subprocess 

def overridenTk():
    import tkinter
    return tkinter.Tk()
    # mglwRoot = mglw_main.startTk()
    # return mglwRoot

caller = inspect.currentframe().f_back
for _ in range(5):
    caller = caller.f_back

caller.f_globals['Tk'] = overridenTk

