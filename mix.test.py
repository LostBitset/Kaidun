from mix import Mixin
import operator as op

assert Mixin({}, {})._strats == {}
assert Mixin()._strats == {}

test1 = Mixin('test1', {'a': 1}, {'a': op.add})

assert 'a' in test1._strats
assert test1.a == 1

base = Mixin('base', {'a': 9000}, {'a': op.add})
hi = Mixin('hi', {'a': 55}).use(base)
print('---')
ye = Mixin('ye', {'a': 5}).use(base)
print('---')

combined = Mixin().use(hi, ye)

print(combined.a)
assert combined.a == 9060

print('Passed!')

