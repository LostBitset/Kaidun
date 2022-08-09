# Kaidun (by HktOverload)

'''
A (better?) version of mixins that actually makes sense to me.
'''

def mixUsing(strategy):
    def decorator(f):
        f._mixStrategy = strategy
        return f

def mix(*classes):
    class Inner_Mixed(object):
        pass
    for cls in classes:
        targets = dict()
        for item in dir(cls):
            if not hasattr(item, '_mixStrategy'):
                continue
            targets[item] = getattr(item, '_mixStrategy')
    mixedAttrs = set()
    

