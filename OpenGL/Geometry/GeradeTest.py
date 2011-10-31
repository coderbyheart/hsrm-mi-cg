# -*- coding: utf-8 -*-

import unittest
from Gerade import Gerade
from HomVec3 import HomVec3

class GeradeTest(unittest.TestCase):
    "Unittest für Gerade"
    
    def test_schneide(self):
        g1 = Gerade(HomVec3(1.5, 3, 0, 1), HomVec3(4.5, 3, 0, 1))
        g2 = Gerade(HomVec3(3, 1.5, 0, 1), HomVec3(3, 4.5, 0, 1))
        s = g1.schnittpunkt2D(g2)
        self.assertEqual(3.0, s.x)
        self.assertEqual(3.0, s.y)
        self.assertEqual(0.0, s.z)
        self.assertEqual(1.0, s.w)
        
    def test_schneide(self):
        g1 = Gerade(HomVec3(1.5, 3, 1, 1), HomVec3(4.5, 3, 1, 1))
        g2 = Gerade(HomVec3(3, 1.5, 1, 1), HomVec3(3, 4.5, 1, 1))
        s = g1.schnittpunkt2DHomVec(g2)
        self.assertEqual(3.0, s.x)
        self.assertEqual(3.0, s.y)
        self.assertEqual(0.0, s.z)
        self.assertEqual(1.0, s.w)
    
if __name__ == '__main__':
    unittest.main()