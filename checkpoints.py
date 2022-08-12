# Kaidun (by HktOverload)

class Checkpoints(object):
    __slots__ = ('items',)
    gameCount = 3

    def __init__(self, items):
        self.items = items

class Checkpoint(object):
    __slots__ = ('t', 'roll')

    def __init__(self, t, roll):
        self.t = t
        self.roll = roll

