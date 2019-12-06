import sys
import time
from source.common.sharedlist import SharedList
from source.common.clock import Clock
from source.common.constants import *
from source.common.world import LogicalWorld as World
from source.common.actors import LogicalActor as Actor

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
      self.incoming = Messenger()
      self.index = Index()

      self.world = World()
      self.world.set_seed(1001)

      self.players = {}

      self.options = {LOGIN_COM.encode(): self.handle_login,
                  POS_UPDATE_COM.encode(): self.handle_pos_update,
                  ACCEPT_COM.encode(): self.handle_accept,
                  DECLINE_COM.encode(): self.handle_decline,
                  MESSAGE_COM.encode(): self.handle_player_message,
                  BATTLE_COM.encode(): self.handle_battle,
                  CHALLENGE_COM.encode(): self.handle_challenge,
                  POS_INFO_COM.encode(): self.handle_pos_info,
                  PART_INFO_COM.encode(): self.handle_part_info,
                  FULL_INFO_COM.encode(): self.handle_full_info,
                  EQUIP_INFO_COM.encode(): self.handle_equip_info,
                  IDLE_COM.encode(): self.handle_idle
                     }

   def start(self):
      self.network.bind()
      self.incoming_handler.start()
      self.run_handler.start()

   def handle_incoming(self):
      #print("Game: Waiting for input")
      while True:
         print("Game: Waiting for input")
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
         packet.data = packet.data.split(b"/")
         self.options[packet.data[-2]](packet)
         
         #except:
         #   print(f"Game: Bad packet {packet.data} from {packet.host}")

   def update_players(self):
      for host in self.players:
         actor = self.players[host]
         msg = f"{actor.get_state()}/{POS_UPDATE_RES}/{self.clock.time.value}"
         self.network.sendto(msg.encode(), host)


   def handle_player_pos_update(self, packet):
      player = self.players.get(packet.host)
      button = int(packet.data[0])
      x = int(packet.data[1])
      y = int(packet.data[1])

      actor = player.actor
      actor.update_pos(x, y)

   def handle_pos_update(self, packet):
      data = packet.data[0].split(b":")
      index = int(data[0])
      x = int(data[1])
      y = int(data[2])

      actor = self.world.actors[index]
      actor.set_tile(x, y)

   def handle_login(self, packet):
      # TODO create an actor for the player on join
      print("Game: Handling join")
      username = packet.data[0]
      password = packet.data[1]

      id = self.index.get()

      actor = Actor(id, 0, 0)
      self.players[packet.host] = actor
      self.world.add_actor(actor)
      self.world.add_player_actor(actor)

      msg = f"{actor.get_state()}/{self.world.get_seed()}/{LOGIN_RES}/{self.clock.time.value}"
      self.network.sendto(msg.encode(), packet.host)

   def handle_player_message(self, packet):
      return

   def handle_battle(self, packet):
      return

   def handle_challenge(self, packet):
      return

   def handle_accept(self, packet):
      return

   def handle_decline(self, packet):
      return

   def handle_pos_info(self, packet):
      return

   def handle_part_info(self, packet):
      return

   def handle_full_info(self, packet):
      return

   def handle_equip_info(self, packet):
      return

   def handle_idle(self, packet):
      return        

   def handle_get_actors(self, packet):
      return packet

   def handle_get_actor_info(self, packet):
      index = int(packet.data[0])
      info = int(packet.data[1])

      packet.data = '%s' % self.world.get_actor_info(index, info)
      packet.command = info

      msg = f"{self.world.get_actor_info(index, info)}/{info}/{self.clock.time.value}"

      print('Game: Get actor: %s' % msg)
      self.network.sendto(msg.encode(), packet.host)
