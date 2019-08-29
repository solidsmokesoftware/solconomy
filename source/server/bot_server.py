import sys
import random
import time
from source.common.clock import Clock
from source.common.constants import *
from threading import Thread

import random


class Server(Thread):
    def __init__(self, game):
        Thread.__init__(self)
        self.host = ('npc_ai', 0)
        self.game = game
        self.clock = Clock(2)

        self.directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def run(self):
        time.sleep(3)
        #try:
        while True:
            if self.clock.tick():
                for actor in self.game.world.actors.get_npcs():
                    r = random.randint(0, len(self.directions)-1)
                    choice = self.directions[r]
                    x = actor.x + choice[0]
                    y = actor.y + choice[1]

                    actor.x_input = x
                    actor.y_input = y
                    actor.has_input = True

            # except:
            #   print('Game error')
            time.sleep(0.001)

