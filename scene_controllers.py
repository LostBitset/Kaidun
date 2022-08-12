# Kaidun (by HktOverload)

import numpy as np

from math import atan2, copysign
import random

from mix import Mixin
import terrain_graph_utils
import scoring

# This seems (at least to me) a lot like the Haskell liftA2 function
# That's where it got this name
# [: Citation https://hackage.haskell.org/package/base-4.17.0.0/docs/Control-Applicative.html#v:liftA2 :]
def lift2(f):
    return lambda x, y: lambda *args, **kwargs: \
        f(x(*args, **kwargs), y(*args, **kwargs))

assoc = lift2(lambda x, y: {**x, **y})
sequential = lift2(lambda x, y: (x, y, None)[2])

def defaultShaderUpdates(gamedata):
    return dict()

def defaultFrame(gamedata, ftime):
    pass

def defaultHandle(gamedata, event):
    pass

control = Mixin(':controller-base', {
    'shaderUpdates': defaultShaderUpdates,
    'frame': defaultFrame,
    'handle': defaultHandle,
}, {
    'shaderUpdates': assoc,
    'frame': sequential,
    'handle': sequential,
})

cameraUpdates = Mixin(':camera-upd', {
    'shaderUpdates': lambda gamedata: {
        'cam_ctr':    gamedata['cam_ctr'],
        'cam_yaw':    gamedata['cam_rot'][0],
        'cam_pitch':  gamedata['cam_rot'][1],
        'cam_roll':   gamedata['cam_rot'][2],
    },
}).use(control)

lightFollowsPlayer = Mixin(':light-to-player', {
    'shaderUpdates': lambda gamedata: {
        'lighting_light_ctr': gamedata['cam_ctr'],
    },
})

def frameMovement(gamedata, ftime):
    ctr, rot = gamedata['cam_ctr'], gamedata['cam_rot']
    dctr, drot = gamedata['d_cam_ctr'], gamedata['d_cam_rot']
    fac = ftime / (1/20)
    gamedata['cam_ctr'] = (
        ctr[0] + (dctr[0] * fac),
        ctr[1] + (dctr[1] * fac),
        ctr[2] + (dctr[2] * fac),
    )
    gamedata['cam_rot'] = (
        rot[0] + (drot[0] * fac),
        rot[1] + (drot[1] * fac),
        rot[2] + (drot[2] * fac),
    )

movement = Mixin(':camera-movement', {
    'frame': frameMovement,
}).use(cameraUpdates)

rspeed = [0.05, 0.02, 0.05]

rspeedController = [
    rspeed[ax] if ax == 1 else None
    for ax in range(3)
]

def handleRotation(gamedata, event):
    posKeys = ['up', 'a', 'left']
    negKeys = ['down', 'd', 'right']
    if 'keys_control_rot_axes' not in gamedata:
        gamedata['keys_control_rot_axes'] = set()
    drot = list(gamedata['d_cam_rot'])
    for ax in range(3):
        if event.isKeypress(posKeys[ax]):
            drot[ax] += rspeed[ax]
            gamedata['keys_control_rot_axes'].add(ax)
        elif event.isKeypress(negKeys[ax]):
            drot[ax] -= rspeed[ax]
            gamedata['keys_control_rot_axes'].add(ax)
        else:
            isRelease = False
            isRelease |= event.isKeyrelease(posKeys[ax])
            isRelease |= event.isKeyrelease(negKeys[ax])
            if isRelease:
                drot[ax] = 0
                gamedata['keys_control_rot_axes'].discard(ax)
    gamedata['d_cam_rot'] = tuple(drot)

rotationKeys = Mixin(':camera-rot', {
    'handle': handleRotation,
})

def handleJumping(gamedata, event):
    ctr = gamedata['cam_ctr']
    onGround = abs(ctr[2]) < 10**-5
    if 'is_jumping' not in gamedata or onGround:
        gamedata['is_jumping'] = False
    if event.isKeypress('z'):
        if not gamedata['is_jumping']:
            gamedata['is_jumping'] = True
            dctr = list(gamedata['d_cam_ctr'])
            dctr[2] = 0.08
            gamedata['d_cam_ctr'] = tuple(dctr)

jumping = Mixin(':jumping-event', {
    'handle': handleJumping,
})

def frameGravity(gamedata, ftime):
    ctr = list(gamedata['cam_ctr'])
    dctr = list(gamedata['d_cam_ctr'])
    if ctr[2] > 0:
        dctr[2] -= 9.8 * (ftime ** 2)
    elif dctr[2] < 0:
        dctr[2] = 0
        ctr[2] = 0
    gamedata['cam_ctr'] = tuple(ctr)
    gamedata['d_cam_ctr'] = tuple(dctr)

gravity = Mixin(':gravity', {
    'frame': frameGravity,
})

