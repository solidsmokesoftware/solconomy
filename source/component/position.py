

class Position:
    def __init__(self, x, y, world=0, level=0):
        self.x = x
        self.y = y
        self.world = world
        self.level = level
        self.pos = x, y

    def move(self, x, y):
        self.x += x
        self.y += y
        self.pos = self.x, self.y

    def set(self, x, y):
        self.x = x
        self.y = y
        self.pos = x, y