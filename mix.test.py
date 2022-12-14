from mix import Mixin
import operator as op

'''
See mix.py for documentation
'''

assert Mixin({}, {})._strats == {}
assert Mixin()._strats == {}

test1 = Mixin('test1', {'a': 1}, {'a': op.add})

assert 'a' in test1._strats
assert test1.a == 1

base = Mixin('base', {'a': 0}, {'a': op.add})
hi = Mixin('hi', {'a': 55}).use(base)
ye = Mixin('ye', {'a': 5}).use(base)

combined = Mixin().use(hi, ye)

assert combined.a == 60

print('Passed!')

