import pyglet
import time
from threading import Thread

import source.sprites as sprites
from source.events import EventHandler
from source.objects import Objects
from source.constants import *



class Client:
   def __init__(self):
      self.window = pyglet.window.Window(WINDOW_SIZE_X, WINDOW_SIZE_Y)
      self.batch = sprites.batch

      self.sprites = sprites

      self.objects = Objects()
      self.actor = None
      self.events = EventHandler(self)


   def start(self):
      print("Game: Starting")
      self.running = True
      self.actor = self.objects.make_actor(0, 0)
      self.events.actor = self.actor

      self.objects.world.set_seed(1955)
      self.objects.camera.focus_on(self.actor)

      self.events.start()
      pyglet.clock.schedule_interval(self.run, MSG_RATE)
      pyglet.app.run()
      
   def run(self, delta):
      self.handle_input()
      self.handle_run(delta)

   def handle_input(self):
      pass

   def handle_run(self, delta):
      self.objects.step(delta)





