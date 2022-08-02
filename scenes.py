# Kaidun (by HktOverload)

import abc

import numpy as np

import cpu_geom

class Scene(abc.ABC):    

    @classmethod
    @abc.abstractmethod
    def geometryState(cls, gamedata):
        pass

    @classmethod
    @abc.abstractmethod
    def buildGeometry(cls, geometryState):
        pass

    @classmethod
    @abc.abstractmethod
    def getController(cls, gamedata):
        pass

class SceneController(abc.ABC):

    @classmethod
    def shaderUpdates(cls, gamedata):
        return dict()

    @classmethod
    def frame(cls, gamedata):
        pass

    @classmethod
    def handle(cls, gamedata, event):
        pass

class MovingCamera(SceneController):

    @classmethod
    def shaderUpdates(cls, gamedata):
        yaw, pitch, roll = gamedata['cam_rot']
        return {
            **super().shaderUpdates(gamedata),
            'cam_ctr': gamedata['cam_ctr'],
            'cam_yaw': yaw,
            'cam_pitch': pitch,
            'cam_roll': roll,
        }

    @classmethod
    def frame(cls, gamedata):
        super().frame(gamedata)
        ctr, dctr = gamedata['cam_ctr'], gamedata['d_cam_ctr']
        rot, drot = gamedata['cam_rot'], gamedata['d_cam_rot']
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
    
    @classmethod
    def handle(cls, gamedata, event):
        super().handle(gamedata, event)

class CameraMotion(MovingCamera):
    
    @classmethod
    def handle(cls, gamedata, event):
        super().handle(gamedata, event)
        tspeed, rspeed = 0.1, 0.03
        movement = {
            'w':        (0, 0, +tspeed, 0, 0, 0),
            'a':        (+tspeed, 0, 0, 0, 0, 0),
            's':        (0, 0, -tspeed, 0, 0, 0),
            'd':        (-tspeed, 0, 0, 0, 0, 0),
            'e':        (0, +tspeed, 0, 0, 0, 0),
            'c':        (0, -tspeed, 0, 0, 0, 0),
            'up':       (0, 0, 0, +rspeed, 0, 0),
            'down':     (0, 0, 0, -rspeed, 0, 0),
            'left':     (0, 0, 0, 0, +rspeed, 0),
            'right':    (0, 0, 0, 0, -rspeed, 0),
            'o':        (0, 0, 0, 0, 0, +rspeed),
            'p':        (0, 0, 0, 0, 0, -rspeed),
        }
        for k, args in movement.items():
            if event.isKeypress(key=k):
                cls.updateCameraMove(*[
                    float(i) \
                        for i in args
                ])
            if event.isKeyrelease(key=k):
                cls.updateCameraMove(*[
                    (0.0 if i == 0 else None) \
                        for i in args
                ])

class CubeScene(Scene):
    cube = [
        (0, 0, 0, 1, 0, 0, 1, 1, 0), (0, 0, 0, 0, 1, 0, 1, 1, 0),
        (0, 0, 1, 1, 0, 1, 1, 1, 1), (0, 0, 1, 0, 1, 1, 1, 1, 1),

        (0, 0, 0, 0, 1, 0, 0, 1, 1), (0, 0, 0, 0, 0, 1, 0, 1, 1),
        (1, 0, 0, 1, 1, 0, 1, 1, 1), (1, 0, 0, 1, 0, 1, 1, 1, 1),

        (0, 0, 0, 0, 0, 1, 1, 0, 1), (0, 0, 0, 1, 0, 0, 1, 0, 1),
        (0, 1, 0, 0, 1, 1, 1, 1, 1), (0, 1, 0, 1, 1, 0, 1, 1, 1),
    ]
    
    @classmethod
    def assembleCube(cls):
        L = []
        for tri in cls.cube:
            normal = cpu_geom.triNormal(tri)
            for i in range(0, 9, 3):
                coord = tri[i : i + 3]
                L.extend(coord)
                L.extend(normal)
        return np.array(L, dtype='f4')

    @classmethod
    def geometryState(cls, *_):
        return "I'm a cube!"

    @classmethod
    def buildGeometry(cls, geometryState):
        if geometryState == "I'm a cube":
            return cls.assembleCube()
        raise Exception(
            f"`{cls.__name__}` cannot have geometry state `{geometryState}`"
        )
    
    @classmethod
    def getController(cls, *_):
        return CameraMotion
