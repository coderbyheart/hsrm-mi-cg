# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import Model
import Raytracing
import time
from Vec import Vec
from Quaternion import *
from Transformation import *
import InputDevice
import Picking




def drawCross():
   """ zeichnet Koordinaten-System Fadenkreuz """
   #Tacker-Code
   glPushMatrix()
   glDisable(GL_LIGHTING)
   glLineWidth(0.01)
   glBegin(GL_LINES)
   #X-Achse
   glColor(1.0, 0.0, 0.0)
   glVertex3f(-10,0,0)
   glVertex3f(10,0,0)
   #Y-Achse
   glColor(0.0, 1.0, 0.0)
   glVertex3f(0,-10,0)
   glVertex3f(0,10,0)
   #Z-Achse
   glColor(0.0, 0.0, 1.0)
   glVertex3f(0,0,-10)
   glVertex3f(0,0,10) 
   glEnd()
   glEnable(GL_LIGHTING)
   glPopMatrix()


def init(width, height):
   """ Init Startparameter, Licht"""
   global light_position0
   glClearColor(1.0, 1.0, 1.0, 0.0)         
   glMatrixMode(GL_PROJECTION)            
   glLoadIdentity()                        
   doProjectionMatrix()
   glMatrixMode(GL_MODELVIEW)               
   glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
   glEnable(GL_DEPTH_TEST)
   glEnable(GL_NORMALIZE)
   glEnable(GL_LIGHTING)
   glEnable(GL_LIGHT0)
   model.createDisplaylist()
   #Licht
   light_position0 = [5.0, 2.0, -1.0, 1.0]
   glLightfv(GL_LIGHT0, GL_POSITION, light_position0)
   glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
   glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
   glLightfv(GL_LIGHT0, GL_SPECULAR , (0.8, 0.8, 0.8, 1.0))



def drawCubeMid():
   """ BlickPunkt """
   glPushMatrix()
   glDisable(GL_LIGHTING)
   glDisable(GL_LIGHT0)
   x,y,z=worldTrans.center.v
   glTranslate(x,y,z)
   glColor(1.0, 1.0, 1.0)
   glutSolidSphere(0.02,10,10)
   glEnable(GL_LIGHTING)
   glEnable(GL_LIGHT0)
   glPopMatrix()
  
def display():
   """ Welt Zeichnen """
   #Background-Color-setzen
   rBack,gBack,bBack=inputDevice.bgColor
   glClearColor(rBack,gBack,bBack, 0.0)
   #Farb-, Tiefen- Speicher Löschen
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
   glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

   #Model Zeichnen
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()
   #LookAt
   worldTrans.openGLLookAt()
   glLightfv(GL_LIGHT0, GL_POSITION, light_position0)
   #Fadenkreuz Zeichnen
   if inputDevice.fadenkreuz:
      drawCross()
      drawCubeMid()
      

   #Model zeichnen
  
   model.draw()
   if inputDevice.shadow:
      model.shadow(light_position0)

   #Text Anzeigen
   if inputDevice.drawText:
      drawText(inputDevice.text,1,1)
   
   glutSwapBuffers()



def drawText(string, x,y):
   """ Text Zeichnen """
   #Bildschrim Seitenlaenge
   width=glutGet( GLUT_WINDOW_WIDTH)
   height=glutGet( GLUT_WINDOW_HEIGHT)
   #factor=float(max(width, height))/float(min(height, width))
   factor1=float( height)/float(width)
   factor2=float( width)/float(height)
  
   glMatrixMode(GL_PROJECTION)
   glPushMatrix()
   glLoadIdentity()
   gluOrtho2D(0,10*factor2,0,10)
   glMatrixMode(GL_MODELVIEW)
   glPushMatrix()
   glDisable(GL_LIGHTING)
   glLoadIdentity()
   glColor3f (1,0,0)
   glTranslate(0,10,0)
   glTranslate(x,-y,0)
   scale=1.0/150.0
   glScale(scale,scale,scale)
   glLineWidth(3.0)
   for i in string:
      glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(i))
   glEnable(GL_LIGHTING)
   glPopMatrix()
   glMatrixMode(GL_PROJECTION)
   glPopMatrix()
   glMatrixMode(GL_MODELVIEW)

   

   


def doProjectionMatrix(width=None, height=None):
   """ Projection / Ortho machen"""
   if width is None:
      width=glutGet( GLUT_WINDOW_WIDTH)
   if height is None:
      height=glutGet( GLUT_WINDOW_HEIGHT)

   #Ortho
   if inputDevice.ortho:
      if width <= height:
          glOrtho(-1.5, 1.5, -1.5*height/width, 1.5*height/width, -10.0, 10.0)
      else:
          glOrtho(-1.5*width/height, 1.5*width/height,  -1.5, 1.5, -10.0, 10.0)
   else:
      #Pers
      gluPerspective(60.0, 1.0*width/height, 0.1, 100.0)




def reshape(width, height):
   """ Aendert  Viewport bei aenderung der Fenstergroesse """
   glViewport(0, 0, width, height)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   doProjectionMatrix(width, height)
   glMatrixMode(GL_MODELVIEW)



def idle():
    """ Idle """

    #Model-Idle
    if model.idle:
       model.idleModel()
       glutPostRedisplay()
    #Welttransformations-Idle
    if worldTrans.idle:
       worldTrans.idleWorld()
       glutPostRedisplay()
       
   



def main():
   """ Main, Pre-Init Init"""
   global model, inputDevice, lookAt, worldTrans
   # Hack for Mac OS X
   cwd = os.getcwd()
   glutInit(sys.argv)
   os.chdir(cwd)

   #StartFenster
   glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
   glutInitWindowSize(500, 500)
   glutCreateWindow("newGoogleBody")
   
   #Model Laden
   model=Model.Model("model/squirrel/squirrel4.obj")
   #model=Model.Model("model/s2/s2.obj")
   
   #Variabeln setzen
   worldTrans=WorldTrans((1,2,3), (0,0,0), (0,1,0))
   inputDevice = InputDevice.InputDevice(model, reshape,  worldTrans, doProjectionMatrix)
   
   #Functionen registrieren
   glutDisplayFunc(display)     #register display function
   glutIdleFunc(idle)            #registrieren Idle-Funktion
   glutReshapeFunc(reshape)     #register reshape function
   glutKeyboardFunc(inputDevice.keyPressed) #register keyboard function 
   glutMouseFunc(inputDevice.mouseClick)         #register mouse function
   glutMotionFunc(inputDevice.mouseMotion)  #register motion function
   glutKeyboardUpFunc(inputDevice.keyRelease)         #register mouse function
   
   init(500,500) #initialize OpenGL state

   glutMainLoop() #start even processing



if __name__ == "__main__":
   main()
