import time
import pyglet

from source.common.network import Client
from source.common.sharedlist import SharedList
from source.common.clock import Clock
from source.common.constants import *


from source.system.world import World
from source.system.system import System
from source.system.entity import Entity
from source.system.client_input import ClientInput
from source.system.player_input import PlayerInput
from source.system.spatial import Spatial
from source.system.visual import Visual
from source.system.value import Value
from source.system.component import Component

from source.client.camera import Camera
import source.client.scenes as scenes


class Game(System):
    def __init__(self):
        System.__init__(self, self)



        self.clock = Clock(1/15.0)

        self.input_channel = SharedList()
        self.output_channel = SharedList()

        
        self.component = Component(self)
        self.entity = Entity(self)
        self.spatial = Spatial(self)
        self.visual = Visual(self)
        self.value = Value(self)

        self.network = Client(self)


        self.world = World(self)
        self.world.visual = True

        self.player = None
        self.actor = None
        
        #  Add visual entity
        self.selection = self.system.entity.add_menu(0, 0, 'blank.png')
        
        self.close_actors = []

        self.camera = Camera()
        self.player_input = PlayerInput(self)
        self.network_input = ClientInput(self)

        self.scenes = scenes.Manager(self)
        scene = self.scenes.load(scenes.MainMenu)
        self.scenes.add(scene)



    def start(self):
        pyglet.app.run()
        self.run()

    def start_connection(self):
        pyglet.clock.schedule_interval(self.network_input.handle_input, 1.0 / MSG_RATE)
        self.network.query_server()
        self.network.start()

    def run(self):
        while True:
            self.player_input.run()
            self.network_input.run()
            if self.clock.tick():
                self.spatial.run()
                self.visual.run()
        time.sleep(0.001)