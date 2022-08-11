# Kaidun (by HktOverload)

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
            res -= 2.0
            self.memo[pos] = res
            return res

    def getValue(self, pos):
        return 1.0

def fromGraph(graph):
    allEdges = set()
    for edges in graph.adjDict.values():
        allEdges.update(edges)
    return Heightmap(list(allEdges))

