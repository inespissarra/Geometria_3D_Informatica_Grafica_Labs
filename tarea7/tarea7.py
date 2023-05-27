########## LIBRERÍAS
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

import numpy as np

from PIL import Image


xw, yw = 1000, 1000 # Tamaño de la ventana 
dnear, dfar = 1.0, 1000.0 # Posición de los planos de recorte próximo y lejano
angle = 45 # Ángulo de visión
aspect = xw/yw # Proporciones

# Ángulo de giro
alpha = 0
theta = 0
gamma = 0
beta = 0

# Tiempos de giro
n = 36.5
tiempo_sol = 1/25 * n
tiempo_tierra_sol = 1/365 * n
tiempo_tierra = 1 * n
tiempo_luna_tierra = 1/27.3 * n


def LoadTextures(image):
    ### Textura
    
    surface = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, surface)
    
    texture = Image.open(image + ".jpg")
    xtexture = texture.size[0]
    ytexture = texture.size[1]
    texturebyte = texture.tobytes("raw", "RGBX", 0, -1)

    glTexImage2D(GL_TEXTURE_2D, 0, 3, xtexture, ytexture, 0, GL_RGBA, GL_UNSIGNED_BYTE, texturebyte)
    
    # Parámetros de la textura
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    return surface

def sun():
    """
    Definimos la figura sol
    """
    global Sun
    
    # Creamos la lista Sun que va a contener a nuestra esfera
    Sun = glGenLists(1)
    
    # Creamos la cuádrica esfera, y le damos los parámetros adecuados
    esfera = gluNewQuadric()
    gluQuadricDrawStyle(esfera, GLU_FILL)
    gluQuadricNormals(esfera, GLU_SMOOTH)
    gluQuadricTexture(esfera, GL_TRUE)
    glNewList(Sun, GL_COMPILE)  
    
    # Cargamos la textura DENTRO de la lista (no fuera)
    surface = LoadTextures("sun")
    glEnable(GL_TEXTURE_2D)

    # Creamos una esfera
    gluSphere(esfera, 10, 100, 100)
    
    # Eliminamos la esfera una vez creada
    gluDeleteQuadric(esfera)
    glDisable(GL_TEXTURE_2D)

    glEndList()
    
def earth():
    """
    Definimos la figura tierra
    """
    global Earth
    
    # Creamos la lista Earth que va a contener a nuestra esfera
    Earth = glGenLists(1)
    
    # Creamos la cuádrica esfera, y le damos los parámetros adecuados
    esfera = gluNewQuadric()
    gluQuadricDrawStyle(esfera, GLU_FILL)
    gluQuadricNormals(esfera, GLU_SMOOTH)
    gluQuadricTexture(esfera, GL_TRUE)
    glNewList(Earth, GL_COMPILE)  
    
    # Cargamos la textura DENTRO de la lista (no fuera)
    surface = LoadTextures("earth")
    glEnable(GL_TEXTURE_2D)

    # Creamos una esfera
    gluSphere(esfera, 10, 100, 100)
    
    # Eliminamos la esfera una vez creada
    gluDeleteQuadric(esfera)
    glDisable(GL_TEXTURE_2D)

    glEndList()

def moon():
    """
    Definimos la figura luna
    """
    global Moon
    
    # Creamos la lista Moon que va a contener a nuestra esfera
    Moon = glGenLists(1)
    
    # Creamos la cuádrica esfera, y le damos los parámetros adecuados
    esfera = gluNewQuadric()
    gluQuadricDrawStyle(esfera, GLU_FILL)
    gluQuadricNormals(esfera, GLU_SMOOTH)
    gluQuadricTexture(esfera, GL_TRUE)
    glNewList(Moon, GL_COMPILE)
    
    # Cargamos la textura DENTRO de la lista (no fuera)
    surface = LoadTextures("moon")
    glEnable(GL_TEXTURE_2D)

    # Creamos una esfera
    gluSphere(esfera, 10, 100, 100)
    
    # Eliminamos la esfera una vez creada
    gluDeleteQuadric(esfera)
    glDisable(GL_TEXTURE_2D)

    glEndList()
    
    
def init():
    # Color blanco de fondo
    glClearColor(0.0, 0.0, 0.0, 0.0)
    
    # Activamos el test de profundidad
    glClearDepth(1.0)  # Habilitamos el borrado del buffer de profundidad
    glDepthFunc(GL_LESS) # Indicamos el tipo de test de profundidad que queremos que realice
    glEnable(GL_DEPTH_TEST)

    # Corrección de perspectiva
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST); 
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(angle, aspect, dnear, dfar)
    
def dibujo():
    global psi, phi
    global alpha, theta, gamma, beta # sol-sol, terra-sol, tierra-tierra, luna-tierra
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    
    # Ojo, en dirección negativa, que es hacia donde vemos nosotros
    glTranslatef(0,0,-100)
    
    glPushMatrix()
    # rotacion de la tierra alrededor del sol
    glRotatef(theta, 0, 1, 0)
    glTranslatef(35,0,0) # distancia de la tierra al sol
    glRotatef(-theta, 0, 1, 0) # vertical no cambia con el movimiento de traslación a lo largo de su órbita
    
    glPushMatrix()
    glRotatef(23, 0, 0, -1) ## La rotacion colocan el eje en la posición que simula la de la Tierra
    glRotatef(gamma, 0, 1, 0) # Rotacion de la Tierra sobre si misma
    glRotatef(-90, 1, 0, 0) # Colocamos en posición vertical la esfera
    glScalef(1/3, 1/3, 1/3)
    
    glCallList(Earth)
    glPopMatrix()
    
    # Rotacion de la Luna sobre la Tierra
    glRotatef(beta, 0, 1, 0)
    glTranslatef(10, 0, 0)
    glScalef(1/9, 1/9, 1/9)
    
    glCallLists(Moon)
    glPopMatrix()
    
    glPushMatrix()
    glRotatef(alpha, 0, 1, 0) # Rotacion del Sol sobre si mismo
    glRotatef(-90, 1, 0, 0) # Colocamos en posición vertical la esfera
    glScalef(1, 1, 1)
    
    glCallLists(Sun)
    glPopMatrix()
    
    glPopMatrix()

    glutSwapBuffers()

def idle():
    global alpha, theta, gamma, beta
    global n, tiempo_sol, tiempo_tierra_sol, tiempo_tierra, tiempo_luna
    alpha = setangle(alpha + tiempo_sol)
    theta = setangle(theta + tiempo_tierra_sol)
    gamma = setangle(gamma + tiempo_tierra)
    beta = setangle(beta + tiempo_luna_tierra)
    glutPostRedisplay()
    
def setangle(alpha):
    if alpha >=360:
        return(alpha - 360)
    if alpha < 0:
        return (alpha + 360)
    return(alpha)
        
def reshape(newwidth, newheight):
    if newheight == 0:
        newheight = 1
    
    glViewport(0, 0, newwidth, newheight)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()# Reseteamos la matriz de proyección 
    gluPerspective(angle, newwidth/newheight, dnear, dfar)
    glMatrixMode(GL_MODELVIEW)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowPosition(0, 0)
glutInitWindowSize(xw, yw)
glutCreateWindow("Sistema Solar: Tierra, Luna y Sol")

init()
sun()
earth()
moon()

glutDisplayFunc(dibujo)
glutIdleFunc(idle)
glutReshapeFunc(reshape)
glutMainLoop()