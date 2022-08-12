# Kaidun (by HktOverload)

import delaunay
from graphs import Graph, EdgeIn2D
import terrain_graph_utils as u

import random

def makeWorldGraph():
    pts = sample1x1()
    superTri = ((-1, 1), (1, -1), (1, 1))
    triangulation = delaunay.boyerWatson(pts, superTri)
    scaled = ScaledTriangulation(triangulation)
    while hasFalseValleys(scaled):
        scaled.fac += 0.2
    return graphOfTriangulation(scaled)

