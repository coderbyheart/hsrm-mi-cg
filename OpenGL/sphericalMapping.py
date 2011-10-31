#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""

Tastaturkommandos:

    Escape: 
        Viewer beenden
    x,X,y,Y,z,Z: 
        Modell um die jeweilige Achse drehen
    p:
        Wechseln zwischen orthogonaler und perspektivischer Projektion
    c:
        Wechseln der Modelfarbe
    b:
        Wechseln der Hintergrundfarbe
    m:
        Modell-Koordinatensystem ein- bzw. ausblenden
    r:
        Rendermode-Wechseln GL_POINT, GL_LINE, GL_FILL
    l:
        Beleuchtung ein- bzw. ausschalten
    s:
        Shading-Mode wechseln
    w:
        Wireframe des Models anzeigen

Mauskommandos:

    Linke Maustause + ziehen:
        Modell um die X- und Y-Achse drehen
        
    Mittlere Maustause + Hoch bzw. Runter ziehen:
        Kamera zum Modell hin, bzw. vom Modell weg bewegen
        
    Rechte Maustaste + ziehen:
        X- und Y-Position des Modells verändern

    Shift + Rechte Maustaste + ziehen:
        X- und Z-Position des Lichts verändern

"""

from Geometry.PointCloud import PointCloud
from ObjParser import ObjParser
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
from itertools import cycle
import math
import os
import sys
if os.uname()[4] == "i686":
    import psyco
    psyco.full()


EXIT = -1
FIRST = 0

# Drehwinkel Modell
xAngle = 15.0
yAngle = -30.0
zAngle = 0.0

# Position Modell
xPosModel = 0.0
yPosModel = 0.0
zPosModel = 0.0

# Position Kamera
xPosCamera = 0.0
yPosCamera = 0.0
zPosCamera = 0.0

windowWidth = 500
windowHeight = 500

mousePressed = False
leftMousePressed = False
middleMousePressed = False
rightMousePressed = False

# Beleuchtung
xPosLight = 0.01
yPosLight = 10.0
zPosLight = 0.01

# Display-Liste
modelList = None

texture = None

def init(width, height):
    """ Initialize an OpenGL window """
    global modelList, yPosModel, texture
    
    glEnable(GL_DEPTH_TEST)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [xPosLight, yPosLight, zPosLight, 1.0])
    
    
    # Model einlesen
    pointsfile = sys.argv[1] if len(sys.argv) > 1 else 'data/elephant.obj'
    
    op = ObjParser().read(pointsfile)
    pc = op.facecloud.normalized()
    yPosModel = pc.getYSize()/2.0
    
    modelList = glGenLists(1)
    
    glNewList(modelList, GL_COMPILE)
    glBegin(GL_TRIANGLES)
    for face in pc.faces:
        for index, pointIndex in enumerate(face.points):
            point = pc[pointIndex]
            if face.normals != None:
                normal = op.facecloud.normals[face.normals[index]]
                glNormal3f(normal.x, normal.y, normal.z)
            glVertex3f(point.x, point.y, point.z)
    glEnd()
    glEndList()
    
    # Textur einlesen
    image = Image.open("data/texture-distorted.jpg")
    twidth, theight = image.size
    image = image.tostring("raw","RGBX",0,-1)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, twidth, theight, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    
def display():
    """ Render all objects"""
      
    glClearColor(0.0, 0.0, 0.0, 0.0)            #background color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #clear screen
    
    glPushMatrix()
    glLoadIdentity()
    gluLookAt(0 + xPosCamera,0 + yPosCamera,3 + zPosCamera, 0,0,zPosCamera, 0,1,0)
   
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glEnable(GL_TEXTURE_GEN_T)   
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_R)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    drawModel()
    
    glPopMatrix()
    
    glutSwapBuffers()

def drawModel():
    # +++++++++ MODEL
    glPushMatrix()

    # Drehung
    glRotatef(xAngle, 1, 0, 0)
    glRotatef(yAngle, 0, 1, 0)
    glRotatef(zAngle, 0, 0, 1)

    glTranslatef(xPosModel, yPosModel, zPosModel)
    
    #glutSolidTeapot(0.75)
    glCallList(modelList)

    glPopMatrix()

def reshape(width, height):
    """ adjust projection matrix to window size"""
    global windowWidth, windowHeight
    windowWidth = width
    windowHeight = height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # todo viewport groß
    if width <= height:
        glViewport(0, (height - width) / 2, width, width)
        gluPerspective(60.0, 1, 0.1, 100.0)
    else:
        # Relativ zu gluLookat
        glViewport((width - height) / 2, 0, height, height)
        gluPerspective(60.0, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def keyPressed(key, x, y):
    """ handle keypress events """
    global xAngle, yAngle, zAngle, ortho
    if key == 'x':
        # Rotiere um X-Achse, im Uhrzeigersinn
        xAngle += 1
    if key == 'X':
        # Rotiere um X-Achse, gegen den Uhrzeigersinn
        xAngle -= 1
    if key == 'y':
        # Rotiere um Y-Achse, im Uhrzeigersinn
        yAngle += 1
    if key == 'Y':
        # Rotiere um Y-Achse, gegen den Uhrzeigersinn
        yAngle -= 1
    if key == 'z':
        # Rotiere um Z-Achse, im Uhrzeigersinn
        zAngle += 1
    if key == 'Z':
        # Rotiere um Z-Achse, gegen den Uhrzeigersinn
        zAngle -= 1
    if key == chr(27): # chr(27) = ESCAPE
         sys.exit()
    
    glutPostRedisplay()

mouseLastX = None
mouseLastY = None

def mouse(button, state, x, y):
    """ handle mouse events """
    global mouseLastX, mouseLastY, mousePressed, middleMousePressed, leftMousePressed, rightMousePressed
    mouseLastX, mouseLastY = None, None
    
    if state == GLUT_UP:
        mousePressed = False
        leftMousePressed = False
        middleMousePressed = False
        rightMousePressed = False
        return
    
    mousePressed = True
    
    if button == GLUT_LEFT_BUTTON:
        leftMousePressed = True
    if button == GLUT_MIDDLE_BUTTON:
        middleMousePressed = True
    if button == GLUT_RIGHT_BUTTON:
        rightMousePressed = True

def mouseMotion(x,y):
    """ handle mouse motion """
    global mouseLastX, mouseLastY
    xdiff = 0
    ydiff = 0
    if mouseLastX != None:
        xdiff = x - mouseLastX
    if mouseLastY != None:
        ydiff = y - mouseLastY
    
    if leftMousePressed:
        global xAngle, yAngle
        if xdiff != 0:
            yAngle += xdiff
        if ydiff != 0:
            xAngle += ydiff
            
    mouseLastX = x
    mouseLastY = y

    glutPostRedisplay()

def main():
    # Hack for Mac OS X
    cwd = os.getcwd()
    glutInit(sys.argv)
    os.chdir(cwd)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutCreateWindow("Spherical Mapping Viewer")

    glutDisplayFunc(display)      #register display function
    glutReshapeFunc(reshape)      #register reshape function
    glutKeyboardFunc(keyPressed) #register keyboard function 
    glutMouseFunc(mouse)            #register mouse function
    glutMotionFunc(mouseMotion)  #register motion function
    
    init(windowWidth, windowHeight) #initialize OpenGL state

    glutMainLoop() #start even processing

if __name__ == "__main__":
    main()
