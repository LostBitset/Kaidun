# Kaidun (by HktOverload)

import numpy as np

# Find the normal vector of a triangle
# [: Citation https://web.ma.utexas.edu/users/m408m/Display12-5-4.shtml :]
# [: Citation https://people.eecs.ku.edu/~jrmiller/Courses/VectorGeometry/VectorOperations.html :]
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

class FillWith(object):
    __slots__ = ('array',)

    def __init__(self, *contents, **kwargs):
        self.array = np.array(
            contents,
            **kwargs,
        )

    def make(self, length):
        return np.tile(
            self.array,
            length,
        ).reshape(
            (length, self.array.size)
        )

class Geometry(object):
    __slots__ = ('tris', 'aux')

    def __init__(self, tris, aux):
        self.tris = tris
        if isinstance(aux, FillWith):
            self.aux = aux.make(len(tris) * 3)
        else:
            self.aux = aux

    # Overload the | operator to merge geometry,
    # just like the union for sets
    def __or__(self, other):
        return Geometry(
            np.vstack((
                self.tris,
                other.tris,
            )),
            np.vstack((
                self.aux,
                other.aux,
            )),
        )

    # Place the geometry in the world
    # This translates it from the tris 2D array
    # and the aux 2D array to a 1D array that will
    # be the new contents of the GPU vertex buffer
    # See mglw_main.py for the format
    # See vbo_utils.py for other vertex buffer stuff
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
        geometryPart = np.array(L, dtype='f4')
        shapeRank2 = (len(geometryPart)//6, 6)
        geometryPart = geometryPart.reshape(shapeRank2)
        allRank2 = np.hstack((
            geometryPart,
            self.aux,
        ))
        return allRank2.reshape((allRank2.size,))

    def placeAbsolute(self):
        return self.place((0, 0, 0))  # TODO use ZeroVec here

