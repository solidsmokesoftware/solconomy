import pyglet
import time
from threading import Thread


import source.client.sprites as sprites
from source.client.events import EventHandler
from source.common.network import Network
from source.common.objects import ClientObjects
from source.common.messenger import Messenger
from source.common.constants import *
from source.pysics.clock import SyncClock



class Client:
   def __init__(self):
      self.clock = SyncClock()
      self.running = False
      self.objects = ClientObjects(ZONE_SIZE)

      self.window = pyglet.window.Window(WINDOW_SIZE_X, WINDOW_SIZE_Y)
      self.batch = sprites.batch

      self.network = None
      self.incoming = Messenger()
      self.outgoing = []
      self.run_network = Thread(target=self.run_incoming)

      self.username = None
      self.password = None
      self.address = None
      self.port = None
      self.host = None

      self.sprites = sprites
      
      self.player = None
      self.actor = None
      self.events = EventHandler(self)

      self.options = {            
         #SERVER_IDENT.encode(): self.handle_ident,
         SERVER_POS.encode(): self.handle_pos,
         SERVER_PING.encode(): self.handle_ping,
         SERVER_NEW_ACTOR.encode(): self.handle_new_actor,
         SERVER_DEL_ACTOR.encode(): self.handle_del_actor,
         }

   def start(self):
      print("Game: Starting")
      self.running = True
      self.events.start()

      self.set_host("Player", "join", "localhost", 65535)

      string = f"{self.username}/{self.password}/{PLAYER_IDENT}"
      self.network.send_con(string)
      message = self.network.recv()
      self.handle_ident(message)
      
      self.run_network.start() #Thread that calls handle_incoming to run the network
      pyglet.clock.schedule_interval(self.run, MSG_RATE)
      pyglet.app.run()

   def update(self):
      updates = self.outgoing
      self.outgoing = []
      return updates

   def set_host(self, username, password, address, port):
      self.username = username
      self.password = password
      self.address = address
      self.port = port
      self.host = address, port

      self.network = Network(address, port, self.clock)

   def handle_ident(self, message):
      print(f"Game: Handle Ident")
      id = int(message.args[0])
      x = int(message.args[1])
      y = int(message.args[2])
      seed = int(message.args[3])

      self.actor = self.objects.make(ACTOR, id, x, y, message.host)
   
      self.events.actor = self.actor
      self.player = message.host
      self.objects.camera.focus_on(self.actor)

   def run_incoming(self):
      while self.running:
         #print("Game: Network handling incoming")
         message = self.network.recv()
         if message:
            #print("Game: income handler has messages")
            self.incoming.give(message)
         time.sleep(SMALL_NUMBER)

   def run(self, delta):
      self.handle_incoming()
      #self.handle_turn(delta)
      self.handle_input(delta)
      self.handle_animations(delta)
      self.handle_outgoing()

   def handle_incoming(self):
      messages = self.incoming.get()
      for message in messages:
         self.clock.time = message.time
         self.options[message.command](message)

   def handle_input(self, delta):
      self.objects.step(delta)

   def handle_animations(self, delta):
      free = []
      for sprite in self.sprites.animations:
         anim = sprite.anim
         if anim.start > -1 and self.clock.time > anim.start :
            anim.time += delta
            if anim.time > anim.rate:
               anim.index += 1
               if anim.index >= anim.max:
                  self.handle_animation_loop(sprite)
                  if anim.repeat:
                     anim.index = 0
                     anim.time = 0
                     sprite.sprite.image = anim.images[anim.index]
                  else:
                     if anim.long:
                        anim.start = -1
                     else:
                        self.handle_animation_end(sprite)
                        free.append(sprite)
               else:
                  anim.time = 0
                  sprite.sprite.image = anim.images[anim.index]

      for sprite in free:
         self.sprites.delete(sprite)

   def handle_animation_loop(self, sprite):
      pass

   def handle_animation_end(self, sprite):
      pass

   def handle_ping(self, message):
      return

   def handle_pos(self, message):
      id = int(message.args[0])
      if id != self.actor.id:
         body = self.objects.get(id)
         if body:
            x = int(message.args[1])
            y = int(message.args[2]) 
            self.objects.place(body, x, y)
         else:
            self.outgoing.append(f"{id}/{PLAYER_ACTOR_INFO}")
   
   def handle_new_actor(self, message):
      id = int(message.args[0])
      if id != self.actor.id:
         x = int(message.args[1])
         y = int(message.args[2])
         key = int(message.args[3])
         if key == ACTOR:
            value = message.host
            body = self.objects.make(key, id, x, y, value)
         elif key == BLOCK:
            value = int(message.args[4])
            body = self.objects.make(key, id, x, y, value)

   def handle_del_actor(self, message):
      id = int(message.args[0])
      body = self.objects.get(id)
      if body:
         self.objects.delete(body)      

   def handle_outgoing(self):
      updates = self.update()
      for string in self.outgoing:
         self.network.send_con(string)
         
      updates = self.objects.update()
      for string in updates:
         self.network.send_con(string)




