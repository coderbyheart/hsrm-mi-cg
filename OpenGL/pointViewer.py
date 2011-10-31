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
from itertools import cycle
import sys
import math
import os
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

showModelCross = True

colors = [
          (0.0, 0.0, 0.0, 0.0), # schwarz
          (1.0, 1.0, 1.0, 0.0), # weiß
          (1.0, 0.0, 0.0, 0.0), # rot
          (0.0, 1.0, 0.0, 0.0), # grün
          (0.0, 0.0, 1.0, 0.0), # blau
          (1.0, 1.0, 0.0, 0.0), # gelb
          ]
mcolor = colors[3]
bgcolor = colors[1]
colorCycle = cycle(colors)

pointsfile = sys.argv[1] if len(sys.argv) > 1 else 'data/elephant.obj'

# Dateien einlesen, Untertsützt werden RAW- und OBJ-Dateien
showTriangles = False
if pointsfile[-3:] == "raw":
    pc = PointCloud().readRaw(pointsfile).normalized()
else:
    op = ObjParser().read(pointsfile)
    pc = op.facecloud.normalized()
    yPosModel = pc.getYSize()/2.0
    showTriangles = True

# Art der Projektion
ortho = False

# OpenGL-Render-Modus
renderModes = [GL_FILL, GL_LINE, GL_POINT]
renderModesCycle = cycle(renderModes)
currentRenderMode = renderModesCycle.next()

# Beleuchtung
lighting = True
xPosLight = 0.01
yPosLight = 10.0
zPosLight = 0.01

# Shading-Mode
shadingModes = [GL_SMOOTH, GL_FLAT]
shadingModesCycle = cycle(shadingModes)

# Wireframe
wireframe = False

# Display-Liste
modelList = None

def init(width, height):
    """ Initialize an OpenGL window """
    global modelList
    
    glPolygonMode(GL_FRONT_AND_BACK, currentRenderMode)
    glShadeModel(shadingModesCycle.next())
    
    modelList = glGenLists(1)
    glNewList(modelList, GL_COMPILE)
    renderModel()
    glEndList()

def display():
    """ Render all objects"""
      
    glClearColor(*bgcolor)            #background color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #clear screen
    
    glPushMatrix()
    glLoadIdentity()
    gluLookAt(0 + xPosCamera,0 + yPosCamera,3 + zPosCamera, 0,0,zPosCamera, 0,1,0)

    if lighting:
        drawShadow()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glLightfv(GL_LIGHT0, GL_POSITION, [xPosLight, yPosLight, zPosLight, 1.0])
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    else: # not lighting
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)

    drawModel()
    
    glPopMatrix()
    
    glutSwapBuffers()

def drawShadow():
        global xPosLight, yPosLight, zPosLight
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        # ++++++ SCHATTEN
        glPushMatrix()
        #glLoadIdentity()
        glRotatef(xAngle, 1, 0, 0)
        glRotatef(yAngle, 0, 1, 0)
        glRotatef(zAngle, 0, 0, 1)
        glTranslate(xPosLight, yPosLight, zPosLight)
        if yPosLight == 0.0:
            yPosLight = 0.1
        p = [1.0, 0, 0, 0, 0, 1.0, 0, -1.0/yPosLight, 0, 0, 1.0, 0, 0, 0, 0, 0]
        glMultMatrixf(p)
        glTranslate(-xPosLight, -yPosLight, -zPosLight)
        glTranslatef(xPosModel, 0, zPosModel) # Mit Model verschieben
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glColor3f(0.15, 0.15, 0.15)
        glCallList(modelList)
        glPopMatrix()

def drawModel():
    # +++++++++ MODEL
    glPushMatrix()

    # Drehung
    glRotatef(xAngle, 1, 0, 0)
    glRotatef(yAngle, 0, 1, 0)
    glRotatef(zAngle, 0, 0, 1)

    # Zeichne Achsen
    if showModelCross:
        glBegin(GL_LINES)
        glColor(0.5, 0.25, 0.25)
        glVertex3f(-10,0,0)
        glVertex3f(10,0,0)
        glColor(0.25, 0.5, 0.25)
        glVertex3f(0,-10,0)
        glVertex3f(0,10,0)
        glColor(0.25, 0.25, 0.5)
        glVertex3f(0,0,-10)
        glVertex3f(0,0,10)
        glEnd()

    # Position
    glTranslatef(xPosModel, yPosModel, zPosModel)
    
    glColor(mcolor[0], mcolor[1], mcolor[2])
    glCallList(modelList)

    # FIXME: OpenGL-Funktionen dazu verwenden
    if wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glScale(1.001, 1.001, 1.001)
        glColor(0, 0, 0)
        glCallList(modelList)
        glPolygonMode(GL_FRONT_AND_BACK, currentRenderMode)
    
    glPopMatrix()

