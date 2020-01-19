import sys
import time
import random
from threading import Thread

from source.pysics.clock import Clock
from source.common.objects import Objects
from source.common.messenger import Messenger
from source.common.network import Network
from source.common.constants import *


class Server:
   def __init__(self, address, port, password):
      self.clock = Clock(MSG_RATE)
      self.running = False

      self.network_runner = Thread(target=self.run_network)

      self.network = Network(address, port, self.clock)
      self.password = password
      self.incoming = Messenger()
      self.outgoing = []

      self.players = {}
      self.objects = Objects(ZONE_SIZE)

      self.options = {
         PLAYER_POS.encode(): self.handle_pos,
         PLAYER_DELETE.encode(): self.handle_del
      }

   def start(self):
      print("Server: Starting")
      self.running = True

      self.objects.world.set_seed(1955)

      self.network.bind()
      self.network_runner.start()

      while self.running:
         delta = self.clock.tick()
         if delta:
            self.run(delta)
         time.sleep(SMALL_NUMBER)

   def update(self):
      updates = self.outgoing
      self.outgoing = []
      return updates
      
   def run_network(self):
      while self.running:
         message = self.network.recv()
         if message:
            #print("Game: Run network got message")
            if message.host in self.players:
               #Passing the message off to the main thread
               #print("...sending to main thread")
               self.incoming.give(message)

            elif message.command == PLAYER_IDENT.encode():
               #print("...handling ident")
               self.handle_ident(message)
            else:
               print("...invalid message")

   def handle_ident(self, message):
      print(f"Game: Handling ident")
      password = message.args[1]
      if password == self.password:
         #print("Game: Player joined the server")
         self.network.new_connection(message)
         self.handle_join(message)
      else:
         print("Game: Join refused, bad password")   

   def run(self, delta):
      self.handle_incoming()
      self.handle_input(delta)
      self.handle_outgoing()

   def handle_incoming(self):
      messages = self.incoming.get()
      for message in messages:
         self.options[message.command](message)

   def handle_join(self, message):
      x = 0
      y = 0
      actor = self.objects.make("actor", None, x, y, message.host)
      string = f"{actor.id}/{int(actor.position.x)}/{int(actor.position.y)}/{self.objects.world.seed}/{SERVER_IDENT}"
      self.network.send(string, message.host)
      
      for host in self.players:
         actor = self.players[host]
         string = f"{actor.add_com()}/{SERVER_NEW_ACTOR}"
         self.outgoing.append((string, message.host))

      self.players[message.host] = actor

   def handle_input(self, delta):
      self.objects.updates.append(f"{SERVER_PING}")

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

   def handle_outgoing(self):
      self.network.resend()
      updates = self.update()
      for packet in updates:
         self.network.send(packet[0], packet[1])

      updates = self.objects.update()
      for host in self.players:
         for string in updates:
            self.network.send(string, host)