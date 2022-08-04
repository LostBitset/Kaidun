import mglw_tk

import inspect

def overridenTk():
    mglwRoot = mglw_tk.startTk()
    return mglwRoot

caller = inspect.currentframe().f_back
for _ in range(5):
    caller = caller.f_back

caller.f_globals['Tk'] = overridenTk
