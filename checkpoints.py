# Kaidun (by HktOverload)

import numpy as np

from math import copysign
import random

from terrain_graph_utils import dist

class Checkpoints(object):
    __slots__ = ('items',)
    count = 10

    def __init__(self, items):
        self.items = items

    def __iter__(self):
        for checkpoint in self.items:
            yield checkpoint

    @classmethod
    def selectForEdge(cls, edge):
        numSteps = 10 * cls.count
        step = 1. / numSteps
        stepDistance = dist(edge.src, edge.dst)
        radsPerMeter = 0.05
        stepRoll = stepDistance * radsPerMeter
        roll = 0.0
        indices = {
            random.randrange(0, numSteps)
            for _ in range(cls.count)
        }
        L = []
        for i in range(numSteps):
            signSource = random.random() - 0.5
            roll += copysign(stepRoll, signSource)
            if abs(roll) > (2. * np.pi):
                roll = copysign(0.4, signSource)
            if i in indices:
                L.append(
                    Checkpoint(i * step, roll)
                )
        res = cls(L)
        print('--- new checkpoints ---')
        for checkpoint in res:
            print(f'| ~> {checkpoint}')
        print('--- end checkpoints ---')
        return res

class Checkpoint(object):
    __slots__ = ('t', 'roll')

    def __init__(self, t, roll):
        self.t = t
        self.roll = roll

    def __repr__(self):
        c = self.__class__.__name__
        return f'{c}(t={self.t}, roll={self.roll})'
