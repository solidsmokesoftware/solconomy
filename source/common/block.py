from source.common.base import Object
from source.common.base import VisualObject


import source.client.sprites as sprites
from source.common.constants import *


class Block:
    def __init__(self, value, item):
        self.type = 'Block'
        self.value = value
        self.item = item


class LogicalBlock(Block, Object):
    def __init__(self, value, item, x, y):
        Object.__init__(self, -1, x, y)
        Block.__init__(self, value, item)


class VisualBlock(Block, VisualObject):
    def __init__(self, value, item, x, y):
        sprite = sprites.make_block(x, y, value)
        VisualObject.__init__(self, -1, x, y, sprite)
        Block.__init__(self, value, item)
 
        if item:
            self.item_sprite = sprites.make_block_item(x, y, item)
        else:
            self.item_sprite = None

    def set_pos(self, x, y):
        self.pos = x, y
        self.sprite.position = x * 31, y * 31

        if self.item_sprite:
            self.item_sprite.position = self.sprite.position

    def delete(self):
        self.sprite.delete()
        self.sprite = None
        self.image = None

        if self.item_sprite:
            self.item_sprite.delete()
            self.item_sprite = None

