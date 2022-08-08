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
    r = x >> 0o100 & 0xFF
    g = x >> 0o010 & 0xFF
    b = x >> 0o000 & 0xFF
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
        raise Exception(
            f"`{cls.__name__}` cannot have geometry state `{geometryState}`"
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

