# Kaidun (by HktOverload)

import numpy as np

from chunks import ChunkConfig
from cpu_geom import Geometry, FillWith
from world_geometry import WorldGeometryObject

defaultCCfg = ChunkConfig.default()

class GroundPlane(WorldGeometryObject):
    __slots__ = ('auxContents', 'resolution', 'ccfg', 'geometryFn')

    def __init__(self, auxC, heightmap, resolution=0.5, ccfg=defaultCCfg):
        self.auxContents = auxC
        self.heightmap = heightmap
        self.resolution = resolution
        self.ccfg = ccfg
        self.geometryFn = None
        self.geometryFn = self.getDefaultGeometry

    # THE geometryFn ATTRIBUTE WILL BE None HERE!
    def getDefaultGeometry(self, playerChunk):
        # print('<start>', end='')
        # '''
        step = self.resolution
        L = []
        for chunk in self.ccfg.loadedFrom(playerChunk):
            for subchunk in chunk.subdivide(step):
                start = subchunk.pos()
                start = (
                    start[0], start[1],
                    self.heightmap.get((start[0], start[1])),
                )
                corner1 = (
                    start[0] + step, start[1],
                    self.heightmap.get((start[0] + step, start[1])),
                )
                corner2 = (
                    start[0], start[1] + step,
                    self.heightmap.get((start[0], start[1] + step)),
                )
                end = (
                    start[0] + step, start[1] + step,
                    self.heightmap.get((start[0] + step, start[1] + step)),
                )
                tri1 = [*start, *corner1, *end]
                tri2 = [*end, *corner2, *start]
                L.append(tri1)
                L.append(tri2)
        tris = np.array(L, dtype='f4')
        '''
        import scenes
        tris = scenes.CubeScene.cube.tris
        '''
        # print('<geom>', end='')
        geom = Geometry(
            tris,
            FillWith(
                *self.auxContents,
                dtype='f4',
            ),
        )
        # print('<end>', end='')
        return geom

    def geometryInChunk(self, playerChunk):
        return (self.geometryFn)(playerChunk)

