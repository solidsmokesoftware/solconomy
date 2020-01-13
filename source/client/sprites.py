import pyglet
from random import randint

from source.common.constants import *

class Sprite:
   def __init__(self, id, sprite, anim=None, xo=0, yo=0):
      self.id = id
      self.sprite = sprite
      self.anim = anim
      self.xo = xo
      self.yo = yo

   def move(self, x, y):
      self.sprite.position = self.sprite.position[0] + x, self.sprite.position[1] + y
      
   def place(self, x, y):
      self.sprite.position = x + self.xo, y + self.yo

   def show(self, image):
      self.sprite.image = image

   def delete(self):
      self.sprite.delete()
      self.sprite = None
      self.anim = None


pyglet.resource.path = ['assets/chars', 'assets/tiles']
pyglet.resource.reindex()

batch = pyglet.graphics.Batch()
tile_group = pyglet.graphics.OrderedGroup(0)
block_group = pyglet.graphics.OrderedGroup(1)
block_item_group = pyglet.graphics.OrderedGroup(2)
actor_group = pyglet.graphics.OrderedGroup(3)
menu_group = pyglet.graphics.OrderedGroup(4)

tile_images = []
for i in range(TILE_COUNT):
   image = pyglet.resource.image('tile-%s.png' % i)
   tile_images.append(image)

block_images = []
for i in range(BLOCK_COUNT):
   image = pyglet.resource.image('block-%s.png' % i)
   block_images.append(image)

for i in range(BLOCK_COUNT, BLOCK_COUNT+BLOCK_ITEM_COUNT):
   image = pyglet.resource.image('min-%s.png' % i)
   block_images.append(image)

blank_image = pyglet.resource.image('blank.png')
red_circle = pyglet.resource.image('red-circle.png')
green_circle = pyglet.resource.image('green-circle.png')
soul = pyglet.resource.image('soul.png')

def make_image(path):
   image = pyglet.resource.image(path)
   return image

def make_sprite(x, y, image, group):
   sprite = pyglet.sprite.Sprite(image, x=x, y=y, batch=batch, group=group)
   return Sprite(-1, sprite)

def get_sprite(x, y, image, group):
   return sprite_pool.get()

def make_tile(x, y, index):
   return make_sprite(x*(TILE_SIZE-1), y*(TILE_SIZE-1), tile_images[index], tile_group)

def make_block(x, y, index):
   return make_sprite(x*(TILE_SIZE-1), y*(TILE_SIZE-1), block_images[index], block_group)

def make_item(x, y, index):
   return make_sprite(x*(TILE_SIZE-1), y*(TILE_SIZE-1), block_images[index], block_item_group)

def make_actor(image, x, y):
   return make_sprite(x, y, image, actor_group)

def make_menu(image, x, y):
   return make_sprite(x, y, image, menu_group)

