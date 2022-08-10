# Kaidun (by HktOverload)

# Represents an event
# The windowRef attribute is a reference to the window
# object (<WindowConfig>.wnd)
class Event(object):
    __slots__ = 'kind', 'data', 'windowRef'

    def __init__(self, kind, data, windowRef):
        self.kind = kind
        self.data = data
        self.windowRef = windowRef

    def isKeypress(self, key=None):
        if self.kind != 'key_event/PRESS':
            return False
        targetKey = self.getKeyCode(key)
        return self.data['key'] == targetKey

    def isKeyrelease(self, key=None):
        if self.kind != 'key_event/RELEASE':
            return False
        targetKey = self.getKeyCode(key)
        return self.data['key'] == targetKey

    def getKeyCode(self, keyname):
        return getattr(
            self.windowRef.keys,
            keyname.upper(),
        )

