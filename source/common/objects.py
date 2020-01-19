
from source.pysics.controller import Controller
from source.pysics.vector import Vector
from source.pysics.body import *
from source.pysics.shape import *

from source.common.world import World
from source.common.constants import *
from source.client.camera import Camera
import source.client.sprites as Sprites




class NetworkBody(Body):
   def __init__(self, id, position, shape):
      super().__init__(id, position, shape)
      self.value = 0

   def pos_com(self):
      return f"{self.id}/{self.position.x}/{self.position.y}"

   def add_com(self):
      return f"{self.id}/{self.position.x}/{self.position.y}/{self.key}"

   def delete_com(self):
      return f"{self.id}"


class NetworkStaticBody(StaticBody):
   def __init__(self, id, position, shape):
      super().__init__(id, position, shape)
      self.value = 0

   def pos_com(self):
      return f"{self.id}/{self.position.x}/{self.position.y}"

   def add_com(self):
      return f"{self.id}/{self.position.x}/{self.position.y}/{self.key}"

   def delete_com(self):
      return f"{self.id}"


class Block(NetworkStaticBody):
   def __init__(self, id, position, shape, value):
      super().__init__(id, position, shape)
      self.value = value
      self.name = "block"
      self.key = BLOCK

   def add_com(self):
      return f"{self.id}/{self.position.x}/{self.position.y}/{self.key}/{self.value}"
        

class Tile(NetworkStaticBody):
   def __init__(self, id, position, shape, value):
      super().__init__(id, position, shape)
      self.value = value
      self.name = "tile"
      self.key = TILE


class Item(NetworkStaticBody):
   def __init__(self, id, position, shape, value):
      super().__init__(id, position, shape)
      self.value = value
      self.name = "item"
      self.key = ITEM


class Actor(NetworkBody):
   def __init__(self, id, position, shape, host):
      shape = Rect(32, 48)
      super().__init__(id, position, shape)
      self.host = host
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
   def __init__(self, size):
      super().__init__(size)
      self.updates = []
      self.world = World()

      self.factory[TILE] = Tile
      self.factory[BLOCK] = Block
      self.factory[ACTOR] = Actor
      self.factory[ITEM] = Item

      self.tile_shape = Rect(32, 32)

   def update(self):
      updates = self.updates
      self.updates = []
      return updates

   def make(self, kind, id, x, y, value):
      if not id:
         id = self.index.get()
      position = Vector(x, y)
      body = self.factory[kind](id, position, self.tile_shape, value)
      self.on_make(body)
      self.add(body)
      return body
      
   def on_area(self, body):
      new_tiles = self.world.build(body.area)
      if new_tiles:
         for data in new_tiles:
            x = data[0]
            y = data[1]
            self.make(TILE, (x, y), x, y, data[2])
            if data[3]:
               self.make(BLOCK, None, x, y, data[3])
            if data[4]:
               self.make(ITEM, None, x, y, data[4])

   def on_add(self, body):
      if body.key == ACTOR or body.key == BLOCK:
         self.updates.append(f"{body.add_com()}/{SERVER_NEW_ACTOR}")

   def on_delete(self, body):
      self.updates.append(f"{body.delete_com()}/{SERVER_DEL_ACTOR}")

   def on_motion(self, body):
      self.updates.append(f"{body.pos_com()}/{SERVER_POS}")


class ClientObjects(Objects):
   def __init__(self, size):
      super().__init__(size)
      self.sprites = Sprites
      self.camera = Camera()

   def on_add(self, body):
      if body.key == TILE:
         body.sprite = self.sprites.make_tile(body.position.x, body.position.y, body.value)

      elif body.key == BLOCK:
         body.sprite = self.sprites.make_block(body.position.x, body.position.y, body.value)

      elif body.key == ITEM:
         body.sprite = self.sprites.make_item(body.position.x, body.position.y, body.value)

      elif body.key == ACTOR:
         sprite = self.sprites.make_actor(self.sprites.eye_left_images[0], body.position.x, body.position.y)
         sprite.anim = self.sprites.eye_left_anim
         sprite.anims["dl"] = self.sprites.eye_left_anim
         sprite.anims["dr"] = self.sprites.eye_right_anim
         sprite.anims["ul"] = self.sprites.eye_back_anim
         sprite.anims["ur"] = self.sprites.eye_back_anim
         body.sprite = sprite

      if body.sprite.anim:
         self.sprites.animations.append(body.sprite)

   def on_move(self, body, distance):
      if self.camera.actor == body:
         self.camera.move(distance[0], distance[1])
         self.updates.append(f"{body.pos_com()}/{PLAYER_POS}")

   def on_motion(self, body):
      body.sprite.place(body.position.x, body.position.y)

   def on_collision(self, body, collisions):
      for other in collisions:
         if other.key == BLOCK:
            self.stop(body)
         elif other.key == ACTOR:
            self.stop(body)
         elif other.key == TILE:
            if other.value == WATER:
               self.stop(body)

   def on_turn(self, body):
      if body.sprite.anim:
         if body.direction.x == 1:
            body.sprite.anim = body.sprite.anims["dr"]

         elif body.direction.x == -1:
            body.sprite.anim = body.sprite.anims["dl"]

         elif body.direction.y == 1:
            body.sprite.anim = body.sprite.anims["ur"]

         elif body.direction.y == -1:
            body.sprite.anim = body.sprite.anims["dl"]

   def on_area(self, body):
      new_tiles = self.world.build(body.area)
      if new_tiles:
         for data in new_tiles:
            x = data[0]
            y = data[1]
            self.make(TILE, (x, y), x, y, data[2])
        
   def on_delete(self, body):
      if body.sprite:
         if body.sprite.anim:
            self.sprites.animations.remove(body.sprite)
      body.sprite.delete()


   
