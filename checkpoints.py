# Kaidun (by HktOverload)

import numpy as np

from math import atan2, copysign
import random

from cpu_geom import Geometry, FillWith
import cpu_linalg
from color_utils import unhexify
from terrain_graph_utils import dist

class Checkpoints(object):
    __slots__ = ('items', 'edge')
    count = 10

    def __init__(self, items, edge):
        self.items = items
        self.edge = edge

    def __iter__(self):
        for checkpoint in self.items:
            yield checkpoint

    @classmethod
    def selectForEdge(cls, edge):
        numSteps = 10 * cls.count
        step = 1. / numSteps
        stepDistance = dist(edge.src, edge.dst)
        radsPerMeter = 0.002
        stepRoll = stepDistance * radsPerMeter
        roll = 0.0
        indices = {
            random.randrange(10, numSteps)
            for _ in range(cls.count)
        }
        L = []
        for i in range(10, numSteps):
            signSource = random.random() - 0.5
            roll += copysign(stepRoll, signSource)
            if abs(roll) > np.pi:
                roll = copysign(0.4, signSource)
            if i in indices:
                L.append(
                    Checkpoint(i * step, roll)
                )
        res = cls(L, edge)
        print('--- new checkpoints ---')
        for checkpoint in res:
            print(f'| ~> {checkpoint}')
        print('--- end checkpoints ---')
        return res

    def asGeometry(self):
        return np.hstack([
            checkpoint.assemble(self.edge)
            for checkpoint in self.items
        ])

class Checkpoint(object):
    __slots__ = ('t', 'roll')

    def __init__(self, t, roll):
        self.t = t
        self.roll = roll

    def __repr__(self):
        c = self.__class__.__name__
        return f'{c}(t={self.t}, roll={self.roll})'

    def assemble(self, edge):
        pos = edge.atT(self.t)
        sx, sy = 0.2, 0.4
        z = 0
        (x, y) = edge.heading()
        theta = atan2(y, x)
        theta += 3*np.pi/2
        verts = [(-sx, 0, z), (sx, 0, z), (0, sy, z)]
        verts = [
            cpu_linalg.rotMat(theta, self.roll, 0.) * i
            for i in verts
        ]
        tri = [ j for i in verts for j in i ]
        tri = [tri]
        geom = Geometry(
            np.array(tri, dtype='f4'),
            FillWith(
                *unhexify(0xFF0000),
                0.0,
                dtype='f4',
            ),
        )
        return geom.place((*pos, +0.25))

