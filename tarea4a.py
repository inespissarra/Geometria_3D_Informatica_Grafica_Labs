from OpenGL.GL import *
from OpenGL.GLU import * 
from OpenGL.GLUT import *
import sys
import numpy as np

x = 350
y = 350
width = 2*x
height = 2*y
centro = [0, 0]
raton = centro
xmin = -float(x)
ymin = -float(y)
xmax = float(x)
ymax = float(y)
tam = 40

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(xmin, xmax, ymin, ymax)
    glMatrixMode(GL_MODELVIEW)
    
    
def mousepassivemotion(x_raton, y_raton):
    global raton
    x0 = (xmax - xmin)/width * x_raton + xmin
    y0 = (ymin - ymax)/height * y_raton + ymax
    if xmin < x0 and x0 < xmax and ymin < y0 and y0 < ymax:
        raton = [x0, y0]
    
    
def idle():
    global centro
    dist = ((raton[0]-centro[0])**2 + (raton[1]-centro[1])**2)**(1/2)
    if dist!=0:
        centro[0] = centro[0] + (raton[0]-centro[0])*(0.05 + 0.001*dist)
        centro[1] = centro[1] + (raton[1]-centro[1])*(0.05 + 0.001*dist)
    glutPostRedisplay()
    
def plano():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor4f(0.0, 0.0, 1.0, 0.5)
    glBegin(GL_QUADS)
    glVertex2fv([centro[0] - tam/2, centro[1] - tam/2])
    glVertex2fv([centro[0] + tam/2, centro[1] - tam/2])
    glVertex2fv([centro[0] + tam/2, centro[1] + tam/2])
    glVertex2fv([centro[0] - tam/2, centro[1] + tam/2])
    glEnd()
    glutSwapBuffers()
        
        
glutInit(sys.argv)

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
# Atributos de la ventana
glutInitWindowPosition(200,500)
glutInitWindowSize(width,height)
glutCreateWindow("Ventana")

init()

glutDisplayFunc(plano)
glutPassiveMotionFunc(mousepassivemotion)
glutIdleFunc(idle)
glutMainLoop()