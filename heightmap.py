# Kaidun (by HktOverload)

class Heightmap(object):
    __slots__ = ('edges',)  # A list of EdgeIn2D objects

    def __init__(self, edges):
        self.edges = edges

    def get(self, pos):
        raise NotImplementedError

def fromGraph(graph):
    allEdges = set()
    for edges in graph.adjDict.values():
        allEdges.update(edges)
    return Heightmap(list(allEdges))

