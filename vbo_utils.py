# Kaidun (by HktOverload)

class VertBufRef(object):
    __slots__ = 'buf', 'size'

    def __init__(self, size, alloc_fn=None):
        self.buf = alloc_fn(size)
        self.size = size

    def reset(self, newData, alloc_fn=None, alloc_hook=None):
        if alloc_fn == None:
            thisMethod = f'{self.__class__}.reset'
            expl = 'it does not have access to an OpenGL context'
            err = f'{thisMethod} needs an alloc_fn specified ({expl})'
            raise Exception(err)
        self.buf.release()
        newSize = len(newData.tobytes())
        if self.size != newSize:
            self.buf = alloc_fn(newSize)
            self.size = newSize
            if alloc_hook != None:
                alloc_hook()
        print(f'Writing: {newData}')
        self.buf.write(newData)

    @classmethod
    def makeAllocFn(cls, ctx):
        def inner(desiredSize):
            return ctx.buffer(reserve=desiredSize)
        return inner

