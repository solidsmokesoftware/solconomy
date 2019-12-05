import pyglet
import glooey

from source.common.constants import *
from source.common.collection import Collection

pyglet.resource.path = ['assets/chars', 'assets/tiles']
pyglet.resource.reindex()


class Sprite:
    def __init__(self):
        self.sprite = sprite
        self.image = sprite.image


class Visual:
    def __init__(self):
        self.sprites = Collection()

        self.window = pyglet.window.Window(WINDOW_SIZE_X, WINDOW_SIZE_Y)

        self.batch = pyglet.graphics.Batch()
        self.tile_group = pyglet.graphics.OrderedGroup(0)
        self.block_group = pyglet.graphics.OrderedGroup(1)
        self.actor_group = pyglet.graphics.OrderedGroup(2)
        self.item_group = pyglet.graphics.OrderedGroup(3)
        self.menu_group = pyglet.graphics.OrderedGroup(4)

        self.gui = glooey.Gui(self.window, batch=self.batch, group=self.menu_group)

        self.blank_image = self.pyg_image('blank.png')

        self.tile_images = []
        for i in range(TILE_COUNT):
            image = self.pyg_image(f'tile-{i}.png')
            self.tile_images.append(image)

        self.block_images = []
        for i in range(BLOCK_COUNT):
            image = self.pyg_image(f'block-{i}.png')
            self.block_images.append(image)

        for i in range(BLOCK_COUNT, BLOCK_COUNT+BLOCK_ITEM_COUNT):
            image = self.pyg_image(f'min-{i}.png')
            self.block_images.append(image)

        self.cursor_images = []
        image = self.pyg_image('red-circle.png')
        self.cursor_images.append(image)
        image = self.pyg_image('green-circle.png')
        self.cursor_images.append(image)

    def start(self):
        self.window.push_handlers(self.on_draw)

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def run(self):
        return

    def pyg_image(self, path):
        return pyglet.resource.image(path)

    def pyg_sprite(self, x, y, image, group):
        return pyglet.sprite.Sprite(image, x=x, y=y, batch=self.batch, group=group)

    def add(self, index, x, y, image, group, path=None):
        if not image:
            image = self.pyg_image(path)
        self.sprites.add(index, )
        return self.pyg_sprite(x, y, image, group)

    def tile_to_pos(self, x, y):
        x = x * 31
        y = y * 31
        return x, y

    def make_tile(self, index, x, y, image_index):
        x, y = self.tile_to_pos(x, y)
        return add(x, y, self.tile_images[image_index], self.tile_group)

    def make_block(self, index, x, y, image_index):
        x, y = self.tile_to_pos(x, y)
        return add(x, y, self.block_images[image_index], self.block_group)

    def make_block_item(self, index, x, y, image_index):
        x, y = self.tile_to_pos(x, y)
        return add(x*(TILE_SIZE-1), y*(TILE_SIZE-1), block_images[image_index], block_item_group)

    def make_actor(self, index, x, y, image):
        x, y = self.tile_to_pos(x, y)
        return add(x, y, image, actor_group)

    def make_menu(self, index, x, y, image):
        return add(x, y, image, menu_group)

    def set_pos(self, index, x, y):
        self.sprites[index].sprite.position = self.tile_to_pos(x, y)

    def hide(self, index):
        self.show_image(index, self.blank_image)

    def show(self, index):
        self.sprites[index].sprite.image = self.sprites[index].image

    def show_image(self, index, image):
        self.sprites[index].sprite.image = image

    def set_image(self, index, image):
        sprite = self.sprites[index]
        sprite.sprite.image = image
        sprite.image = image



