class RGBException(Exception):
    pass

class RGB(object):
    "Verwaltet Farbangaben im RGB-Farbraum"
    
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        
    def getR(self):
        return self._r
    def setR(self, r):
        r = float(r)
        if r < 0 or r > 1:
            raise RGBException("Value must be between 0 and 1")
        self._r = r
        return self
    r = property(getR, setR, None, "R value")
        
    def getG(self):
        return self._g
    def setG(self, g):
        g = float(g)
        if g < 0 or g > 1:
            raise RGBException("Value must be between 0 and 1")
        self._g = g
        return self
    g = property(getG, setG, None, "G value")
        
    def getB(self):
        return self._b
    def setB(self, b):
        b = float(b)
        if b < 0 or b > 1:
            raise RGBException("Value must be between 0 and 1")
        self._b = b
        return self
    b = property(getB, setB, None, "B value")
    
    def getRGB(self):
        return (int(self.r * 255), int(self.g * 255), int(self.b * 255))
    rgb = property(getRGB, None, None, "Returns the RGB as a dict")
    
    def __add__(self, color):
        if not isinstance(color, RGB):
            raise RGBException("Can only add another RGB")
        r = min((self.r + color.r, 1.0))
        g = min((self.g + color.g, 1.0))
        b = min((self.b + color.b, 1.0))
        return RGB(r,g,b)
    
    def __sub__(self, color):
        if not isinstance(color, RGB):
            raise RGBException("Can only subtract another RGB")
        r = max((self.r - color.r, 0))
        g = max((self.g - color.g, 0))
        b = max((self.b - color.b, 0))
        return RGB(r,g,b)
    
    def __mul__(self, m):
        return RGB(self.r * m, self.g * m, self.b * m)