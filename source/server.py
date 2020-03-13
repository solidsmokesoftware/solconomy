import sys
import time
import random
from threading import Thread

from pecrs.clock import Clock
from renet import *

from source.common.objects import Objects
from source.common.messenger import Messenger
from source.common.constants import *


class Server:
   def __init__(self, address, port, password):
      self.clock = Clock(MSG_RATE)
      self.running = False

      self.network_runner = Thread(target=self.run_network)

      self.network = Network(address, port)
      self.password = password
      self.incoming = Messenger()

      self.players = {}
      self.objects = Objects(self.network, ZONE_SIZE)

      self.options = {
         PLAYER_POS.encode(): self.handle_pos,
         PLAYER_DELETE.encode(): self.handle_del
      }

   def start(self):
      print("Server: Starting")
      self.running = True

      self.objects.world.set_seed(SEED)

      self.network.bind()
      self.network_runner.start()

      while self.running:
         delta = self.clock.tick()
         if delta:
            self.run(delta)
         time.sleep(SMALL_NUMBER)
      
   def run_network(self):
      while self.running:
         messages = self.network.recv()
         for message in messages:
            #print("Game: Run network got message")
            if message.host in self.players:
               #Passing the message off to the main thread
               #print("...sending to main thread")
               self.incoming.give(message)

            elif message.args[-1] == PLAYER_IDENT.encode():
               #print("...handling ident")
               self.handle_ident(message)
            else:
               print(f"Server: invalid message: {message.data} from {message.host}")

   def handle_ident(self, message):
      print(f"Game: Handling ident")
      password = message.args[1]
      if password == self.password:
         #print("Game: Player joined the server")
         self.handle_join(message)
      else:
         print("Game: Join refused, bad password")   

   def run(self, delta):
      self.handle_incoming()
      self.handle_run(delta)
      self.handle_outgoing()

   def handle_incoming(self):
      messages = self.incoming.get()
      for message in messages:
         self.options[message.args[-1]](message)

   def handle_run(self, delta):
      self.objects.step(delta)

   def handle_outgoing(self):
      self.network.resend_all()
      self.network.send_all()

   def handle_join(self, message):
      x = 0
      y = 0
      actor = self.objects.make(ACTOR, None, x, y, message.host)
      ident_msg = f"{actor.id}/{int(actor.position.x)}/{int(actor.position.y)}/{self.objects.world.seed}/{SERVER_IDENT}"
      connection = Connection(message.host[0], message.host[1])
      self.network.connections[message.host] = connection

      connection.buffer(ident_msg, RELIABLE_I)
      self.network.send(connection)
      
      add_msg = f"{actor.add_com()}/{SERVER_NEW_ACTOR}"
      for host in self.players:
         other = self.players[host]
         add_other_msg = f"{other.add_com()}/{SERVER_NEW_ACTOR}"
         other_connection = self.network.connections[host]
         other_connection.buffer(add_msg, RELIABLE_I)
         connection.buffer(add_other_msg, RELIABLE_I)
         
      self.players[message.host] = actor

   def handle_pos(self, message):
      #print("Game: Moving Object")
      id = int(message.args[0])
      body = self.objects.get(id)
      if body:
         x = int(message.args[1])
         y = int(message.args[2])
         self.objects.place(body, x, y)

   def handle_del(self, message):
      id = int(message.args[0])
      body = self.objects.get(id)
      if body:
         self.objects.delete(body)

   
