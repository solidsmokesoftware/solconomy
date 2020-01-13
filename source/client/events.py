import pyglet
from pyglet.window import key

from source.pysics.vector import Vector
from source.pysics.shape import Point
from source.common.objects import Actor
from source.common.objects import Block
from source.common.constants import *

class EventHandler:
   def __init__(self, game):
      self.game = game
      self.outgoing = game.outgoing
      self.objects = game.objects
      self.world = game.objects.world
      self.space = game.objects.space
      self.network = game.network
      self.clock = game.clock
      self.sprites = game.objects.sprites

      self.actor = None
      self.search_pos = Vector(0, 0)
      
      self.camera = game.camera
      self.window = game.window
      self.batch = game.objects.sprites.batch

      self.pos = Vector(0, 0)
      self.dir = Vector(0, 0)
      self.block = None
      self.select = None

   def start(self):
      print("Events: Starting")
      self.window.push_handlers(self.on_draw, self.on_key_press, self.on_key_release, self.on_mouse_press, self.on_mouse_release, self.on_mouse_motion)

   def on_draw(self):
      self.window.clear()
      self.batch.draw()

   def on_key_press(self, symbol, modifiers):
      #print(f"Events: Key press {symbol}")
      if symbol == key.W:
         self.dir.y = 1
      elif symbol == key.A:
         self.dir.x = -1
      elif symbol == key.S:
         self.dir.y = -1     
      elif symbol == key.D:
         self.dir.x = 1

   def on_key_release(self, symbol, modifiers):
      self.dir.x = 0
      self.dir.y = 0
      return
       
   def on_mouse_press(self, x, y, button, modifiers):
      xo = self.actor.position.x - (WINDOW_SIZE_X // 2) + x
      yo = self.actor.position.y - (WINDOW_SIZE_Y // 2) + y
      if button == 1:
         print("click")
         collisions = self.objects.find(xo, yo)
         for body in collisions:
            print(body.name)
            if body.name == "block":
               string = f"{body.id}/{PLAYER_DEL_ACTOR}"
               self.objects.updates.append(string)
               self.objects.delete(body)
      
      elif button == 4:
         xd = xo - self.actor.position.x
         yd = yo - self.actor.position.y
         self.objects.place(self.actor, xo, yo)
         self.camera.move(xd, yd)

   def on_mouse_motion(self, x, y, dx, dy):
      return

   def on_mouse_release(self, x, y, button, modifier):
      return

   def move(self, delta):
      if self.dir.x == 0 and self.dir.y == 0:
         return
      else:
         step = self.actor.speed * delta  
         xi = int(self.dir.x * step)
         yi = int(self.dir.y * step)
         self.pos.x = self.actor.position.x + xi
         self.pos.y = self.actor.position.y + yi

         #Collision handling
         blocked = False
         collisions = self.space.get(self.pos, self.objects.tile_shape)
         for body in collisions:
            print((body.id, body.name))
            if body.name == "block":
               blocked = True
            elif body.name == "actor":
               if body.id != self.actor.id:
                  blocked = True
            elif body.name == "tile":
               if body.value == WATER:
                  blocked = True

         if not blocked:
            self.objects.place(self.actor, self.pos.x, self.pos.y)
            self.camera.move(xi, yi)
            self.objects.updates.append(f"{self.actor.pos_info()}/{PLAYER_POS}")
            #print(f"Events: Moving actor {self.actor.id} to {self.pos.x}:{self.pos.y}")
            return
         else:
            print(f"Events: Not moving due to collision at {self.pos.x}:{self.pos.y}")
            return
