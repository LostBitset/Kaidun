# Kaidun (by HktOverload)

from math import copysign
import random

class Checkpoints(object):
    __slots__ = ('items',)
    count = 3

    def __init__(self, items):
        self.items = items

    @classmethod
    def selectForEdge(cls, edge, numSteps=10):
        step = 1. / numSteps
        stepDistance = edge.length()
        radsPerMeter = 1.0
        stepRoll = stepDistance * radsPerMeter
        roll = 0.0
        indices = {
            random.randrange(0, numSteps)
            for _ in range(cls.count)
        }
        res = []
        for i in range(numSteps):
            if i in indices:
                res.append(
                    Checkpoint(i * step, roll)
                )
            signSource = random.random() - 0.5
            roll += copysign(stepRoll, signSource)
        return cls(res)

class Checkpoint(object):
    __slots__ = ('t', 'roll')

    def __init__(self, t, roll):
        self.t = t
        self.roll = roll

