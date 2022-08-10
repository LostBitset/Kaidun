# Kaidun (by HktOverload)

from math import arccos, pi

import cpu_linalg

# Both a and b must be unit vectors
def angle(a, b):
    return arccos(cpu_linalg.dot(a, b))

# Both v1 and v2 must be unit vectors
def onlyOneSide(a, v1, v2):
    theta1 = angle(a, v1)
    theta2 = angle(v1, v2)
    return (theta1 + theta2) > pi

