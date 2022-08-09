# Kaidun (by HktOverload)

'''
A (better?) version of mixins that actually makes sense to me.
'''

def mixUsing(strategy):
    def decorator(f):
        f._mixStrategy = strategy
        return f
    return decorator

def mix(*classes):
    class Inner_Mixed(object):
        pass
    strategies, seen = dict(), set()
    for cls in classes:
        for sub in reversed(cls.mro()):
            if sub in seen:
                continue
            seen.add(sub)
            for name in dir(sub):
                item = getattr(sub, name)
                if not hasattr(Inner_Mixed, name):
                    if hasattr(item, '_mixStrategy'):
                        strategies[name] = item._mixStrategy
                        setattr(Inner_Mixed, name, item)
                else:
                    if name in strategies:
                        old = getattr(Inner_Mixed, name)
                        new = strategies[name](old, item)
                        setattr(Inner_Mixed, name, new)
    return Inner_Mixed

