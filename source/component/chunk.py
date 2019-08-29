

class Chunk:
    def __init__(self, x, y):
        self.tiles = {}

    def get_tile(self, x, y):
        return self.tiles[(x, y)]

    def set_tile(self, x, y, tile):
        self.tiles[(x, y)] = tile