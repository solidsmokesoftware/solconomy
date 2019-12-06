from source.common.constants import *


class Player:
    def __init__(self, host, actor):
        self.host = host
        self.actor = actor
        self.index = actor.index
        self.nearby_actors = {}

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

