import unittest
import sys

class CohenSutherland(object):
    def __init__(self, xmin, ymin, xmax, ymax):
        #print("Bereich: ", xmin, ymin, xmax, ymax)
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        
    def mask(self, x, y):
        "Erzeugt die Bitmaske für den Punkt an der Stelle x, y"
        mask = 0
        if x - self.xmin < 0:
            mask = mask | 1
        if self.xmax - x < 0:
            mask = mask | (1 << 2)
        if y - self.ymin < 0:
            mask = mask | (1 << 3)
        if self.ymax - y < 0:
            mask = mask | (1 << 4)
        return mask
    
    def clip(self, *c):
        #print(c)
        c = list(c)
        c1 = self.mask(c[0], c[1])
        c2 = self.mask(c[2], c[3])
        lc = c1|c2
        if lc == 0:
            # Linie liegt vollständig innerhalb
            return (c[0], c[1], c[2], c[3])
        if c1&c2 != 0:
            # Linie liegt vollständig außerhalb
            return None
        
        if lc & 1 == 1:
            #print("Berechne Schnitt mit xmin")
            y = ((c[3] - c[1])/(c[2] - c[0]))*(self.xmin-c[2]) + c[3]
            if c[0] < self.xmin:
                c[0] = self.xmin
                c[1] = y
            if c[2] < self.xmin:
                c[2] = self.xmin
                c[3] = y
        if lc & 1 << 2 == 1 << 2:
            #print("Berechne Schnitt mit xmax")
            y = ((c[3] - c[1])/(c[2] - c[0]))*(self.xmax-c[2]) + c[3]
            if c[0] > self.xmax:
                c[0] = self.xmax
                c[1] = y
            if c[2] > self.xmax:
                c[2] = self.xmax
                c[3] = y
        if lc & 1 << 3 == 1 << 3:
            #print("Berechne Schnitt mit ymin")
            x = ((c[2] - c[0])/(c[3] - c[1]))*(self.ymin-c[3]) + c[2]
            if c[1] < self.ymin:
                c[0] = x
                c[1] = self.ymin
            if c[3] < self.ymin:
                c[2] = x 
                c[3] = self.ymin
        if lc & 1 << 4 == 1 << 4:
            #print("Berechne Schnitt mit ymax")
            x = ((c[2] - c[0])/(c[3] - c[1]))*(self.ymax-c[3]) + c[2]
            if c[1] > self.ymax:
                c[0] = x
                c[1] = self.ymax
            if c[3] > self.ymax:
                c[2] = x
                c[3] = self.ymax
        return self.clip(c[0], c[1], c[2], c[3])
        
class CohenSutherlandTest(unittest.TestCase):
    "Unittest für CohenSutherland"
    
    def test_simple(self):
        cs = CohenSutherland(1,1,5,4)
        p =(8,5)
        q =(2,2)
        c1 = cs.mask(*p)
        c2 = cs.mask(*q)
        self.assertTrue(c1|c2 != 0)
        self.assertTrue(c1 & c2 == 0)
        
    def test_inside(self):
        cs = CohenSutherland(1,1,5,4)
        p =(3,3)
        q =(2,2)
        c1 = cs.mask(*p)
        c2 = cs.mask(*q)
        self.assertTrue(c1|c2 == 0)
    
    def test_outside(self):
        cs = CohenSutherland(1,1,5,4)
        p =(7,7)
        q =(6,6)
        c1 = cs.mask(*p)
        c2 = cs.mask(*q)
        self.assertTrue(c1&c2 != 0)
        
    def test_clip_outside(self):
        cs = CohenSutherland(0,0,8,6)
        # beide aussen
        l = cs.clip(2,-2,10,6)
        self.assertEqual(4,l[0])
        self.assertEqual(0,l[1])
        self.assertEqual(8,l[2])
        self.assertEqual(4,l[3])
        
    def test_clip(self):
        cs = CohenSutherland(0,0,8,6)
        # Rechts aussen
        l = cs.clip(6,2,10,6)
        self.assertEqual(6,l[0])
        self.assertEqual(2,l[1])
        self.assertEqual(8,l[2])
        self.assertEqual(4,l[3])
        # links aussen
        l = cs.clip(6,2,2,-2)
        self.assertEqual(6,l[0])
        self.assertEqual(2,l[1])
        self.assertEqual(4,l[2])
        self.assertEqual(0,l[3])

if __name__ == '__main__':
    unittest.main()