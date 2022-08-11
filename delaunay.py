# Kaidun (by HktOverload)

'''
This is an implementation ofthe Bowyer-Watson algorithm for finding
the Delaunay Triangulation (DT) of a set of points.
In this case, we're in 2D.
Based off of the explanation and pseudocode at:
[: Citation https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm :]
'''

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

# Formula found here:
# [: Citation https://algs4.cs.princeton.edu/91primitives/ :]
def isCCW(tri):
    a = tri[0]
    b = tri[1]
    c = tri[2]
    det = (b[0] - a[0]) * (c[1] - a[1])
    det -= (c[0] - a[0]) * (b[1] - a[1])
    return det > 0

# Formula found here:
# [: Citation https://planetcalc.com/157/ :]
def det3x3(a, b, c, d, e, f, g, h, i):
    return (a*e*i) - (a*f*h) - (b*d*i) + (b*f*g) + (c*d*h) - (c*e*g)

# Formula found here:
# [: Citation https://en.wikipedia.org/wiki/Delaunay_triangulation :]
def pointInCircumcircle(pt, tri):
    if not isCCW(tri):
        tri = list(reversed(tri))
    a, b, c, d = tri[0], tri[1], tri[2], pt
    det = det3x3(
        (a[0] - d[0]), (a[1] - d[1]),
        (a[0]**2 - d[0]**2) + (a[1]**2 - d[1]**2),
        (b[0] - d[0]), (b[1] - d[1]),
        (b[0]**2 - d[0]**2) + (b[1]**2 - d[1]**2),
        (c[0] - d[0]), (c[1] - d[1]),
        (c[0]**2 - d[0]**2) + (c[1]**2 - d[1]**2),
    )
    return det > 0

def edgesOf(tri):
    yield {tri[1], tri[2]}
    yield {tri[0], tri[2]}
    yield {tri[1], tri[2]}

# See citation at top of file
def boyerWatson(points, supertri):
    print('Starting boyerWatson...')
    triangulation = Triangulation()
    triangulation.addTri(supertri)
    for point in points:
        badTriangles = {
            tri
            for tri in triangulation
            if pointInCircumcircle(point, tri)
        }
        print(f'#badTriangles is {len(badTriangles)}', end=' ')
        polygon = {
            badEdge
            for badTri in badTriangles
            for badEdge in edgesOf(badTri)
            if not any(
                badEdge == badEdge2
                for badTri2 in badTriangles
                for badEdge2 in edgesOf(badTri2)
            )
        }
        print(f'polygon={polygon}')
        for badTri in badTriangles:
            triangulation.dropTri(badTri)
        for edge in polygon:
            newTri = [point, *edge]
            print('adding tri')
            triangulation.addTri(newTri)
    for tri in triangulation:
        for vert in tri:
            if vert in supertri:
                triangulation.dropTri(tri)
    return triangulation

