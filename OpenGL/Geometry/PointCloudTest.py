# -*- coding: utf-8 -*-

import unittest
from PointCloud import PointCloud

class PointCloudTest(unittest.TestCase):
    """Unittests für PointCloud"""
    
    def test_wuerfel5(self):
        pc = PointCloud()
        pc.readRaw('data/wuerfel5_points.raw')
        
        bb = pc.getBoundingBox()
        self.assertEqual(5.0, bb['x'])
        self.assertEqual(5.0, bb['y'])
        self.assertEqual(0.0, bb['z'])
        self.assertEqual(0.0, bb['-x'])
        self.assertEqual(0.0, bb['-y'])
        self.assertEqual(-5.0, bb['-z'])
        
        self.assertEqual(5.0, pc.getXSize())
        self.assertEqual(5.0, pc.getYSize())
        self.assertEqual(5.0, pc.getZSize())
        
    def test_wuerfel_normalize(self):
        #for file in ['data/line_points.raw']:
        for file in ['data/wuerfel5_points.raw', 'data/wuerfel5-allpos_points.raw', 'data/wuerfel5-allneg_points.raw', 'data/wuerfel10_points.raw']:
            pc = PointCloud()
            pc.readRaw(file)
            pcn = pc.normalized()
        
            bb = pcn.getBoundingBox()
            self.assertEqual(1.0, bb['x'])
            self.assertEqual(1.0, bb['y'])
            self.assertEqual(1.0, bb['z'])
            self.assertEqual(-1.0, bb['-x'])
            self.assertEqual(-1.0, bb['-y'])
            self.assertEqual(-1.0, bb['-z'])
            
            self.assertEqual(2.0, pcn.getXSize())
            self.assertEqual(2.0, pcn.getYSize())
            self.assertEqual(2.0, pcn.getZSize())

if __name__ == '__main__':
    unittest.main()