import sys
import time
from source.common.sharedlist import SharedList
from source.common.clock import Clock
from source.common.constants import *
from source.common.world import LogicalWorld as World
from source.common.actors import LogicalActor as Actor
from source.common.communication import Parser

import random

###

from threading import Thread
from source.common.messenger import Messenger
from source.common.network import Network
from source.common.index import Index


class Game:
   def __init__(self, address, port):
      self.incoming_handler = Thread(target=self.handle_incoming)
      self.run_handler = Thread(target=self.run)
      self.tile_loader = Thread(target=self.load_tiles)

      self.clock = Clock(1/MSG_RATE)
      self.world_clock = Clock(1)
      self.network = Network(address, port, self.clock)
      self.parser = Parser()
      self.incoming = Messenger()
      self.index = Index()

      self.world = World()
      self.world.set_seed(1001)

      self.players = {}

      self.options = {
         PLAYER_IDENT.encode(): self.handle_ident,
         PLAYER_POS.encode(): self.handle_pos,
         PLAYER_BLOCK.encode(): self.handle_block,
         PLAYER_MSG.encode(): self.handle_msg,
         PLAYER_ACTION.encode(): self.handle_action
      }

   def start(self):
      self.network.bind()
      self.incoming_handler.start()
      self.run_handler.start()

   def handle_incoming(self):
      print("Game: Waiting for input")
      while True:
         #print("Game: Waiting for input")
         packet = self.network.recv()
         if packet:
            self.incoming.give(packet)
         time.sleep(SMALL_NUMBER)

   def load_tiles(self):
      while True:
         if self.world_clock.tick():
            self.world.update()

         time.sleep(SMALL_NUMBER)

   def run(self):
      #try:
      while True:
         if self.clock.tick():
            #print(f"Game: Running {self.clock.time.value}")
            self.handle_input()
            self.update_players()

         time.sleep(SMALL_NUMBER)

   def handle_input(self):
      packets = self.incoming.get()
      for packet in packets:
         #try:
         packet.data = self.parser.decode(packet.data)
         self.options[packet.data[-2]](packet)
         
         #except:
         #   print(f"Game: Bad packet {packet.data} from {packet.host}")

   def update_players(self):
      time = self.clock.time.value
       
      for host in self.players:
         actor = self.players[host]
         msg = self.parser.encode(SERVER_POS, actor.get_state(), time)
         print(f"Game: Update players {msg}")
         self.network.sendall(msg)

   def handle_pos(self, packet):
      #print("Game: Handling pos {packet.data}")
      data = self.parser.pos(packet.data[0])

      index = int(data[0])
      x = int(data[1])
      y = int(data[2])

      actor = self.players[packet.host]
      actor.set_tile(x, y)

   def handle_ident(self, packet):
      print(f"Game: Handling join {packet.data}")
      username = packet.data[0]
      password = packet.data[1]

      index = self.index.get()
      actor = Actor(index, 0, 0)
      state = actor.get_state()
      self.world.add_actor(actor)
      self.world.add_player_actor(actor)
      time = self.clock.time.value

      data = f"{state}/{self.world.get_seed()}"
      msg = self.parser.encode(SERVER_IDENT, data, time)
      self.network.sendto(msg, packet.host)
      
      msg = self.parser.encode(SERVER_NEW_ACTOR, state, time)
      for host in self.players:
         self.network.sendto(msg, host) #Tell everyone the new player has joined
         
         other = self.players[host] #Tell the new player about all the other players
         actor_msg = self.parser.encode(SERVER_NEW_ACTOR, other.get_state(), time)
         self.network.sendto(actor_msg, packet.host)

      self.players[packet.host] = actor #Adding to players starts the updates
      print(f"Game: handling ident finished: {actor.get_state()}")

   def handle_msg(self, packet):
      return

   def handle_block(self, packet):
      return

   def handle_action(self, packet):
      return


