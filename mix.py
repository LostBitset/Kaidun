# Extensible mixins without classes

class Mixin(object):

    def __init__(self, name=None, items={}, strats={}, sources=None):
        self.__dict__.update(items)
        self._strats = strats
        if name == None:
            name = id(self)
        if sources == None:
            self._sources = { k: name for k in strats }
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
                print(f'{name} <- (strat) {other._strats[name]}')
                print(f'{name} <- (source) {other._sources[name]}')
                newStrats[name] = other._strats[name]
                newSources[name] = other._sources[name]
        newItems = dict()
        print(f'newStrats = {newStrats}')
        for name, strat in newStrats.items():
            print(f'strat={strat}')
            for other in others:
                if not hasattr(other, name):
                    continue
                item = getattr(other, name)
                if name in newItems:
                    old = newItems[name]
                    print(f'using (old) {old}')
                    mixed = strat(old, item)
                    newItems[name] = mixed
                else:
                    print(f'using {item}')
                    newItems[name] = item
        print('items =', newItems)
        print('strats =', newStrats)
        print('sources =', newSources)
        return Mixin(
            None,
            newItems,
            newStrats,
            newSources,
        )

    def _oldVer_use(*others):
        self = Mixin('mixed')
        strats, sources = self._strats, self._sources
        for other in others:
            for name, strat in other._strats.items():
                if name not in strats:
                    strats[name] = strat
                    print(other._sources[name])
                    sources[name] = other._sources[name]
                elif sources[name] != other._sources[name]:
                    print(sources[name], other._sources[name])
                    raise Exception(
                        f'Duplicate strategy {repr(strat)} for {name}.'
                    )
        print(f'strats={strats}')
        print(f'sources={sources}')

