# -*- coding: utf-8 -*-
'Repräsentiert eine Gerade'

from HomVec3 import HomVec3

class Gerade(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
    def schnittpunkt2DHomVec(self, g):
        "Berechnet den Schnittpunkt zwischen dieser Gerade und g mittels des Kreuzproduktes. Funktioniert nur in 2D. Z muss 1 sein"
        g1 = self.start.cross(self.end)
        g2 = g.start.cross(g.end)
        s = g1.cross(g2)
        c = HomVec3(s.x/s.z, s.y/s.z, 0, 1)
        return c
                
    def schnittpunkt2D(self, g):
        "Berechnet den Schnittpunkt zwischen dieser Gerade und g im 2D-Raum"
        # See http://paulbourke.net/geometry/lineline2d/
        
        d = ((g.end.y - g.start.y)*(self.end.x - self.start.x)) - ((g.end.x - g.start.x)*(self.end.y - self.start.y))
        a = ((g.end.x - g.start.x)*(self.start.y - g.start.y)) - ((g.end.y - g.start.y)*(self.start.x - g.start.x))
        b = ((self.end.x - self.start.x)*(self.start.y - g.start.y)) - ((self.end.y - self.start.y)*(self.start.x - g.start.x))

        if d == 0:
            if a == 0 and b == 0:
                # Gerade sind gleich
                return None
            # Geraden sind parallel
            return None
        
        ua = a / d;
        ub = b / d;

        if ua >= 0 and ua <= 1 and ub >= 0 and ub <= 1:
            x = self.start.x + ua*(self.end.x - self.start.x);
            y = self.start.y + ua*(self.end.y - self.start.y);

            return HomVec3(x, y, 0, 1)

        # Kein Schnittpunkt
        return None;