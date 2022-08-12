# Kaidun (by HktOverload)

import terrain_graph_utils as u

def ok(triangulation, thresh=4.0):
    for tri in triangulation:
        incenter = u.incenter(tri)
        localMinDist = u.minSideDist(tri, incenter)
        if localMinDist < thresh:
            return False
    return True

