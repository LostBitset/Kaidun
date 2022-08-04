from cmu_112_graphics import *

def keyPressed(app, event):
    print(f':recv_key {event.key};')

if __name__ == '__main__':
    runApp(
        width=3840//3, height=2160//3,
        title='Game Window',
    )
