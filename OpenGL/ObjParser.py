# -*- coding: utf-8 -*-
"""Parser für .obj-Dateien
Siehe http://paulbourke.net/dataformats/obj/"""

import re
from Geometry.PointCloud import PointCloud
from Geometry.HomVec3 import HomVec3

class TriangleFaceCloud(PointCloud):
    
    def __init__(self):
        super(TriangleFaceCloud,self).__init__()
        self.faces = []
        self.normals = []
    
    def addFace(self, points, normals = None):
        "Fügt ein Dreick mit den drei gegebenen Punkten hinzu"
        # Indices are 1-based
        # points
        p1i = int(points[0]) - 1
        p2i = int(points[1]) - 1
        p3i = int(points[2]) - 1
        c1 = self[p1i]
        c2 = self[p2i]
        c3 = self[p3i]
        # normals
        normalIndices = None
        if normals[0] != None and normals[1] != None and normals[2] != None:
            n1i = int(normals[0]) - 1
            n2i = int(normals[1]) - 1
            n3i = int(normals[2]) - 1
            nc1 = self.normals[n1i]
            nc2 = self.normals[n2i]
            nc3 = self.normals[n3i]
            normalIndices = (n1i, n2i, n3i)
        self.faces.append(Face((p1i, p2i, p3i), normalIndices))

    def addNormal(self, p1, p2, p3):
        "Fügt einen Normalenvektor hinzu"
        self.normals.append(HomVec3(p1, p2, p3, 1.0))
        
    def normalized(self):
        pn = super(TriangleFaceCloud,self).normalized()
        pn.faces = self.faces
        return pn

class Face(object):
    def __init__(self, points, normals):
        self.points = points
        self.normals = normals

class ObjParser(object):
    
    def __init__(self):
        self.facecloud = TriangleFaceCloud()
    
    def read(self, filename):
        "Liest eine .obj-Datei ein"
        floatrx = '(-?([0-9]+(\.[0-9]+)?e(\+|-)[0-9]+)|-?([0-9]+(\.[0-9]+)?))'
        vre = re.compile("^v\s+" + floatrx + "\s+" + floatrx + "\s+" + floatrx)
        nre = re.compile("^vn\s+" + floatrx + "\s+" + floatrx + "\s+" + floatrx)
        facerx = "([0-9]+)(/([0-9]+)?/([0-9]+)?)?"
        fre = re.compile("^f\s+" + facerx + "\s+" + facerx + "\s+" + facerx)
        for line in open(filename).readlines():
            # Point?
            vmatch = vre.match(line)
            if vmatch:
                self.facecloud.addPoint(vmatch.groups()[0], vmatch.groups()[6], vmatch.groups()[12])
                continue
            # Normal?
            nmatch = nre.match(line)
            if nmatch:
                self.facecloud.addNormal(nmatch.groups()[0], nmatch.groups()[6], nmatch.groups()[12])
                continue
            # Face?
            fmatch = fre.match(line)
            if fmatch:
                self.facecloud.addFace((fmatch.groups()[0], fmatch.groups()[4], fmatch.groups()[8]), (fmatch.groups()[3], fmatch.groups()[7], fmatch.groups()[11]))
                continue
        return self
