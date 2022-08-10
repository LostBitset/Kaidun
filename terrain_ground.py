# Kaidun (by HktOverload)

class GroundPlane(object):
    __slots__ = ('resolution', 'geometry')

    def __init__(self, resolution=0.5):
        self.resolution = resolution
        self.geometry = None
        self.geometry = self.getDefaultGeometry()

    # THE geometry ATTRIBUTE WILL BE None HERE!
    def getDefaultGeometry(self):
        import scenes
        return scenes.CubeScene.buildGeometry({'origin':(0,0,0)})

    # Get the geometry of the plane
    def assemble(self):
        return self.geometry

