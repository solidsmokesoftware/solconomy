
### Communication Protocol constants ###
PLAYER_IDENT = "0"
PLAYER_POS = "1"
PLAYER_DELETE = "2"
PLAYER_MSG = "3"

SERVER_IDENT = "50"
SERVER_POS = "51"
SERVER_PING = "52"
SERVER_NEW_ACTOR = "55"
SERVER_DEL_ACTOR = "56"
SERVER_MSG = "57"
SERVER_KICK = "58"




### Object keys ###
TILE = 0
BLOCK = 1
ACTOR = 2
ITEM = 3



PING_RATE = 10
CONNECTION_WARN_RATE = 30
TIMEOUT_WARNINGS_TO_KILL = 3
MSG_RATE = 1.0 / 60.0

### World Constants ###
WORLD_UPDATE_RATE = 1
WORLD_SCALE = 10.0
DRAW_DISTANCE_X = 25  # in chunks
DRAW_DISTANCE_Y = 15  # in chunks
TILE_SIZE = 32  # Pixels
CHUNK_SIZE = 8  # Tiles
ZONE_SIZE = TILE_SIZE * CHUNK_SIZE
SMALL_NUMBER = 0.0001


### Input Constants ###
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

up_key = 1 << 0
down_key = 1 << 1
left_key = 1 << 2
right_key = 1 << 3
shift_key = 1 << 4
ctrl_key = 1 << 5

accept_key = 1 << 0
select_key = 1 << 1
r_key = 1 << 2
f_key = 1 << 3
q_key = 1 << 4
e_key = 1 << 5
z_key = 1 << 6
tab_key = 1 << 7
esc_key = 1 << 8


### Screen Constants ###
WINDOW_SIZE_X = 600 #1200
WINDOW_SIZE_Y = 600 #700


### Block Constants ###
BLUESTONE = 0
BLOODSTONE = 1
#SAND = 2  # Aligns with the tilemap constsants
#DIRT = 3
#STONE = 4
#GRASS = 5
OBSID = 6

### Blockitem Constants ###
COPPER = 0
IRON = 1
SILVER = 2
GOLD = 3
SAPPHIRE = 4
RUBY = 5
EMREALD = 6
ONXY = 7
DIAMOND = 8

### Tilemap Constants ###
SEA = 0
WATER = 1
SAND = 2
DIRT = 3
STONE = 4
GRASS = 5
SNOW = 6
ICE = 7
DESERT = 8
HELL = 9



BLOCK_COUNT = 7
BLOCK_ITEM_COUNT = 9
TILE_COUNT = 10

