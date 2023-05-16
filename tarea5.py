from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np

def glTranslatef(a,b,c):
    translate_matrix = np.array([[1, 0, 0, 0],[0,1,0,0],[0,0,1,0],[a,b,c,1]])
    glMultMatrixf(translate_matrix)
    
def glScalef(a,b,c):
    scale_matrix = np.array([[a,0,0,0],[0,b,0,0],[0,0,c,0],[0,0,0,1]])
    glMultMatrixf(scale_matrix)
    
def gluLookAt(x0, y0, z0, xref, yref, zref, Vx, Vy, Vz):
    P0 = [x0,y0,z0]
    Pref = [xref, yref, zref]
    V = [Vx, Vy, Vz]
    
    n = [Pref[i] - P0[i] for i in range(3)]
    n = [n[i]/np.sqrt(sum([n[j]**2 for j in range(3)])) for i in range(3)]
    u = np.cross(V, n)
    u = [u[i]/np.sqrt(sum([u[j]**2 for j in range(3)])) for i in range(3)]
    v = np.cross(n, u)
    
    lookAt_matrix = np.array([[u[0], v[0], -n[0], 0], 
                              [u[1], v[1], -n[1], 0], 
                              [u[2], v[2], -n[2], 0],
                              [-np.dot(u, P0), -np.dot(v, P0), -np.dot(n, P0), 1]])
    
    glMultMatrixf(lookAt_matrix)