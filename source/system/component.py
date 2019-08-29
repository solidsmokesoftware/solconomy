from source.system.system import System

from source.component.position import Position
from source.component.sprite import Sprite
from source.component.data import Data
from source.component.tile import Tile
from source.component.chunk import Chunk


class Component(System):
    def __init__(self, system):
        System.__init__(self, system)

        self.position = Position
        self.sprite = Sprite
        self.data = Data
        self.tile = Tile
        self.chunk = Chunk