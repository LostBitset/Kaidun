# Kaidun (by HktOverload)

class Edge(object):
    __slots__ = ('pts',)

    def __init__(self, p1, p2):
        self.pts = {p1, p2}

    def __repr__(self):
        prefix = 'Edge('
        sep = ' -> '
        suffix = ')'
        return f'{prefix}{sep.join(self.pts)}{suffix}'

