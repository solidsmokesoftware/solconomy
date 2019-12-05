import pyglet
from pyglet.window import key
from source.system.system import Process
from source.common.constants import *



class PlayerInput(Process):
    def __init__(self, system):
        Process.__init__(self, system)
        self.world = system.world

        self.actor = system.actor
        self.selection = system.selection
        self.camera = system.camera
        self.window = system.visual.window
        self.batch = system.visual.batch


    def update(self, delta):
        return

    def move(self, direction):
        x = self.actor.x + direction[0]
        y = self.actor.y + direction[1]

        tile = self.world.get_tile(x, y)
        if tile.block:
            self.selection.set_tile(x, y)
            self.selection.show_green()
            self.selection.target = tile

        elif self.actor.can_move(tile):
            if self.selection.target:
                self.selection.hide()
                self.selection.target = None

            self.actor.set_tile(x, y)
            self.camera.scroll(direction[0]*31, direction[1]*31)
            self.world.center_on(self.actor.pos)

    def harvest(self, tile):
        if tile.block:
            self.actor.give(tile.block.value)
            tile.block.delete()
            tile.block = None

        self.selection.hide()
        print(self.actor.inventory)

    def push(self, tile, direction):
        x = tile.x + direction[0]
        y = tile.y + direction[1]
        dest = self.world.get_tile(x, y)
        if not dest.block:
            self.world.move(tile.block, x, y)

    def on_key_press(self, symbol, modifiers):
        print('EH key press')
   
        if symbol == key.W:
            self.move(UP)
        elif symbol == key.A:
            self.move(LEFT)
        elif symbol == key.S:
            self.move(DOWN)
        elif symbol == key.D:
            self.move(RIGHT)

        if self.selection.target:
            if symbol == key.SPACE:
                if self.selection.target.block.type == 'Block':
                    self.harvest(self.selection.target)

            elif symbol == key.I:
                self.push(self.selection.target, UP)
            elif symbol == key.J:
                self.push(self.selection.target, LEFT)
            elif symbol == key.K:
                self.push(self.selection.target, DOWN)
            elif symbol == key.L:
                self.push(self.selection.target, RIGHT)


        if symbol == key.I:
            print(self.actor.inventory)

    def on_key_release(self, symbol, modifiers):
        print('EH key release')
       
    def on_mouse_press(self, x, y, button, modifiers):
        print(x, y, button, modifiers)

    def start(self):
        print('EH starting')
        self.window.push_handlers(self.on_key_press, self.on_key_release, self.on_mouse_press)
        pyglet.clock.schedule_interval(self.update, 1 / 30.0)
