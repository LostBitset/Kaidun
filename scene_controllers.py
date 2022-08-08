import abc

import cpu_linalg

class SceneController(abc.ABC):

    @classmethod
    def shaderUpdates(cls, gamedata):
        return dict()

    @classmethod
    def frame(cls, gamedata, ftime):
        pass

    @classmethod
    def handle(cls, gamedata, event):
        pass

class MovingCamera(SceneController):

    @classmethod
    def shaderUpdates(cls, gamedata):
        yaw, pitch, roll = gamedata['cam_rot']
        return {
            'cam_ctr': gamedata['cam_ctr'],
            'cam_yaw': yaw,
            'cam_pitch': pitch,
            'cam_roll': roll,
            **super().shaderUpdates(gamedata),
        }

    @classmethod
    def frame(cls, gamedata, ftime):
        ctr = gamedata['cam_ctr']
        dctr = cpu_linalg.add(
            gamedata.get('d_cam_ctr_abs', cpu_linalg.ZeroVec),
            cls.cameraRotation(gamedata) * gamedata['d_cam_ctr_rel'],
        )
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
        super().frame(gamedata, ftime)

    @classmethod
    def handle(cls, gamedata, event):
        super().handle(gamedata, event)

class CameraMotion(MovingCamera):

    @classmethod
    def cameraRotation(cls, gamedata):
        return cpu_linalg.rotMat(
            *gamedata['cam_rot'],
        )

    @classmethod
    def updateCameraMove(cls, gamedata, x, y, z, a, b, c):
        drot = gamedata['d_cam_rot']
        dctr = gamedata['d_cam_ctr_rel']
        dctr = (
            (dctr[0] + x) if x != None else 0.0,
            (dctr[1] + y) if y != None else 0.0,
            (dctr[2] + z) if z != None else 0.0,
        )
        gamedata['d_cam_ctr_rel'] = dctr
        gamedata['d_cam_rot'] = (
            (drot[0] + a) if a != None else 0.0,
            (drot[1] + b) if b != None else 0.0,
            (drot[2] + c) if c != None else 0.0,
        )

    @classmethod
    def handle(cls, gamedata, event):
        tspeed, rspeed = 0.1, 0.03
        movement = {
            'a':        (+tspeed, 0, 0, 0, 0, 0),
            'd':        (-tspeed, 0, 0, 0, 0, 0),
            'w':        (0, 0, +tspeed, 0, 0, 0),
            's':        (0, 0, -tspeed, 0, 0, 0),
            'up':       (0, 0, 0, +rspeed, 0, 0),
            'down':     (0, 0, 0, -rspeed, 0, 0),
            'left':     (0, 0, 0, 0, +rspeed, 0),
            'right':    (0, 0, 0, 0, -rspeed, 0),
            'o':        (0, 0, 0, 0, 0, +rspeed),
            'p':        (0, 0, 0, 0, 0, -rspeed),
        }
        for k, args in movement.items():
            if event.isKeypress(key=k):
                cls.updateCameraMove(
                    gamedata,
                    *[
                        float(i)
                        for i in args
                    ],
                )
            if event.isKeyrelease(key=k):
                cls.updateCameraMove(
                    gamedata,
                    *[
                        (0.0 if i == 0 else None)
                        for i in args
                    ],
                )
        super().handle(gamedata, event)

class CameraMotionAxisAlternatives(CameraMotion, abc.ABC):

    @classmethod
    def getCamX(cls, gamedata, *_):
        return gamedata['cam_ctr'][0]

    @classmethod
    def getCamY(cls, gamedata, *_):
        return gamedata['cam_ctr'][1]

    @classmethod
    def getCamZ(cls, gamedata, *_):
        return gamedata['cam_ctr'][2]

    @classmethod
    def frame(cls, gamedata, ftime):
        gamedata['cam_ctr'] = (
            cls.getCamX(gamedata, ftime),
            cls.getCamY(gamedata, ftime),
            cls.getCamZ(gamedata, ftime),
        )

class GravityBoundPlayer(CameraMotionAxisAlternatives):

    @classmethod
    def getCamZ(cls, gamedata, *_):
        return gamedata.get('z', 0.0)

    @classmethod
    def frame(cls, gamedata, ftime):
        boundary = gamedata['current_terrain_height']
        boundary += gamedata['player_height']
        boundary += gamedata['cam_near']
        if gamedata['z'] < boundary:
            print('fallin')
            gamedata['vel_gravity'] = 0.0
            gamedata['z'] = 0.0
        else:
            gamedata['vel_gravity'] -= (ftime ** 2) * 9.8
            gamedata['z'] = gamedata.get('z', 0.0)
            gamedata['z'] += gamedata['vel_gravity']
        super().frame(gamedata, ftime)