def renderModel():
    if showTriangles:
        glBegin(GL_TRIANGLES)
        for face in pc.faces:
            for index, pointIndex in enumerate(face.points):
                point = pc[pointIndex]
                if face.normals != None:
                    normal = op.facecloud.normals[face.normals[index]]
                    glNormal3f(normal.x, normal.y, normal.z)
                glVertex3f(point.x, point.y, point.z)
        glEnd()
    else:
        glBegin(GL_POINTS)
        for point in pc:
             glVertex3f(point.x, point.y, point.z)
        glEnd()

def reshape(width, height):
    """ adjust projection matrix to window size"""
    global windowWidth, windowHeight
    windowWidth = width
    windowHeight = height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if ortho:
        glViewport(0, 0, width, height)
        of = 1.5 + zPosCamera
        if width <= height:
             glOrtho(-of, of,
                    -of*height/width, of*height/width,
                    -4.0, 4.0)
        else:
            # Relativ zu gluLookat
             glOrtho(-of*width/height, of*width/height,
                     -of, of,
                     -4.0, 4.0)
    else:
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
    
    if key == 'p':
          ortho = not ortho
          glutReshapeWindow(windowWidth, windowHeight)
          
    if key == 'm':
        global showModelCross
        showModelCross = not showModelCross

    if key == 'l':
        global lighting
        lighting = not lighting

    if key == 'w':
        global wireframe
        wireframe = not wireframe

    if key == 'r':
        global currentRenderMode
        currentRenderMode = renderModesCycle.next()
        glPolygonMode(GL_FRONT_AND_BACK, currentRenderMode)

    if key == 's':
        glShadeModel(shadingModesCycle.next())
    
    global mcolor, bgcolor
    if key == 'b':
        nextcolor = colorCycle.next()
        while nextcolor == mcolor:
            nextcolor = colorCycle.next()
        bgcolor = nextcolor
    if key == 'c':
        nextcolor = colorCycle.next()
        while nextcolor == bgcolor:
            nextcolor = colorCycle.next()
        mcolor = nextcolor
    
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
            
    if middleMousePressed:
        # Zoom, eine Bildschirmhöhe ist Entfernung um 10 Einheiten
        global zPosCamera
        zScale = float(windowHeight) / 10.0
        if ydiff != 0:
            zPosCamera += ydiff / zScale
            glutReshapeWindow(windowWidth, windowHeight)
            
    if rightMousePressed:
        # Verschieben, eine Bildschirmbreite ist Entfernung um 1 Einheit
        mScale = float(windowWidth) / 2.0
        global xPosModel, yPosModel
        global xPosLight, zPosLight
        shift = glutGetModifiers() & GLUT_ACTIVE_SHIFT
        if xdiff != 0:
            if shift:
                xPosLight += xdiff / mScale
            else:
                xPosModel += xdiff / mScale
        if ydiff != 0:
            if shift:
                zPosLight += ydiff / mScale
            else:
                yPosModel += -ydiff / mScale
            
    mouseLastX = x
    mouseLastY = y

    glutPostRedisplay()

def menu_func(value):
    """ handle menue selection """
    print "menue entry ", value, "choosen..."
    if value == EXIT:
         sys.exit()
    glutPostRedisplay()


def main():
    # Hack for Mac OS X
    cwd = os.getcwd()
    glutInit(sys.argv)
    os.chdir(cwd)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutCreateWindow("simple openGL/GLUT template")

    glutDisplayFunc(display)      #register display function
    glutReshapeFunc(reshape)      #register reshape function
    glutKeyboardFunc(keyPressed) #register keyboard function 
    glutMouseFunc(mouse)            #register mouse function
    glutMotionFunc(mouseMotion)  #register motion function
    
    # glutCreateMenu(menu_func)     #register menue function
    # glutAddMenuEntry("First Entry",FIRST) #Add a menu entry
    # glutAddMenuEntry("EXIT",EXIT)            #Add another menu entry
    # glutAttachMenu(GLUT_RIGHT_BUTTON)      #Attach mouse button to menue

    init(windowWidth, windowHeight) #initialize OpenGL state

    glutMainLoop() #start even processing


if __name__ == "__main__":
    main()
