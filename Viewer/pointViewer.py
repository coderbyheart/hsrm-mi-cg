#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
Einfacher OpenGL-Viewer

@author: Markus Tacker <m@tacker.org>

Konsolen-Argumente:
    <file>:
        Die .OBJ-Datei mit dem anzuzeigenden Model kann übergeben werden

Tastaturkommandos:

    Escape: 
        Viewer beenden
    x,X,y,Y,z,Z: 
        Modell um die jeweilige Achse drehen
    m:
        Modell-Koordinatensystem ein- bzw. ausblenden
    t:
        Textur ein- bzw. ausschalten

Mauskommandos:

    Linke Maustause + ziehen:
        Modell um die X- und Y-Achse drehen
        
    Shift + Linke Maustause + ziehen:
        Modell um die Z- und Y-Achse drehen
        
    Mittlere Maustause + Hoch bzw. Runter ziehen:
        Kamera zum Modell hin, bzw. vom Modell weg bewegen
        
    Rechte Maustaste + ziehen:
        X- und Y-Position des Modells verändern

    Shift + Rechte Maustaste + ziehen:
        X- und Z-Position des Lichts verändern

"""

from util.PointCloud import PointCloud
from util.ObjParser import ObjParser
from viewer.Config import Config
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
from itertools import cycle
import sys
import math
import os
import platform
import numpy
if platform.system() == "Linux" and os.uname()[4] == "i686":
    import psyco #@UnresolvedImport
    psyco.full()
    
config = Config()
op = None # Instanz von ObjParser
pc = None # Instanz von PointCloud

# Display-Liste
modelList = None

texture = None

def init(width, height):
    """ Initialize an OpenGL window """
    global modelList, currentRenderMode, texture
    
    modelList = glGenLists(1)
    glNewList(modelList, GL_COMPILE)
    renderModel()
    glEndList()
    
    if len(op.materials) > 0:
        for material in op.materials:
            # FIXME: Support für mehrere Texturen
            # Texturen einlesen
            image = Image.open(material.map_Kd)
            twidth, theight = image.size
            image_data = numpy.array(list(image.getdata()), numpy.int8)
                                   
            texture = glGenTextures(1)
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glBindTexture(GL_TEXTURE_2D, texture)
            
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, twidth, theight, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

            glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

def display():
    """ Render all objects"""
    global config
      
    glClearColor(*config.bgcolor)            #background color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #clear screen
    
    glPushMatrix()
    glLoadIdentity()
    gluLookAt(0 + config.xPosCamera,0 + config.yPosCamera,3 + config.zPosCamera, 0,0,config.zPosCamera, 0,1,0)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glShadeModel(GL_SMOOTH)

    glLightfv(GL_LIGHT0, GL_POSITION, [config.xPosLight, config.yPosLight, config.zPosLight, 1.0])
    
    drawModel()
    
    glPopMatrix()
    
    #glutSwapBuffers()

def drawModel():
    global config, texture
    # +++++++++ MODEL
    glPushMatrix()

    # Drehung
    glRotatef(config.xAngle, 1, 0, 0)
    glRotatef(config.yAngle, 0, 1, 0)
    glRotatef(config.zAngle, 0, 0, 1)
    
    # Zeichne Achsen
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)

    if config.showModelCross:
        glBegin(GL_LINES)
        glColor(1.0, 0.0, 0.0)
        glVertex3f(-10,0,0)
        glVertex3f(10,0,0)
        glColor(0.0, 1.0, 0.0)
        glVertex3f(0,-10,0)
        glVertex3f(0,10,0)
        glColor(0.0, 0.0, 1.0)
        glVertex3f(0,0,-10)
        glVertex3f(0,0,10)
        glEnd()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Position
    glTranslatef(config.xPosModel, config.yPosModel, config.zPosModel)
    
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_COLOR_MATERIAL)
    if config.useTexture and texture != None:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)
        
        glColor4f(2.2, 2.2, 2.2, 1.0)
        
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, 0)  
        
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.6, 0.6, 0.6, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.6, 0.6, 0.6, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.8, 0.8, 0.8, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 15)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)    
        glLightModeli( GL_LIGHT_MODEL_COLOR_CONTROL, GL_SEPARATE_SPECULAR_COLOR )
        
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0, 0, 0, 0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.8, 0.8, 0.8, 0])
    else:  
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        # Farbe    
        glColor(config.mcolor[0], config.mcolor[1], config.mcolor[2])
    
    #glutSolidTeapot(0.75)
    glCallList(modelList)
    # pick(0,0)

    glPopMatrix()
    
    glutSwapBuffers()

def renderModel():
    global config
    glBegin(GL_TRIANGLES)
    for face in pc.faces:
        for index, pointIndex in enumerate(face.points):
            point = pc[pointIndex]
            if face.normals != None:
                normal = op.facecloud.normals[face.normals[index]]
                glNormal3f(normal.x, normal.y, normal.z)
            if face.textureCoords != None:
                textureCoord = op.facecloud.textcoords[face.textureCoords[index]]
                glTexCoord2f(textureCoord.x, -textureCoord.y); 
            glVertex3f(point.x, point.y, point.z)
    glEnd()

def reshape(width, height):
    """ adjust projection matrix to window size"""
    global config
    config.windowWidth = width
    config.windowHeight = height
    viewMatrix()

def viewMatrix():
    global config
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, config.windowWidth, config.windowHeight)
    gluPerspective(60.0, 1.0 * config.windowWidth/config.windowHeight, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def keyPressed(key, x, y):
    """ handle keypress events """
    global config
    if key == 'x':
        # Rotiere um X-Achse, im Uhrzeigersinn
        config.xAngle += 1
    if key == 'X':
        # Rotiere um X-Achse, gegen den Uhrzeigersinn
        config.xAngle -= 1
    if key == 'y':
        # Rotiere um Y-Achse, im Uhrzeigersinn
        config.yAngle += 1
    if key == 'Y':
        # Rotiere um Y-Achse, gegen den Uhrzeigersinn
        config.yAngle -= 1
    if key == 'z':
        # Rotiere um Z-Achse, im Uhrzeigersinn
        config.zAngle += 1
    if key == 'Z':
        # Rotiere um Z-Achse, gegen den Uhrzeigersinn
        config.zAngle -= 1
    if key == chr(27): # chr(27) = ESCAPE
        sys.exit()
    
    if key == 'm':
        config.showModelCross = not config.showModelCross
        
    if key == 't':
        config.useTexture = not config.useTexture

    glutPostRedisplay()

def mouse(button, state, x, y):
    """ handle mouse events """
    global config
    config.mouseLastX, config.mouseLastY = None, None
    
    if state == GLUT_UP:
        config.mousePressed = False
        config.leftMousePressed = False
        config.middleMousePressed = False
        config.rightMousePressed = False
        return
    
    config.mousePressed = True
    
    if button == GLUT_LEFT_BUTTON:
        config.leftMousePressed = True
    if button == GLUT_MIDDLE_BUTTON:
        config.middleMousePressed = True
    if button == GLUT_RIGHT_BUTTON:
        config.rightMousePressed = True
        
    pick(x, y)
    
def pick(x, y):
    global config
    
    viewMatrix()
    
    glPushMatrix()
    glLoadIdentity()
    gluLookAt(0 + config.xPosCamera,0 + config.yPosCamera,3 + config.zPosCamera, 0,0,config.zPosCamera, 0,1,0)

    glRotatef(config.xAngle, 1, 0, 0)
    glRotatef(config.yAngle, 0, 1, 0)
    glRotatef(config.zAngle, 0, 0, 1)
    
    glTranslatef(config.xPosModel, config.yPosModel, config.zPosModel)
    
    ccolor = 1
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)
    glBegin(GL_TRIANGLES)
    for face in pc.faces:
        r = ccolor % 0xFF
        g = (ccolor / 0xFF) % 0xFF
        b = (ccolor / 0xFF / 0xFF) % 0xFF
        glColor3ub(r,g,b)
        for index, pointIndex in enumerate(face.points):
            point = pc[pointIndex]
            if face.normals != None:
                normal = op.facecloud.normals[face.normals[index]]
                glNormal3f(normal.x, normal.y, normal.z)
            if face.textureCoords != None:
                textureCoord = op.facecloud.textcoords[face.textureCoords[index]]
                glTexCoord2f(textureCoord.x, -textureCoord.y)
            glVertex3f(point.x, point.y, point.z)
        ccolor += 100;
    glEnd()
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    print x,config.windowHeight - y
    
    print glReadPixelsub(x, config.windowHeight - y, 1, 1, GL_RGB)
    
    glPopMatrix()
    glutSwapBuffers()
    
def pickMatrix(x, y):
    glSelectBuffer(512)
    glRenderMode(GL_SELECT)
    glMatrixMode (GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    viewport = glGetIntegerv(GL_VIEWPORT)
    gluPickMatrix(x,viewport[3]-y, 5,5, viewport)
    viewMatrix()
    proMat = glGetDouble(GL_PROJECTION_MATRIX)
    
    glInitNames()
    glMatrixMode(GL_MODELVIEW)
    glPushName(0)
    glLoadIdentity()
    gluLookAt(0 + config.xPosCamera,0 + config.yPosCamera,3 + config.zPosCamera, 0,0,config.zPosCamera, 0,1,0)
    renderModel()
    modMat = glGetDouble(GL_MODELVIEW_MATRIX)
    glPopName()
    
    hits = glRenderMode(GL_RENDER)
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW);
    glFlush()
       
    # treffer  verarbeiten
    if len(hits)>0:
        hit = reduce(getNearestHit, hits)
        distance = min(hits[0].near, hit.far)
        point = gluUnProject(x, viewport[3]-y, distance, modMat, proMat, viewport)
        print "name: ", hit.names
        print "point:  ", point
        
        """
        
        facet = Raytracing.doRaytracing(x, y, distance, proMat, modMat, viewport, model, hit)
        print "name: ", hit.names, model.getName(hit.names[0])
        
        print "point:  ", point
        print "facet:  ", facet
        if facet is not None:
           vortex= [model.v[face[0]] for face in facet]
           print "vortex: ", vortex
        centerFacet( point, facet)
        print "time: ", time.time()-tim
        return model.getName(hit.names[0])
        """
        
    
def getNearestHit(hit0, hit1):
   """ holt vordesten hit vom Picking """
   if hit0.near < hit1.near:
      return hit0
   return hit1

def mouseMotion(x,y):
    """ handle mouse motion """
    global config
    shift = glutGetModifiers() & GLUT_ACTIVE_SHIFT
    
    xdiff = 0
    ydiff = 0
    
    if config.mouseLastX != None:
        xdiff = x - config.mouseLastX
    if config.mouseLastY != None:
        ydiff = y - config.mouseLastY
    
    if config.leftMousePressed:
        if xdiff != 0:
            if shift:
                config.zAngle += xdiff
            else:
                config.yAngle += xdiff
        if ydiff != 0:
            config.xAngle += ydiff
            
    if config.middleMousePressed:
        # Zoom, eine Bildschirmhöhe ist Entfernung um 10 Einheiten
        zScale = float(config.windowHeight) / 10.0
        if ydiff != 0:
            config.zPosCamera += ydiff / zScale
            glutReshapeWindow(config.windowWidth, config.windowHeight)
            
    if config.rightMousePressed:
        # Verschieben, eine Bildschirmbreite ist Entfernung um 1 Einheit
        mScale = float(config.windowWidth) / 2.0
        if xdiff != 0:
            if shift:
                config.xPosLight += xdiff / mScale
            else:
                config.xPosModel += xdiff / mScale
        if ydiff != 0:
            if shift:
                config.zPosLight += ydiff / mScale
            else:
                config.yPosModel += -ydiff / mScale
            
    config.mouseLastX = x
    config.mouseLastY = y

    glutPostRedisplay()

def menu_func(value):
    """ handle menue selection """
    print "menue entry ", value, "choosen..."
    if value == -1:
        sys.exit()
    glutPostRedisplay()


def main():
    global config, op, pc 
    if len(sys.argv) > 1:
        config.pointsfile = sys.argv[1]
    
    # Model laden
    op = ObjParser().read(config.pointsfile)
    pc = op.facecloud.normalized()

    # Hack for Mac OS X
    cwd = os.getcwd()
    glutInit(sys.argv)
    os.chdir(cwd)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutCreateWindow("OpenGL Viewer")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyPressed) 
    glutMouseFunc(mouse)
    glutMotionFunc(mouseMotion)
    
    init(config.windowWidth, config.windowHeight)

    glutMainLoop()

if __name__ == "__main__":
    main()
