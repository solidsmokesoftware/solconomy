from pyglet.gl import *


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.scale = 1

    def move(self, x, y):
        self.x = self.y + x
        self.y = self.y + y
        glTranslatef(-x, -y, 0)

    def zoom(self, z):
        self.scale += z
        glScalef(self.scale, self.scale, self.scale)

    def focus_on(self, actor):
        xo = actor.position.x - 300
        yo = actor.position.y - 300
        glTranslatef(-xo, -yo, 0)
        self.x = 0
        self.y = 0


    def place(self, x, y):
        self.x = x
        self.y = y
        glTranslatef(-x, -y, 0)
