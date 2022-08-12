# Kaidun (by HktOverload)

import heightmap
from scenes import unhexify
from terrain_ground import GroundPlane
from terrain_graphs import makeWorldGraph

def makeGraph():
    return makeWorldGraph()
    # BEGIN TEMP
    import graphs
    res = graphs.Graph()
    a, b, c = (0.0, 0.0), (10.0, -2.0), (2.0, -8.0)
    for i in (a, b, c):
        res.addNode(i)
    edgecls = graphs.EdgeIn2D
    res.addEdge(edgecls(a, b))
    res.addEdge(edgecls(b, c))
    res.addEdge(edgecls(c, a))
    return res
    # END TEMP

# Generate terrain geometry from a the graph
def fromGraph(graph, triangulation):
    res = GroundPlane(
        unhexify(0xC2B280),
        heightmap.fromGraph(graph, triangulation),
    )
    return res

