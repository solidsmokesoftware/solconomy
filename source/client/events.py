import pyglet
from pyglet.window import key
from source.common.constants import *

from source.pysics.vector import Vector


class EventHandler:
   def __init__(self, client):
      self.client = client
      self.outgoing = client.outgoing
      self.objects = client.objects
      self.camera = client.objects.camera
      self.network = client.network
      self.clock = client.clock
      self.sprites = client.objects.sprites

      self.actor = None
      self.search_pos = Vector(0, 0)
      
      self.window = client.window
      self.batch = client.objects.sprites.batch

      self.pos = Vector(0, 0)
      self.dir = Vector(0, 0)
      self.block = None
      self.select = None

   def start(self):
      print("Events: Starting")
      self.window.push_handlers(self.on_draw, self.on_key_press, self.on_key_release, self.on_mouse_press, self.on_mouse_release, self.on_mouse_motion)
      #pyglet.clock.schedule_interval(self.update, 1 / 30.0)

   def on_draw(self):
      self.window.clear()
      self.batch.draw()

   def on_key_press(self, symbol, modifiers):
      self.objects.moving(self.actor)
      if symbol == key.W:
         self.objects.turn(self.actor, 0, 1)     
      elif symbol == key.A:
         self.objects.turn(self.actor, -1, 0)
      elif symbol == key.S:
         self.objects.turn(self.actor, 0, -1)
      elif symbol == key.D:
         self.objects.turn(self.actor, 1, 0)
      
   def on_key_release(self, symbol, modifiers):
      self.objects.stop(self.actor)
       
   def on_mouse_press(self, x, y, button, modifiers):
      xo = self.actor.position.x - (WINDOW_SIZE_X // 2) + x
      yo = self.actor.position.y - (WINDOW_SIZE_Y // 2) + y
      if button == 1:
         print("click")
         collisions = self.objects.find(xo, yo)
         for body in collisions:
            print(body.name)
            if body.name == "block":
               string = f"{body.id}/{PLAYER_DELETE}"
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

