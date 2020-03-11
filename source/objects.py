
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
      self.moving = True
      self.direction = (0,0)
      self.area = None


class Block(SpriteBody):
   def __init__(self, value, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.value = value
      self.name = "block"
      self.key = BLOCK


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

   def make_tile(self, x, y, value):
      body = Tile(value, Sprites.tile_images[value], x=x, y=y, batch=Sprites.batch, group=Sprites.tile_group)
      self.add(body)
      return body

   def make_block(self, x, y, value):
      body = Block(value, Sprites.block_images[value], x=x, y=y, batch=Sprites.batch, group=Sprites.block_group)
      self.add(body)
      return body

   def make_actor(self, x, y):
      body = Actor(Sprites.soul_anims, Sprites.soul_image, x=x, y=y, batch=Sprites.batch, group=Sprites.actor_group)
      #self.sprites.animations.append(shape)
      self.add(body)
      return body

   def make_item(self, x, y, value):
      body = Item(value, Sprites.item_images[value], x=x, y=y, batch=Sprites.batch, group=Sprites.items_group)
      self.add(body)
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

   def on_collision(self, body, collisions):
      for other in collisions:
         if other.key == BLOCK:
            self.stop_moving(body)
         elif other.key == ACTOR:
            self.stop_moving(body)
         elif other.key == TILE:
            if other.value == WATER:
               self.stop_moving(body)

   def on_turn(self, body):
      try:
         body.anim
         if body.direction[0] == 1:
            body.anim = body.anims["dr"]

         elif body.direction[0] == -1:
            body.anim = body.anims["dl"]

         elif body.direction[1] == 1:
            body.anim = body.anims["ur"]

         elif body.direction[1] == -1:
            body.anim = body.anims["dl"]
      except:
         pass
        
   def on_delete(self, body):
      if body.anim in self.sprites.animations:
         self.sprites.animations.remove(body)
      
      try:
         body.delete()
      except:
         pass
         

   
