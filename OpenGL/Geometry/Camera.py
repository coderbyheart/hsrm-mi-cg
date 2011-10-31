# -*- coding: utf-8 -*-
from HomVec3 import HomVec3

class CameraException(Exception):
    pass
                  
class Camera(object):
    "Eine Kamera"
    
    def getPosition(self):
        return self._pos
    def setPosition(self, pos):
        if not isinstance(pos, HomVec3) or not pos.isPoint():
            raise CameraException("Postion must be a HomVec3 and a point")
        self._pos = pos
        return self
    position = property(getPosition, setPosition, None, "Standpunkt der Kamera")
    
    def getUp(self):
        return self._up
    def setUp(self, up):
        if not isinstance(up, HomVec3) or up.isPoint():
            raise CameraException("Up must be a HomVec3 and not a point")
        self._up = up
        return self
    up = property(getUp, setUp, None, "Vektor der Kamera, der nach oben zeigt")
    
    def getTarget(self):
        return self._target
    def setTarget(self, target):
        if not isinstance(target, HomVec3) or not target.isPoint():
            raise CameraException("Target must be a HomVec3 and a point")
        self._target = target
        return self
    target = property(getTarget, setTarget, None, "Zielpunkt der Kamera")
    
    def getAngle(self):
        return self._angle
    def setAngle(self, angle):
        angle = int(angle)
        if angle >= 180:
            raise CameraException("Angle must be a < 180")
        self._angle = angle
        return self
    angle = property(getAngle, setAngle, None, "Öffnungswinkel der Kamera")
    
    def getFVector(self):
        "Gibt den Vektor zurück, der zum Ziel zeigt"
        return (self.target - self.position).normalized()
    
    def getSVector(self):
        "Gibt den Vektor zurück, der senkrecht auf dem F- und dem Up-Vektor steht"
        return (self.getFVector() % self.getUp()).normalized()
    
    def getUVector(self):
        "Gibt den Vektor zurück, der senkrecht auf dem S- und F-Vektor steht"
        return (self.getSVector() % self.getFVector()).normalized()
        