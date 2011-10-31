# -*- coding: utf-8 -*-

from Camera import Camera
from math import tan, radians, fabs
from Ray import Ray
from RGB import RGB
from PIL import Image
import sys

class Raytracer(object):
    "Ein einfacher Raytracer"
    
    _bg = RGB(0,0,0)
    _ambient = RGB(0.1,0.1,0.1)
    
    def __init__(self, width, height):
        self._width = float(width)
        self._height = float(height)
        self._objlist = []
        self._lights = []
        
    def addObject(self, obj):
        self._objlist.append(obj)
        
    def addLight(self, light):
        self._lights.append(light)

    def render(self):
        self._image = Image.new('RGB', (int(self._width), int(self._height)), self._bg.rgb)
        self._cameraangle = self.camera.angle / 2
        self._viewheight = 2 * tan(radians(self._cameraangle))
        self._viewwidth = (self._width / self._height) * self._viewheight
        self._pixelWidth = self._viewwidth / (self._width - 1)
        self._pixelHeight = self._viewheight / (self._height - 1)
        
        self._camerapos = self.camera.position
        self._f = self.camera.getFVector()
        self._s = self.camera.getSVector()
        self._u = self.camera.getUVector()
        
        for y in range(int(self._height)):
            sys.stdout.write("%d%%\n" % ((float(y) / self._height) * 100))
            sys.stdout.write("\033[1A")
            for x in range(int(self._width)):
                ray = self.calcRay(x, y)
                maxdist = float('inf')
                hit = False
                hitObject = None
                color = self._bg
                for object in self._objlist:
                    hitdist = object.intersectionParameter(ray)
                    if hitdist:
                        hit = True
                        if hitdist < maxdist:
                            maxdist = hitdist
                            color = object.colorAt(ray)
                            hitObject = object
                if hit:
                    # Schatten?
                    # Schnittpunkt
                    intP = (ray.direction * maxdist) + self._camerapos
                    for light in self._lights:
                        # prüfe, ob Lichtstrahl geschnitten wird
                        lightRay = Ray(intP, light.position - intP)
                        shadow = False
                        for lobject in self._objlist:
                            sHitDist = lobject.intersectionParameter(lightRay)
                            # Eigenschatten von Kugeln
                            #if sHitDist is not None and fabs(sHitDist) < 0.000001:
                            # Schatten auf Kugeln und Ebene
                            if sHitDist is not None and sHitDist > -0.000001:
                            # Schatten auf Flächen
                            #if sHitDist is not None and sHitDist > 0.000001:
                            #if sHitDist is not None and sHitDist < 0.000001:
                                shadow = True
                                break
                        # Add Light
                        if not shadow:
                            color = color + light.color
                    # Add ambient
                    color = color + self._ambient
                    # Darken in distance
                    color = color - RGB(1,1,1) * min((max(((maxdist - 20) / 100), 0), 1))
                self._image.putpixel((x, int(self._height - y - 1)), color.getRGB())
        sys.stdout.write("\n")
        self._image.save('render.png', 'PNG')
    
    def calcRay(self, x, y):
        xcomp = self._s.scale(x * self._pixelWidth - self._viewwidth/2)
        ycomp = self._u.scale(y * self._pixelHeight - self._viewheight/2)
        return Ray(self._camerapos, self._f + xcomp + ycomp) # evtl. mehrere Strahlen pro Pixel
                
    def setCamera(self, c):
        if not isinstance(c, Camera):
            raise RaytraceException("Must provide an instance of Camera")
        self._camera = c
        return self
    def getCamera(self):
        return self._camera
    camera = property(getCamera, setCamera, None, "The camera")

if __name__ == "__main__":
    from Sphere import ColoredSphere
    from Plane import ColoredPlane
    from Triangle import ColoredTriangle
    from HomVec3  import HomVec3
    from Light import PointLight
    
    c = Camera()
    c.position = HomVec3(0,2,10,True)
    # c.position = HomVec3(30,30,10,True)
    c.up = HomVec3(0,1,0)
    c.target = HomVec3(0,3,0,True)
    c.angle = 45

    r = Raytracer(400, 400)
    r.camera = c
    r.addObject(ColoredPlane(HomVec3(0,0,0,True), HomVec3(0,1,0), RGB(0.5,0.5,0.5)))
    r.addObject(ColoredSphere(HomVec3(2.5,3,-10,True), 2, RGB(0.5,0,0)))
    r.addObject(ColoredSphere(HomVec3(-2.5,3,-10,True), 2, RGB(0,0.5,0)))
    r.addObject(ColoredSphere(HomVec3(0,7,-10,True), 2, RGB(0,0,0.5)))
    r.addObject(ColoredTriangle(HomVec3(2.5,3,-10,True),HomVec3(-2.5,3,-10,True), HomVec3(0,7,-10,True), RGB(0.95,.7,0.07)))
    r.addLight(PointLight(HomVec3(30,30,10,True)))
    
    #r.addObject(ColoredSphere(HomVec3(0,1,0,True), 1, RGB(0,0.5,0)))
    #r.addObject(ColoredSphere(HomVec3(2.5,1,0,True), 1.5, RGB(0,0,0.5)))
    #r.addLight(PointLight(HomVec3(10,0,0,True)))
    #c.position = HomVec3(20,0,0,True)
    
    r.render()