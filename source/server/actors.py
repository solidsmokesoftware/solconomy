from sharing import *
from manager import Manager
import words
import random


class ActorMan(Manager):
    def __init__(self, world):
        Manager.__init__(self)
        self.world = world
        self.actor_list = []
        self.npc_list = []
        self.index = 0

        races = (Dragon,
                 Dragonling,
                 Dray,
                 Gritling,
                 Kobold,
                 Lizardman,
                 CaveElf,
                 Elf,
                 HighElf,
                 WoodElf,
                 Dwarf,
                 Barbarian,
                 CommonHuman,
                 HalfElf,
                 Halfling,
                 NobelHuman,
                 CaveTroll,
                 Cyclopse,
                 Goblin,
                 Gnome,
                 Grel,
                 Grimlin,
                 HalfOrc,
                 Ogre,
                 Orc,
                 SnowTroll,
                 StoneTroll,
                 Troll)

        self.races = {}
        for race in races:
            self.races[race(0).subrace] = race

        self.langs = words.Manager()


    def get_actors(self):
        return self.actor_list

    def get_npcs(self):
        return self.npc_list

    def get_actor_info(self, index, info):
        actor = self.get(index)
        results = actor.get_info(info)
        return results

    def update(self):
        for key in self.items:
            actor = self.items[key]
            if actor.chunk_pos in self.world.chunks:
                self.update_actor(actor)
            else:
                self.simulate_actor_update(actor)

    def update_actor(self, actor):
        if actor.has_input:
            x = actor.x_input
            y = actor.y_input
            self.move(actor, x, y)
            actor.has_input = False

    def simulate_actor_update(self, actor):
        return

    def move(self, actor, x, y):
        self.world.attempt_move(x, y, actor)
        #move =
        #results = (actor, x, y, moved)
        #print('Game: Moving actor %s to %s:%s - %s' % results)

    def spawn(self, subrace):
        actor = self.races[subrace](self.index)

        lang = actor.get_lang()
        names = self.langs.get_names(lang)
        actor.set_names(names)

        invalid_location = True
        while invalid_location:
            x = random.randint(0, self.world.x - 1)
            y = random.randint(0, self.world.y - 1)
            tile = self.world.gen_tile(x, y)
            results = actor.can_walk(tile)

            invalid_location = not results

        actor.set_pos(x, y)

        actor.update_hash()
        actor.tile = tile.value
        self.world.hashmap.add_key(actor.get_hash(), actor)

        self.add(actor, self.index)
        self.actor_list.append(actor)
        self.npc_list.append(actor)

        self.index += 1

        return actor



