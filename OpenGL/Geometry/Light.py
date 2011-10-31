from HomVec3 import HomVec3
from RGB import RGB

class PointLightException(Exception):
    pass
                  
class PointLight(object):
    "Eine Punktlichtquelle"
    
    def __init__(self, pos, color = None):
        self.position = pos
        self.color = color if color is not None else RGB(0.1,0.1,0.1)

    def getPosition(self):
        return self._pos
    def setPosition(self, pos):
        if not isinstance(pos, HomVec3) or not pos.isPoint():
            raise PointLightException("Postion must be a HomVec3 and a point")
        self._pos = pos
        return self
    position = property(getPosition, setPosition, None, "Standpunkt der Lichtquelle")
    
    def getColor(self):
        return self._color
    def setColor(self, color):
        if not isinstance(color, RGB):
            raise PointLightException("Color must be a RGB instance")
        self._color = color
        return self
    color = property(getColor, setColor, None, "Farbe des Lichts")
    
