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
        # [: Citation https://moderngl.readthedocs.io/en/latest/reference/buffer.html :]
        self.buf.release()
        print('> writing data to vbo@vram')
        print('^ newData@cpu = begin')
        print([ i for i in newData ])
        print(newData.dtype)
        print('^ end')
        newSize = len(newData.tobytes())
        if self.size != newSize:
            print('> reallocating vbo@vram')
            print(f'^ vbo size={self.size} -> size={newSize}')
            self.buf = alloc_fn(newSize)
            self.size = newSize
            if alloc_hook != None:
                alloc_hook()
        self.buf.write(newData)

    @classmethod
    def makeAllocFn(cls, ctx):
        def inner(desiredSize):
            # [: Citation https://moderngl.readthedocs.io/en/latest/reference/buffer.html :]
            return ctx.buffer(reserve=desiredSize)
        return inner

