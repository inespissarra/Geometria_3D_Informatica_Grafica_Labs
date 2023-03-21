from OpenGL.GL import *
from OpenGL.GLU import * 
from OpenGL.GLUT import *
import sys
import numpy as np

# Tamanho de la ventana :)
width = 700
height = 700
centro = [0, 0]
old_mouse = []
valid = 0
xmin = -float(width/2)
ymin = -float(height/2)
xmax = float(width/2)
ymax = float(height/2)
tam = 60

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(xmin, xmax, ymin, ymax)
    glMatrixMode(GL_MODELVIEW)
    
def mouse(button, state, x, y):
    global old_mouse
    global valid
    x0 = (xmax - xmin)/width * x + xmin
    y0 = (ymin - ymax)/height * y + ymax
    if state == GLUT_DOWN and \
            (centro[0] - tam/2) < x0 and x0 < (centro[0] + tam/2) and \
            (centro[1] - tam/2) < y0 and y0 < (centro[1] + tam/2):
        valid = True
        old_mouse = [x0, y0]
    else:
        valid = False
        

def mousemotion(x, y):
    global centro
    global old_mouse
    x0 = (xmax - xmin)/width * x + xmin
    y0 = (ymin - ymax)/height * y + ymax
    if valid:
        desl = [x0 - old_mouse[0], y0 - old_mouse[1]]
        centro = [centro[0] + desl[0], centro[1] + desl[1]]
        old_mouse = [x0,y0]
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
    glFlush()
        
glutInit(sys.argv)

glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
# Atributos de la ventana
glutInitWindowPosition(200,500)
glutInitWindowSize(width,height)
glutCreateWindow("Ventana")

init()

glutDisplayFunc(plano)
glutMotionFunc(mousemotion)
glutMouseFunc(mouse)
glutMainLoop()