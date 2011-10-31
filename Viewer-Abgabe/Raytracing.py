# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from Vec import Vec
import time



def doRaytracing(cursorX,cursorY ,distancePoint, projectionMatrix, modelMatrix, viewport, model, pickingHit ):
    """ Raytracing machen"""
    #geklickte mausKoordinaten
    x, y = cursorX, viewport[3] - cursorY
    # gepickter Punkt
    point =Vec(gluUnProject(x, y,distancePoint, modelMatrix, projectionMatrix,viewport))
    #Berechnet Picking-ray
    near = Vec(gluUnProject(x, y, 0,            modelMatrix, projectionMatrix, viewport))
    far  = Vec(gluUnProject(x, y, 1,            modelMatrix, projectionMatrix, viewport))
    ray = Ray(near, far - near)

    # Facet des gepickten Bereichs
    facetList = model.nameFacet[model.getName(pickingHit.names[0])]
    minDis = float("inf")
    hitFacet = None
    scaleFactor=model.triangleLen
    for facet in facetList:
       #Punkte des Facet
       points = [Vec(model.v[vortex[0]]) for vortex in facet]
       #Schnellprüfung ob Facet im Bereich des geckligten Puznktes liegt
       if pointInTriangle(point, points, scaleFactor):
           #Dreieck erstellen
           triangle = Triangle(points[0], points[1], points[2])
           #Ray mit Dreieck intersection
           distance = triangle.intersectionParameter(ray)
           #najestes dreieck/Facet bestimmen
           if distance != None and distance < minDis:
               minDis=distance
               hitFacet=facet
    return hitFacet




def pointInTriangle(point, triangle, scaleFactor):
    """ schnellpruefung ob Dreieck inder nähe des Hitpunktes ist"""
    for i in range(3):
        if point[i]<=min(triangle[j][i] for j in range(3))-scaleFactor:
            return False
        if point[i]>=max(triangle[j][i] for j in range(3))+scaleFactor:
            return False
    return True


class Triangle(object):
    """ dreieck"""
    def __init__(self, a, b, c):
        self.a = a # point
        self.b = b # point
        self.c = c # point
        self.u = self.b - self.a # direction vector
        self.v = self.c - self.a # direction vector
        
       

    def __repr__(self):
        return 'Triangle(%s,%s,%s)' % (repr(self.a), repr(self.b), repr(self.c))

    def intersectionParameter(self, ray):
        """prueft ob ay durch dreick geht und leiefert gegebenfalls distance"""
        w = ray.origin - self.a
        dv = ray.direction.kreuzprodukt(self.v)
        dvu = dv.dot(self.u)
        if dvu == 0.0:
            return None
        r = dv.dot(w) / dvu
        if r<0 and r>1:
            return None
        wu = w.kreuzprodukt(self.u)
       
        s = wu.dot(ray.direction) / dvu
        
        if s>=0 and s<=1 and r+s <=1:
            return wu.dot(self.v) / dvu
        else:
            return None



class Ray():
    """ Ray-darstelllung """
    def __init__(self, origin, direction):
        self.origin = origin # point
        self.direction = direction.normalized() # vector

    def __repr__(self):
        return 'Ray(%s,%s)' % (repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + self.direction * t

if __name__ == "__main__":
   import newGoogleBody
   newGoogleBody.main()
