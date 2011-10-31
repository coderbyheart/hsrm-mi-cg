class Triangle(object):
    def __init__(self, a, b, c):
        self.a = a # point
        self.b = b # point
        self.c = c # point
        self.u = self.b - self.a # direction vector
        self.v = self.c - self.a # direction vector

    def __repr__(self):
        return 'Triangle(%s,%s,%s)' % (repr(self.a), repr(self.b), repr(self.c))

    def intersectionParameter(self, ray):
        w = ray.origin - self.a
        dv = ray.direction.cross(self.v)
        dvu = dv.dot(self.u)
        if dvu == 0.0:
            return None
        wu = w.cross(self.u)
        r = dv.dot(w) / dvu
        s = wu.dot(ray.direction) / dvu
        if 0<=r and r<=1 and 0<=s and s<=1 and r+s <=1:
            return wu.dot(self.v) / dvu
        else:
            return None

    def normalAt(self, p):
        return self.u.cross(self.v).normalized()
    
from RGB import RGB

class ColoredTriangleException(Exception):
    pass

class ColoredTriangle(Triangle):
    def __init__(self, a, b, c, color):
        super(self.__class__,self).__init__(a, b, c)
        if not isinstance(color, RGB):
            raise ColoredTriangleException("Color must be a RGB instance")
        self._color = color
        
    def colorAt(self, ray):
        return self._color