# A proportional controller (like PID but only P)
# [: Citation https://eng.libretexts.org/Bookshelves/Industrial_and_Systems_Engineering/Book%3A_Chemical_Process_Dynamics_and_Controls_(Woolf)/09%3A_Proportional-Integral-Derivative_(PID)_Control/9.02%3A_P%2C_I%2C_D%2C_PI%2C_PD%2C_and_PID_control :]
class PController(object):
    __slots__ = ('kP', 'max')

    def __init__(self, kP, maxD):
        self.kP = kP
        self.max = maxD

    def get(self, x, setpoint):
        err = x - setpoint
        pComponent = self.kP * err
        if abs(pComponent) < 0.01:
            pComponent = 0.0
        if self.max != None:
            if abs(pComponent) > self.max:
                return copysign(self.max, pComponent)
        return -pComponent

# A variant of the proprtional controller that doesn't go the
# wrong direction half the time when used with angles
# (in radians)
class AnglePController(PController):

    def get(self, x, setpoint):
        adj = abs(x - setpoint)
        if adj > np.pi:
            return super().get(
                (x + (3*np.pi)) % (2*np.pi),
                (setpoint + (3*np.pi)) % (2*np.pi),
            )
        else:
            return super().get(
                x,
                setpoint,
            )

followRotationControllers = [
    AnglePController(0.4, speed)
    for speed in rspeedController
]

def setFollowRotation(gamedata, ftime):
    if not gamedata['is_following']:
        return
    if 'drv_dx' in gamedata and 'drv_dy' in gamedata:
        rot = gamedata['cam_rot']
        drot = list(gamedata['d_cam_rot'])
        x = gamedata['drv_dx']
        y = gamedata['drv_dy']
        setpoints = [
            np.pi / 2,
            np.pi,
            atan2(y, x) + (np.pi / 2),
        ]
        for i in range(3):
            if i in gamedata.get('keys_control_rot_axes', set()):
                continue
            drot[i] = followRotationControllers[i].get(
                rot[i],
                setpoints[i],
            )
        gamedata['d_cam_rot'] = tuple(drot)

followRotation = Mixin(':camera-rot-follow', {
    'frame': setFollowRotation,
})

def setFollowTranslation(gamedata, ftime):
    tspeed = 0.09
    tspeed *= ftime * 30
    edge = gamedata['follow_edge']
    tspeed /= terrain_graph_utils.dist(edge.src, edge.dst)
    if not gamedata['is_following']:
        dctr = list(gamedata['d_cam_ctr'])
        dctr[0] = 0
        dctr[1] = 0
        gamedata['d_cam_ctr'] = tuple(dctr)
    else:
        target = edge.atT(gamedata['follow_t'])
        ctr = list(gamedata['cam_ctr'])
        dx = target[0] - ctr[0]
        dy = target[1] - ctr[1]
        ctr[0] = target[0]
        ctr[1] = target[1]
        gamedata['cam_ctr'] = tuple(ctr)
        gamedata['drv_dx'] = dx
        gamedata['drv_dy'] = dy
        gamedata['follow_t'] += tspeed
        gamedata['score'] += ftime

followTranslation = Mixin(':camera-tr-follow', {
    'frame': setFollowTranslation,
})

def handleStartAndStop(gamedata, event):
    if event.isKeypress('enter'):
        gamedata['is_following'] ^= True
        gamedata['following_event'] = True

def frameStartAndStop(gamedata, ftime):
    # print(f't={gamedata["follow_t"]}')
    gamedata['following_event'] = False
    ctr = gamedata['cam_ctr']
    edge = gamedata['follow_edge']
    if gamedata['follow_t'] > 1.0:
        '''
        gamedata['following_event'] = gamedata['is_following']
        gamedata['is_following'] = False
        '''
        graph = gamedata['follow_graph']
        print('--- REACHED END OF EDGE ---')
        print(f'| expected: {edge.dst}')
        print(f'| edge: {edge}')
        print(f'| ctr: {ctr}')
        print('--- [[ t >= 1. ]] CONTINUING...')
        opts = graph.adjDict[edge.dst]
        opts.difference_update(edge.asUndirected())
        chosenEdge = random.choice(tuple(opts))
        print(f'^^^ chosenEdge: {chosenEdge}')
        gamedata['follow_edge'] = chosenEdge.awayFrom(edge.dst)
        gamedata['follow_t'] = 0.0
        print('^^^ updating score...')
        scoring.updateScore(gamedata['scoring_ts'], gamedata['score'])
        gamedata['score'] = 0.0
        print('^^^ all done')

startAndStop = Mixin(':start-and-stop', {
    'handle': handleStartAndStop,
    'frame': frameStartAndStop,
})

def frameStopGracefully(gamedata, ftime):
    if gamedata['following_event']:
        gamedata['d_cam_rot'] = (0.0, 0.0, 0.0)

stopGracefully = Mixin(':stop-gracefully-rot', {
    'frame': frameStopGracefully,
})

# Taken from cmu_112_graphics
def showTkWindow(root):
    root.update()
    root.deiconify()
    root.lift()
    root.focus()

ensureShown = Mixin(':ensure-window-shown-tk', {
    'frame': lambda gamedata, _: showTkWindow(gamedata['<wnd>']._tk)
})

movementWithKeys = Mixin(':camera-movement-all').use(
    startAndStop,
    stopGracefully,
    rotationKeys,
    gravity,
    followTranslation,
    followRotation,
    movement,
    lightFollowsPlayer,
)

# jumping isn't actually used
# it was just to test the gravity impl
# the alien plane-thing can spin really fast
# but it can't jump

