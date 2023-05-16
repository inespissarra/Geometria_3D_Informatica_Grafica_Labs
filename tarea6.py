from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

import numpy as np

# Librería PIL
from PIL import Image

# Cargamos la imagen
image = Image.open("box.jpg")

# Guardamos las dimeniones de la imagen
ix, iy = image.size

# pasamos la imagen a bytes
textura = image.tobytes("raw", "RGBX", 0, -1)

angle, aspect = 30, 1
dnear, dfar = 0.1, 1000

# Ángulo
theta = 0.0
gamma = 0.0
beta = 0.0

# Vértices del cubo
vertexcube = [
    [0, 0, 0],
    [1, 0, 0],
    [0, 1, 0],
    [1, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [0, 1, 1],
    [1, 1, 1]
]

# índice de recorrido
indexcube = [
    0, 1, 3, 2,# z = 0
    4, 5, 7, 6,# z = 1
    0, 1, 5, 4,# y = 0
    2, 3, 7, 6,# y = 1
    1, 3, 7, 5,# x = 0
    0, 2, 6, 4 # x = 1
]



def init():
    global M, P
    glClearColor(0.0, 0.0, 0.2, 1.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    
    glEnable(GL_DEPTH_TEST)
    
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    
    glMatrixMode(GL_PROJECTION)

    gluPerspective(angle, aspect, dnear, dfar)
    
    P = np.array(glGetDouble(GL_PROJECTION_MATRIX))
    
    glMatrixMode(GL_MODELVIEW)
    
    
def figure():
    global box
    
    vertex = [
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1]
    ]*6
    
    
    glScalef(2, 2, 2)
    glTranslatef(-0.5, -0.5, -0.5)
    
    #Generamos la figura de la caja
    box = glGenLists(1)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, textura)
    
    # Comenzamos la lista llamada fig
    glNewList(box, GL_COMPILE)

    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    for i in range(len(indexcube)):
        glTexCoord2fv(vertex[i])
        glVertex3fv(vertexcube[indexcube[i]])
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    glEndList()# Fin de la lista

def dibujo():
    global theta, gamma, beta
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    
    # Ojo, en dirección negativa, que es hacia donde vemos nosotros
    glTranslatef(0, 0, -400)
    
    glPushMatrix()
    glRotatef(theta, 1, 1, 1)
    glScalef(25, 25, 25)
    glCallList(box)# Primera caja
    glPopMatrix()
    
    
    glRotatef(gamma, 0, 0, 1)
    glTranslatef(0, 75, 0)
    glRotatef(-gamma, 0, 0, 1)

    glPushMatrix()
    glScalef(15, 15, 15)
    glCallList(box)# Segunda caja
    glPopMatrix()
    
    glRotatef(beta, 0, 1, 0)
    glTranslatef(50, 0, 0)
    glRotatef(-beta, 0, 1, 0)
    glScalef(10, 10, 10)
    glCallList(box)# Tercera caja
    
    glPopMatrix()
    theta += 1
    if theta > 360:
        theta -= 360
        
    gamma += 0.83
    if gamma > 360:
        gamma -= 360
        
    beta += 0.77
    if beta > 360:
        beta -= 360
    #glFlush()
    glutSwapBuffers()


glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowPosition(0, 0)
glutInitWindowSize(1000, 1000)
glutCreateWindow(b"Cubo")

init()
figure()# Cargamos nuestra figura

glutDisplayFunc(dibujo)
glutIdleFunc(dibujo)# Con esta función, una vez que haya terminado de hacer un búfer, vuelve a ejecutar dibujo
glutMainLoop()
