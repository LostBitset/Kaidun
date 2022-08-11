# Kaidun (by HktOverload)

'''
This is an implementation ofthe Bowyer-Watson algorithm for finding
the Delaunay Triangulation (DT) of a set of points.
In this case, we're in 2D.
Based off of the explanation and pseudocode at:
[: Citation https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm :]
'''

# During Bowyer-Watson, only three
# extra vertices are ever added, so
# this is way more memory efficient
# than a set of tuples or something
class Triangulation(object):
    __slots__ = ('verts', 'refs', 'counter')

    def __init__(self):
        self.verts = dict()  # maps points to IDs
        self.refs = set()  # set of 3-tuples of IDs
        self.counter = 0  # Keep track of IDs

    def addTri(self, tri):
        for vert in tri:
            if vert not in self.vert:


