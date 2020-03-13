
from source.opensimplex import OpenSimplex
from source.constants import *

from random import randint


class Builder:
   def __init__(self):
      self.seed = None
      self.height_table = OpenSimplex()
      self.water_table = OpenSimplex()
      self.danger_table = OpenSimplex()
      self.value_table = OpenSimplex()
      self.metal_table = OpenSimplex()
      self.mana_table = OpenSimplex()
      self.noise_table = OpenSimplex()

   def set_seed(self, seed):
      self.seed = seed
      self.height_table.set_seed(seed)
      self.water_table.set_seed(seed+2)
      self.value_table.set_seed(seed+6)
      self.metal_table.set_seed(seed+8)
      self.mana_table.set_seed(seed+10)
      self.noise_table.set_seed(seed+12)

   def temp_grad(self, x, y):
      return 60 + (y / 16.0)

   def get(self, x, y, scale=WORLD_SCALE):
      #print(f"Generating tile {x}:{y}")
        
      height = self.height_table.smooth_noise2(x, y, 5) - 2  # Base -2 - 3
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

      return (x*(TILE_SIZE-1), y*(TILE_SIZE-1), result, block, block_item)


class World:
   def __init__(self):
      self.seed = None
      self.builder = Builder()
      self.spatial = {}

   def start(self, seed):
      self.seed = seed
      self.builder.set_seed(seed)
   
   def build(self, zone, scale=WORLD_SCALE):
      if zone in self.spatial:
         return False
      else:
         #print(f"World: Generating chunk at {zone[0]}:{zone[1]} ({scale})")
         chunk = []

         x_min = zone[0] * CHUNK_SIZE
         x_max = x_min + CHUNK_SIZE
         y_min = zone[1] * CHUNK_SIZE
         y_max = y_min + CHUNK_SIZE

         for xi in range(x_min, x_max):
            for yi in range(y_min, y_max):
               tile = self.builder.get(xi, yi, scale)
               chunk.append(tile)

         self.spatial[zone] = chunk
         return chunk

   def get(self, zone):
      if zone in self.spatial:
         return self.spatial[zone]
      else:
         chunk = self.build(zone)
         self.spatial[zone] = chunk
         return chunk


