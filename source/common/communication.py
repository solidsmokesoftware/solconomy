
from source.common.constants import *

# PLAYER_IDENT = "0"
# PLAYER_POS = "1"
# PLAYER_BLOCK = "2"
# PLAYER_MSG = "3"
# PLAYER_ACTION = "4"

# SERVER_IDENT = "100"
# SERVER_POS = "101"
# SERVER_PING = "102"
# SERVER_LEVEL = "103"
# SERVER_BLOCK = "104"
# SERVER_NEW_ACTOR = "105"
# SERVER_DEL_ACTOR = "106"
# SERVER_MSG = "107"
# SERVER_KICK = "108" 


class Parser:
   def __init__(self):
      self.sep = [b"/", b":", b"-"]

   def encode(self, command, data, time):
      return f"{data}/{command}/{time}".encode()

   def decode(self, data):
      return data.split(self.sep[0])

   def player_pos(self, data):
      data = data.split(self.sep[0])
      data[0] = data.split(self.sep[1])
      return data