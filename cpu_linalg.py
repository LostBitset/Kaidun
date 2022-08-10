# Kaidun (by HktOverload)

import math
from math import sin, cos

# A singleton representing a zero vector
# It doesn't have a specified dimension, and therefore
# can be used with anything
# In actuality, it's only useable as the first argument
# to the add function, but this is really useful for building
# up a vector by repeatedly adding n-dimensional vectors
# This singleton pattern was found on:
# [: Citation https://stackoverflow.com/questions/41048643/how-to-create-a-second-none-in-python-making-a-singleton-object-where-the-id-is :]
ZeroVec = None

class _ZeroVecT(object):

    def __new__(cls):
        return ZeroVec

    def __copy__(self):
        return ZeroVec

    def __deepcopy__(self):
        return ZeroVec

    def __reduce__(self):
        return (_ZeroVecT, ())

# It's a singleton! Only create a new instance if it doesn't
# exist already
if 'ZeroVec' not in globals():
    ZeroVec = object.__new__(_ZeroVecT)

# Add vectors
def add(a, b):
    if a == ZeroVec:
        return b
    assert len(a) == len(b)
    return [ a[i]+b[i] for i in range(len(a)) ]

# Scale vectors
def sc(a, scalar):
    return [ i * scalar for i in a ]

# Dot product of vectors
def dot(a, b):
    assert len(a) == len(b)
    return sum( a[i]*b[i] for i in range(len(a)) )

# Negate a vector
def neg(a):
    return [ -i for i in a ]

# Normalize a vector
# [: Citation https://docs.python.org/3/library/math.html#math.hypot :]
def norm(a):
    length = math.hypot(*a)
    if length == 0:
        return a
    return sc(a, 1/length)

# A matrix with elements stored in column-major order
# [: Citation https://en.wikipedia.org/wiki/Row-_and_column-major_order :]
class Mat(object):
    __slots__ = 'odim', 'idim', 'cols'

    def __init__(self, cols, odim=None, idim=None):
        cnt = len(cols)
        if odim == None and idim == None:
            raise Exception('No parts of mat size given')
        elif odim == None:
            if cnt % idim != 0:
                raise Exception(
                    f'Given idim {idim} must be fac of {cnt}'
                )
            else:
                odim = cnt // idim
        elif idim == None:
            if cnt % odim != 0:
                raise Exception(
                    f'Given odim {odim} must be fac of {cnt}'
                )
            else:
                idim = cnt // odim
        else:
            if (odim*idim) != cnt:
                raise Exception(
                    f'No {odim}x{idim} mat has {cnt} elems'
                )
        self.odim, self.idim = odim, idim
        self.cols = cols

    # getting a column
    def col(self, n):
        start = range(0, self.odim*self.idim, self.odim)[n]
        return self.cols[start:start+self.odim]

    # getting a row
    def row(self, n):
        return [
            self.cols[i]
            for i in range(n, self.odim*self.idim, self.odim)
        ]

    # transpose
    def t(self):
        return Mat(
            [ j for i in range(self.odim) for j in self.row(i) ],
            odim=self.idim, idim=self.odim,
        )

    # mat-vec-mul
    def __mul__(self, v):
        res = ZeroVec
        for i in range(self.idim):
            res = add(res, sc(self.col(i), v[i]))
        return res

    # mat-mat-mul
    # In python this overloads the @ operator
    # [: Citation https://en.wikipedia.org/wiki/Matrix_multiplication#Definition :]
    def __matmul__(self, other):
        assert isinstance(other, self.__class__)
        assert other.odim == self.idim
        resList = []
        for i in range(self.odim):
            for j in range(other.idim):
                resList.append(
                    dot(self.row(i), other.col(j))
                )
        return (self.__class__)(resList, other.idim, self.odim).t()


# A 3D rotation matrix
# Arguments are Tait-Bryan angles
# [: Citation https://en.wikipedia.org/wiki/Rotation_matrix#General_rotations :] 
def rotMat(a, b, c):
    return Mat([
        cos(a)*cos(b), sin(a)*cos(b), -sin(b),
        (cos(a)*sin(b)*sin(c))-(sin(a)*cos(c)),
        (sin(a)*sin(b)*sin(c))+(cos(a)*cos(c)),
        cos(b)*sin(c),
        (cos(a)*sin(b)*cos(c))+(sin(a)*sin(c)),
        (sin(a)*sin(b)*cos(c))-(cos(a)*sin(c)),
        cos(b)*cos(c),
    ], 3, 3)

