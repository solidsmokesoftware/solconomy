from source.common.opensimplex import OpenSimplex
from source.common.spatialhash import SpatialHash
from source.common.clock import Clock
from source.common.pool import Pool
from source.common.constants import *
from source.common.block import LogicalBlock
from source.common.block import VisualBlock

import source.client.sprites as sprites
import time
import pyglet
from threading import Thread
from random import randint


class Tile:
    def __init__(self):
        self.x = None
        self.y = None
        self.value = None
        self.block = None



class TilePool(Pool):
    def __init__(self, size):
        Pool.__init__(self, size, Tile)


class Chunk:
    def __init__(self, x, y):
        self.pos = x, y
        self.tiles = {}

    def get_tile(self, x, y):
        return self.tiles[(x, y)]

    def set_tile(self, x, y, tile):
        self.tiles[(x, y)] = tile


class World:
    def __init__(self):
        self.seed = None

        self.chunks = {}
        self.valid_chunks = {}

        self.height_table = OpenSimplex()
        self.water_table = OpenSimplex()
        self.danger_table = OpenSimplex()
        self.value_table = OpenSimplex()
        self.metal_table = OpenSimplex()
        self.mana_table = OpenSimplex()
        self.noise_table = OpenSimplex()

        self.spatial = SpatialHash(CHUNK_SIZE)

        self.actors = {}
        self.player_actors = []
        self.new_player_actors = []
        self.old_player_actors = []

    def run(self):
        while True:
            if self.clock.tick():
                self.update()
            time.sleep(0.001)
        
    def get_seed(self):
        return '%s|' % self.seed

    def set_game(self, game):
        self.game = game
        self.input_channel = game.input_channel

    def set_seed(self, value):
        self.seed = value
        self.height_table.set_seed(value)
        self.water_table.set_seed(value+2)
        self.danger_table.set_seed(value+4)
        self.value_table.set_seed(value+6)
        self.metal_table.set_seed(value+8)
        self.mana_table.set_seed(value+10)
        self.noise_table.set_seed(value+12)

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

        tile = Tile()
        tile.x = x
        tile.y = y
        tile.value = result
        tile.block = block
        tile.block_item = block_item

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
            tile = self.gen_tile(x, y)

        return tile

    def remove_chunk(self, pos):
        del self.chunks[pos]
        del self.valid_chunks[pos]

    def make_chunk(self, x, y, scale):
        #print('World: Generating chunk at %s:%s (%s)' % (x, y, scale))
        pos = (x, y)
        chunk = Chunk(x, y)
        self.chunks[pos] = chunk

        x_min = x * CHUNK_SIZE
        x_max = x_min + CHUNK_SIZE
        y_min = y * CHUNK_SIZE
        y_max = y_min + CHUNK_SIZE


        for xi in range(x_min, x_max):
            for yi in range(y_min, y_max):
                tile = self.gen_tile(xi, yi, scale)
                chunk.set_tile(xi, yi, tile)

        self.visualize_chunk(chunk)

    def visualize_chunk(self, chunk):
        return

    def add_actor(self, actor):
        self.actors[actor.index] = actor
        self.spatial.add_key(actor.chunk, actor)

    def remove_actor(self, actor):
        self.spatial.remove_key(actor.chunk, actor)
        del self.actors[actor.index]

    # Actors that the world will generate chunks around during its update process
    def add_player_actor(self, actor):
        self.new_player_actors.append(actor)

    def remove_player_actor(self, actor):
        self.old_player_actors.append(actor)

    def can_move(self, actor, x, y):
        tile = self.get_tile(x, y)
        return actor.can_move(tile)

    def move(self, actor, x, y):
        tile = self.get_tile(actor.x, actor.y)
        tile.block = None

        tile = self.get_tile(x, y)
        tile.block = actor

        actor.set_tile(x, y)


    def get_near_pos(self, x, y, dist=2):
        return self.spatial.get_near(x, y, dist)

    def get_near_chunk(self, x, y, dist=2):
        return self.spatial.get_near_key((x, y), dist)

    def get_near_actor(self, actor, dist=2):
        return self.spatial.get_near_key(actor.chunk, dist)

    def update(self):
        invalid_chunks = {}

        for actor in self.new_player_actors:
            self.player_actors.append(actor)
        self.new_player_actors = []

        for actor in self.old_player_actors:
            self.player_actors.remove(actor)
        self.old_player_actors = []

        for actor in self.player_actors:
            x = actor.x
            y = actor.y
            new_chunk = self.tile_to_chunk(x, y)
            if new_chunk != actor.chunk:
                self.spatial.remove_key(actor.chunk, actor)
                self.spatial.add_key(new_chunk, actor)
                actor.chunk = new_chunk

                self.center_on(actor.chunk, WORLD_SCALE)

        for pos in self.chunks:
            if pos not in self.valid_chunks:
                invalid_chunks[pos] = self.chunks[pos]

        for pos in invalid_chunks:
            self.remove_chunk(pos)

    def center_on(self, pos, scale=WORLD_SCALE):
        for xi in range(pos[0] - DRAW_DISTANCE_X, pos[0] + DRAW_DISTANCE_X + 1):
            for yi in range(pos[1] - DRAW_DISTANCE_Y, pos[1] + DRAW_DISTANCE_Y + 1):
                pos = (xi, yi)
                self.valid_chunks[pos] = True
                if pos not in self.chunks:
                    self.make_chunk(xi, yi, WORLD_SCALE)


class LogicalWorld(World):
    def __init__(self):
        World.__init__(self)

        self.actors = {}
        self.player_actors = []
        self.new_player_actors = []
        self.old_player_actors = []


class WorldServer(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.world = LogicalWorld()
        self.clock = Clock(WORLD_UPDATE_RATE)

    def run(self):
        while True:
            if self.clock.tick():
                self.world.update()
            time.sleep(0.001)

    def set_game(self, game):
        self.world.set_game(game)

    def set_seed(self, seed):
        self.world.set_seed(seed)

    def add_actor(self, actor):
        self.world.add_actor(actor)

    def get_actor(self, index):
        return self.world.actors.get(index)
    
    def add_player_actor(self, actor):
        self.world.add_player_actor(actor)

    def get_seed(self):
        return self.world.get_seed()

    def get_actor_info(index, info):
        return self.world.actors.get_actor_info(index, info)


class VisualWorld(World):
    def __init__(self):
        World.__init__(self)
        
        self.tile_pool = TilePool(50*30)  # TODO figure out actual number of tiles needed for the screen
        self.tiles = {}
        self.actor = None
        self.pos = None

    def set_actor(self, actor):
        self.actor = actor

    def update(self):
        if self.pos != self.actor.pos:
            self.pos = self.actor.pos
            self.center_on(self.pos)

    def center_on(self, position):
        start = position[0] - DRAW_DISTANCE_X, position[1] - DRAW_DISTANCE_Y
        end = position[0] + DRAW_DISTANCE_X, position[1] + DRAW_DISTANCE_Y
        for x in range(start[0], end[0]):
            for y in range(start[1], end[1]):
                self.get_tile(x, y)


    def get_tile(self, x, y):
        pos = x, y
        if pos in self.tiles:
            tile = self.tiles[pos]
        else:
            tile = self.gen_tile(x, y)
            self.tiles[pos] = tile

            tile.sprite = sprites.make_tile(x, y, tile.value)
            if tile.block:
                tile.block = VisualBlock(tile.block, tile.block_item, x, y)

        return tile



