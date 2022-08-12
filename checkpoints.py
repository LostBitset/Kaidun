# Kaidun (by HktOverload)

class Checkpoint(object):
    __slots__ = ('t', 'roll')
    gameCount = 3

    def __init__(self, t, roll):
        self.t = t
        self.roll = roll

