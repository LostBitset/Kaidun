import abc
import math

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
            **super().shaderUpdates(gamedata),
            'cam_ctr': gamedata['cam_ctr'],
            'cam_yaw': yaw,
            'cam_pitch': pitch,
            'cam_roll': roll,
        }

    @classmethod
    def frame(cls, gamedata, ftime):
        super().frame(gamedata, ftime)
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
    def cameraRotation(cls, gamedata):
        return cpu_linalg.rotMat(
            *gamedata['cam_rot'],
        )

    @classmethod
    def updateCameraMove(cls, gamedata, x, y, z, a, b, c):
        dctr = gamedata['d_cam_ctr']
        drot = gamedata['d_cam_rot']
        gamedata['d_cam_ctr'] = (
            (dctr[0] + x) if x != None else 0.0,
            (dctr[1] + y) if y != None else 0.0,
            (dctr[2] + z) if z != None else 0.0,
        )
        gamedata['d_cam_rot'] = (
            (drot[0] + a) if a != None else 0.0,
            (drot[1] + b) if b != None else 0.0,
            (drot[2] + c) if c != None else 0.0,
        )

    @classmethod
    def handle(cls, gamedata, event):
        super().handle(gamedata, event)
        tspeed, rspeed = 0.1, 0.03
        movement = {
            'w':        (+tspeed, 0, 0, 0, 0, 0),
            's':        (-tspeed, 0, 0, 0, 0, 0),
            'a':        (0, +tspeed, 0, 0, 0, 0),
            'd':        (0, -tspeed, 0, 0, 0, 0),
            'e':        (0, 0, +tspeed, 0, 0, 0),
            'c':        (0, 0, -tspeed, 0, 0, 0),
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

class GravityBoundPlayer(CameraMotion):

    @classmethod
    def frame(cls, gamedata, ftime):
        super().frame(gamedata, ftime)
        ctr = gamedata['cam_ctr']
        boundary = gamedata['current_terrain_height']
        boundary += gamedata['player_height']
        boundary += gamedata['cam_near']
        if ctr[1] < boundary:
            gamedata['vel_gravity'] = 0.0
        gamedata['cam_ctr'] = (
            ctr[0],
            ctr[1] + gamedata['vel_gravity'],
            ctr[2],
        )
        gamedata['vel_gravity'] -= (ftime ** 2) * 9.8

