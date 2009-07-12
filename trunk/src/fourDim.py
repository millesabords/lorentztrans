import numpy as N
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

global c
c = 299792458

xspeed = yspeed = 0.0
xrot = yrot = 0.0

class fourDim:
    def __init__(self, v = 0.8e6):
        self.beta = float(v) / c
        self.Lfactor = 1. / N.sqrt(1 - N.power(self.beta, 2))
        self.matrix = N.zeros((4, 4))
        self.matrix[0][0] = self.Lfactor
        self.matrix[0][1] = - self.beta * self.Lfactor
        self.matrix[1][0] = self.beta * self.Lfactor
        self.matrix[1][1] = - self.Lfactor
        self.matrix[2][2] = -1.
        self.matrix[3][3] = 1.

    def addPoints(self, points):
        self.points = N.zeros((len(points), 4))
        for i in xrange(len(points)):
            for j in xrange(4):
                self.points[i][j] = points[i][j]
        print self.points

    def lorentz_X(self):
        for i in xrange(len(self.points)):
            self.points[i] = N.dot(self.matrix, self.points[i])

class display:
    def __init__(self, fourdim):
        self.fd = fourdim
        video_flags = OPENGL|DOUBLEBUF
        pygame.init()
        pygame.display.set_mode((640,480), video_flags)
        self.resize((640,480))
        self.init()

        while True:
            event = pygame.event.poll()
            if event.type == QUIT:
                break
            if event.type == KEYDOWN:
                if self.handle_keys(event.key) == 0:
                    break
            self.draw()
#            self.fd.lorentz_X()
            pygame.display.flip()

    def draw(self):
        global xrot, yrot, xspeed, yspeed, z, filter

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        glTranslatef(0.0, 0.0, -10.0)
        glRotatef(xrot, 1.0, 0.0, 0.0)
        glRotatef(yrot, 0.0, 1.0, 0.0)

        glBegin(GL_LINES)
        for i in xrange(len(self.fd.points)):
            glColor3f(1.0, 0.0, 0.0)
            glVertex3f(self.fd.points[i][0], self.fd.points[i][1], self.fd.points[i][2])
            glVertex3f(self.fd.points[i + 1][0], self.fd.points[i + 1][1], self.fd.points[i + 1][2])
            glVertex3f(self.fd.points[i + 2][0], self.fd.points[i + 2][1], self.fd.points[i + 2][2])
            if (i + 2 == len(self.fd.points) - 1):
                glVertex3f(self.fd.points[i + 1][0], self.fd.points[i + 1][1], self.fd.points[i + 1][2])
                glVertex3f(self.fd.points[0][0], self.fd.points[0][1], self.fd.points[0][2])
                break
        glEnd()

        xrot += xspeed
        yrot += yspeed

    def resize(self, (width, height)):
        if height==0:
            height=1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0*width/height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def init(self):
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    def handle_keys(self, key):
        global z, xspeed, yspeed
        
        if key == K_UP:
            xspeed -= 0.01
        elif key == K_DOWN:
            xspeed += 0.01
        elif key == K_LEFT:
            yspeed -= 0.01
        elif key == K_RIGHT:
            yspeed += 0.01
        return 1

############

fd = fourDim()
fd.addPoints([[0, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0],
              [0, 0, 1, 0], [1, 0, 1, 0], [1, 1, 1, 0], [0, 1, 1, 0]])
display(fd)
