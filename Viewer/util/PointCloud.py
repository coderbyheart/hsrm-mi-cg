# -*- coding: utf-8 -*-

from HomVec3 import HomVec3
from HomMatrix3 import HomMatrix3

class PointCloudException(Exception):
    pass

class PointCloud(object):
    "Repräsentiert eine Punktwolke"
    
    def __init__(self):
        self._points = []
        self._bb = {
            'x': None,
            '-x': None,
            'y': None,
            '-y': None,
            'z': None,
            '-z': None,
        }        
    
    def readRaw(self, objfile):
        "List Punkte aus einer RAW-Datei ein"
        f = open(objfile)
        for line in f.readlines():
            self.addPoint(*line.strip().split(' '))
        f.close()
        return self
    
    def addPoint(self, x, y, z):
        x, y, z = map(lambda x: float(x), [x, y, z])
        "Fügt der Punktwolke einen neuen Punkt hinzu"
        self._points.append(HomVec3(x, y, z, True))
        p = {'x': x, 'y': y, 'z': z}
        for k in p:
            bbmin = '-%s' % k
            if self._bb[bbmin] is None or p[k] < self._bb[bbmin]:
                 self._bb[bbmin] = p[k]
            bbmax = '%s' % k
            if self._bb[bbmax] is None or p[k] > self._bb[bbmax]:
                 self._bb[bbmax] = p[k]
        
    def getBoundingBox(self):
        "Liefert die Bounding-Box der Punktwolke"
        return self._bb
    
    def getXSize(self):
        return self.getDSize('x')
    
    def getYSize(self):
        return self.getDSize('y')
    
    def getZSize(self):
        return self.getDSize('z')
    
    def getDSize(self, d):
        return self._bb[d] + -self._bb['-%s' % d]
        
    def getNumPoints(self):
        "Liefert die Anzahl der Punkte in der Wolke"
        return len(self._points)
    
    def __iter__(self):
        "Gibt die Punkte zurück"
        return iter(self._points)

    def normalized(self):
        """Gibt eine normalisierte Version der Wolke zurück
        d.h. alle Punkt liegen im Bereich zwischen 1 und -1
        auf allen Achsen."""
        pn = PointCloud()
        # Zentriere alle Koordinaten
        maxSize = max(self.getXSize(), self.getYSize(), self.getZSize())
        bb = self.getBoundingBox()
        minX = bb['-x']
        minY = bb['-y']
        minZ = bb['-z']
        xMov = 1 - self.getXSize() / maxSize;
        yMov = 1 - self.getYSize() / maxSize;
        zMov = 1 - self.getZSize() / maxSize;
        
        for point in self._points:
            x = (point.x - minX) / maxSize * 2 - 1 + xMov
            y = (point.y - minY) / maxSize * 2 - 1 + yMov
            z = (point.z - minZ) / maxSize * 2 - 1 + zMov
            #print('(%.1f,%.1f,%.1f) -> (%.1f,%.1f,%.1f)' % (point.x, point.y, point.y, x, y, z))
            pn.addPoint(x, y, z)
            
        return pn
        
    def rotateX(self, angle):
        "Rotiert die Punkte um die X-Achse"
        rmat = HomMatrix3()
        rmat.setRotation(1,0,0,angle)
        for i, point in enumerate(self._points):
            self._points[i] = rmat * point
            
    def rotateY(self, angle):
        "Rotiert die Punkte um die Y-Achse"
        rmat = HomMatrix3()
        rmat.setRotation(0,1,0,angle)
        for i, point in enumerate(self._points):
            self._points[i] = rmat * point
            
    def rotateZ(self, angle):
        "Rotiert die Punkte um die Z-Achse"
        rmat = HomMatrix3()
        rmat.setRotation(0,0,1,angle)
        for i, point in enumerate(self._points):
            self._points[i] = rmat * point
    
    def __getitem__(self, key):
        "Called to implement evaluation of self[key]."
        return self._points[key]
        