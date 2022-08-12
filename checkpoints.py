# Kaidun (by HktOverload)

class Checkpoints(object):
    __slots__ = ('items',)
    gameCount = 3

    def __init__(self, items):
        self.items = items

    @classmethod
    def selectForEdge(cls, edge):
        pass  # TODO

class Checkpoint(object):
    __slots__ = ('t', 'roll')

    def __init__(self, t, roll):
        self.t = t
        self.roll = roll

