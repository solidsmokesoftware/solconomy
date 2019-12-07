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

      self.clock = Clock(1/10.0)
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

         time.sleep(1)

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
      for host in self.players:
         actor = self.players[host]
         msg = self.parser.encode(SERVER_POS, actor.get_state(), self.clock.time.value)
         self.network.sendto(msg, host)

   def handle_pos(self, packet):
      #print("Game: Handling pos {data[0]}")
      data = self.parser.pos(packet.data[0])

      index = int(data[0])
      x = int(data[1])
      y = int(data[2])

      actor = self.world.actors[index]
      actor.set_tile(x, y)

   def handle_ident(self, packet):
      # TODO create an actor for the player on join
      print("Game: Handling join")
      username = packet.data[0]
      password = packet.data[1]

      id = self.index.get()

      actor = Actor(id, 0, 0)
      self.players[packet.host] = actor
      self.world.add_actor(actor)
      self.world.add_player_actor(actor)

      data = f"{actor.get_state()}/{self.world.get_seed()}"
      msg = self.parser.encode(SERVER_IDENT, data, self.clock.time.value)
      self.network.sendto(msg, packet.host)

   def handle_msg(self, packet):
      return

   def handle_block(self, packet):
      return

   def handle_action(self, packet):
      return


