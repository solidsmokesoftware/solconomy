from source.common.constants import *

class ClientInput:
    def __init__(self, system):
        self.system = system

        self.network = system.network
        self.input_channel = system.input_channel
        self.output_channel = system.output_channel

        self.world = system.world


        self.options = {LOGIN_RES: self.handle_login,
                        WORLD_INFO_RES: self.handle_world_info,
                        JOIN_RES: self.handle_join,
                        POS_UPDATE_RES: self.handle_pos_update,
                        ACCEPT_RES: self.handle_accept,
                        DECLINE_RES: self.handle_decline,
                        MESSAGE_RES: self.handle_player_message,
                        BATTLE_RES: self.handle_battle,
                        CHALLENGE_RES: self.handle_challenge,
                        POS_INFO_RES: self.handle_pos_info,
                        PART_INFO_RES: self.handle_part_info,
                        FULL_INFO_RES: self.handle_full_info,
                        EQUIP_INFO_RES: self.handle_equip_info,
                        IDLE_RES: self.handle_idle,

                        MAKE_ACTOR_COM: self.handle_make_actor,
                        DEL_ACTOR_COM: self.handle_del_actor
                        }


    def set_host(self, username, password, address, port):
        self.username = username
        self.password = password
        self.address = address
        self.port = port
        self.host = address, port

        self.network.set_host(address, port)


    def set_actor(self, actor):
        self.actor = actor
        #self.player.actor = actor
        self.player_input.actor = actor


    def handle_input(self, delta):
        #print('Handling input')
        messages = self.input_channel.get('game')
        for message in messages:
            self.handle_message(message)

    def handle_message(self, message):
        results = self.options[message.command](message)
        #print('Game: handling message %s' % message.command)
        return results

    def handle_pos_update(self, message):
        print(message.value)

        for value in message.value:
            actor_index = int(value[0][0])
            x = int(value[1][0])
            y = int(value[1][1])
            pos = x * tile_size, y * tile_size
            self.close_actors.append([actor_index, pos])

            if actor_index in self.world.actors.items:
                if actor_index == self.player.index:
                    pass
                else:
                    actor = self.world.actors[actor_index]
                    self.world.actors.move(actor, x, y)
            else:
                actor = self.world.actors.recreate(actor_index, 'Orc', ('unknown', 'unknown'), x, y)

    def handle_join(self, message):
        print('Game: handling join called %s' % message.value)
        value = message.value
        index = int(value[0][0][0])
        x = int(value[0][1][0]) * TILE_SIZE
        y = int(value[0][1][1]) * TILE_SIZE

        pyglet.clock.schedule_interval(self.update_server, 1.0 / MSG_RATE)
        self.camera.focus_on(self.actor)
        self.player_input.start()

    def handle_bad_message(self, message):
        return

    def handle_world_info(self, message):
        print('Game: Generating world from message')
        value = message.value
        seed = int(value[0][0][0])
        token = int(value[1][0][0])

        print('Game World seed')
        self.world.set_seed(seed)

        self.network.login_server(self.username, self.password)

    def handle_login(self, message):
        print('Game: Logging into server')
        value = message.value
        index = int(value[0][0][0])
        x = int(value[0][1][0])
        y = int(value[0][1][1])

        image = sprites.make_image('soul.png')
        sprite = sprites.make_actor(image, x, y)
        actor = VisualActor(index, x, y, sprite)
        self.set_actor(actor)

        host = self.network.connection.host
        pool = self.network.connection.message_pool
        self.player = Player(host, self.actor, pool)
        
        self.world.set_actor(self.actor)
        self.world.update()

        self.network.join_server(self.username, self.password)

    def handle_accept(self, message):
        return

    def handle_decline(self, message):
        return

    def handle_player_message(self, message):
        return

    def handle_battle(self, message):
        value = message.value
        print(value)

    def handle_challenge(self, message):
        value = message.value
        print(value)

    def handle_pos_info(self, message):
        value = message.value
        print(value)

    def handle_part_info(self, message):
        value = message.value
        print(value)

    def handle_equip_info(self, message):
        value = message.value
        print(value)

    def handle_full_info(self, message):
        value = message.value
        print(value)

        index = value[0][0][0]
        full_name = value[0][1][0]
        subrace = value[0][2][0]
        warband = value[0][3][0]
        rank = value[0][3][1]
        level = value[0][4][0]
        x = value[0][5][0]
        y = value[0][5][1]
        hp = value[0][6][0]
        hp_max = value[0][6][1]
        values = [full_name, level, subrace, rank, warband, hp, hp_max]
        value = '%s\n%s, %s\n%s, %s\n%s/%s' % values
        player.view(value)

    def handle_idle(self, message):
        value = message.value
        print(value)

    def handle_make_actor(self, message):
        value = message.value
        print(value)

    def handle_del_actor(self, message):
        value = message.value
        print(value)

    def update_server(self, delta):
        print('Game: Updating server')
        state = self.actor.get_state()
        message = self.network.message(POS_UPDATE_COM, state)
        self.output_channel.give(message, 'server')


