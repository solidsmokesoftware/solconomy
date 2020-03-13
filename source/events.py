import pyglet
from pyglet.window import key
from source.constants import *


class EventHandler:
   def __init__(self, client):
      self.client = client
      self.objects = client.objects
      self.camera = client.objects.camera
      self.sprites = client.objects.sprites

      self.actor = None
      
      self.window = client.window
      self.batch = client.objects.sprites.batch


   def start(self):
      self.window.push_handlers(self.on_draw, self.on_key_press, self.on_key_release, self.on_mouse_press, self.on_mouse_release, self.on_mouse_motion)
      #pyglet.clock.schedule_interval(self.update, 1 / 30.0)

   def on_draw(self):
      self.window.clear()
      self.batch.draw()

   def on_key_press(self, symbol, modifiers):
      self.objects.start_moving(self.actor)
      if symbol == key.W:
         self.objects.turn(self.actor, 0, 1)     
      elif symbol == key.A:
         self.objects.turn(self.actor, -1, 0)
      elif symbol == key.S:
         self.objects.turn(self.actor, 0, -1)
      elif symbol == key.D:
         self.objects.turn(self.actor, 1, 0)
      elif symbol == key.I:
         print(self.actor.inventory)
      
   def on_key_release(self, symbol, modifiers):
      self.objects.stop_moving(self.actor)
       
   def on_mouse_press(self, x, y, button, modifiers):
      xo = self.actor.position[0] - (WINDOW_SIZE_X // 2) + x
      yo = self.actor.position[1] - (WINDOW_SIZE_Y // 2) + y
      if button == 1:
         print("click")
         collisions = self.objects.collisions_at(xo, yo)
         for body in collisions:
            print(body.name)
            if body.key == BLOCK:
               self.actor.give((body.key, body.value))
               self.objects.delete(body)
            elif body.key == ITEM:
               self.actor.give((body.key, body.value))
               self.objects.delete(body)
      
      elif button == 4:
         xd = xo - self.actor.position[0]
         yd = yo - self.actor.position[1]
         self.objects.place(self.actor, xo, yo)
         self.camera.move(xd, yd)

   def on_mouse_motion(self, x, y, dx, dy):
      return

   def on_mouse_release(self, x, y, button, modifier):
      return

