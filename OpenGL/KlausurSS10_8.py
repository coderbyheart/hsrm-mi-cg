from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys, math

def init(width, height):
	"""Initialize an OpenGL window"""
	pass
	
def display():
	"""Render all objects"""
	glClearColor(1.0, 1.0, 1.0, 0.0)
	glClear(GL_COLOR_BUFFER_BIT)
	glColor3f(0, 0, 0)
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(-2, 2, -2, 2, -3.0, 3.0)
	gluLookAt(1,1,1, 0,0,0, 1,0,0)
	
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glutWireCube(1)
	glTranslate(0.5,0.5,0.5)
	
	glFlush() #force GL execution
	
def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(500, 500)
	glutCreateWindow("Einfaches OpenGL Programm")
	glutDisplayFunc(display) #register displayf.
	init(500,500) #initialize OpenGL state
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
	glutMainLoop() #start even processing

if __name__ == "__main__":
	main()