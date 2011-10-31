from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys, math

def init(width, height):
	"""Initialize an OpenGL window"""
	glClearColor(0.0, 0.0, 1.0, 0.0) #blue bg
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0, 25, -17, 0, -1.0, 1.0)
	
def display():
	"""Render all objects"""
	glClear(GL_COLOR_BUFFER_BIT)
	glColor3f(.75, .75, .75) #gray color
	
	glBegin(GL_TRIANGLE_STRIP)
	glVertex(2,-8,0)
	glVertex(5,-6,0)
	glVertex(2,-11,0)
	glVertex(5,-9,0)
	glVertex(5,-6,0)
	glVertex(9,-6,0)
	glVertex(5,-9,0)
	glVertex(9,-12,0)
	glVertex(5,-12,0)
	glEnd()
	
	glBegin(GL_TRIANGLE_FAN)
	glVertex(16,-9,0)
	glVertex(14,-14,0)
	glVertex(12,-11,0)
	glVertex(16,-4,0)
	glVertex(20,-11,0)
	glVertex(18,-14,0)
	glEnd()
	
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