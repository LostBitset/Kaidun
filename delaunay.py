# Kaidun (by HktOverload)

from triangulations import Triangulation

'''
This is an implementation ofthe Bowyer-Watson algorithm for finding
the Delaunay Triangulation (DT) of a set of points.
In this case, we're in 2D.
Based off of the explanation and pseudocode at:
[: Citation https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm :]
'''

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
    yield frozenset([tri[1], tri[2]])
    yield frozenset([tri[0], tri[2]])
    yield frozenset([tri[0], tri[1]])

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
        print(f'badTriangles={badTriangles}')
        '''
        polygon = set()
        for badTri in badTriangles:
            print('e')
            print(list(edgesOf(badTri)))
            edgeSet1 = set(edgesOf(badTri))
            others = badTriangles.difference({badTri})
            edgeSet2 = {
                edge
                for other in others
                for edge in edgesOf(other)
            }
            print('- begin edgesets')
            print(edgeSet1)
            print('-')
            print(edgeSet2)
            print('- end edgesets')
            if len(edgeSet1 & edgeSet2) == 0:
                polygon.update(edgeSet1)
        '''
        polygon = {
            frozenset(badEdge)
            for badTri in badTriangles
            for badEdge in edgesOf(badTri)
            if not any(
                badEdge == badEdge2
                for badTri2 in badTriangles.difference(
                    {badTri}
                )
                for badEdge2 in edgesOf(badTri2)
            )
        }
        print(f'polygon={polygon}')
        for badTri in badTriangles:
            print('-', end=',')
            triangulation.dropTri(badTri)
        for edge in polygon:
            newTri = [point, *edge]
            print('+', end=',')
            triangulation.addTri(newTri)
    # '''
    connectedToSuper = []
    for tri in triangulation:
        for vert in tri:
            if vert in supertri:
                connectedToSuper.append(tri)
    for tri in connectedToSuper:
        triangulation.dropTri(tri)
    # '''
    print(f'total {len(triangulation.refs)}')
    print([ i for i in triangulation ])
    return triangulation

