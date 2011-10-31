class Plane(object):
    def __init__(self, point, normal):
        self.point = point # point
        self.normal = normal.normalized() # vector

    def __repr__(self):
        return 'Plane(%s,%s)' % (repr(self.point), repr(self.normal))

    def intersectionParameter(self, ray):
        op = ray.origin - self.point
        a = op.dot(self.normal)
        b = ray.direction.dot(self.normal)
        if b < 0:
            return -a/b
        else:
            return None

    def normalAt(self, p):
        return self.normal

from RGB import RGB

class ColoredPlaneException(Exception):
    pass

class ColoredPlane(Plane):
    def __init__(self, point, normal, color):
        super(self.__class__,self).__init__(point, normal)
        if not isinstance(color, RGB):
            raise ColoredPlaneException("Color must be a RGB instance")
        self._color = color
        
    def colorAt(self, ray):
        return self._color