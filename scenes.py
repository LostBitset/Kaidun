# Kaidun (by HktOverload)

import abc

import numpy as np

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

def unhexify(x):
    r = x >> 0o20 & 0xFF
    g = x >> 0o10 & 0xFF
    b = x >> 0o00 & 0xFF
    r /= 0xFF
    g /= 0xFF
    b /= 0xFF
    return (r, g, b)

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

class WorldScene(Scene):

    @classmethod
    def geometryState(cls, gamedata):
        worldGeometry = gamedata['world_geometry']
        chunkSize = worldGeometry.ccfg.size
        playerChunk = (
            gamedata['cam_ctr'][0] // chunkSize,
            gamedata['cam_ctr'][1] // chunkSize,
        )
        return (
            '~worldGeometryRef',
            worldGeometry,
            playerChunk,
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
        playerChunk = geometryState[2]
        geometry = worldGeometry.geometryInChunk((0, 0, 0))
        return geometry.placeAbsolute()

    @classmethod
    def getController(cls, gamedata):
        return c.movementWithKeys

