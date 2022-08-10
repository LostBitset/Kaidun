# Kaidun (by HktOverload)

from functools import reduce
from math import arccos, hypot, pi

import cpu_linalg

# Both a and b must be unit vectors
# [: Citation https://en.wikipedia.org/wiki/Cosine_similarity :]
def angle(a, b):
    return arccos(cpu_linalg.dot(a, b))

# Both v1 and v2 must be unit vectors
def onlyOneSide(a, v1, v2):
    theta1 = angle(a, v1)
    theta2 = angle(v1, v2)
    return (theta1 + theta2) > pi

# L2 Distance
def dist(a, b):
    return hypot(
        cpu_linalg.add(
            a, cpu_linalg.neg(b)
        )
    )

# [: Citation https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line :]
def distToSegment(dEdge, pt):
    a, b = dEdge.src, dEdge.dst
    numer = abs(
        (
            (b[0]-a[0]) * (a[1]-pt[1])
        ) - (
            (a[0]-pt[0]) * (b[1]-a[1])
        )
    )
    denom = dist(a, b)
    return numer / denom

# Barycentric coordinates
# (convert from barycentric to cartesian coords)
# [: Citation https://mathworld.wolfram.com/BarycentricCoordinates.html :]
def fromBarycentric(tri, barycentric):
    total = sum(barycentric)
    areal = [ i / total for i in barycentric ]
    weightedVertices = (
        cpu_linalg.sc(vert, weight)
        for vert, weight in zip(tri, areal)
    )
    return reduce(
        cpu_linalg.add,
        weightedVertices,
        cpu_linalg.ZeroVec,
    )

