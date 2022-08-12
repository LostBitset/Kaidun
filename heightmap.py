# Kaidun (by HktOverload)

from terrain_graph_utils import dist, distToSegment

class Heightmap(object):
    __slots__ = ('edges', 'memo')  # A list of EdgeIn2D objects

    def __init__(self, edges):
        self.edges = edges
        print(self.edges)
        self.memo = dict()

    def get(self, pos, tri):
        if pos in self.memo:
            return self.memo[pos]
        else:
            res = self.getValue(pos, tri)
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

def fromGraph(graph):
    allEdges = set()
    for edges in graph.adjDict.values():
        allEdges.update(edges)
    return Heightmap(list(allEdges))

