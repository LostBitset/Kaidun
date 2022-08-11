# Kaidun (by HktOverload)

import numpy as np

from chunks import ChunkConfig
from cpu_geom import Geometry, FillWith

defaultCCfg = ChunkConfig.default()

class GroundPlane(object):
    __slots__ = ('auxContents', 'resolution', 'ccfg', 'geometry')

    def __init__(self, auxContents, resolution=0.5, ccfg=defaultCCfg):
        self.auxContents = auxContents
        self.resolution = resolution
        self.ccfg = ccfg
        self.geometry = None
        self.geometry = self.getDefaultGeometry()

    # THE geometry ATTRIBUTE WILL BE None HERE!
    def getDefaultGeometry(self):
        # '''
        z, step = 0, self.resolution
        L = []
        for chunk in self.ccfg.loadedAt((0, 0, 0)):
            for subchunk in chunk.subdivide(step):
                start = subchunk.pos()
                start = (start[0], start[1], z)
                corner1 = (start[0] + step, start[1], z)
                corner2 = (start[0], start[1] + step, z)
                end = (start[0] + step, start[1] + step, z)
                tri1 = [*start, *corner1, *end]
                tri2 = [*end, *corner2, *start]
                L.append(tri1)
                L.append(tri2)
        tris = np.array(L, dtype='f4')
        '''
        import scenes
        tris = scenes.CubeScene.cube.tris
        '''
        geom = Geometry(
            tris,
            FillWith(
                *self.auxContents,
                dtype='f4',
            ),
        )
        return geom

    # Get the geometry of the plane
    def assemble(self):
        return self.geometry

