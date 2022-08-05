# Kaidun (by HktOverload)

import abc

import numpy as np

import cpu_geom
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
        if geometryState == "I'm a cube!":
            return cls.assembleCube()
        raise Exception(
            f"`{cls.__name__}` cannot have geometry state `{geometryState}`"
        )
    
    @classmethod
    def getController(cls, *_):
        return scene_controllers.GravityBoundPlayer
