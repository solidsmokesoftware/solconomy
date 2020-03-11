import pyglet
from random import randint

from pecrs.index import Index
from source.constants import *


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

class Sprite(pyglet.sprite.Sprite):
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.id = None
      self.speed = 100
      self.moving = True
      self.direction = None
      self.area = None

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

def make_animation(images, rate, start=0, repeat=False, long=False):
   #print("Sprites: Making animation")
   return Animation(images, rate, start, repeat, long)

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
soul_image = pyglet.resource.image('soul.png')

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

soul_anims = {}
soul_anims["dl"] = eye_left_anim
soul_anims["dr"] = eye_right_anim
soul_anims["ul"] = eye_back_anim
soul_anims["ur"] = eye_back_anim
soul_anims["cast"] = eye_cast_anim
soul_anims["damage"] = eye_damage_anim