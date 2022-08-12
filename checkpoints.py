# Kaidun (by HktOverload)

from math import copysign
import random

from terrain_graph_utils import dist

class Checkpoints(object):
    __slots__ = ('items',)
    count = 3

    def __init__(self, items):
        self.items = items

    @classmethod
    def selectForEdge(cls, edge, numSteps=10):
        step = 1. / numSteps
        stepDistance = dist(edge.src, edge.dst)
        radsPerMeter = 1.0
        stepRoll = stepDistance * radsPerMeter
        roll = 0.0
        indices = {
            random.randrange(0, numSteps)
            for _ in range(cls.count)
        }
        L = []
        for i in range(numSteps):
            if i in indices:
                L.append(
                    Checkpoint(i * step, roll)
                )
            signSource = random.random() - 0.5
            roll += copysign(stepRoll, signSource)
        res = cls(L)
        print(f'~> new checkpoints: {res}')
        return res

class Checkpoint(object):
    __slots__ = ('t', 'roll')

    def __init__(self, t, roll):
        self.t = t
        self.roll = roll

