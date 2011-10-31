# -*- coding: utf-8 -*-
"""Parser für .obj-Dateien
Siehe http://paulbourke.net/dataformats/obj/"""

import re
import os
from PointCloud import PointCloud
from HomVec3 import HomVec3

class TriangleFaceCloud(PointCloud):
    
    def __init__(self):
        super(TriangleFaceCloud,self).__init__()
        self.faces = []
        self.normals = []
        self.textcoords = []
    
    def addFace(self, points, normals = None, texcoords = None):
        "Fügt ein Dreick mit den drei gegebenen Punkten hinzu"
        # Indices are 1-based
        # points
        p1i = int(points[0]) - 1
        p2i = int(points[1]) - 1
        p3i = int(points[2]) - 1
        # normals
        normalIndices = None
        if normals[0] != None and normals[1] != None and normals[2] != None:
            n1i = int(normals[0]) - 1
            n2i = int(normals[1]) - 1
            n3i = int(normals[2]) - 1
            normalIndices = (n1i, n2i, n3i)
        # texture coordinates
        textureIndices = None
        if texcoords[0] != None and texcoords[1] != None and texcoords[2] != None:
            t1i = int(texcoords[0]) - 1
            t2i = int(texcoords[1]) - 1
            t3i = int(texcoords[2]) - 1
            textureIndices = (t1i, t2i, t3i)
        self.faces.append(Face((p1i, p2i, p3i), normalIndices, textureIndices))

    def addNormal(self, p1, p2, p3):
        "Fügt einen Normalenvektor hinzu"
        self.normals.append(HomVec3(p1, p2, p3, 1.0))
        
    def addTexture(self, p1, p2):
        "Fügt eine Texture-Koordinate hinzu"
        self.textcoords.append(HomVec3(p1, p2, 0.0, 1.0))
        
    def normalized(self):
        pn = super(TriangleFaceCloud,self).normalized()
        pn.faces = self.faces
        return pn

class Face(object):
    def __init__(self, points, normals, textureCoords):
        self.points = points
        self.normals = normals
        self.textureCoords = textureCoords

class Material(object):
    name = None
    illum = None
    Kd = None
    ka = None
    Ks = None
    Ke = None
    Ns = None
    map_Kd = None
    
    def __init__(self, name):
        self.name = name

class ObjParser(object):
    
    materials = []
    
    def __init__(self):
        self.facecloud = TriangleFaceCloud()
    
    def read(self, filename):
        "Liest eine .obj-Datei ein"
        commentre = re.compile("^#")
        floatrx = '(-?([0-9]+(\.[0-9]+)?e(\+|-)[0-9]+)|-?([0-9]+(\.[0-9]+)?))'
        vre = re.compile("^v\s+" + floatrx + "\s+" + floatrx + "\s+" + floatrx)
        nre = re.compile("^vn\s+" + floatrx + "\s+" + floatrx + "\s+" + floatrx)
        tre = re.compile("^vt\s+" + floatrx + "\s+" + floatrx)
        facerx = "([0-9]+)(/([0-9]+)?/([0-9]+)?)?"
        fre = re.compile("^f\s+" + facerx + "\s+" + facerx + "\s+" + facerx)
        mtre = re.compile("^mtllib ([^ ]+\.mtl)")
        for line in open(filename).readlines():
            if commentre.match(line):
                continue
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
            # Texture
            tmatch = tre.match(line)
            if tmatch:
                self.facecloud.addTexture(tmatch.groups()[0], tmatch.groups()[6])
                continue
            # Face?
            fmatch = fre.match(line)
            if fmatch:
                self.facecloud.addFace((fmatch.groups()[0], fmatch.groups()[4], fmatch.groups()[8]), (fmatch.groups()[3], fmatch.groups()[7], fmatch.groups()[11]), (fmatch.groups()[2], fmatch.groups()[6], fmatch.groups()[10]))
                continue
            # Material?
            mtmatch = mtre.match(line)
            if mtmatch:
                self.readMaterials(os.path.join(os.path.dirname(filename), mtmatch.groups()[0]))
        return self
    
    def readMaterials(self, filename):
        """Liest eine .mtl-Datei ein
        
        newmtl Material01
        illum 2
        Kd 0.800000 0.800000 0.800000
        Ka 0.200000 0.200000 0.200000
        Ks 0.000000 0.000000 0.000000
        Ke 0.000000 0.000000 0.000000
        Ns 0.000000
        map_Kd squirrel-texture.png
        """
        
        currentMat = None
        commentre = re.compile("^#")
        newmatre = re.compile("^newmtl ([^\s]+)")
        mapre = re.compile("^map_Kd ([^\s]+)")
        illumre = re.compile("^illum ([0-9]+)")
        floatrx = '(-?([0-9]+(\.[0-9]+)?e(\+|-)[0-9]+)|-?([0-9]+(\.[0-9]+)?))'
        kre = re.compile("^(K[dase])\s+" + floatrx + "\s+" + floatrx + "\s+" + floatrx)
        nre = re.compile("^(N[s])\s+" + floatrx)
        for line in open(filename).readlines():
            if commentre.match(line):
                continue
            newmatmatch = newmatre.match(line)
            if newmatmatch:
                if currentMat != None:
                    self.materials.append(currentMat)
                currentMat = Material(newmatmatch.groups()[0])
                continue
            mapmatch = mapre.match(line)
            if mapmatch:
                currentMat.map_Kd = os.path.join(os.path.dirname(filename), mapmatch.groups()[0])
                continue
            illummatch = illumre.match(line)
            if illummatch:
                currentMat.illum = int(illummatch.groups()[0])
                continue
            kmatch = kre.match(line)
            if kmatch:
                t = kmatch.groups()[0]
                val = (kmatch.groups()[1], kmatch.groups()[7], kmatch.groups()[11])
                if t == "Kd":
                    currentMat.Kd = val
                elif t == "Ka":
                    currentMat.Ka = val
                elif t == "Ks":
                    currentMat.Ks = val
                elif t == "Ke":
                    currentMat.Ke = val
            nmatch = nre.match(line)
            if nmatch:
                t = nmatch.groups()[0]
                if t == "Ns":
                    currentMat.Ns = nmatch.groups()[1]
        
        if currentMat != None:
            self.materials.append(currentMat)