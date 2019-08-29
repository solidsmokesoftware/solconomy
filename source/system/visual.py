import pyglet
import glooey

from source.system.system import Process

from source.component.sprite import Sprite

from source.common.constants import *

pyglet.resource.path = ['assets/chars', 'assets/tiles']
pyglet.resource.reindex()


class Visual(Process):
    def __init__(self, system):
        Process.__init__(self, system)

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
        self.window.push_handlers(self.run)

    def run(self):
        self.window.clear()
        self.batch.draw()

    def set_pos(self, index, x, y):
        self.sprites[index].set_pos(x, y)

    def hide(self, index):
        self.sprites[index].show_image(self.blank_image)

    def show(self, index):
        self.sprites[index].sprite.image = self.sprites[index].image

    def show_image(self, index, image):
        self.sprites[index].sprite.image = image

    def set_image(self, index, image):
        sprite = self.sprites[index]
        sprite.sprite.image = image
        sprite.image = image

    def pyg_image(self, path):
        return pyglet.resource.image(path)

    def pyg_sprite(self, x, y, image, group):
        return pyglet.sprite.Sprite(image, x=x, y=y, batch=self.batch, group=group)

    def make_sprite(self, index, path, group):
        pos = self.system.spatial.get(index)
        image = self.pyg_image(path)
        sprite = self.pyg_sprite(pos.x, pos.y, image, group)
        return Sprite(sprite)

    def add_actor(self, index, path):
        sprite = self.make_sprite(index, path, self.actor_group)
        self.add(index, sprite)

    def add_tile(self, index, value):
        pos = self.system.spatial.get(index)
        x, y = self.tile_to_pos(pos.x, pos.y)
        image = self.tile_images[value]
        sprite = self.pyg_sprite(x, y, image, self.tile_group)
        sprite = Sprite(sprite)
        self.add(index, sprite)

    def add_block(self, index, value):
        pos = self.system.spatial.get(index)
        x, y = self.tile_to_pos(pos.x, pos.y)
        image = self.block_images[value]
        sprite = self.pyg_sprite(x, y, image, self.block_group)
        sprite = Sprite(sprite)
        self.add(index, sprite)

    def add_item(self, index, value):
        pos = self.system.spatial.get(index)
        x, y = self.tile_to_pos(pos.x, pos.y)
        image = self.block_images[value]
        sprite = self.pyg_sprite(x, y, image, self.block_group)
        sprite = Sprite(sprite)
        self.add(index, sprite)

    def add_menu(self, index, path):
        sprite = self.make_sprite(index, path, self.menu_group)
        self.add(index, sprite)


    def tile_to_pos(self, x, y):
        x = x * 31
        y = y * 31
        return x, y
