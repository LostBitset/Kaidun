# Kaidun (by HktOverload)

import abc
from math import sin, cos, atan2

import numpy as np

from color_utils import unhexify
from checkpoints import Checkpoints
from cpu_geom import Geometry, FillWith
import scene_controllers as c

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

class CubeScene(Scene, abc.ABC):
    cube = Geometry(
        np.array((
            (0, 0, 0, 1, 0, 0, 1, 1, 0), (0, 0, 0, 0, 1, 0, 1, 1, 0),
            (0, 0, 1, 1, 0, 1, 1, 1, 1), (0, 0, 1, 0, 1, 1, 1, 1, 1),

            (0, 0, 0, 0, 1, 0, 0, 1, 1), (0, 0, 0, 0, 0, 1, 0, 1, 1),
            (1, 0, 0, 1, 1, 0, 1, 1, 1), (1, 0, 0, 1, 0, 1, 1, 1, 1),

            (0, 0, 0, 0, 0, 1, 1, 0, 1), (0, 0, 0, 1, 0, 0, 1, 0, 1),
            (0, 1, 0, 0, 1, 1, 1, 1, 1), (0, 1, 0, 1, 1, 0, 1, 1, 1),
        ), dtype='f4'),
        FillWith(
            *unhexify(0xDC7633),
            0.0,
            dtype='f4'
        ),
    )

    @classmethod
    def buildGeometry(cls, geometryState):
        if 'origin' in geometryState:
            return cls.cube.place(geometryState['origin'])
        r = f'`{repr(geometryState)}`'
        raise Exception(
            f'`{cls.__name__}` cannot have geometry state {r}'
        )

    @classmethod
    def getController(cls, *_):
        return c.GravityBoundPlayer

class CubeScene1(CubeScene):

    @classmethod
    def geometryState(cls, gamedata):
        return {
            'origin': (0, 0, 0),
        }

class CubeScene2(CubeScene):

    @classmethod
    def geometryState(cls, gamedata):
        return {
            'origin': (3, 3, 3),
        }

class CheckpointScene(Scene):

    @classmethod
    def geometryState(cls, gamedata):
        return gamedata['checkpoints']

    @classmethod
    def buildGeometry(cls, geometryState):
        if not isinstance(geometryState, Checkpoints):
            raise Exception(
                '''
                In {cls.__name__}, geometryState is:
                {geometryState}
                (type {type(geometryState)})
                It must be an instance of Checkpoints
                '''
            )
        return geometryState.asGeometry()

    @classmethod
    def getController(cls, gamedata):
        raise Exception(
            '''
            {cls.__name__} does not specify a controller
            (It is intended to be used in a scene group)
            '''
        )

class WorldScene(Scene):

    @classmethod
    def getPlayerViewCenter(cls, gamedata):
        pos = gamedata['cam_ctr']
        if 'drv_dx' in gamedata:
            dx = gamedata['drv_dx']
            dy = gamedata['drv_dy']
            angle = atan2(dy, dx)
            step = np.pi / 16
            angle = int(angle / step) * step
            fac = 4.0
            return (
                pos[0] + (cos(angle) * fac),
                pos[1] + (sin(angle) * fac),
            )
        else:
            return (pos[0], pos[1])

    @classmethod
    def geometryState(cls, gamedata):
        worldGeometry = gamedata['world_geometry']
        chunkSize = worldGeometry.ccfg.size
        superchunk = chunkSize * 1
        playerViewPos = cls.getPlayerViewCenter(gamedata)
        playerChunk = (
            playerViewPos[0] // superchunk,
            playerViewPos[1] // superchunk,
        )
        return (
            '~worldGeometryRef',
            worldGeometry,
            playerChunk,
            superchunk,
        )

    @classmethod
    def buildGeometry(cls, geometryState):
        typeOk = isinstance(geometryState, tuple)
        if not typeOk or geometryState[0] != '~worldGeometryRef':
            r = f'`{geometryState}`'
            raise Exception(
                f'`{cls.__name__}` cannot have geometry state {r}'
            )
        worldGeometry = geometryState[1]
        superchunk = geometryState[3]
        playerChunk = (
            geometryState[2][0] * superchunk,
            geometryState[2][1] * superchunk,
        )
        print('Calling geometryInChunk...')
        geometry = worldGeometry.geometryInChunk(playerChunk)
        print('done')
        print('Placing geometry...')
        res = geometry.placeAbsolute()
        print('done')
        return res

    @classmethod
    def getController(cls, gamedata):
        return c.movementWithKeys

