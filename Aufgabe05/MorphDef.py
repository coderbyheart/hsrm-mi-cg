# -*- coding: utf-8 -*-

from math import sqrt, pow

class MorphDef(object):
    "Berechnet die Paare von Koordinaten zum Morphen von Shape A nach Shape B "
    _morphdef = []
    shapeA = None
    shapeB = None

    def __init__(self, shapeA, shapeB, nearest = False):
        "Konstruktor: shapeA: Liste mit (x,y)-Tupel, shapeB: Liste mit (x,y)-Tupel, nearest gibt an, ob beim Suchen passender Punkt der nächstgelegene verwendet werden soll"
        self.shapeA = shapeA[:]
        self.shapeB = shapeB[:]
        self.nearest = nearest
        # Finde passende Punkte
        for p in self.shapeA:
            t = self.getNextTarget(p)
            self._morphdef.append((p, t))
        # Sind noch Punkte in shapeB enthalten?
        if len(self.shapeB) > 0:
            for point in self.shapeB:
                # Finde nächsten Punkt in shapeA
                nearestPoint = self.getNearest(self.shapeA, p)
                self._morphdef.append((nearestPoint, point))
        
    def getNextTarget(self, p):
        if len(self.shapeB) > 0:
            # Es sind noch Punkte aus der Ziel-Form zu verteilen
            if self.nearest:
                t = self.getNearest(self.shapeB, p)
                del(self.shapeB[self.shapeB.index(t)])
            else:
                t = self.shapeB[0]
                del(self.shapeB[0])
        else:
            # Nimm bereits vergebene Punkte und verschiebe mit
            nearestPoint = self.getNearest([x[0] for x in self._morphdef], p)
            for md in self._morphdef:
                if md[0] == nearestPoint:
                    t = md[1]
                    break
            
            #nearestPoint = self.getNearest([x[1] for x in self._morphdef], p)
            #t = nearestPoint
        return t

    def getNearest(self, pointList, point):
        pointDistances = []
        for p in pointList:
            pointDistances.append({"p": p, "d": self.getPointDistance(p, point)})
        return sorted(pointDistances, lambda x,y: cmp(x["d"], y["d"]))[0]["p"]

    def getPointDistance(self, p, q):
        "Berechnte die Entfernung zwischen den Punkten p und q"
        x = q[0] - p[0]
        y = q[1] - p[1]
        d = sqrt(pow(x,2) + pow(y,2))
        return d
            

    @property
    def morphdef(self):
        return self._morphdef

if __name__ == "__main__":
    shapeQuad = [
        (0.25, 0.25),
        (0.25, 0.75),
        (0.75, 0.75),
        (0.75, 0.25),
    ]

    shapeTriangle = [
        (0.5, 0.25),
        (0.75, 0.75),
        (0.75, 0.25)
    ]

    shapePoint = [
        (0.5, 0.5)
    ]

    # md = MorphDef(shapeTriangle, shapeQuad)
    # md = MorphDef(shapeQuad, shapeTriangle)
    md = MorphDef(shapePoint, shapeQuad)
    print md.morphdef

