from cmu_112_graphics import *

class MglwTkSingleton(object):
    mglwSingletonRoot = None

def runApp(*args, **kwargs):
    app = App(*args, **kwargs)

def keyPressed(app, event):
    print(f':recv_key {event.key};')

def main():
    runApp(
        width=3840//3, height=2160//3,
        title='Game Window',
    )

if __name__ == '__main__':
    main()
