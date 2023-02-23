from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import numpy as np

from PIL import Image
import requests
from io import BytesIO

texture = Image.open("sun_circle.jpg")
texX = texture.size[0]
texY = texture.size[1]
texturebyte = texture.tobytes("raw", "RGBX", 0, -1)
radio_im = 0.38

def init():
    glClearColor(1.0, 0.8, 0.3, 0.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-5, 5, -5, 5)

def circle(centro, radio):
    glClear(GL_COLOR_BUFFER_BIT)
    
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, texX, texY, 0, GL_RGBA, GL_UNSIGNED_BYTE, texturebyte)
    
    
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_POLYGON)
    for i in range(700):
        j = i * 0.01
        
        xcos = np.cos(j)
        ysin = np.sin(j)
        x = centro[0] + radio * xcos
        y = centro[1] + radio * ysin
        
        xi = 0.5 + radio_im * xcos
        yi = 0.5 + radio_im * ysin
        
        glTexCoord2f(xi, yi)
        glVertex2f(x, y) 
        
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
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