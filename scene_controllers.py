# Kaidun (by HktOverload)

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
    rspeed = 0.1
    posKeys = ['up', 'left', 'o']
    negKeys = ['down', 'right', 'p']
    drot = list(gamedata['d_cam_rot'])
    for ax in range(3):
        if event.isKeypress(posKeys[ax]):
            drot[ax] += rspeed
        elif event.isKeypress(negKeys[ax]):
            drot[ax] -= rspeed
        else:
            isRelease = False
            isRelease |= event.isKeyrelease(posKeys[ax])
            isRelease |= event.isKeyrelease(negKeys[ax])
            if isRelease:
                drot[ax] = 0
    gamedata['d_cam_rot'] = tuple(drot)

rotationKeys = Mixin(':camera-rot', {
    'handle': handleRotation,
})

movementWithKeys = Mixin().use(
    rotationKeys,
    movement,
)

