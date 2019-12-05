from source.common.manager import Manager
from source.common.constants import *


class Player:
    def __init__(self, host, actor, message_pool):
        self.host = host
        self.actor = actor
        self.index = actor.index
        self.nearby_actors = {}
        self.message_pool = message_pool

    def get_changes(self, actors):
        results = ''
        for actor in actors:
            results += actor.get_state()
        return results[0:-1]

    def __get_changes(self, actors):  # Testing
        results = self.actor.get_state()
        for actor in actors:
            state = actor.get_state()
            if actor in self.nearby_actors:
                old_state = self.nearby_actors[actor]
                if state != old_state:
                    results += state
                    self.nearby_actors[actor] = state

            else:
                results += state
                self.nearby_actors[actor] = state

        return results[0:-1]


class PlayerMan(Manager):
    def __init__(self, game):
        Manager.__init__(self)
        self.game = game

    def add(self, host, actor, message_pool):
        self.items[host] = Player(host, actor, message_pool)

    def update(self):
        for host in self.items:
            player = self.items[host]

            nearby = self.game.world.get_nearby(player.actor)
            changes = player.get_changes(nearby)

            message = player.message_pool.get(self.game.clock.get_value(), POS_UPDATE_RES, changes, player.host)
            self.game.send(message)