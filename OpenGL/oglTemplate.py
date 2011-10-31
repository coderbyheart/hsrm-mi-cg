#import oglFixme
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys, math, os

EXIT = -1
FIRST = 0

def init(width, height):
   """ Initialize an OpenGL window """
   glClearColor(0.0, 0.0, 0.0, 0.0)         #background color
   glMatrixMode(GL_PROJECTION)              #switch to projection matrix
   glLoadIdentity()                         #set to 1
   glOrtho(-1.5, 1.5, -1.5, 1.5, -1.0, 1.0) #multiply with new p-matrix
   glMatrixMode(GL_MODELVIEW)               #switch to modelview matrix


def display():
   """ Render all objects"""
   glClear(GL_COLOR_BUFFER_BIT) #clear screen
   glColor(0.0, 0.0, 1.0)       #render stuff
   glRectf(-1.0 ,-1.0 ,1.0, 1.0)
   glutSwapBuffers()            #swap buffer


def reshape(width, height):
   """ adjust projection matrix to window size"""
   glViewport(0, 0, width, height)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   if width <= height:
       glOrtho(-1.5, 1.5,
               -1.5*height/width, 1.5*height/width,
               -1.0, 1.0)
   else:
       glOrtho(-1.5*width/height, 1.5*width/height,
               -1.5, 1.5,
               -1.0, 1.0)
   glMatrixMode(GL_MODELVIEW)


def keyPressed(key, x, y):
   """ handle keypress events """
   if key == chr(27): # chr(27) = ESCAPE
       sys.exit()


def mouse(button, state, x, y):
   """ handle mouse events """
   if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
       print "left mouse button pressed at ", x, y


def mouseMotion(x,y):
   """ handle mouse motion """
   print "mouse motion at ", x, y


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

   glutDisplayFunc(display)     #register display function
   glutReshapeFunc(reshape)     #register reshape function
   glutKeyboardFunc(keyPressed) #register keyboard function 
   glutMouseFunc(mouse)         #register mouse function
   glutMotionFunc(mouseMotion)  #register motion function
   glutCreateMenu(menu_func)    #register menue function




   glutAddMenuEntry("First Entry",FIRST) #Add a menu entry
   glutAddMenuEntry("EXIT",EXIT)         #Add another menu entry
   glutAttachMenu(GLUT_RIGHT_BUTTON)     #Attach mouse button to menue

   init(500,500) #initialize OpenGL state

   glutMainLoop() #start even processing


if __name__ == "__main__":
   main()