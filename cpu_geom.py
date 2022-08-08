# Kaidun (by HktOverload)

import numpy as np

def triNormal(tri):
    a1 = tri[3] - tri[0]
    a2 = tri[4] - tri[1]
    a3 = tri[5] - tri[2]
    b1 = tri[6] - tri[0]
    b2 = tri[7] - tri[1]
    b3 = tri[8] - tri[2]
    return (
        (a2*b3) - (a3*b2),
        (a3*b1) - (a1*b3),
        (a1*b2) - (a2*b1),
    )

class Geometry(object):
    __slots__ = ('tris',)

    def __init__(self, tris):
        self.tris = tris

    def __or__(self, other):
        return Geometry(
            np.vstack((
                self.tris,
                other.tris,
            ))
        )

    def place(self, loc):
        L = []
        for tri in self.tris:
            normal = triNormal(tri)
            for i in range(0, 9, 3):
                coord = tri[i:(i + 3)]
                L.extend((
                    coord[0] + loc[0],
                    coord[1] + loc[1],
                    coord[2] + loc[2],
                ))
                L.extend(normal)
        return np.array(L, dtype='f4')

