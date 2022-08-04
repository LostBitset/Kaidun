import inspect

def overridenTk():
    caller = inspect.currentframe().f_back
    for _ in range(4):
        caller = caller.f_back
    return caller.f_globals['MglwTkSingleton'].mglwSingletonRoot

caller = inspect.currentframe().f_back
for _ in range(5):
    caller = caller.f_back

caller.f_globals['Tk'] = overridenTk
