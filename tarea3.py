from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import numpy as np

def unit(theta):
    return complex(np.cos(theta), np.sin(theta))

def complex2vect(z: complex):
    return (z.real, z.imag)

def vect2complex(v: list):
    return complex(v[0], v[1])

vertex = [unit(theta*np.pi*2/3) for theta in range(3)]
color = np.identity(3)

z0 = 2+0j
theta_fig = 0
theta_plano = 0
step_fig = 0.1
step_plano = 0.01


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-3.0, 3.0, -3.0, 3.0)
    glMatrixMode(GL_MODELVIEW)
    
def idle():
    global theta_fig
    global theta_plano
    
    theta_fig = theta_fig + step_fig
    if theta_fig > 2*np.pi:
        theta_fig = theta_fig - 2*np.pi
        
    theta_plano = theta_plano + step_plano
    if theta_plano > 2*np.pi:
        theta_plano = theta_plano - 2*np.pi
        
    glutPostRedisplay()

def escena():
    glClear(GL_COLOR_BUFFER_BIT)
    
    glBegin(GL_TRIANGLES)
    for i in range(len(vertex)):
        z = vertex[i]
        glColor3f(color[i,0], color[i,1], color[i,2])
        glVertex2fv(complex2vect(z*unit(theta_fig) + z0*unit(theta_plano)))
    glEnd()

    glutSwapBuffers()
    
glutInit(sys.argv)

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
# Atributos de la ventana
glutInitWindowPosition(200,500)
glutInitWindowSize(500,500)
glutCreateWindow("Giro")

init()

glutDisplayFunc(escena)
glutIdleFunc(idle)
glutMainLoop()