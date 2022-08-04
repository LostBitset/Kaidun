import tkinter

import inspect
import subprocess 

def overridenTk():
    subprocess.Popen(['lxterminal', '-e', 'suod'])
    return tkinter.Tk()

caller = inspect.currentframe().f_back
for _ in range(5):
    caller = caller.f_back

caller.f_globals['Tk'] = overridenTk

