
from source.pysics.manager import Manager
from source.pysics.vector import Vector
from source.pysics.body import *
from source.pysics.shape import *

from source.common.world import World
from source.common.constants import *
import source.client.sprites as sprites



class NetworkBody(Body):
   def __init__(self, id, position, shape):
      super().__init__(id, position, shape)
      self.value = 0

   def add_info(self):
      return f"{self.id}/{int(self.position.x)}/{int(self.position.y)}/{self.name}/{self.value}"

   def delete_info(self):
      return f"{self.id}"

   def pos_info(self):
      return f"{self.id}/{int(self.position.x)}/{int(self.position.y)}"


class NetworkStaticBody(StaticBody):
   def __init__(self, id, position, shape):
      super().__init__(id, position, shape)
      self.value = 0

   def add_info(self):
      return f"{self.id}/{int(self.position.x)}/{int(self.position.y)}/{self.name}/{self.value}"

   def delete_info(self):
      return f"{self.id}"

   def pos_info(self):
      return f"{self.id}/#{int(self.position.x)}/{int(self.position.y)}"


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
      super().__init__(id, position, shape)
      self.host = host
      self.inventory = {}
      self.name = "actor"

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


class Objects(Manager):
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
      
   def on_zone(self, body):
      new_tiles = self.world.build(body.zone)
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
         self.updates.append(f"{body.add_info()}/{SERVER_NEW_ACTOR}")

      elif body.name == "block":
         self.updates.append(f"{body.add_info()}/{SERVER_NEW_ACTOR}")

   def on_delete(self, body):
      self.updates.append(f"{body.delete_info()}/{SERVER_DEL_ACTOR}")

   def on_pos(self, body):
      self.updates.append(f"{body.pos_info()}/{SERVER_POS}")


class ClientObjects(Objects):
   def __init__(self, size):
      super().__init__(size)
      self.sprites = sprites

   def on_add(self, body):
      if body.name == "tile":
         body.sprite = sprites.make_tile(body.position.x, body.position.y, body.value)

      elif body.name == "block":
         body.sprite = sprites.make_block(body.position.x, body.position.y, body.value)

      elif body.name == "item":
         body.sprite = sprites.make_item(body.position.x, body.position.y, body.value)

      elif body.name == "actor":
         body.sprite = sprites.make_actor(sprites.soul, body.position.x, body.position.y)

   def on_pos(self, body):
      body.sprite.place(body.position.x, body.position.y)

   def on_zone(self, body):
      new_tiles = self.world.build(body.zone)
      if new_tiles:
         for data in new_tiles:
            x = data[0]
            y = data[1]
            self.make("tile", (x, y), x, y, data[2])
        
   def on_delete(self, body):
      body.sprite.delete()


   
