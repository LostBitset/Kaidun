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

    def use(self, *others):
        for other in others:
            for k, v in other._strats.items():
                strats = self._strats
                if k not in self._strats:
                    strats[k] = v
                elif strats[k] != v:
                    raise Exception(
                        f'Two distinct strategies given for {k}.'
                    )

