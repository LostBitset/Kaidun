# Extensible mixins without classes

class Mixin(object):

    def __init__(self, items={}, strats={}):
        self.__dict__.update(items)
        self._strats = strats
        self._sources = { k: id(self) for k in strats }

    def __setattr__(self, name, value):
        fallback = super().__setattr__
        if name in ('_strats', '_sources'):
            return fallback(name, value)
        else:
            items = self.__dict__
            items[name] = value



    def use(*others):
        self = Mixin()
        for other in others:
            for k, v in other._strats.items():
                strats, sources = self._strats, self._sources
                if k not in self._strats:
                    strats[k] = v
                    sources[k] = id(other)
        strats, sources = self._strats, self._sources
        seen = set()
        for other in others:
            for name in other.__dict__:
                if name not in other._sources or name.startswith('_'):
                    continue
                key = (other._sources[name], name)
                if key in seen:
                    continue
                seen.add(key)
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

