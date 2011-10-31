# -*- coding: utf-8 -*-

from HomVec3 import HomVec3
import unittest
from math import sqrt

class HomVec3Test(unittest.TestCase):
    """Unittests für HomVec3"""
    
    def test_create(self):
        p = HomVec3(1,2,3,True)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
        self.assertEqual(p.z, 3)
        self.assertEqual(p.isPoint(), True)
        
    def test_length(self):
        p = HomVec3(1,1,1)
        self.assertEquals(sqrt(3), p.length())
        p = HomVec3(2,2,2)
        self.assertEquals(sqrt(12), p.length())
        p = HomVec3(1,0,0)
        self.assertEquals(1, p.length())
        p = HomVec3(0,1,0)
        self.assertEquals(1, p.length())
        p = HomVec3(0,0,1)
        self.assertEquals(1, p.length())
        
    def test_add(self):
        for (p,q,r) in [
                      ((1,2,3),(4,5,6),(5,7,9)),
                      ((1,2,3),(-4,-5,-6),(-3,-3,-3))
                      ]:
            pv = HomVec3(*p)
            qv = HomVec3(*q)
            rv = pv + qv
            self.assertEqual(r[0], rv.x)
            self.assertEqual(r[1], rv.y)
            self.assertEqual(r[2], rv.z)
    
    def test_sub(self):
        for (p,q,r) in [
                      ((1,2,3),(4,5,6),(-3,-3,-3)),
                      ((1,2,3),(-4,-5,-6),(5,7,9))
                      ]:
            pv = HomVec3(*p)
            qv = HomVec3(*q)
            rv = pv - qv
            self.assertEqual(r[0], rv.x)
            self.assertEqual(r[1], rv.y)
            self.assertEqual(r[2], rv.z)
            
    def test_scalar(self):
        self.assertEquals(32, HomVec3(1,2,3) * HomVec3(4,5,6))
        
    def test_norm(self):
        p = HomVec3(3,4,5)
        p.normalize()
        self.assertEquals(1, round(p.length(), 10))
        self.assertEquals(3/sqrt(50), p.x)
        self.assertEquals(4/sqrt(50), p.y)
        self.assertEquals(5/sqrt(50), p.z)
        
    def test_cross(self):
        p = HomVec3(1,2,3) % HomVec3(-7,8,9)
        self.assertEqual(-6, p.x)
        self.assertEqual(-30, p.y)
        self.assertEqual(22, p.z)
        
    def test_mult(self):
        p = HomVec3(1,2,3) * 2
        self.assertEquals(2, p.x)
        self.assertEquals(4, p.y)
        self.assertEquals(6, p.z)
        
    def test_angle(self):
        self.assertEqual(18.43, round(HomVec3(1,1,0).angle(HomVec3(2,1,0)), 2))
        self.assertEqual(45, round(HomVec3(1,1,0).angle(HomVec3(1,0,0))))        
        
    def test_triangle_area(self):
        p1, p2, p3 = HomVec3(2,2,0,True), HomVec3(4,5,0,True), HomVec3(6,3,0,True)
        self.assertEquals(5, ((p2-p1)%(p3-p1)).length()/2.0)
        self.assertEquals(5, (p1%p2+p2%p3+p3%p1).length()/2.0)
        
        p1, p2, p3 = HomVec3(1,1,0,True), HomVec3(4,1,0,True), HomVec3(1,4,0,True)
        self.assertEquals(9/2.0, ((p2-p1)%(p3-p1)).length()/2.0)
        self.assertEquals(9/2.0, (p1%p2+p2%p3+p3%p1).length()/2.0)

if __name__ == '__main__':
    unittest.main()