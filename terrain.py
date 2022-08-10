# Kaidun (by HktOverload)

import graphs

def genTestGraph():
    res = graphs.Graph()
    a, b, c = (0.0, 0.0), (10.0, -2.0), (2.0, -8.0)
    for i in (a, b, c):
        res.addNode(i)
    edgecls = graphs.DirectedEdgeIn2D
    res.addEdge(edgecls(a, b))
    res.addEdge(edgecls(b, c))
    res.addEdge(edgecls(c, a))
    return res

