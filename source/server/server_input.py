from source.common.constants import *


class ServerInput:
    def __init__(self, system):
        self.system = system

        self.input_channel = system.input_channel
        self.output_channel = system.output_channel

        self.players = system.data['players']
        self.world = system.world

        self.options = {LOGIN_COM: self.handle_login,
                        WORLD_INFO_COM: self.handle_world_info,
                        JOIN_COM: self.handle_join,
                        POS_UPDATE_COM: self.handle_pos_update,
                        ACCEPT_COM: self.handle_accept,
                        DECLINE_COM: self.handle_decline,
                        MESSAGE_COM: self.handle_player_message,
                        BATTLE_COM: self.handle_battle,
                        CHALLENGE_COM: self.handle_challenge,
                        POS_INFO_COM: self.handle_pos_info,
                        PART_INFO_COM: self.handle_part_info,
                        FULL_INFO_COM: self.handle_full_info,
                        EQUIP_INFO_COM: self.handle_equip_info,
                        IDLE_COM: self.handle_idle
                        }

    def run(self):
        self.handle_input()

    def handle_input(self):
        messages = self.input_channel.get('game')
        for message in messages:
            self.options[message.command](message)

    def handle_player_pos_update(self, message):
        player = self.players.get(message.host)
        button = int(message.value[0][0][0])
        x = int(message.value[0][1][0])
        y = int(message.value[0][1][1])

        actor = player.actor
        actor.update_pos(x, y)

    def handle_pos_update(self, message):
        index = int(message.value[0][0][0])
        x = int(message.value[0][1][0])
        y = int(message.value[0][1][1])

        actor = self.world.get_actor(index)
        actor.set_tile(x, y)

    def handle_join(self, message):
        # TODO create an actor for the player on join
        username = message.value[0][0][0]
        password = message.value[0][1][0]

        random.seed(message.host_name)
        index = random.randint(0, sys.maxsize)

        actor = Actor(0, 0, 0)
        self.world.add_actor(actor)
        self.world.add_player_actor(actor)

        message.update(0, JOIN_RES, '0:0#0', message.host)
        self.send(message)

    def handle_world_info(self, message):
        value = '%s%s|' % (self.world.get_seed(), random.randint(0, sys.maxsize))
        message.update(-1, WORLD_INFO_RES, value, message.host)
        self.send(message)

    def handle_login(self, message):
        username = message.value[0][0][0]
        password = message.value[0][1][0]

        # TODO log the player in if they have an account and retrive their character list

        random.seed(message.host_name)
        index = random.randint(0, sys.maxsize)



        #value = '%s:%s#%s' % (index, x, y)
        value = '0:0#0'

        message.update(-2, LOGIN_RES, value, message.host)
        self.send(message)

    def handle_player_message(self, message):
        return

    def handle_battle(self, message):
        return

    def handle_challenge(self, message):
        return

    def handle_accept(self, message):
        return

    def handle_decline(self, message):
        return

    def handle_pos_info(self, message):
        return

    def handle_part_info(self, message):
        return

    def handle_full_info(self, message):
        return

    def handle_equip_info(self, message):
        return

    def handle_idle(self, message):
        return        

    def send(self, message):
        self.output_channel.give(message, message.host)

    def handle_get_actors(self, message):
        return message

    def handle_get_actor_info(self, message):
        value = message.value
        index = int(value[0][0][0])
        info = int(value[0][1][0])

        message.value = '%s' % self.world.get_actor_info(index, info)
        message.command = info

        print('Game: Get actor: %s' % message.value)
        self.send(message)

