# Kaidun (by HktOverload)

from cpu_geom import Geometry
import scenes as s
import scene_controllers as c

class StateGroup(object):
    __slots__ = ('states',)

    def __init__(self, states):
        self.states = states

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        self.states == other.states

def group(*classes):
    # This class is defined when you call the outer function
    class Inner_SceneGroupController(c.SceneController):

        @classmethod
        def shaderUpdates(cls, gamedata):
            updates, seenControllers = dict(), set()
            for i in classes:
                controller = i.getController(gamedata)
                if i in seenControllers:
                    continue
                seenControllers.add(controller)
                updates |= controller.shaderUpdates(gamedata)
            return updates

        @classmethod
        def frame(cls, gamedata, ftime):
            for i in classes:
                i.frame(gamedata, ftime)

        @classmethod
        def handle(cls, gamedata, event):
            for i in classes:
                i.handle(gamedata, event)

    # This class is defined when you call the outer function
    class Inner_SceneGroup(s.Scene):

        @classmethod
        def geometryState(cls, gamedata):
            return StateGroup([
                (
                    i,
                    i.geometryState(gamedata)
                )
                for i in classes
            ])

        @classmethod
        def buildGeometry(cls, geometryState):
            return Geometry.merge([
                i.buildGeometry(substate)
                for i, substate in geometryState
            ])

        @classmethod
        def getController(cls, gamedata):
            return Inner_SceneGroupController

    return Inner_SceneGroup

TwoCubes = group(s.CubeScene1, s.CubeScene2)

