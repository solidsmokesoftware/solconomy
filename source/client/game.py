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


class Game:
   def __init__(self):
      self.window = pyglet.window.Window(WINDOW_SIZE_X, WINDOW_SIZE_Y)
      self.gui = glooey.Gui(self.window, batch=sprites.batch, group=sprites.menu_group)

      self.batch = sprites.batch
      self.clock = Clock(1.0/10.0)
      self.network = None
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
      self.selection = Selection()
      self.close_actors = []
      self.camera = Camera()
      self.events = EventHandler(self)

      self.options = {LOGIN_RES.encode(): self.handle_login,
                  POS_UPDATE_RES.encode(): self.handle_pos_update,
                  ACCEPT_RES.encode(): self.handle_accept,
                  DECLINE_RES.encode(): self.handle_decline,
                  MESSAGE_RES.encode(): self.handle_player_message,
                  BATTLE_RES.encode(): self.handle_battle,
                  CHALLENGE_RES.encode(): self.handle_challenge,
                  POS_INFO_RES.encode(): self.handle_pos_info,
                  PART_INFO_RES.encode(): self.handle_part_info,
                  FULL_INFO_RES.encode(): self.handle_full_info,
                  EQUIP_INFO_RES.encode(): self.handle_equip_info,
                  IDLE_RES.encode(): self.handle_idle,

                  MAKE_ACTOR_COM.encode(): self.handle_make_actor,
                  DEL_ACTOR_COM.encode(): self.handle_del_actor
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
      
      msg = f"{self.username}/{self.password}/{LOGIN_COM}/0"
      self.network.send_data(msg.encode())
      packet = self.network.recv()
      data = packet.data.split(b"/")
      self.handle_login(data)

      self.incoming_handler.start() #Thread that calls handle_incoming to run the network
      self.run_handler.start()
      self.events.start()

   def handle_login(self, data):
      print('Game: Logging into server')
      values = data[0].split(b":")
      seed = int(data[1])

      index = int(values[0])
      x = int(values[1])
      y = int(values[2])
     
      image = sprites.make_image('soul.png')
      sprite = sprites.make_actor(image, x, y)
      actor = Actor(index, x, y, sprite)
      self.actor = actor
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
            packet.data = packet.data.split(b"/")
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
               print(f"Game: Packet {packet.data} from {packet.host}")
               self.server_tick = int(packet.data[-1])
               self.options[packet.data[-2]](packet.data)
               #except:
               #   print(f"Game: Bad packet {packet.data} from {packet.host}")
            
            self.update_server(delta)

   def handle_pos_update(self, data):
      print(f"Game: Handling pos update {data}")

      objects = data[0].split(b"-")

      for object in objects:
         print(f"Game: step {object}")
         values = object.split(b":")
         index = int(values[0])
         x = int(values[0])
         y = int(values[1])
         pos = x * TILE_SIZE, y * TILE_SIZE
         self.close_actors.append([index, pos])

         if index in self.world.actors:
            if index == self.player.index:
               pass
            else:
               actor = self.world.actors[index]
               self.world.actors.move(actor, x, y)
         else:
            image = sprites.make_image('soul.png')
            sprite = sprites.make_actor(image, x, y)
            actor = Actor(index, x, y, sprite)
            self.world.actors[id] = actor

   def update_server(self, delta):
      print('Game: Updating server')
      state = self.actor.get_state()
      msg = f"{state}/{POS_UPDATE_COM}/{self.server_tick}"
      self.network.send_data(msg.encode())

   def handle_bad_message(self, data):
      return

   def handle_accept(self, data):
      return

   def handle_decline(self, data):
      return

   def handle_player_message(self, data):
      return

   def handle_battle(self, data):
      print(data)

   def handle_challenge(self, data):
      print(data)

   def handle_pos_info(self, data):
      print(data)

   def handle_part_info(self, data):
      print(data)

   def handle_equip_info(self, data):
      print(data)

   def handle_full_info(self, data):
      print(data)

      index = data[0]
      full_name = data[1]
      subrace = data[2]
      warband = data[3]
      rank = data[4]
      level = data[5]
      x = data[6]
      y = data[7]
      hp = data[8]
      hp_max = data[9]
      datas = [full_name, level, subrace, rank, warband, hp, hp_max]
      data = '%s\n%s, %s\n%s, %s\n%s/%s' % datas
      player.view(data)

   def handle_idle(self, data):
      print(data)

   def handle_make_actor(self, data):
      print(data)

   def handle_del_actor(self, data):
      print(data)




