from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-5, 5, -5, 5)

def circle(centro, radio):
    glClear(GL_COLOR_BUFFER_BIT)
    
    glBegin(GL_POLYGON)
    for i in range(700):
        # j es el ángulo en radianes. 
        # Va de 0 a 7 en pasos de 0.01 (2 * pi < 7, asi se completa el circulo). 
        # Tenemos 700 puntos.
        j = i * 0.01
        # Elige el color
        glColor3f(1.0 - j, 0.4, j)
        # coordenadas de sus "vértices":
        x = centro[0] + radio * math.cos(j)
        y = centro[1] + radio * math.sin(j)
        glVertex2f(x, y) 
    glEnd()
    
def dibujo():
    circle([1, 1], 2)
    glFlush()
    
glutInit(sys.argv)

glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowPosition(200, 500)
glutInitWindowSize(500, 500)
glutCreateWindow("Circle")

init()
    
glutDisplayFunc(dibujo)
glutMainLoop()