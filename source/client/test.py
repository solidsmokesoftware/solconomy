import pyglet
from pyglet.gl import *


from source.client.events import EventHandler
from source.client.camera import Camera
from source.common.world import World
from source.common.actors import VisualActor as Actor
from source.common.constants import *

window = pyglet.window.Window(500, 500)
batch = pyglet.graphics.Batch()
tileGroup = pyglet.graphics.OrderedGroup(0)
actorGroup = pyglet.graphics.OrderedGroup(1)
menuGroup = pyglet.graphics.OrderedGroup(2)

camera = Camera()

pyglet.resource.path = ['assets/chars', 'assets/tiles']
pyglet.resource.reindex()

cloak_image = pyglet.resource.image('shadow_brown.png')
shadow_image = pyglet.resource.image('shadow.png')

shadow_sprite = pyglet.sprite.Sprite(shadow_image, x=50, y=50, batch=batch, group=actorGroup)
cloak_sprite = pyglet.sprite.Sprite(cloak_image, x=150, y=150, batch=batch, group=actorGroup)

actor = Actor(0, 50, 50, shadow_sprite)
other = Actor(1, 150, 150, cloak_sprite)

world = VisualWorld(1001, 100, 100, batch, tileGroup, actorGroup)
world.add_actor(actor)
world.add_actor(other)
world.add_player_actor(actor)
#world.start()

'''
tile_images = []
for i in range(TILE_COUNT):
            path = 'sprite_%s.png' % i
            print(path)
            image = pyglet.resource.image(path)
            tile_images.append(image)

def get_tile_sprite(x, y, index):
    sprite = pyglet.sprite.Sprite(tile_images[index], x=x, y=y, batch=batch, group=tileGroup)
    return sprite

ts = get_tile_sprite(50, 50, sand)
'''

world.update()



events = EventHandler(actor, camera, window, batch)
events.start()

pyglet.app.run()