class Actor:
    def __init__(self, index):
        self.type = 'actor'
        self.index = index
        self.self_name = 'None'
        self.kin_name = 'None'
        self.full_name = 'None None'
        self.actor = self

        self.arm = 5
        self.hand = 5
        self.leg = 5
        self.chest = 5
        self.head = 5
        self.soul = 5

        self.arm_training = 0
        self.hand_training = 0
        self.leg_training = 0
        self.chest_training = 0
        self.head_training = 0

        self.meat_max = 10
        self.blood_max = 10
        self.bone_max = 10
        self.mana_max = 0

        self.meat = 10
        self.blood = 10
        self.bone = 10
        self.mana = 0

        self.wounds = []

        self.rank = 0
        self.level = 1
        self.level_mod = 1
        self.ep = 0
        self.ep_to_next = 100

        self.langs = {'Gobish': 0, 'Himan': 0, 'Loma': 0, 'Dwarish': 0, 'Elvish': 0, 'Dragonish':0}
        self.race = 'none'
        self.subrace = 'none'
        self.band = 'none'
        self.hostility = {}
        self.friendly = {}

        self.merchant = False
        self.can_act = True
        self.talking = False
        self.targets = []
        self.target = None

        self.x = 0
        self.y = 0
        self.pos = 0, 0

        self.chunk_x = 0
        self.chunk_y = 0
        self.chunk_pos = 0, 0

        self.x_input = 0
        self.y_input = 0
        self.has_input = False



        self.hash = (0, 0)
        self.tile = ''
        self.movement_types = [sand_wet, sand, swamp, snow, brushland, grassland, desert]

    def update_input(self, message):
        self.x_input = message.values['x']
        self.y_input = message.values['y']
        self.has_input = True


    def update_pos(self, x, y):
        self.x_input = x
        self.y_input = y
        self.has_input = True


    def can_walk(self, tile):
        results = False
        if tile.move_req in self.movement_types:
            results = True
        #    else:
        #        print('Tile occupied')
        #else:
        #    print('Cant walk on %s' % tile.value)
        return results

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.pos = x, y
        self.chunk_x = int(x / 32)
        self.chunk_y = int(y / 32)
        self.chunk_pos = self.chunk_x, self.chunk_y
        self.x_input = x
        self.y_input = y
        self.has_input = False

    def get_pos(self):
        return '%s#%s' % (self.x, self.y)

    def get_chunk(self):
        return '%s#%s' % (self.chunk_x, self.chunk_y)

    def get_state(self):
        return '%s:%s|' % (self.index, self.get_pos())

    def get_new_hash(self):
        x = int(self.x / hash_cell_size)
        y = int(self.y / hash_cell_size)

        return x, y

    def get_hash(self):
        return self.hash

    def hash_changed(self):
        results = False
        new_hash = self.get_new_hash()
        if new_hash != self.hash:
            results = True

        return results

    def update_hash(self):
        self.hash = self.get_new_hash()

    def set_names(self, names):
        self.self_name = names[0]
        self.kin_name = names[1]
        self.full_name = '%s %s' % (names[0], names[1])

    def get_lang(self):
        best_lang = None
        best_value = 0
        for key in self.langs:
            if self.langs[key] > best_value:
                best_lang = key
                best_value = self.langs[key]
        return best_lang

    def get_level_mod(self):
        value = 1
        if self.level > 1:
            level_re = 1 / self.level
            level_mod = 1 - level_re
            value += level_mod
        return value

    def get_hp(self):
        if self.blood > self.blood_max / 2:
            value_mod = 2
        else:
            value_mod = 1
        blood_value = self.blood * value_mod
        blood_value_max = self.blood_max * 2

        if self.bone > self.bone_max / 2:
            value_mod = 2
        else:
            value_mod = 1
        bone_value = self.bone * value_mod
        bone_value_max = self.bone_max * 2

        if self.meat > self.meat_max / 2:
            value_mod = 3
        else:
            value_mod = 2
        meat_value = self.meat * value_mod
        meat_value_max = self.meat_max * 3

        total = meat_value + bone_value + blood_value
        total_max = meat_value_max + bone_value_max + blood_value_max

        results = '%s#%s' % (total, total_max)
        return results

    def get_ranking(self):
        return '%s#%s:%s' % (self.band, self.rank, self.level)

    def get_info(self, detail):
        results = None
        if detail == POS_INFO_REQUEST:
            results = '%s:%s' % (self.index, self.get_pos())

        elif detail == PART_INFO_REQUEST:
            results = '%s:%s:%s' % (self.index, self.full_name, self.subrace)

        elif detail == EQUIP_INFO_REQUEST:
            results = '%s:%s' % (self.index, self.full_name)

        elif detail == FULL_INFO_REQUEST:
            full_info = (self.index, self.full_name, self.subrace, self.get_ranking(), self.get_pos(),
                         self.get_hp())
            results = '%s:%s:%s:%s:%s:%s' % full_info

        return results


