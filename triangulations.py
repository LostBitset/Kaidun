# Kaidun (by HktOverload)

import cpu_linalg

# During Bowyer-Watson, only three
# extra vertices are ever added, so
# this is (I think) more memory efficient
# than a set of tuples or something
class Triangulation(object):
    __slots__ = ('verts', 'toVerts', 'refs', 'counter')

    def __init__(self):
        self.verts = dict()  # maps points to IDs
        self.toVerts = dict()  # maps IDs to points
        self.refs = set()  # set of 3-tuples of IDs
        self.counter = 0  # Keep track of IDs

    def addTri(self, tri):
        ids = []
        for vert in tri:
            if vert not in self.verts:
                self.verts[vert] = self.counter
                self.toVerts[self.counter] = vert
                self.counter += 1
            ids.append(self.verts[vert])
        self.refs.add(tuple(ids))

    def dropTri(self, tri):
        ids = [ self.verts[vert] for vert in tri ]
        self.refs.discard(tuple(ids))

    def dropVertex(self, vert):
        badID = self.verts.pop(vert)
        for tri in self.refs:
            if badID in tri:
                self.refs.discard(tri)

    # Convert member of self.refs
    # to the actual triangle
    def getTri(self, tri):
        return (
            self.toVerts[tri[0]],
            self.toVerts[tri[1]],
            self.toVerts[tri[2]],
        )

    def __iter__(self):
        for triRef in self.refs:
            yield self.getTri(triRef)

# Represents a scaled view into a triangulation
class ScaledView(object):
    __slots__ = ('triangulation', 'fac')

    def __init__(self, triangulation):
        self.triangulation = triangulation
        self.fac = 1.

    def getTri(self, tri):
        return [
            cpu_linalg.sc(
                self.triangulation.toVerts[tri[ax]],
                self.fac,
            )
            for ax in range(3)
        ]

    def __iter__(self):
        for triRef in self.triangulation.refs:
            yield self.getTri(triRef)

