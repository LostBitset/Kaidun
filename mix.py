# Extensible mixins without classes

class Mixin(object):

    def __init__(self, name=None, items={}, strats={}, sources=None):
        self.__dict__.update(items)
        self._strats = strats
        if name == None:
            self._name = id(self)
        else:
            self._name = name
        if sources == None:
            self._sources = { k: self._name for k in strats }
        else:
            self._sources = sources

    def __setattr__(self, name, value):
        fallback = super().__setattr__
        if name.startswith('_'):
            return fallback(name, value)
        else:
            items = self.__dict__
            items[name] = value

    def use(self, *extraOthers):
        others = [self, *extraOthers]
        newStrats, newSources = dict(), dict()
        for other in others:
            for name in other._strats:
                if name in newSources:
                    if newSources[name] != other._sources[name]:
                        raise Exception(
                            f'Duplicate strategy for {name}.'
                        )
                newStrats[name] = other._strats[name]
                newSources[name] = other._sources[name]
        newItems = dict()
        for name, strat in newStrats.items():
            for other in others:
                if not hasattr(other, name):
                    continue
                item = getattr(other, name)
                if name in newItems:
                    old = newItems[name]
                    mixed = strat(old, item)
                    newItems[name] = mixed
                else:
                    newItems[name] = item
        return Mixin(
            f'::mixed#{[ i._name for i in others ]}',
            newItems,
            newStrats,
            newSources,
        )

