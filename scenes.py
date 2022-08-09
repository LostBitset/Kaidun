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

class CubeScene(Scene):
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
    def geometryState(cls, gamedata):
        return 'cubey boi'

    @classmethod
    def buildGeometry(cls, geometryState):
        if geometryState != 'cubey boi':
            return cls.cube.place(geometryState['origin'])
        raise Exception(
            f"`{cls.__name__}` cannot have geometry state `{geometryState}`"
        )

    @classmethod
    def getController(cls, *_):
        return c.movementWithKeys

