import pyglet
import glooey

import source.client.scenes as scenes
import source.client.sprites as sprites
from source.client.camera import Camera
from source.client.events import EventHandler

from source.common.constants import *
from source.common.network import Network
from source.common.sharedlist import SharedList
from source.common.players import Player
from source.common.base import Selection
from source.common.actors import VisualActor as Actor
from source.common.world import VisualWorld as World

###

import time
from threading import Thread
from source.common.clock import Clock
from source.common.messenger import Messenger
from source.common.communication import Parser


class Game:
   def __init__(self):
      self.window = pyglet.window.Window(WINDOW_SIZE_X, WINDOW_SIZE_Y)
      self.gui = glooey.Gui(self.window, batch=sprites.batch, group=sprites.menu_group)

      self.batch = sprites.batch
      self.clock = Clock(1.0/MSG_RATE)
      self.network = None
      self.parser = Parser()
      self.incoming = Messenger()
      self.incoming_handler = Thread(target=self.handle_incoming)
      self.run_handler = Thread(target=self.run)

      self.actors = {}
      self.direction = b"0/0"
      self.server_tick = 0

      #pyglet.clock.schedule_interval(self.on_draw, 1.0 / 10.0)
      #pyglet.clock.schedule_interval(self.run, 1.0 / 10.0)

      self.username = None
      self.password = None
      self.address = None
      self.port = None
      self.host = None

      self.sprites = sprites
      self.scenes = scenes.Manager(self)
      scene = self.scenes.load(scenes.MainMenu)
      self.scenes.add(scene)

      self.world = World()

      self.player = None
      self.actor = None
      self.actors = {}
      self.selection = Selection()
      self.close_actors = []
      self.camera = Camera()
      self.events = EventHandler(self)

      self.options = {            
         #SERVER_IDENT.encode(): self.handle_ident,
         SERVER_POS.encode(): self.handle_pos,
         SERVER_PING.encode(): self.handle_ping,
         SERVER_LEVEL.encode(): self.handle_level,
         SERVER_BLOCK.encode(): self.handle_block,
         SERVER_NEW_ACTOR.encode(): self.handle_new_actor,
         SERVER_DEL_ACTOR.encode(): self.handle_del_actor,
         SERVER_KICK.encode(): self.handle_kick, 
         SERVER_MSG.encode(): self.handle_message
         }

   def start(self):
      pyglet.app.run()

   def set_host(self, username, password, address, port):
      self.username = username
      self.password = password
      self.address = address
      self.port = port
      self.host = address, port

      self.network = Network(address, port, self.clock)

   def start_connection(self):
      print("Game: Starting connection")
      
      data = f"{self.username}/{self.password}"
      msg = self.parser.encode(PLAYER_IDENT, data, 0)
      self.network.send_data(msg)
      packet = self.network.recv()
      self.handle_ident(packet)

      self.incoming_handler.start() #Thread that calls handle_incoming to run the network
      self.run_handler.start()
      self.events.start()

   def handle_ident(self, packet):
      print('Game: Logging into server')
      data = self.parser.decode(packet.data)
      values = self.parser.pos(data[0])

      seed = int(data[1])

      index = int(values[0])
      x = int(values[1])
      y = int(values[2])
     
      image = sprites.make_image('soul.png')
      sprite = sprites.make_actor(image, x, y)
      actor = Actor(index, x, y, sprite)
      self.actor = actor
      self.actors[index] = actor
      self.events.actor = actor

      host = self.network.connection.host
      pool = self.network.connection
      self.player = Player(host, self.actor)

      self.world.set_seed(seed)
      self.world.set_actor(self.actor)
      self.world.update()

      self.camera.focus_on(self.actor)


   #Network thread
   def handle_incoming(self):
      while True:
         packet = self.network.recv()
         if packet:
            packet.data = self.parser.decode(packet.data)
            self.incoming.give(packet)
         time.sleep(SMALL_NUMBER)

   def run(self):
      while True:
         #print('Game: Running')
         delta = self.clock.delta()
         if delta > 0:
            #print("Game: Tick")
            packets = self.incoming.get()
            for packet in packets:
               #try:
               #print(f"Game: Packet {packet.data} from {packet.host}")
               self.server_tick = int(packet.data[-1])
               self.options[packet.data[-2]](packet)
               #except:
               #   print(f"Game: Bad packet {packet.data} from {packet.host}")
            
            self.update_server(delta)

   def handle_pos(self, packet):
      print(f"Game: Handling pos update {packet.data}")
      values = self.parser.pos(packet.data[0])
      index = int(values[0])
      if index != self.actor.index:
         x = int(values[1])
         y = int(values[2])
         actor = self.actors[index]
         actor.set_tile(x, y)
      

   def update_server(self, delta):
      state = self.actor.get_state()
      #print(f"Game: Updating server {state}")
      msg = self.parser.encode(PLAYER_POS, state, self.server_tick)
      self.network.send_data(msg)

   def handle_message(self, packet):
      print(packet.data)

   def handle_ping(self, packet):
      print(packet.data)

   def handle_new_actor(self, packet):
      print(f"Handling new actor: {packet.data}")
      values = self.parser.pos(packet.data[0])
      index = int(values[0])
      if index != self.actor.index:
         x = int(values[1])
         y = int(values[2])

         image = sprites.make_image('soul.png')
         sprite = sprites.make_actor(image, x, y)
         actor = Actor(index, x, y, sprite)
         self.actors[index] = actor 
         #Not adding other actors to the world for right now.

   def handle_del_actor(self, packet):
      print(packet.data)
      del self.actors[index]

   def handle_block(self, packet):
      print(packet.data)

   def handle_level(self, packet):
      print(packet.data)

   def handle_kick(self, packet):
      print(packet.data)



