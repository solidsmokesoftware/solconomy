from pyglet.gl import *


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.scale = 1
        self.move = (0, 0)

    def scroll(self, x, y):
        self.x = self.y + x
        self.y = self.y + y
        glTranslatef(-x, -y, 0)

    def zoom(self, z):
        self.scale += z
        glScalef(self.scale, self.scale, self.scale)

    def focus_on(self, x, y):
        x -= 600
        y -= 350
        self.scroll(x, y)

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        glTranslatef(-x, -y, 0)