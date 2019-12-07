import source.client.sprites as sprites
from source.common.constants import *

class Object:
   def __init__(self, index, x, y):
      self.type = 'Object'
      self.index = index
      self.x = x
      self.y = y
      self.pos = x, y
      
   def get_state(self):
      #TODO delimit index and pos with / to let handlers grab index with first parse. Maybe no pos parse since not sending multiples
      return f"{self.index}:{self.x}:{self.y}"

   def set_tile(self, x, y):
      self.x = x
      self.y = y
      self.set_pos(x, y)

   def move(self, x, y):
      self.x += x
      self.y += y
      self.set_pos(self.x, self.y)

   def set_pos(self, x, y):
      self.pos = x, y


class VisualObject(Object):
   def __init__(self, index, x, y, sprite):
      Object.__init__(self, index, x, y)
      self.type = 'Visual Object'
      self.sprite = sprite
      self.image = sprite.image

   def set_pos(self, x, y):
      self.pos = x, y
      self.sprite.position = x * 31, y * 31

   def hide(self):
      self.sprite.image = sprites.blank_image

   def show(self):
      self.sprite.image = self.image

   def set_image(self, image):
      self.image = image
      self.sprite.image = image

   def delete(self):
      self.sprite.delete()
      self.sprite = None
      self.image = None


class Selection(VisualObject):
   def __init__(self):
      sprite = sprites.make_menu(sprites.blank_image, 0, 0)
      VisualObject.__init__(self, -1, 0, 0, sprite)

      self.target = None

   def hide(self):
      self.sprite.image = sprites.blank_image
      self.target = None

   def show_green(self):
      self.set_image(sprites.green_circle)

   def show_red(self):
      self.set_image(sprites.red_circle)
