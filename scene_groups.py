# Kaidun (by HktOverload)

import numpy as np

import scenes as s
import scene_controllers as c

# The geometryState of a group of scenes is a StateGroup
# object that contains all of the other geometryStates
# Each invocation of buildGeometry only sees the geometryState
# for it's own class, this never gets passed to a buildGeometry
# function of the members of the group
class StateGroup(object):
    __slots__ = ('states',)

    def __init__(self, states):
        self.states = states

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.states == other.states

    def __iter__(self):
        for i in self.states:
            yield i

def groupOldControllers(*classes):
    # This class is defined when you call the outer function
    class Inner_SceneGroupController(c.SceneController):

        @classmethod
        def shaderUpdates(cls, gamedata):
            updates, seenControllers = dict(), set()
            for i in classes:
                controller = i.getController(gamedata)
                if controller in seenControllers:
                    continue
                seenControllers.add(controller)
                updates |= controller.shaderUpdates(gamedata)
            return updates

        @classmethod
        def frame(cls, gamedata, ftime):
            seenControllers = set()
            for i in classes:
                controller = i.getController(gamedata)
                if controller in seenControllers:
                    continue
                seenControllers.add(controller)
                controller.frame(gamedata, ftime)

        @classmethod
        def handle(cls, gamedata, event):
            seenControllers = set()
            for i in classes:
                controller = i.getController(gamedata)
                if controller in seenControllers:
                    continue
                seenControllers.add(controller)
                controller.handle(gamedata, event)

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
            return np.hstack([
                i.buildGeometry(substate)
                for i, substate in geometryState
            ])

        @classmethod
        def getController(cls, gamedata):
            return Inner_SceneGroupController

    return Inner_SceneGroup

def group(*classes, controller=None):
    if controller == None:
        raise Exception(
            'You must pass in a controller to the new group method'
        )
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
            return np.hstack([
                i.buildGeometry(substate)
                for i, substate in geometryState
            ])

        @classmethod
        def getController(cls, gamedata):
            return controller

    return Inner_SceneGroup

TwoCubes = group(s.CubeScene1, s.CubeScene2, controller=c.movementWithKeys)

