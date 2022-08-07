# Kaidun (by HktOverload)

import abc

import numpy as np

from cpu_geom import Geometry
import scene_controllers

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

class CubeScene(Scene):
    cube = Geometry(
        np.array((
            (0, 0, 0, 1, 0, 0, 1, 1, 0), (0, 0, 0, 0, 1, 0, 1, 1, 0),
            (0, 0, 1, 1, 0, 1, 1, 1, 1), (0, 0, 1, 0, 1, 1, 1, 1, 1),

            (0, 0, 0, 0, 1, 0, 0, 1, 1), (0, 0, 0, 0, 0, 1, 0, 1, 1),
            (1, 0, 0, 1, 1, 0, 1, 1, 1), (1, 0, 0, 1, 0, 1, 1, 1, 1),

            (0, 0, 0, 0, 0, 1, 1, 0, 1), (0, 0, 0, 1, 0, 0, 1, 0, 1),
            (0, 1, 0, 0, 1, 1, 1, 1, 1), (0, 1, 0, 1, 1, 0, 1, 1, 1),
        ), dtype='f4')
    )

    @classmethod
    def geometryState(cls, *_):
        return "I'm a cube!"

    @classmethod
    def buildGeometry(cls, geometryState):
        if geometryState == "I'm a cube!":
            return cls.cube.place((0, 0, 0))
        raise Exception(
            f"`{cls.__name__}` cannot have geometry state `{geometryState}`"
        )

    @classmethod
    def getController(cls, *_):
        return scene_controllers.GravityBoundPlayer

