# Kaidun (by HktOverload)

from terrain_graph_utils import dist, distToSegment
import triangulations

class Heightmap(object):
    __slots__ = ('edges', 'memo', 'triangulation')
    # The property edges is a list of EdgeIn2D objects

    def __init__(self, edges, triangulation):
        self.edges = edges
        print(self.edges)
        self.triangulation = triangulation
        self.memo = dict()

    def get(self, pos):
        if pos in self.memo:
            return self.memo[pos]
        else:
            res = self.getValue(
                pos,
                self.getTri(pos)
            )
            res -= 0.5
            res *= 2.0
            res -= 2.0
            self.memo[pos] = res
            return res

    def getValue(self, pos, tri):
        '''
        top3 = [None, None, None]
        for idx in range(0, 3):
            best = None
            for edge in self.edges:
                edge = edge.toDirectedND()
                score = dist(edge.midpoint(), pos)
                if best == None or score < best:
                    if edge not in top3:
                        best = score
                        top3[idx] = edge
        '''
        if tri == None:
            return 0.0
        minDist = min(
            distToSegment(
                edge,
                pos,
            )
            for edge in tri
        )
        skipThresh = 0.5
        res = minDist
        if minDist < skipThresh + 0.1:
            return 1.0
        '''
        res = 1.0
        for edge in self.edges:
            for vert in edge:
                if dist(vert, pos) < 3.0:
                    res = 0.0
        '''
        res = max(0., min(1., res))
        res = 1. - res
        res *= 2.1
        for edge in self.edges:
            for vert in edge:
                distance = dist(vert, pos)
                thresh = 2.5
                if distance < thresh:
                    fac = (thresh - distance) / thresh
                    res *= 1. + (0.5 * fac)
        res = max(0., min(1., res))
        return res

    def getTri(self, pos):
        return triangulations.getCell(
            self.triangulation,
            pos
        )

def fromGraph(graph, triangulation):
    allEdges = set()
    for edges in graph.adjDict.values():
        allEdges.update(edges)
    return Heightmap(list(allEdges), triangulation)

