# Kaidun (by HktOverload)

from terrain_graph_utils import dist, distToSegment

class Heightmap(object):
    __slots__ = ('edges', 'memo')  # A list of EdgeIn2D objects

    def __init__(self, edges):
        self.edges = edges
        print(self.edges)
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
        best, top3 = None, [None, None, None]
        for idx in range(0, 3):
            for edge in self.edges:
                edge = edge.toDirectedND()
                score = dist(edge.midpoint(), pos)
                if best == None or score < best:
                    if edge not in top3:
                        best = score
                        top3[idx] = edge
        minDist = min(
            distToSegment(
                edge.toDirectedND(),
                pos,
            )
            for edge in top3
        )
        return max(0., min(1., minDist))

def fromGraph(graph):
    allEdges = set()
    for edges in graph.adjDict.values():
        allEdges.update(edges)
    return Heightmap(list(allEdges))

