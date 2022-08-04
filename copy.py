import inspect

def overridenTk():
    caller = inspect.currentframe().f_back
    for _ in range(2):
        caller = caller.f_back
        print(caller.f_globals['__name__'])
    mglwRoot = caller.f_globals['MglwTkSingleton'].mglwSingletonRoot
    print('*** GOT MGLW ROOT:', type(mglwRoot), mglwRoot, '***')
    return mglwRoot

caller = inspect.currentframe().f_back
for _ in range(5):
    caller = caller.f_back

caller.f_globals['Tk'] = overridenTk
