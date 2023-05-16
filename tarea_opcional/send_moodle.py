########## LIBRERÍAS
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

import numpy as np
import math

from PIL import Image

# Posición de la cámara
x0, y0, z0 = 0, 0, -50
xref, yref, zref = 0, 0, 0
Vx, Vy, Vz = 0, 1, 0

# Tamaño de la ventana 
xw, yw = 1000, 1000

# Posición de los planos de recorte próximo y lejano
dnear, dfar = 1.0, 1000.0

# Ángulo de visión
angle = 45

# Proporciones
aspect = xw/yw

# Ángulo de giro
theta = 0

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


# Centramos los puntos del cubo
scale = 8
center = -0.5
vertexcube = [scale*(np.array(v) + np.array([center]*3)) for v in vertexcube]


# Son seis caras, y cada cara se corresponde con x = 0, x = 1, y = 0, y = 1, etc.
# Cuidado con el orden en el que se realizan los cuadrados
indexcube = [0, 1, 3, 2,# z = 0
             4, 5, 7, 6,# z = 1
             0, 1, 5, 4,# y = 0
             2, 3, 7, 6,# y = 1
             1, 3, 7, 5,# x = 0
             0, 2, 6, 4 # x = 1
            ]

# Array para la textura
squareTex = [
    [0,0],
    [1,0],
    [1,1],
    [0,1]
]*6


import math

class Cuaternion:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __str__(self):
        return f"{self.a} + {self.b}i + {self.c}j + {self.d}k"

    def __add__(self, other):
        return Cuaternion(self.a + other.a, self.b + other.b, self.c + other.c, self.d + other.d)

    def __sub__(self, other):
        return Cuaternion(self.a - other.a, self.b - other.b, self.c - other.c, self.d - other.d)

    def __mul__(self, other):
        real = self.a * other.a - self.b * other.b - self.c * other.c - self.d * other.d
        imag1 = self.a * other.b + self.b * other.a + self.c * other.d - self.d * other.c
        imag2 = self.a * other.c - self.b * other.d + self.c * other.a + self.d * other.b
        imag3 = self.a * other.d + self.b * other.c - self.c * other.b + self.d * other.a
        return Cuaternion(real, imag1, imag2, imag3)

    def norma(self):
        return math.sqrt(self.a**2 + self.b**2 + self.c**2 + self.d**2)

    def conjugado(self):
        return Cuaternion(self.a, -self.b, -self.c, -self.d)

    def exponencial(self):
        norm = self.norma()
        exp_real = math.exp(self.a) * math.cos(norm)
        exp_imag = (math.exp(self.a) / norm) * (self.b * math.sin(norm) +
                                                self.c * math.sin(norm) +
                                                self.d * math.sin(norm))
        return Cuaternion(exp_real, exp_imag, exp_imag, exp_imag)

    def logaritmo(self):
        norm = self.norma()
        log_real = math.log(norm)
        log_imag = (math.acos(self.a / norm) / norm) * (self.b * math.sin(norm) +
                                                       self.c * math.sin(norm) +
                                                       self.d * math.sin(norm))
        return Cuaternion(log_real, log_imag, log_imag, log_imag)

    def potencia(self, exponente):
        log = self.logaritmo()
        log_mul_exp = Cuaternion(log.a * exponente, log.b * exponente,
                                 log.c * exponente, log.d * exponente)
        return log_mul_exp.exponencial()
    
    def bcd(self):
        return [self.b, self.c, self.d]
    

def rotationCuarternion(angle, x, y, z):
    # Convertir el ángulo a radianes
    angle_rad = math.radians(angle)

    # Calcular el seno y coseno del ángulo medio
    angle_half = angle_rad / 2
    cos_half = math.cos(angle_half)
    sin_half = math.sin(angle_half)
    

    # Normalizar el vector de rotación
    length = math.sqrt(x * x + y * y + z * z)
    if length != 0:
        x /= length
        y /= length
        z /= length

    # Calcular los componentes del cuaternión de rotación
    a = cos_half
    b = x * sin_half
    c = y * sin_half
    d = z * sin_half

    # Crear el cuaternión de rotación
    return Cuaternion(a, b, c, d)


def LoadTextures():
    ### Textura

    texture = Image.open("box.jpg")
    xtexture = texture.size[0]
    ytexture = texture.size[1]

    texturebyte = texture.tobytes("raw", "RGBX", 0, -1)
    
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)

    glTexImage2D(GL_TEXTURE_2D, 0, 3, xtexture, ytexture, 0, GL_RGBA, GL_UNSIGNED_BYTE, texturebyte)
    
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    
def init():
    # LoadTextures()
    # glEnable(GL_TEXTURE_2D)
    
    # Color blanco de fondo
    glClearColor(0.0, 0.0, 0.0, 0.0)
    
    # Activamos el test de profundidad
    glClearDepth(1.0)  # Habilitamos el borrado del buffer de profundidad
    glDepthFunc(GL_LESS) # Indicamos el tipo de test de profundidad que queremos que realice
    glEnable(GL_DEPTH_TEST)

    # Esto está desactivado por defecto, pero insistimos
    glDisable(GL_CULL_FACE)
    
    # Corrección de perspectiva
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST); 
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(angle, aspect, dnear, dfar)
    
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(x0, y0, z0, xref, yref, zref, Vx, Vy, Vz)# Posición de la cámara
    
def dibujo():
    global theta
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
 
    q = rotationCuarternion(theta, 2, 3, 0)

    q_conjugado = q.conjugado()
    
    glEnable(GL_TEXTURE_2D)
    LoadTextures()
    glBegin(GL_QUADS)
    for k in range(len(indexcube)):
        glTexCoord2fv(squareTex[k])
        w = Cuaternion(0, *vertexcube[indexcube[k]])
        w_rotado = q * w * q_conjugado
        glVertex3fv(w_rotado.bcd())

    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    theta += 0.5
    if theta >= 360:
        theta -= 360

    glutSwapBuffers()

def reshape(newwidth, newheight):
    if newheight == 0:
        newheight = 1
    
    glViewport(0, 0, newwidth, newheight)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()# Reseteamos la matriz de proyección 
    gluPerspective(angle, newwidth/newheight, dnear, dfar)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(x0, y0, z0, xref, yref, zref, Vx, Vy, Vz)# Posición de la cámara

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowPosition(0, 0)
glutInitWindowSize(xw, yw)
glutCreateWindow("Perspectiva de un cubo")

init()

glutDisplayFunc(dibujo)
glutIdleFunc(dibujo)
glutReshapeFunc(reshape)
glutMainLoop()