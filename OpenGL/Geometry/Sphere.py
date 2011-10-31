from math import sqrt

class Sphere(object):
    def __init__(self, center, radius):
        self.center = center # point
        self.radius = radius # scalar

    def __repr__(self):
        return 'Sphere(%s,%s)' % (repr(self.center), self.radius)

    def intersectionParameter(self, ray):
        # Schwan
        co = self.center - ray.origin
        v = co.dot(ray.direction)
        discriminant = v*v - co.dot(co) + self.radius*self.radius 
        if discriminant < 0:
            return None
        else:
            return v - sqrt(discriminant)

    def normalAt(self, p):
        return (p - self.center).normalized()

from RGB import RGB

class ColoredSphereException(Exception):
    pass

class ColoredSphere(Sphere):
    def __init__(self, center, radius, color):
        super(self.__class__,self).__init__(center, radius)
        if not isinstance(color, RGB):
            raise ColoredSphereException("Color must be a RGB instance")
        self._color = color
        
    def colorAt(self, ray):
        return self._color