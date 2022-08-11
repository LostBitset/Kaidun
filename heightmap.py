# Kaidun (by HktOverload)

from terrain_graph_utils import distToSegment

class Heightmap(object):
    __slots__ = ('edges', 'memo')  # A list of EdgeIn2D objects

    def __init__(self, edges):
        self.edges = edges
        self.memo = dict()

    def get(self, pos):
        if pos in self.memo:
            return self.memo[pos]
        else:
            res = self.getValue(pos)
            res -= 0.5
            res *= 2.0
            res -= 2.0
            self.memo[pos] = res
            return res

    def getValue(self, pos):
        minDist = min(
            distToSegment(
                edge.toDirectedND(),
                pos,
            )
            for edge in self.edges
        )
        return max(0., min(1., minDist))

def fromGraph(graph):
    allEdges = set()
    for edges in graph.adjDict.values():
        allEdges.update(edges)
    return Heightmap(list(allEdges))

