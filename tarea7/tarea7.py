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


def LoadTextures(choose):
    ### Textura
    
    if choose=="sun":
        sun_texture = Image.open("sun.jpg")
        sun_xtexture = sun_texture.size[0]
        sun_ytexture = sun_texture.size[1]

        sun_texturebyte = sun_texture.tobytes("raw", "RGBX", 0, -1)
        
        surface = glGenTextures(1)

        glTexImage2D(GL_TEXTURE_2D, 0, 3, sun_xtexture, sun_ytexture, 0, GL_RGBA, GL_UNSIGNED_BYTE, sun_texturebyte)

        # Parámetros de la textura
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        
    elif choose=="earth":
        earth_texture = Image.open("earth.jpg")
        earth_xtexture = earth_texture.size[0]
        earth_ytexture = earth_texture.size[1]

        earth_texturebyte = earth_texture.tobytes("raw", "RGBX", 0, -1)
        
        surface = glGenTextures(1)
    
        glTexImage2D(GL_TEXTURE_2D, 0, 3, earth_xtexture, earth_ytexture, 0, GL_RGBA, GL_UNSIGNED_BYTE, earth_texturebyte)

        # Parámetros de la textura
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    
    elif choose=="moon":
        moon_texture = Image.open("moon.jpg")
        moon_xtexture = moon_texture.size[0]
        moon_ytexture = moon_texture.size[1]

        moon_texturebyte = moon_texture.tobytes("raw", "RGBX", 0, -1)
    
        surface = glGenTextures(1)

        glTexImage2D(GL_TEXTURE_2D, 0, 3, moon_xtexture, moon_ytexture, 0, GL_RGBA, GL_UNSIGNED_BYTE, moon_texturebyte)

        # Parámetros de la textura
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    return surface

def sphere():
    """
    Definimos la figura esfera
    """
    global Sun, Earth, Moon
    
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
    glBindTexture(GL_TEXTURE_2D, surface)

    # Creamos una esfera
    gluSphere(esfera, 10, 100, 100)
    
    # Eliminamos la esfera una vez creada
    gluDeleteQuadric(esfera)
    glDisable(GL_TEXTURE_2D)

    glEndList()
    
    #----------------------------------------------------------------
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
    glBindTexture(GL_TEXTURE_2D, surface)

    # Creamos una esfera
    gluSphere(esfera, 10, 100, 100)
    
    # Eliminamos la esfera una vez creada
    gluDeleteQuadric(esfera)
    glDisable(GL_TEXTURE_2D)

    glEndList()
    
    #----------------------------------------------------------------
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
    glBindTexture(GL_TEXTURE_2D, surface)

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
    glRotatef(23, 0, 0, -1) ## La rotacion colocan el eje en la posición que simula la de la Tierra ??
    glRotatef(gamma, 0, 1, 0) # Rotacion de la Tierra sobre si misma
    glRotatef(-90, 1, 0, 0) # Colocamos en posición vertical la esfera
    glScalef(1/3, 1/3, 1/3)
    
    glCallList(Sun)
    glPopMatrix()
    
    # Rotacion de la Luna sobre la Tierra
    glRotatef(beta, 0, 1, 0)
    glTranslatef(10, 0, 0)
    glScalef(1/9, 1/9, 1/9)
    
    glCallLists(Earth)
    glPopMatrix()
    
    glPushMatrix()
    glRotatef(alpha, 0, 1, 0) # Rotacion del Sol sobre si mismo
    glRotatef(-90, 1, 0, 0) # Colocamos en posición vertical la esfera
    glScalef(1, 1, 1)
    
    glCallLists(Moon)
    glPopMatrix()
    
    glPopMatrix()

    glutSwapBuffers()

def idle():
    global alpha, theta, gamma, beta
    alpha = setangle(alpha + 1.46)
    theta = setangle(theta + 0.1)
    gamma = setangle(gamma + 36.5)
    beta = setangle(beta + 0.97)
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
sphere()

glutDisplayFunc(dibujo)
glutIdleFunc(idle)
glutReshapeFunc(reshape)
glutMainLoop()