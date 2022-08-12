# Kaidun (by HktOverload)

defaultSize = 4
defaultDist = 3

class ChunkConfig(object):
    __slots__ = ('size', 'dist')

    def __init__(self, size, dist):
        self.size = size
        self.dist = dist

    @classmethod
    def default(cls):
        return cls(
            size=defaultSize,
            dist=defaultDist,
        )

    def loadedAt(self, point):
        minC, maxC = -self.dist + 1, self.dist
        for cX in range(minC, maxC):
            for cY in range(minC, maxC):
                yield self.getChunk(
                    cX + (point[0] // self.size),
                    cY + (point[1] // self.size),
                )

    def loadedFrom(self, chunk):
        minC, maxC = -self.dist + 1, self.dist
        for cX in range(minC, maxC):
            for cY in range(minC, maxC):
                yield self.getChunk(
                    cX + chunk[0],
                    cY + chunk[1],
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
        xs, ys = [], []
        while x < self.size:
            xs.append(x)
            x += resolution
        while y < self.size:
            ys.append(y)
            y += resolution
        for x in xs:
            for y in ys:
                yield Chunk(
                    x + self.x,
                    y + self.y,
                    resolution,
                )

