# -*- coding: utf-8 -*-

from math import cos, sin, radians
from HomVec3 import HomVec3

class HomMatrix3Exception(Exception):
    pass

class HomMatrix3(object):
    "Repräsentiert eine homogene Transformationsmatrix"
    
    def __init__(self, *els):
        "Erzeugt eine neue Matrix"
        self._matrix = self.newMatrix()
        for i, e in enumerate(els):
            self._matrix[i] = e
            
    def __add__(self, add):
        "Zwei Matrizen addieren"
        if not isinstance(add, HomMatrix3):
            raise HomMatrix3Exception("Can only add another matrix")
        r = self.newMatrix()
        for i in range(0, len(self._matrix)):
            r[i] = self._matrix[i] + add[i]
        return r
    
    def __sub__(self, add):
        "Zwei Matrizen subtrahieren"
        if not isinstance(add, HomMatrix3):
            raise HomMatrix3Exception("Can only subtract another matrix")
        #r = self.newMatrix()
        r = [x[0]-x[1] for x in zip(self._matrix, add)]
        return HomMatrix3(*r)
        #for i in range(0, len(self._matrix)):
        #    r[i] = self._matrix[i] - add[i]
        #return r
    
    def setScale(self, sx, sy, sz):
        "Setzt den Skalierungsfaktor in x-, y-, bzw. z-Richtung"
        self[0] = sx
        self[5] = sy
        self[10] = sz
        
    def setTranslation(self, tx, ty, tz):
        "Setzt die Verschiebung in x-, y-, bzw. z-Richtung"
        self[3] = tx
        self[7] = ty
        self[11] = tz
        
    def setRotation(self, x, y, z, alpha):
        "Setzt die Drehung um die Achse x,y,z mit dem Winkel alpha (Standard-Rotation ohne Quaternionen)"
        c = cos(radians(-alpha))
        s = sin(radians(-alpha))
        t = 1-c
        
        self[0]  = x*x*t + c
        self[1]  = x*y*t - z*s
        self[2]  = x*z*t + y*s
        self[4]  = x*y*t + z*s
        self[5]  = y*y*t + c
        self[6]  = y*z*t - x*s
        self[8]  = x*z*t - y*s
        self[9]  = y*z*t + x*s
        self[10] = z*z*t + c
        
    def newMatrix(self):
        "Erzeugt eine neue, neutrale Matrix"
        return [
            1,0,0,0, #  0  1  2  3
            0,1,0,0, #  4  5  6  7
            0,0,1,0, #  8  9 10 11
            0,0,0,1  # 12 13 14 15 
        ]
        
    def __mul__(self, mul):
        "Multiplikation mit einer Matrix oder einem Vektor"
        # TODO: Umbauen
        #for k in range(n):
        #    for l in range(o):
        #        for t in range(m):
        #            r[k][l] = a[k][t] + b[t][l]
        if isinstance(mul, HomMatrix3):
            m = self.newMatrix()
            m[0] = self[0] * mul[0] + self[1] * mul[4] + self[2] * mul[8] + self[3] * mul[12]
            m[1] = self[0] * mul[1] + self[1] * mul[5] + self[2] * mul[9] + self[3] * mul[13]
            m[2] = self[0] * mul[2] + self[1] * mul[6] + self[2] * mul[10] + self[3] * mul[14]
            m[3] = self[0] * mul[3] + self[1] * mul[7] + self[2] * mul[11] + self[3] * mul[15]
            m[4] = self[4] * mul[0] + self[5] * mul[4] + self[6] * mul[8] + self[7] * mul[12]
            m[5] = self[4] * mul[1] + self[5] * mul[5] + self[6] * mul[9] + self[7] * mul[13]
            m[6] = self[4] * mul[2] + self[5] * mul[6] + self[6] * mul[10] + self[7] * mul[14]
            m[7] = self[4] * mul[3] + self[5] * mul[7] + self[6] * mul[11] + self[7] * mul[15]
            m[8]  = self[8] * mul[0] + self[9] * mul[4] + self[10] * mul[8] + self[11] * mul[12]
            m[9]  = self[8] * mul[1] + self[9] * mul[5] + self[10] * mul[9] + self[11] * mul[13]
            m[10] = self[8] * mul[2] + self[9] * mul[6] + self[10] * mul[10] + self[11] * mul[14]
            m[11] = self[8] * mul[3] + self[9] * mul[7] + self[10] * mul[11] + self[11] * mul[15]
            m[12] = self[12] * mul[0] + self[13] * mul[4] + self[14] * mul[8] + self[15] * mul[12]
            m[13] = self[12] * mul[1] + self[13] * mul[5] + self[14] * mul[9] + self[15] * mul[13]
            m[14] = self[12] * mul[2] + self[13] * mul[6] + self[14] * mul[10] + self[15] * mul[14]
            m[15] = self[12] * mul[3] + self[13] * mul[7] + self[14] * mul[11] + self[15] * mul[15]
            return HomMatrix3(*m)
        elif isinstance(mul, HomVec3):
            x = self[0] * mul.x + self[1] * mul.y + self[2] * mul.z + self[3] * mul.w
            y = self[4] * mul.x + self[5] * mul.y + self[6] * mul.z + self[7] * mul.w
            z = self[8] * mul.x + self[9] * mul.y + self[10] * mul.z + self[11] * mul.w
            w = self[12] * mul.x + self[13] * mul.y + self[14] * mul.z + self[15] * mul.w
            #x = mul.x * self[0] + mul.y * self[1] + mul.z * self[2] 
            #y = mul.x * self[4] + mul.y * self[5] + mul.z * self[6]
            #z = mul.x * self[8] + mul.y * self[9] + mul.z * self[10]
            #w = mul.x * self[12] + mul.y * self[13] + mul.z * self[14]
            return HomVec3(x, y, z, w)
        # TODO: Scalar
        else:
            raise HomMatrix3Exception("Multiplikation not supported for this type")
    
    def __getitem__(self, index):
        "Zugriff auf Element der Matrix"
        return self._matrix[index]
    
    def __setitem__(self, index, value):
        "Element der Matrix setzen"
        self._matrix[index] = value
        
    def __repr__(self):
        "Gibt einen hübschen String der Matrix zurück"
        m = ""
        for i in range(0, len(self._matrix)):
            m += "%.2f " % self[i]
            if i % 4 == 3:
                m += "\n"
        return m
    
    def det(self):
        "Berechnet die Determinante"
        
    def trans(self):
        "Berechnet die Transponierte"
            
class FrustrumMatrix(HomMatrix3):
    "Repräsentiert eine Frustrum-Martrix"
    def __init__(self, xl, xr, yb, yt, N, F):
        self.xl = xl
        self.xr = xr
        self.yb = yb
        self.yt = yt
        self.N = N
        self.F = F
        super(self.__class__,self).__init__(
            2/(xr-xl),0,0,-((xr+xl)/(xr-xl)),
            0,2/(yt-yb),0,-((yt+yb)/(yt-yb)),
            0,0,-((F+N)/(F-N)),-((2*F*N)/(F-N)),
            0,0,-1,0 
        )