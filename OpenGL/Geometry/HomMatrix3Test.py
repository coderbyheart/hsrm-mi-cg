# -*- coding: utf-8 -*-

from HomMatrix3 import HomMatrix3, FrustrumMatrix
from HomVec3 import HomVec3
import unittest

class HomMatrix3Test(unittest.TestCase):
    "Unittest für HomMatrix3"
    
    def test_add(self):
        m1 = HomMatrix3(1,-3,2,1,2,7)
        m2 = HomMatrix3(0,3,5,2,1,-1)
        m3 = m1 + m2
        self.assertEqual(1, m3[0])
        self.assertEqual(0, m3[1])
        self.assertEqual(7, m3[2])
        self.assertEqual(3, m3[3])
        self.assertEqual(3, m3[4])
        self.assertEqual(6, m3[5])
        
    def test_sub(self):
        m1 = HomMatrix3(1,-3,2,1,2,7)
        m2 = HomMatrix3(0,3,5,2,1,-1)
        m3 = m1 - m2
        self.assertEqual(1, m3[0])
        self.assertEqual(-6, m3[1])
        self.assertEqual(-3, m3[2])
        self.assertEqual(-1, m3[3])
        self.assertEqual(1, m3[4])
        self.assertEqual(8, m3[5])
        
    def test_setscale(self):
        m1 = HomMatrix3()
        m1.setScale(1,2,3)
        self.assertEqual(1, m1[0])
        self.assertEqual(2, m1[5])
        self.assertEqual(3, m1[10])
        
    def test_settrans(self):
        m1 = HomMatrix3()
        m1.setTranslation(1,2,3)
        self.assertEqual(1, m1[3])
        self.assertEqual(2, m1[7])
        self.assertEqual(3, m1[11])
        
    def test_setrot(self):
        m1 = HomMatrix3()
        m1.setRotation(1,2,3,45)
        
    def test_rotate(self):
        m = HomMatrix3()
        m.setRotation(0,0,1,90)
        p = HomVec3(1,0,0,True)
        pr = m * p
        self.assertEqual(0.0, round(pr.x))
        self.assertEqual(-1.0, round(pr.y))
        self.assertEqual(0.0, round(pr.z))
        
    def test_aufg3_6(self):
        m1 = HomMatrix3()
        m1.setTranslation(-1,0,0)
        m2 = HomMatrix3()
        m2.setRotation(1,1,1,45)
        m3 = HomMatrix3()
        m3.setTranslation(1,0,0)
        #print(m1 * m2 * m3)
        
    def test_frustrum(self):
        ## Sichtvolumen Kamera
        xl = -2 # Linke Ecke
        xr = 2  # rechte  Ecke
        yb = -4 # untere Ecke
        yt = 4 # obere Ecke
        N = 1
        F = 100
        f = FrustrumMatrix(xl, xr, yb, yt, N, F)
        self.assertEqual(1/2, f[0])
        self.assertEqual(1/4, f[5])
        self.assertEqual(-(101/99), f[10])
        self.assertEqual(-(200/99), f[11])
        self.assertEqual(-1, f[14])
        self.assertEqual(0, f[15])
        
        p = HomVec3(10,10,-10,1)
        pt = f * p 
        self.assertEqual(5, pt.x)
        self.assertEqual(5/2, pt.y)
        self.assertEqual(round(90/11, 6), round(pt.z, 6))
        self.assertEqual(10, pt.w)
        
        ptn = pt.normalized()
        self.assertEqual(round(1/2, 6), round(ptn.x, 6))
        self.assertEqual(round(1/4, 6), round(ptn.y, 6))
        self.assertEqual(round(9/11, 6), round(ptn.z, 6))
        self.assertEqual(1, ptn.w)
    
if __name__ == '__main__':
    unittest.main()