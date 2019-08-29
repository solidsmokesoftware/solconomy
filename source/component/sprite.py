

class Sprite:
    def __init__(self, sprite):
        self.sprite = sprite
        self.image = sprite.image

    def show(self):
        self.sprite.image = self.image

    def show_image(self, image):
        self.sprite.image = image

    def set_image(self, image):
        self.sprite.image = image
        self.image = image

    def set_pos(self, x, y):
        self.sprite.position = x, y

        