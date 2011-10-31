from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys, math

def init(width, height):
	"""Initialize an OpenGL window"""
	glClearColor(0.0, 0.0, 1.0, 0.0) #blue bg
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(-0.5, 2.5, -1.5, 1.5, -1.0, 1.0)
	
def display():
	"""Render all objects"""
	glClear(GL_COLOR_BUFFER_BIT)
	glColor3f(.75, .75, .75) #gray color
	glBegin(GL_TRIANGLES)
	a = 0.25
	h1 = (1.0/2.0) * math.sqrt(3.0) * a
	glVertex3f(0.0, 0.0, 0.0) # 1
	glVertex3f(a/2.0, h1, 0.0) # 2
	glVertex3f(a, 0.0, 0.0) # 3
	
	glVertex3f(a/2.0, h1, 0.0) # 2
	glVertex3f(a, 0.0, 0.0) # 3
	glVertex3f(a*1.5, h1, 0.0) # 4
	
	glVertex3f(a, 0.0, 0.0) # 3
	glVertex3f(a*1.5, h1, 0.0) # 4
	glVertex3f(a*2, 0, 0.0) # 5
	
	glVertex3f(a*1.5, h1, 0.0) # 4
	glVertex3f(a*2, 0, 0.0) # 5
	glVertex3f(a*2.5, h1, 0.0) # 6
	
	glVertex3f(a*2, 0, 0.0) # 5
	glVertex3f(a*2.5, h1, 0.0) # 6
	glVertex3f(a*3, 0, 0.0) # 7
	
	glVertex3f(a*2.5, h1, 0.0) # 6
	glVertex3f(a*3, 0, 0.0) # 7
	glVertex3f(a*3.5, h1, 0.0) # 8
	
	glVertex3f(a*2.5, h1, 0.0) # 6
	glVertex3f(a*3.5, h1, 0.0) # 8
	glVertex3f(a*3, h1*2, 0.0) # 9
	
	glVertex3f(a*3.5, h1, 0.0) # 8
	glVertex3f(a*3, h1*2, 0.0) # 9
	glVertex3f(a*4, h1*2, 0.0) # 10
	
	glVertex3f(a*3.5, h1, 0.0) # 8
	glVertex3f(a*4, h1*2, 0.0) # 10
	glVertex3f(a*4.5, h1, 0.0) # 11
	
	glVertex3f(a*4, h1*2, 0.0) # 10
	glVertex3f(a*4.5, h1, 0.0) # 11
	glVertex3f(a*5, h1*2, 0.0) # 12
	
	glVertex3f(a*4.5, h1, 0.0) # 11
	glVertex3f(a*5, h1*2, 0.0) # 12
	glVertex3f(a*5.5, h1, 0.0) # 13
	
	glVertex3f(a*5, h1*2, 0.0) # 12
	glVertex3f(a*5.5, h1, 0.0) # 13
	glVertex3f(a*6, h1*2, 0.0) # 14
	
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