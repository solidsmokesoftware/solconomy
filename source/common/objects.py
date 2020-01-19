
from source.pysics.controller import Controller
from source.pysics.vector import Vector
from source.pysics.body import *
from source.pysics.shape import *

from source.common.world import World
from source.common.constants import *
import source.client.sprites as Sprites



class NetworkBody(Body):
   def __init__(self, id, position, shape):
      super().__init__(id, position, shape)
      self.value = 0

   def pos_com(self):
      return f"{self.id}/{self.position.x}/{self.position.y}/{PLAYER_POS}"

   def add_com(self):
      return f"{self.id}/{self.position.x}/{self.position.y}/{self.name}/{PLAYER_POS}"

   def delete_com(self):
      return f"{self.id}/{PLAYER_DELETE}"


class NetworkStaticBody(StaticBody):
   def __init__(self, id, position, shape):
      super().__init__(id, position, shape)
      self.value = 0

   def pos_com(self):
      return f"{self.id}/{self.position.x}/{self.position.y}/{PLAYER_POS}"

   def add_com(self):
      return f"{self.id}/{self.position.x}/{self.position.y}/{self.name}/{PLAYER_POS}"

   def delete_com(self):
      return f"{self.id}/{PLAYER_DELETE}"


class Block(NetworkStaticBody):
   def __init__(self, id, position, shape, value):
      super().__init__(id, position, shape)
      self.value = value
      self.name = "block"
        

class Tile(NetworkStaticBody):
   def __init__(self, id, position, shape, value):
      super().__init__(id, position, shape)
      self.value = value
      self.name = "tile"


class Item(NetworkStaticBody):
   def __init__(self, id, position, shape, value):
      super().__init__(id, position, shape)
      self.value = value
      self.name = "item"


class Actor(NetworkBody):
   def __init__(self, id, position, shape, host):
      shape = Rect(32, 64)
      super().__init__(id, position, shape)
      self.host = host
      self.speed = 300
      self.inventory = {}
      self.name = "actor"
      self.moving = True

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

      self.factory["tile"] = Tile
      self.factory["block"] = Block
      self.factory["item"] = Item
      self.factory["actor"] = Actor

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
            self.make("tile", (x, y), x, y, data[2])
            if data[3]:
               self.make("block", None, x, y, data[3])
            if data[4]:
               self.make("item", None, x, y, data[4])

   def on_add(self, body):
      if body.name == "actor":
         self.updates.append(f"{body.add_com()}/{SERVER_NEW_ACTOR}")

      elif body.name == "block":
         self.updates.append(f"{body.add_com()}/{SERVER_NEW_ACTOR}")

   def on_delete(self, body):
      self.updates.append(f"{body.delete_com()}/{SERVER_DEL_ACTOR}")

   def on_motion(self, body):
      self.updates.append(f"{body.pos_com()}/{SERVER_POS}")


class ClientObjects(Objects):
   def __init__(self, size):
      super().__init__(size)
      self.sprites = Sprites

   def on_add(self, body):
      if body.name == "tile":
         body.sprite = self.sprites.make_tile(body.position.x, body.position.y, body.value)

      elif body.name == "block":
         body.sprite = self.sprites.make_block(body.position.x, body.position.y, body.value)

      elif body.name == "item":
         body.sprite = self.sprites.make_item(body.position.x, body.position.y, body.value)

      elif body.name == "actor":
         sprite = self.sprites.make_actor(self.sprites.eye_left_images[0], body.position.x, body.position.y)
         sprite.anim = self.sprites.eye_left_anim
         sprite.anims["dl"] = self.sprites.eye_left_anim
         sprite.anims["dr"] = self.sprites.eye_right_anim
         sprite.anims["ul"] = self.sprites.eye_back_anim
         sprite.anims["ur"] = self.sprites.eye_back_anim
         body.sprite = sprite

      if body.sprite.anim:
         self.sprites.animations.append(body.sprite)

   def on_motion(self, body):
      body.sprite.place(body.position.x, body.position.y)
   
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
            self.make("tile", (x, y), x, y, data[2])
        
   def on_delete(self, body):
      if body.sprite:
         if body.sprite.anim:
            self.sprites.animations.remove(body.sprite)
      body.sprite.delete()


   
