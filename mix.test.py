from mix import Mixin
import operator as op

assert Mixin({}, {})._strats == {}
assert Mixin()._strats == {}

test1 = Mixin({'a': 1}, {'a': op.add})

assert 'a' in test1._strats
assert test1.a == 1

base = Mixin({'a': 9000}, {'a': op.add})
hi = Mixin({'a': 55}).use(base)
ye = Mixin({'a': 5}).use(base)

combined = Mixin().use(hi, ye)

print('Passed!')

