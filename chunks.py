# Kaidun (by HktOverload)

from math import hypot

def euclidean2D(a, b):
    return hypot(a[0] - b[0], a[1] - b[1])

defaultSize = 1
defaultDist = 1

class ChunkConfig(object):
    __slots__ = ('size', 'dist', 'metric')

    def __init__(self, size, dist, metric=euclidean2D):
        self.size = size
        self.dist = dist
        self.metric = metric

    @classmethod
    def default(cls):
        return cls(
            size=defaultSize,
            dist=defaultDist,
            metric=euclidean2D,
        )

    def loadedAt(self, point):
        minC, maxC = -self.dist + 1, self.dist
        for cX in range(minC, maxC):
            for cY in range(minC, maxC):
                yield self.getChunk(
                    cX + (point[0] // self.size),
                    cY + (point[1] // self.size),
                )

    def getChunk(self, cX, cY):
        return Chunk(cX, cY, self.size)

class Chunk(object):
    __slots__ = ('x', 'y', 'size')

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def pos(self):
        return (self.x, self.y)

    def subdivide(self, resolution):
        x, y = 0, 0
        while x < self.size:
            while y < self.size:
                yield Chunk(
                    x + self.x,
                    y + self.y,
                    resolution,
                )
                x += resolution
                y += resolution

