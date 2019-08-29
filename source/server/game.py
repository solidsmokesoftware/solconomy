import time

from source.common.network import Server
from source.common.sharedlist import SharedList
from source.common.clock import Clock

from source.system.world import WorldThread
from source.system.system import Process
from source.system.component import Component
from source.system.entity import Entity
from source.system.server_input import ServerInput
from source.system.spatial import Spatial
from source.system.value import Value


class Game(Process):
    def __init__(self):
        Process.__init__(self, self)

        self.clock = Clock(1/15.0)

        self.input_channel = SharedList()
        self.output_channel = SharedList()

        self.component = Component(self)
        self.entity = Entity(self)
        self.spatial = Spatial(self)
        self.value = Value(self)

        self.world = WorldThread(self)
        self.world.set_seed(1001)

        self.network = Server(self, 'localhost', 45456)
        self.network_input = ServerInput(self)


    def start(self):
        self.network.start()
        self.world.start()
        self.run()

    def run(self):
        while True:
            self.network_input.run()
            if self.clock.tick():
                self.spatial.run()

            time.sleep(0.001)

    def add_actor(self, x, y):
        return

