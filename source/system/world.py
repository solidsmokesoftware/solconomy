from source.system.system import System

from source.component.tile import Tile
from source.component.chunk import Chunk

from source.common.opensimplex import OpenSimplex
from source.common.clock import Clock
from source.common.pool import Pool
from source.common.constants import *



import time
from threading import Thread
from random import randint


class World(System):
    def __init__(self, system):
        System.__init__(self, system)
        self.input_channel = system.input_channel

        self.seed = None
        self.visual = False
        
        self.spatial = self.system.spatial

        self.chunks = {} 
        self.valid_chunks = {}

        self.height_table = OpenSimplex()
        self.water_table = OpenSimplex()
        self.danger_table = OpenSimplex()
        self.value_table = OpenSimplex()
        self.metal_table = OpenSimplex()
        self.mana_table = OpenSimplex()
        self.noise_table = OpenSimplex()
        
    def get_seed(self):
        return '%s|' % self.seed

    def set_seed(self, value):
        self.seed = value
        self.height_table.set_seed(value)
        self.water_table.set_seed(value+2)
        self.danger_table.set_seed(value+4)
        self.value_table.set_seed(value+6)
        self.metal_table.set_seed(value+8)
        self.mana_table.set_seed(value+10)
        self.noise_table.set_seed(value+12)

    def set_player(self, index):
        self.player = index


    def temp_grad(self, x, y):
        return 60 + (y / 16.0)

    def gen_tile(self, x, y, scale=WORLD_SCALE):
        
        height = self.height_table.smooth_noise2(x, y, 5) - 2  # Base -2 - 3

        danger = self.danger_table.scale_noise2(x, y)
        metal = self.metal_table.scale_noise2(x, y)
        value = self.value_table.scale_noise2(x, y)
        noise = self.noise_table.scale_noise2(x, y)
        
        water_base = self.water_table.scale_noise2(x, y)  # Base 0-1
        water = water_base * 20
        
        mana_base = self.mana_table.scale_noise2(x, y)  # Base 0-1
        mana = mana_base * 10

        temp_base = self.temp_grad(x, y)  # Base 60 +/- dist
        temp = temp_base + water + mana 

        veg_base = (temp / 10.0) + water + mana
        veg = veg_base / 10.0

        block = None
        block_item = None
        if height < -1:
            result = SEA

        elif height < 0:
            result = WATER

        else:
            if height < 1:
                result = SAND
                if value > 0.5:
                    block = SAND

            elif height < 2:
                if temp > 120:
                    result = HELL
                    if value > 0.6:
                        if mana > 0.6 and danger > 0.5:
                            block = BLOODSTONE
                        else:
                            block = STONE
                    elif value > 0.5:
                        block = SAND

                elif temp > 100:
                    result = DESERT
                    if value > 0.9 and mana > 0.6 and danger > 0.5:
                        block = BLOODSTONE
                    elif value > 0.7:
                        block = STONE
                    elif value > 0.5:
                        block = SAND

                elif temp < 0:
                    result = ICE
                    if value > 0.7:
                        if mana > 0.6 and danger < 0.3:
                            block = BLUESTONE
                        else: block = STONE
                    elif value > 0.5:
                        block = DIRT

                elif temp < 30:
                    result = SNOW
                    if value > 0.9 and mana > 0.6 and danger < 0.3:
                        block = BLUESTONE
                    elif value > 0.7:
                        block = STONE
                    elif value > 0.5:
                        block = DIRT

                elif veg > 2:
                    result = GRASS
                    if veg > 3 and value > 0.5:
                        block = GRASS

                else:
                    result = DIRT
                    if value > 0.5:
                        block = DIRT
            else:
                result = STONE
                if height > 4:
                    block = STONE
                elif value > 0.5:
                    block = STONE

            if block == STONE:
                if value > 0.6:
                    if metal > 0.6:
                        if noise > 0.6:
                            if mana > 0.5:
                                block_item = COPPER
                        elif noise < 0.4:
                            block_item = IRON

                    elif metal < 0.4:
                        if noise > 0.6:
                            if mana > 0.6:
                                block_item = SAPPHIRE
                        elif noise < 0.4:
                            if mana > 0.6:
                                block_item = RUBY

                elif value > 0.8:
                    if metal > 0.6:
                        if mana > 0.5:
                            block_item = SILVER

                    elif metal < 0.4:
                        if mana > 0.7:
                            block_item = EMERALD

                else:
                    if metal > 0.6:
                        block_item = GOLD

                    elif metal < 0.4:
                        if mana > 0.7 and temp > 70 and noise > 0.4:
                            block_item = DIAMOND
                        elif mana > 0.5 and temp < 50:
                            block_item = ONXY


        tile = self.system.entity.add_tile(x, y, result, self.visual)
        if block:
            block = self.system.entity.add_block(x, y, block, self.visual)
            if block_item:
                block_item = self.system.entity.add_item(x, y, block_item, self.visual)

        return tile
    
    def pos_hash(self, x, y, size):
        x = int(x / size)
        y = int(y / size)
        return (x, y)

    # Converts coords in the pyglet screen to coords in the tilemap
    def sprite_to_tile(self, x, y):
        return self.pos_hash(x, y, TILE_SIZE)

    # Converts coords in the worldmap to coords in the chunkmap
    def tile_to_chunk(self, x, y):
        return self.pos_hash(x, y, CHUNK_SIZE)

    def get_tile(self, x, y):
        tile = None
        pos = self.tile_to_chunk(x, y)
        if pos in self.chunks:
            tile = self.chunks[pos].get_tile(x, y)
        else:
            tile = self.gen_tile(x, y, tile)

        return tile

    def remove_chunk(self, pos):
        del self.chunks[pos]
        del self.valid_chunks[pos]

    def make_chunk(self, x, y, scale):
        print('World: Generating chunk at %s:%s (%s)' % (x, y, scale))
        pos = (x, y)
        chunk = Chunk(x, y)
        self.chunks[pos] = chunk

        x_min = x * CHUNK_SIZE
        x_max = x_min + CHUNK_SIZE
        y_min = y * CHUNK_SIZE
        y_max = y_min + CHUNK_SIZE


        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                tile = self.gen_tile(x, y, scale)
                chunk.set_tile(x, y, tile)

    def can_move(self, actor, x, y):
        tile = self.get_tile(x, y)
        return actor.can_move(tile)

    def move(self, actor, x, y):
        tile = self.get_tile(actor.x, actor.y)
        tile.block = None

        tile = self.get_tile(x, y)
        tile.block = actor

    def update(self):
        for index in self.items:
            pos = self.spatial.get(index)
            new_chunk = self.tile_to_chunk(pos.x, pos.y)
            old_chunk = self.get(index)

            if new_chunk != old_chunk:
                self.set(index, new_chunk)
                self._update(new_chunk, WORLD_SCALE)


    def _update(self, pos, scale=WORLD_SCALE):
        for xi in range(pos[0] - DRAW_DISTANCE_X, pos[0] + DRAW_DISTANCE_X + 1):
            for yi in range(pos[1] - DRAW_DISTANCE_Y, pos[1] + DRAW_DISTANCE_Y + 1):
                pos = (xi, yi)
                self.valid_chunks[pos] = True
                if pos not in self.chunks:
                    self.make_chunk(xi, yi, WORLD_SCALE)


class WorldThread(World, Thread):
    def __init__(self, system):
        Thread.__init__(self)
        World.__init__(self, system)

        self.clock = Clock(WORLD_UPDATE_RATE)
        self.new_items = {}
        self.old_items = {}

        self.invalid_chunks = {}

    def run(self):
        while True:
            if self.clock.tick():
                self.update()
            time.sleep(0.001)

    def update(self):
        for index in self.new_items:
            self.add(index, self.new_items[index])
        self.new_items = []

        for index in self.old_items:
            self.remove(index)
        self.old_items = []

        for index in self.items:
            x, y = self.spatial.get(index)
            new_chunk = self.tile_to_chunk(x, y)
            old_chunk = self.get(index)

            if new_chunk != old_chunk:
                self.set(index, new_chunk)
                self._update(new_chunk, WORLD_SCALE)

        for pos in self.chunks:
            if pos not in self.valid_chunks:
                self.invalid_chunks[pos] = self.chunks[pos]

        for pos in self.invalid_chunks:
            self.remove_chunk(pos)

        self.invalid_chunks = {}

    def add_item(self, index, pos):
        self.new_items[index] = pos

    def remove_item(self, index):
        self.old_item[index] = True