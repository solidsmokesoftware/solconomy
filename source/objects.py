
from pecrs.controller import Controller
from pecrs.body import *
from pecrs.shape import *

import pyglet

from source.world import World
from source.constants import *
from source.camera import Camera
import source.sprites as Sprites


class SpriteBody(pyglet.sprite.Sprite):
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.id = None
      self.speed = 100
      self.moving = False
      self.direction = (0,0)
      self.area = None
      self.solid = False


class Block(SpriteBody):
   def __init__(self, value, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.value = value
      self.name = "block"
      self.key = BLOCK
      self.solid = True


class Tile(SpriteBody):
   def __init__(self, value, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.value = value
      self.name = "tile"
      self.key = TILE


class Item(SpriteBody):
   def __init__(self, value, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.value = value
      self.name = "item"
      self.key = ITEM


class Actor(SpriteBody):
   def __init__(self, anims, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.anims = anims
      self.speed = 300
      self.inventory = {}
      self.name = "actor"
      self.moving = True
      self.key = ACTOR
      self.solid = True

   def give(self, item):
      if item in self.inventory:
         self.inventory[item] += 1
      else:
         self.inventory[item] = 1

   def get(self, item):
      results = False
      if item in self.inventory:
         results = True
         self.inventory[item] -= 1
         if self.inventory[item] <= 0:
            del self.inventory[item]

      return results


class Objects(Controller):
   def __init__(self, size=256):
      super().__init__(size)
      self.world = World()
      self.camera = Camera()
      self.sprites = Sprites

   def start(self, seed):
      self.world.start(seed)
      span = -2, -1, 0, 1, 2
      for xi in span:
         for yi in span:
            new_tiles = self.world.build((xi, yi))
            if new_tiles:
               for data in new_tiles:
                  x = data[0]
                  y = data[1]
                  self.make_tile(x, y, data[2])
                  if data[3]:
                     self.make_block(x, y, data[3])
                     if data[4]:
                        self.make_item(x, y, data[4])

   def step(self, delta):
      for body in self.actives:
         if body.moving:
            start = body.position
            distance = self.space.move(body, body.direction[0], body.direction[1], body.speed*delta)
            if body.solid:
               collision = False
               collisions = self.space.collisions_with(body)
               for other in collisions:
                  self.on_collision(self, other)
                  if collision == False and other.solid:
                     collision = True
                     body.position = start
               if collision:
                  return
            self.on_move(body, distance)
            area = self.space.update_area(body)
            if area:
               self.on_area(body, area)
            

   def make_tile(self, x, y, value):
      body = Tile(value, Sprites.tile_images[value], x=x, y=y, batch=Sprites.batch, group=Sprites.tile_group)
      self.add(body, static=True)
      if value == WATER:
         body.solid = True
      return body

   def make_block(self, x, y, value):
      body = Block(value, Sprites.block_images[value], x=x, y=y, batch=Sprites.batch, group=Sprites.block_group)
      self.add(body, static=True)
      return body

   def make_actor(self, x, y):
      body = Actor(Sprites.soul_anims, Sprites.soul_image, x=x, y=y, batch=Sprites.batch, group=Sprites.actor_group)
      #self.sprites.animations.append(shape)
      self.add(body)
      return body

   def make_item(self, x, y, value):
      body = Item(value, Sprites.block_item_images[value], x=x, y=y, batch=Sprites.batch, group=Sprites.block_item_group)
      self.add(body, static=True)
      return body

   def on_area(self, body, start):
      new_tiles = self.world.build(body.area)
      if new_tiles:
         for data in new_tiles:
            x = data[0]
            y = data[1]
            self.make_tile(x, y, data[2])
            if data[3]:
               self.make_block(x, y, data[3])
            if data[4]:
               self.make_item(x, y, data[4])

   def on_move(self, body, distance):
      if self.camera.actor == body:
         self.camera.move(distance[0], distance[1])



   # def on_turn(self, body):
   #    body.anim
   #    if body.direction[0] == 1:
   #       body.anim = body.anims["dr"]

   #    elif body.direction[0] == -1:
   #       body.anim = body.anims["dl"]

   #    elif body.direction[1] == 1:
   #       body.anim = body.anims["ur"]

   #    elif body.direction[1] == -1:
   #       body.anim = body.anims["dl"]
        
   def on_delete(self, body):
      if body in self.sprites.animations:
         self.sprites.animations.remove(body)
      
      try:
         body.delete()
      except:
         pass
         

   
