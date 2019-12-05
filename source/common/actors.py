from source.common.base import Object
from source.common.base import VisualObject


import source.client.sprites as sprites
from source.common.constants import *


class Actor:
    def __init__(self):
        self.type = 'Actor'
        self.chunk = None
        self.inventory = {}

    def can_move(self, tile):
        results = False
        if not tile.block:
            if tile.value != WATER:
                if tile.value != SEA:
                    results = True

        return results

    def set_chunk(self, x, y):
        self.chunk = x, y

    def give(self, item):
        if item in self.inventory:
            self.inventory[item] += 1
        else:
            self.inventory[item] = 1

    def get(self, item):
        results = False
        if item in self.inventory:
            results = True
            self.inventory[item] -= 1
            if self.inventory[item] <= 0:
                del self.inventory[item]

        return results


class LogicalActor(Actor, Object):
    def __init__(self, index, x, y):
        Object.__init__(self, index, x, y)
        Actor.__init__(self)


class VisualActor(Actor, VisualObject):
    def __init__(self, index, x, y, sprite):
        VisualObject.__init__(self, index, x, y, sprite)
        Actor.__init__(self)