### Dragons ###
class Dragon(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Dragon'
        self.subrace = 'Dragon'
        self.langs['Dragonish'] = 2


class Dragonling(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Dragon'
        self.subrace = 'Dragonling'
        self.langs['Dragonish'] = 2
        self.langs['Elvish'] = 2
        self.langs['Dwarish'] = 2
        self.langs['Himan'] = 2

### Dragonoids ###
class Dray(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Dragonoid'
        self.subrace = 'Dray'
        self.langs['Gobish'] = 2
        self.langs['Dragonish'] = 1


class Gritling(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Dragonoid'
        self.subrace = 'Gritling'
        self.langs['Gobish'] = 1
        self.langs['Dragonish'] = 1


class Kobold(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Dragonoid'
        self.subrace = 'Kobold'
        self.langs['Gobish'] = 2
        self.langs['Dragonish'] = 1


class Lizardman(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Dragonoid'
        self.subrace = 'Lizardman'
        self.langs['Loman'] = 2
        self.langs['Dragonish'] = 1

### Elves ###
class CaveElf(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Elf'
        self.subrace = 'Cave Elf'
        self.langs['Elvish'] = 2
        self.langs['Gobish'] = 1


class Elf(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Elf'
        self.subrace = 'Elf'
        self.langs['Elvish'] = 2


class HighElf(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Elf'
        self.subrace = 'High Elf'
        self.langs['Elvish'] = 2
        self.langs['Himan'] = 1
        self.langs['Loman'] = 1


class WoodElf(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Elf'
        self.subrace = 'Wood Elf'
        self.langs['Elvish'] = 2

### Dwarves ###
class Dwarf(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Dwarf'
        self.subrace = 'Dwarf'
        self.langs['Dwarish'] = 2
        self.langs['Himan'] = 1

### Humans ##
class Barbarian(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Human'
        self.subrace = 'Barbarian'
        self.langs['Loman'] = 2


class CommonHuman(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Human'
        self.subrace = 'Commoner'
        self.langs['Loman'] = 2


class HalfElf(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Humanoid'
        self.subrace = 'Half-Elf'
        self.langs['Loman'] = 2
        self.langs['Elvish'] = 1


class Halfling(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Humanoid'
        self.subrace = 'Halfling'
        self.langs['Loman'] = 2
        self.langs['Dwarish'] = 1
        self.langs['Gobish'] = 1


class NobelHuman(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Human'
        self.subrace = 'Nobelman'
        self.langs['Himan'] = 2
        self.langs['Elvish'] = 1
        self.langs['Loman'] = 1


### Goblinoids ###
class CaveTroll(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Goblinoid'
        self.subrace = 'Cave Troll'
        self.langs['Gobish'] = 2
        self.langs['Elvish'] = 1


class Cyclopse(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Goblinoid'
        self.subrace = 'Cyclopse'
        self.langs['Gobish'] = 2
        self.langs['Elvish'] = 1


class Goblin(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Goblinoid'
        self.subrace = 'Goblin'
        self.langs['Gobish'] = 2


class Gnome(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Humanoid'
        self.subrace = 'Gnome'
        self.langs['Dwarish'] = 2
        self.langs['Gobish'] = 2
        self.langs['Loman'] = 1


class Grel(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Goblinoid'
        self.subrace = 'Grel'
        self.langs['Gobish'] = 2


class Grimlin(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Goblinoid'
        self.subrace = 'Grimlin'
        self.langs['Gobish'] = 2


class HalfOrc(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Goblinoid'
        self.subrace = 'Half-Orc'
        self.langs['Gobish'] = 2
        self.langs['Loman'] = 1


class Ogre(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Goblinoid'
        self.subrace = 'Ogre'
        self.langs['Gobish'] = 2


class Orc(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Goblinoid'
        self.subrace = 'Orc'
        self.langs['Gobish'] = 2


class SnowTroll(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Goblinoid'
        self.subrace = 'Snow Troll'
        self.langs['Gobish'] = 2
        self.langs['Elvish'] = 1


class StoneTroll(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Goblinoid'
        self.subrace = 'Stone Troll'
        self.langs['Gobish'] = 2
        self.langs['Elvish'] = 1


class Troll(Actor):
    def __init__(self, index):
        Actor.__init__(self, index)
        self.race = 'Goblinoid'
        self.subrace = 'Troll'
        self.langs['Gobish'] = 2
        self.langs['Elvish'] = 1


