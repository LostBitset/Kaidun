# Kaidun (by HktOverload)

class VertBufRef(object):
    __slots__ = 'buf', 'size'

    def __init__(self, size, alloc_fn=None):
        self.buf = alloc_fn(size)
        self.size = size

    def reset(self, newData, alloc_fn=None, alloc_hook=None):
        if alloc_fn == None:
            raise Exception(
                'VertBufRef.reset needs an alloc_fn specified'
                + ' (it does not have an OpenGL/moderngl context'
            )
        self.buf.release()
        newSize = len(newData.tobytes())
        if self.size != newSize:
            self.buf = alloc_fn(newSize)
            self.size = newSize
            if alloc_hook != None:
                alloc_hook()
        self.buf.write(newData)
        
    @classmethod
    def makeAllocFn(cls, ctx):
        def inner(desiredSize):
            return ctx.buffer(reserve=desiredSize)
        return inner
