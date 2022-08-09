# Extensible mixins without classes

class Mixin(object):

    def __init__(self, name=None, items={}, strats={}):
        self.__dict__.update(items)
        self._strats = strats
        if name == None:
            name = id(self)
        self._sources = { k: name for k in strats }

    def __setattr__(self, name, value):
        fallback = super().__setattr__
        if name in ('_strats', '_sources'):
            return fallback(name, value)
        else:
            items = self.__dict__
            items[name] = value

    def use(self, *extraOthers):
        others = [self, *extraOthers]
        newStrats, newSources = dict(), dict()
        for other in others:
            for name in other._strats:
                if name in newStrats:
                    raise Exception(
                        f'Duplicate strategy for {name}.'
                    )
                newStrats[name] = other._strats[name]
                newSources[name] = other._sources[name]
        print(newStrats, newSources)
        for name, strat in newStrats.items():
            for other in others:
                if not hasattr(other, name):

    def _oldVer_use(*others):
        self = Mixin('mixed')
        strats, sources = self._strats, self._sources
        for other in others:
            for name, strat in other._strats.items():
                if name not in strats:
                    strats[name] = strat
                                continue
                            item = getattr(other, name)
                            items = self.__dict__
                            if name in items:
                                old = items[name]
                            mixed = strat(old, item)
                            setattr(self, name, mixed)
                        else:
                            setattr(self, name, item)
                    print(other._sources[name])
                    sources[name] = other._sources[name]
                elif sources[name] != other._sources[name]:
                    print(sources[name], other._sources[name])
                    raise Exception(
                        f'Duplicate strategy {repr(strat)} for {name}.'
                    )
        print(f'strats={strats}')
        print(f'sources={sources}')

