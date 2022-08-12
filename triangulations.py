# Kaidun (by HktOverload)

import cpu_linalg
from graphs import Graph, EdgeIn2D

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

def edgeTuples(tri):
    yield (tuple(tri[1]), tuple(tri[2]))
    yield (tuple(tri[0]), tuple(tri[2]))
    yield (tuple(tri[0]), tuple(tri[1]))

def toGraph(triangulation):
    res = Graph()
    verts = set()
    for tri in triangulation:
        for edge in edgeTuples(tri):
            for vert in edge:
                if vert not in verts:
                    verts.add(vert)
                    res.addNode(vert)
            res.addEdge(
                EdgeIn2D(edge[0], edge[1])
            )
    return res

# Formula for conversion into barycentric coorinates found here:
# [: Citation https://stackoverflow.com/questions/13300904/determine-whether-point-lies-inside-triangle :]
def toBarycentric(tri, x):
    a, b, c = tri[0], tri[1], tri[2]
    alpha = ((b[1]-c[1])*(x[0]-c[0])) + ((c[0]-b[0])*(x[1]-c[1]))
    alpha /= ((b[1]-c[1])*(a[0]-c[0])) + ((c[0]-b[0])*(a[1]-c[1]))
    beta = ((c[1]-a[1])*(x[0]-c[0])) + ((a[0]-c[0])*(x[1]-c[1]))
    beta /= ((b[1]-c[1])*(a[0]-c[0])) + ((c[0]-b[0])*(a[1]-c[1]))
    gamma = 1. - alpha - beta
    return alpha, beta, gamma

# See toBarycentric function for citation and where I got this useful routine
def insideTri(tri, x):
    barycentric = toBarycentric(tri, x)
    return all(
        baryCoord > 0 for baryCoord in barycentric
    )

# Get the triangle which a given point is inside of
# (from a triangulation)
def getCell(triangulation, pt):
    for tri in triangulation:
        if insideTri(tri, pt):
            return tri
    return None

