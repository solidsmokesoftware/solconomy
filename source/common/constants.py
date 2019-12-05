
### Server communication constants ###
LOGIN_COM = -1
LOGIN_RES = -101

WORLD_INFO_COM = -2
WORLD_INFO_RES = -102

JOIN_COM = 0
JOIN_RES = 100

POS_UPDATE_COM = 1
POS_UPDATE_RES = 101

ACCEPT_COM = 2
ACCEPT_RES = 102

DECLINE_COM = 3
DECLINE_RES = 103

MESSAGE_COM = 4
MESSAGE_RES = 104

BATTLE_COM = 10
BATTLE_RES = 110

CHALLENGE_COM = 11
CHALLENGE_RES = 111

POS_INFO_COM = 50
POS_INFO_RES = 150

PART_INFO_COM = 51
PART_INFO_RES = 151

FULL_INFO_COM = 152
FULL_INFO_RES = 152

EQUIP_INFO_COM = 153
EQUIP_INFO_RES = 153

IDLE_COM = 99
IDLE_RES = 199

### Internal messaging commands ###
MAKE_TILE_COM = 400
DEL_TILE_COM = 401

MAKE_ACTOR_COM = 402
DEL_ACTOR_COM = 403

MAKE_VAR_COM = 404
DEL_VAR_COM = 405

PING_RATE = 10
CONNECTION_WARN_RATE = 30
TIMEOUT_WARNINGS_TO_KILL = 3
MSG_RATE = 1 #15

### World Constants ###
WORLD_UPDATE_RATE = 1
WORLD_SCALE = 10.0
DRAW_DISTANCE_X = 25  # in chunks
DRAW_DISTANCE_Y = 15  # in chunks
TILE_SIZE = 32  # Pixels
CHUNK_SIZE = 16  # Tiles


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
WINDOW_SIZE_X = 1200
WINDOW_SIZE_Y = 700


### Block Constants ###
BLUESTONE = 0
BLOODSTONE = 1
#SAND = 2  # Aligns with the tilemap constsants
#DIRT = 3
#STONE = 4
#GRASS = 5
OBSID = 6

### Blockitem Constants ###
COPPER = 7
IRON = 8
SILVER = 9
GOLD = 10
SAPPHIRE = 11
RUBY = 12
EMREALD = 13
ONXY = 14
DIAMOND = 15

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

