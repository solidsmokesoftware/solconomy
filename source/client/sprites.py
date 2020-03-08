import pyglet
from random import randint

from pecrs.index import Index
from source.common.constants import *


#A wrapper over pyglet's sprite
class Sprite:
   def __init__(self, id, sprite, xo=0, yo=0):
      self.id = id
      self.sprite = sprite
      self.anim = None
      self.anims = {}
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
      self.anims = None


class Animation:
   def __init__(self, images, rate=1, start=0, repeat=False, long=False):
      self.images = images
      self.rate = rate / len(images) #Rate is overall time for a full animation loop
      self.start = start
      self.repeat = repeat
      self.long = long #Long playing animation, keep in the animation list even when over and not repeating

      self.index = 0
      self.time = 0
      self.max = len(images)


index = Index()
list = {}
animations = []

pyglet.resource.path = ['assets/chars', 'assets/tiles', 'assets/chars/eye']
pyglet.resource.reindex()

batch = pyglet.graphics.Batch()
tile_group = pyglet.graphics.OrderedGroup(0)
block_group = pyglet.graphics.OrderedGroup(1)
block_item_group = pyglet.graphics.OrderedGroup(2)
actor_group = pyglet.graphics.OrderedGroup(3)
menu_group = pyglet.graphics.OrderedGroup(4)

def make_image(path):
   image = pyglet.resource.image(path)
   return image

def make_sprite(image, x, y, group):
   #print("Sprites: Making sprite")
   id = index.next()
   pyg_sprite = pyglet.sprite.Sprite(image, x=x, y=y, batch=batch, group=group)
   sprite = Sprite(id, pyg_sprite)
   index.add(sprite, id)
   return sprite

def make_animation(images, rate, start=0, repeat=False, long=False):
   #print("Sprites: Making animation")
   return Animation(images, rate, start, repeat, long)

def get_sprite(x, y, image, group):
   return sprite_pool.get()

def make_tile(x, y, index):
   return make_sprite(tile_images[index], x, y, tile_group)

def make_block(x, y, index):
   return make_sprite(block_images[index], x, y, block_group)

def make_item(x, y, index):
   return make_sprite(block_images[index], x, y, block_item_group)

def make_actor(image, x, y):
   return make_sprite(image, x, y, actor_group)

def make_menu(image, x, y):
   return make_sprite(image, x, y, menu_group)


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

a = pyglet.resource.image("eye-front-a.png")
b = pyglet.resource.image("eye-front-b.png")
c = pyglet.resource.image("eye-front-c.png")
d = pyglet.resource.image("eye-front-d.png")
eye_front_images = a, b, c, d, c, b
eye_front_anim = make_animation(eye_front_images, 1, repeat=True)

a = pyglet.resource.image("eye-back-a.png")
b = pyglet.resource.image("eye-back-b.png")
c = pyglet.resource.image("eye-back-c.png")
d = pyglet.resource.image("eye-back-d.png")
eye_back_images = a, b, c, d, c, b
eye_back_anim = make_animation(eye_back_images, 1, repeat=True)

a = pyglet.resource.image("eye-left-a.png")
b = pyglet.resource.image("eye-left-b.png")
c = pyglet.resource.image("eye-left-c.png")
d = pyglet.resource.image("eye-left-d.png")
eye_left_images = a, b, c, d, c, b
eye_left_anim = make_animation(eye_left_images, 1, repeat=True)

a = pyglet.resource.image("eye-right-a.png")
b = pyglet.resource.image("eye-right-b.png")
c = pyglet.resource.image("eye-right-c.png")
d = pyglet.resource.image("eye-right-d.png")
eye_right_images = a, b, c, d, c, b
eye_right_anim = make_animation(eye_right_images, 1, repeat=True)

a = pyglet.resource.image("eye-damage-a.png")
b = pyglet.resource.image("eye-damage-b.png")
c = pyglet.resource.image("eye-damage-c.png")
d = pyglet.resource.image("eye-damage-d.png")
eye_damage_images = a, b, c, d, c, b
eye_damage_anim = make_animation(eye_damage_images, 1, repeat=True)

a = pyglet.resource.image("eye-cast-a.png")
b = pyglet.resource.image("eye-cast-b.png")
c = pyglet.resource.image("eye-cast-c.png")
d = pyglet.resource.image("eye-cast-d.png")
eye_cast_images = a, b, c, d
eye_cast_anim = make_animation(eye_cast_images, 1, repeat=True)