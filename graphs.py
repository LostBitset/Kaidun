# Kaidun (by HktOverload)

from cpu_geom_utils import manhattan
import cpu_linalg

class DirectedEdge(object):
    __slots__ = ('src', 'dst')

    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __iter__(self):
        yield self.src
        yield self.dst

    def __repr__(self):
        return f'DEdge({self.src} -> {self.dst})'

class Edge(object):
    __slots__ = ('pts',)

    def __init__(self, p1, p2):
        self.pts = {p1, p2}

    def __iter__(self):
        for pt in self.pts:
            yield pt

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

    # Check if the manhattan distance to a node is larger than the
    # manhattan distance between the nodes
    def isBeyond(self, coord):
        toSrc = manhattan(self.src, coord)
        toDst = manhattan(self.dst, coord)
        between = manhattan(self.src, self.dst)
        return max(toSrc, toDst) > (between + 10**-5)

# Edges in 2D space are line segments, we can do special things with them
class EdgeIn2D(Edge):

    def towards(self, dest, newcls=DirectedEdgeIn2D):
        return super().towards(dest, newcls=newcls)

    def __repr__(self):
        orig = super().__repr__()
        return f'{{In2D}}{orig}'

    def beyond(self, coord):
        ordered = sorted(self.pts)
        dEdge = DirectedEdgeIn2D(ordered[0], ordered[1])
        return dEdge.beyond(coord)

# A graph represented as an adjacency list
# [: Citation https://www.khanacademy.org/computing/computer-science/algorithms/graph-representation/a/representing-graphs :]
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
        for pt in newEdge:
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

