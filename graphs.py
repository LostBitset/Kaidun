# Kaidun (by HktOverload)

class Edge(object):
    __slots__ = ('pts',)

    def __init__(self, p1, p2):
        self.pts = {p1, p2}

    def __repr__(self):
        prefix = 'Edge('
        sep = ' -> '
        suffix = ')'
        return f'{prefix}{sep.join(self.pts)}{suffix}'

# A graph represented as an adjacency list
class Graph(object):
    __slots__ = ('adjDict',)

    def __init__(self):
        self.adjDict = dict()

    def edges(self):
        return EdgesIterator(self)

    def nodes(self):
        return NodesIterator(self)

    def addNode(self, newNode):
        self.adjDict[newNode] = set()

    def addEdge(self, newEdge):
        for pt in newEdge.pts:
            self.adjDict[pt] = newEdge

class EdgesIterator(object):
    __slots__ = ('graph',)

    def __init__(self, graph):
        self.graph = graph

    def __iter__(self):
        for edgeSet in self.graph.adjDict.values():
            for edge in edgeSet:
                yield edge

class NodesIterator(object):
    __slots__ = ('graph',)

    def __init__(self, graph):
        self.graph = graph

    def __iter__(self):
        for node in self.graph.adjDict:
            yield node

