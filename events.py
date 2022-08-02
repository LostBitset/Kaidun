# Kaidun (by HktOverload)

class Event(object):
    __slots__ = 'kind', 'data', 'windowRef'
    def __init__(self, kind, data, windowRef):
        self.kind = kind
        self.data = data
        self.windowRef = windowRef

    def isKeypress()
