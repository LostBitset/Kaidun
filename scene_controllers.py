# Kaidun (by HktOverload)

from math import atan2

import cpu_linalg
from mix import Mixin

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

def frameMovement(gamedata, ftime):
    ctr, rot = gamedata['cam_ctr'], gamedata['cam_rot']
    dctr, drot = gamedata['d_cam_ctr'], gamedata['d_cam_rot']
    gamedata['cam_ctr'] = (
        ctr[0] + dctr[0],
        ctr[1] + dctr[1],
        ctr[2] + dctr[2],
    )
    gamedata['cam_rot'] = (
        rot[0] + drot[0],
        rot[1] + drot[1],
        rot[2] + drot[2],
    )

movement = Mixin(':camera-movement', {
    'frame': frameMovement,
}).use(cameraUpdates)

def handleRotation(gamedata, event):
    rspeed = 0.05
    posKeys = ['up', 'left', 'o']
    negKeys = ['down', 'right', 'p']
    drot = list(gamedata['d_cam_rot'])
    for ax in range(3):
        if event.isKeypress(posKeys[ax]):
            drot[ax] += rspeed
            if ax == 2:
                gamedata['keys_control_yaw'] = True
        elif event.isKeypress(negKeys[ax]):
            drot[ax] -= rspeed
            if ax == 2:
                gamedata['keys_control_yaw'] = True
        else:
            isRelease = False
            isRelease |= event.isKeyrelease(posKeys[ax])
            isRelease |= event.isKeyrelease(negKeys[ax])
            if isRelease:
                drot[ax] = 0
            if ax == 2:
                gamedata['keys_control_yaw'] = False
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

class PController(object):
    __slots__ = ('kP',)

    def __init__(self, kP):
        self.kP = kP

    def get(self, x, setpoint):
        err = x - setpoint
        pComponent = self.kP * err
        return -pComponent

followRotationController = PController(0.1)

def setFollowRotation(gamedata, ftime):
    if gamedata.get('keys_control_yaw', False):
        return
    rot = gamedata['cam_rot']
    drot = list(gamedata['d_cam_rot'])
    edge = gamedata['follow_edge']
    [y, x] = edge.heading()
    setpoint = -atan2(y, x)
    drot[2] = followRotationController.get(rot[2], setpoint)
    gamedata['d_cam_rot'] = tuple(drot)

followRotation = Mixin(':camera-rot-follow', {
    'frame': setFollowRotation,
})

def setFollowTranslation(gamedata, ftime):
    dctr = list(gamedata['d_cam_ctr'])
    ctr = gamedata['cam_ctr']
    tspeed = 0.1
    edge = gamedata['follow_edge']
    if edge.isBeyond(ctr):
        dctr[0] = 0
        dctr[1] = 0
    else:
        heading = edge.heading()
        heading = cpu_linalg.sc(heading, tspeed)
        dctr[0] = heading[0]
        dctr[1] = heading[1]
    gamedata['d_cam_ctr'] = tuple(dctr)

followTranslation = Mixin(':camera-tr-follow', {
    'frame': setFollowTranslation,
})

movementWithKeys = Mixin(':camera-movement-all').use(
    rotationKeys,
    jumping,
    gravity,
    followTranslation,
    followRotation,
    movement,
)

