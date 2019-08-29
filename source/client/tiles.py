from source.common.opensimplex import OpenSimplex
from source.common.spatialhash import SpatialHash
from source.common.clock import Clock
from source.common.message import MessagePool
from source.common.constants import *
import time
import pyglet
from threading import Thread


class Chunk:
    def __init__(self):
        self.tiles = {}

    def get_tile(self, x, y):
        return self.tiles[(x, y)]

    def set_tile(self, x, y, value):
        self.tiles[(x, y)] = value


class Engine(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.host = 'Tile Engine', 0
        self.game = None
        self.input_channel = None

        self.message_pool = MessagePool(16*16*16)

        self.seed = None
        self.x_size = None
        self.y_size = None

        self.actor = None
        self.chunk = None

        self.chunks = {}
        self.valid_chunks = {}
        self.height_table = OpenSimplex()

        self.clock = Clock(WORLD_UPDATE_RATE)

    def run(self):
        while True:
            if self.clock.tick():
                self.update()
            time.sleep(0.001)

    def set_game(self, game):
        self.game = game
        self.input_channel = game.input_channel

    def set_seed(self, value):
        self.seed = value
        self.height_table.set_seed(value)

    def set_world(self, value, x, y):
        self.seed = value
        self.height_table.set_seed(value)
        self.x_size = x
        self.y_size = y

    def set_actor(self, actor):
        self.actor = actor

    def island(self, x, y):
        dist_x = abs(x - self.x_size * 0.5)
        dist_y = abs(y - self.y_size * 0.5)

        if dist_x > dist_y:
            dist = dist_x
        else:
            dist = dist_y

        max_width = self.x_size * 0.5 - 10
        delta = dist / max_width
        gradient = delta * delta

        return gradient

    def gen_tile(self, x, y, scale=WORLD_SCALE):
        height = 1.2
        height += self.height_table.scaled_noise2(x, y, scale, 2, 1.2)
        height -= self.island(x, y)

        if height <= 0:
            value = abyss
        elif height <= 0.2:
            value = water_deep
        elif height <= 0.4:
            value = water
        elif height <= 0.5:
            value = sand_wet
        elif height <= 0.6:
            value = sand

        elif height <= 1.2:
            value = grassland

        elif height <= 1.25:
            value = mountain
        else:
            value = mountain_snow

        return value

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


    def get_tactical_map(self, upper_left, lower_left, upper_right, lower_right):
        return

    def attempt_move(self, actor, x, y):
        results = self.can_move(actor, x, y)
        if results:
            self.move(actor, x, y)
        return results

    def can_move(self, actor, x, y):
        tile = self.get_tile(x, y)
        results = actor.can_move(tile)
        return results

    def move(self, actor, x, y):
        actor.set_tile(x, y)

    def update(self):
        scale = WORLD_SCALE
        self.actor.chunk = self.tile_to_chunk(self.actor.x, self.actor.y)
        if self.chunk != self.actor.chunk:
            self.center_on(self.actor.chunk, scale)
            self.chunk = self.actor.chunk

            invalid_chunks = {}
            for pos in self.chunks:
                if pos not in self.valid_chunks:
                    invalid_chunks[pos] = self.chunks[pos]

            for pos in invalid_chunks:
                self.remove_chunk(pos)

    def center_on(self, position, scale=WORLD_SCALE):
        self.valid_chunks = {}
        for xi in range(position[0] - DRAW_DISTANCE, position[0] + DRAW_DISTANCE + 1):
            for yi in range(position[1] - DRAW_DISTANCE, position[1] + DRAW_DISTANCE + 1):
                pos = (xi, yi)
                self.valid_chunks[pos] = True
                
                if pos not in self.chunks:
                    self.make_chunk(xi, yi, scale)

    def make_chunk(self, x, y, scale):
        print('World: Generating chunk at %s:%s (%s)' % (x, y, scale))
        pos = (x, y)
        chunk = Chunk()
        self.chunks[pos] = chunk

        x_min = x * CHUNK_SIZE
        x_max = x_min + CHUNK_SIZE
        y_min = y * CHUNK_SIZE
        y_max = y_min + CHUNK_SIZE

        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                value = self.gen_tile(x, y, scale)
                chunk.set_tile(x, y, value)
                message = self.message_pool.get(0, MAKE_TILE_COM, (x, y, value), self.host)
                self.input_channel.give(message, 'game')

                if x % 16 == 0 and y % 16 == 0:
                    print('%s:%s = %s' % (x, y, value))

    def remove_chunk(self, pos):
        chunk = self.chunks[pos]
        del self.chunks[pos]

        for pos in chunk.tiles:
            message = self.message_pool.get(0, DEL_TILE_COM, pos, self.host)
            self.input_channel.give(message, 'game')
