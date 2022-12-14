# Kaidun (by HktOverload)

import delaunay
import false_valley_checker
import triangulations
import terrain_graph_utils as u

import random

nodeCount = 10

def makeWorldGraph():
    pts = sample1x1(nodeCount)
    superTri = ((-1, 1), (1, -1), (1, 1))
    triangulation = delaunay.boyerWatson(pts, superTri)
    print(triangulation)
    scaled = triangulations.ScaledView(triangulation)
    while not false_valley_checker.ok(scaled):
        scaled.fac += 0.2
    print(f'makeWorldGraph> FOUND SCALE FACTOR: {scaled.fac}')
    return scaled, triangulations.toGraph(scaled)

def random1x1():
    return (
        random.random(),
        random.random(),
    )

def sample1x1(nodeCount, thresh=0.07):
    extras = nodeCount
    pts = [
        random1x1()
        for _ in range(nodeCount + extras)
    ]
    count = 0
    done = False
    while not done:
        done = True
        badIndices = set()
        for a in range(len(pts)):
            for b in range(len(pts)):
                if a != b and a not in badIndices and b not in badIndices:
                    if u.dist(pts[a], pts[b]) < thresh:
                        badIndices.add(a)
                        done = False
        count += 1
        if len(badIndices) > extras:
            for idx in badIndices:
                pts[idx] = random1x1()
        else:
            done = True
    finalPts, idx = [], 0
    while len(finalPts) < nodeCount:
        if idx not in badIndices:
            finalPts.append(pts[idx])
        idx += 1
    print(f'<sample1x1> ok ({count} total O(n^2) loops)')
    return finalPts

