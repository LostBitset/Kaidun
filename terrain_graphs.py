# Kaidun (by HktOverload)

from functools import reduce
import math
from numpy import pi

import cpu_linalg
from graphs import DirectedEdgeIn2D

# A version of the math.hypot function that
# takes a list instead of the coordinates
# as arguments directly
def hypot(xs):
    return math.hypot(*xs)

# Both a and b must be unit vectors
# [: Citation https://en.wikipedia.org/wiki/Cosine_similarity :]
def angle(a, b):
    return math.acos(cpu_linalg.dot(a, b))

# Both v1 and v2 must be unit vectors
# This is a handy routine I created that
# ^^^-(v2)-__
# -(a)------O
#           ^^---__(v1)__
# just checks if the sum of the angles
# (a -> v1) and (v1 -> v2) are greater than 180
# degs
# This fails if both (v1) and (v2) are on the same
# side of (a)
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

# Find the incenter of a triangle
# Representation as barycentric coordinates found here:
# [: Citation (repeat) https://mathworld.wolfram.com/BarycentricCoordinates.html :]
def incenter(tri):
    side0 = dist(tri[1], tri[2])
    side1 = dist(tri[0], tri[2])
    side2 = dist(tri[0], tri[1])
    return fromBarycentric(tri, [
        side0,
        side1,
        side2,
    ])

# The minimum distance to a side of the triangle
# This is used for generating terrain heightmaps
def minSideDist(tri, pt):
    edgecls = DirectedEdgeIn2D
    sides = [
        edgecls(tri[1], tri[2]),
        edgecls(tri[0], tri[2]),
        edgecls(tri[0], tri[1]),
    ]
    return min(
        distToSegment(edge, pt)
        for edge in sides
    )

