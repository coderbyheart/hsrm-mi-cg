# -*- coding: utf-8 -*-

from math import sqrt, acos, pi

class HomVec3Exception(Exception):
    pass

class HomVec3(object):
    """Klasse zur Verwaltung von Punkten und Vektoren im R³
    
    @author Markus Tacker <m@tacker.org>
    """
    
    _x = None
    _y = None
    _z = None
    _w = None
    
    def __init__(self, x, y, z, w = 0):
        "Erzeugt ein neues Objekt mit den Koordinaten X,Y,Z und optional der Angabe, ob es sich um einen Punkt handelt"
        self._x = float(x)
        self._y = float(y)
        self._z = float(z)
        self._w = float(w)
        
    def getx(self):
        "Gibt die X-Koordinate zurück"
        return self._x
    def setx(self, x):
        "Setzt die X-Koordinate zurück"
        self._x = x
    x = property(getx, setx, None, "Gibt die X-Koordinate zurück")
    
    def gety(self):
        "Gibt die Y-Koordinate zurück"
        return self._y
    def sety(self, y):
        "Setzt die Y-Koordinate"
        self._y = y
    y = property(gety, sety, None, "Gibt die Y-Koordinate zurück")
    
    def getz(self):
        "Gibt die Z-Koordinate zurück"
        return self._z
    def setz(self, z):
        "Setzt die Z-Koordinate"
        self._z = z
    z = property(getz, setz, None, "Gibt die Z-Koordinate zurück")
    
    def getw(self):
        "Gibt die W zurück"
        return self._w
    def setw(self, w):
        "Setzt W"
        self._w = w
    w = property(getw, setw, None, "Gibt W zurück")
    
    def isPoint(self):
        "Gibt an, ob es sich um einen Punkt handelt"
        return self._w > 0
    
    def isVector(self):
        "Gibt an, ob es sich um einen Vektor handelt"
        return not self.isPoint()
    
    def length(self):
        """Gibt die Länge des Vektors zurück"""
        return sqrt(self.x**2 + self.y**2 + self.z**2) if self.isVector() else 0
    
    def normalize(self):
        """Normiert den Vektor auf die Länge 1 oder den Punkt durch perspektivisches Teiles"""
        if self.isPoint():
            self._x = self.x / self._w
            self._y = self.y / self._w
            self._z = self.z / self._w
            self._w = 1
        else:
            s = 1 / self.length()
            self._x = self.x * s
            self._y = self.y * s
            self._z = self.z * s
    
    def normalized(self):
        """Gibt den normierten Vektor oder Punkt zurück"""
        if self.isPoint():
            return HomVec3(self.x / self._w, self.y / self._w, self.z / self.w, 1)
        else:
            return self.scale(1 / self.length())
    
    def scale(self, s):
        "Liefert den Vektor skaliert um den Faktor s zurück"
        if self.isPoint():
            raise HomVec3Exception("Cannot scale points.")
        return HomVec3(self.x * s, self.y * s, self.z * s)

    def angle(self, q):
        "Berechnet den Winkel in Grad zwischen zwei Vektoren"
        return acos((self * q) / (self.length() * q.length())) * (180/pi)
        
    def __add__(self, q):
        """Implementiert die Addition von zwei Vektoren"""
        # Prüfen ob Punkt und Punkt
        return HomVec3(self.x + q.x, self.y + q.y, self.z + q.z)
        
    def __sub__(self, q):
        """Implementiert die Subtraktion von zwei Vektoren"""
        return HomVec3(self.x - q.x, self.y - q.y, self.z - q.z)
        
    def __mul__(self, q):
        """Implementierte das Skalarprodukt von zwei Vektoren oder die Multiplikation eines Vektor mit einem Skalar"""
        if isinstance(q, HomVec3):
            return self.dot(q)
        else:
            return HomVec3(self.x * q, self.y * q, self.z * q, self.isPoint())
        
    def dot(self, q):
        """Implementierte das Skalarprodukt von zwei Vektoren"""
        return self.x * q.x + self.y * q.y + self.z * q.z
    
    def cross(self, q):
        """Implementiert das Kreuzprodukt von zwei Vektoren"""
        return HomVec3(
           self.y * q.z - self.z * q.y,
           self.z * q.x - self.x * q.z,
           self.x * q.y - self.y * q.x
        )
    
    def __mod__(self, q):
        """Implementiert das Kreuzprodukt von zwei Vektoren"""
        return self.cross(q)
    
    def __repr__(self):
        return "%s(%.6f|%.6f|%.6f|%.6f)" % ("Pnt" if self.isPoint() else "Vec", self.x, self.y, self.z, self._w)