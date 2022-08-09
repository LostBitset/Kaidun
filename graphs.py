# Kaidun (by HktOverload)

import cpu_linalg

class DirectedEdge(object):
    __slots__ = ('src', 'dst')

    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __repr__(self):
        return f'DEdge({self.src} -> {self.dst})'

class Edge(object):
    __slots__ = ('pts',)

    def __init__(self, p1, p2):
        self.pts = {p1, p2}

    def __repr__(self):
        prefix = 'Edge('
        sep = ' <-> '
        suffix = ')'
        return f'{prefix}{sep.join(self.pts)}{suffix}'

    def towards(self, dest, newcls=DirectedEdge):
        src, dst = None, None
        for pt in self.pts:
            if pt == dest:
                dst = pt
            else:
                src = pt
        return newcls(src, dst)


# Edges in 2D space are line segments, we can do special things with them
class EdgeIn2D(Edge):

    def towards(self, dest, newcls=DirectedEdgeIn2D):
        return super().towards(dest, newcls=newcls)

    def __repr__(self):
        orig = super().__repr__()
        return f'{{In2D}}{orig}'

# Directed line segments are the actually useful thing that this has been
# working towards
class DirectedEdgeIn2D(DirectedEdge):

    def __repr__(self):
        orig = super().__repr__()
        return f'{{In2D}}{orig}'

    # Get the heading as a normalized 2D vector
    def heading(self):
        res = cpu_linalg.add(
            cpu_linalg.neg(self.src),
            self.dst,
        )
        res = cpu_linalg.norm(res)
        return res

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

