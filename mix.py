# Extensible mixins without classes

class Mixin(object):

    def __init__(self, items={}, strats={}):
        self.__dict__.update(items)
        self._strats = strats

    def __setattr__(self, name, value):
        fallback = super().__setattr__
        if name in ('_strats',):
            return fallback(name, value)
        else:
            items = self.__dict__
            items[name] = value

    def use(*others):
        self = Mixin()
        for other in others:
            for k, v in other._strats.items():
                strats = self._strats
                if k not in self._strats:
                    strats[k] = v
                elif strats[k] != v:
                    raise Exception(
                        f'Two distinct strategies given for {k}.'
                    )
        strats = self._strats
        seen = set()
        for other in others:
            for name in other.__dict__:
                if (other, name) in seen:
                    continue
                seen.add((other, name))
                if not name.startswith('_'):
                    try:
                        item = getattr(other, name)
                    except:
                        continue
                    if name not in self.__dict__:
                        setattr(self, name, item)
                    else:
                        items = self.__dict__
                        old = items[name]
                        mixed = strats[name](item, old)
                        setattr(self, name, mixed)
        return self
