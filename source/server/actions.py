from manager import Manager

class ActionMan(Manager):
    def __init__(self, game):
        Manager.__init__(self, game)

        actions = (AssignMission(),
                   Challenge(),
                   Combat(),
                   CreateMission(),
                   Equip(),
                   Gift(),
                   JoinConflict(),
                   Talk(),
                   Trade(),
                   ViewActor(),
                   ViewConflict()
                   )

        self.actions = {}
        for action in actions:
            self.actions[action.key] = action

    def get_string(self, action):
        return self.actions[action].string

    def execute(self, action, actor, target):
        return self.actions[action].execute(actor, target)

    def get_interactions(self, actor, target):
        options = {}

        if target.type == 'actor':
            names = '%s %s' % (target.self_name, target.kin_name)
            options['names'] = names

            if actor == target:
                option = self.actions['view_actor']
                options[option.key] = option.string

                option = self.actions['equip']
                options[option.key] = option.string
                return options

            if target.merchant:
                option = self.actions['trade']
                options[option.key] = option.string

            option = self.actions['talk']
            options[option.key] = option.string

            if actor.band == target.band:
                if actor.rank > target.rank:
                    option = self.actions['assign_mission']
                    options[option.key] = option.string

            option = self.actions['gift']
            options[option.key] = option.string

            option = self.actions['challenge']
            options[option.key] = option.string

            option = self.actions['view_actor']
            options[option.key] = option.string

        elif target.type == 'actable':
            options['names'] = 'Conflict'

            option = self.actions['join_conflict']
            options[option.key] = option.string

            option = self.actions['view_conflict']
            options[option.key] = option.string

        return options


class Action:
    def __init__(self, key, string):
        self.key = key
        self.string = string

    def execute(self, actor, target):
        return


class AssignMission(Action):
    def __init__(self):
        Action.__init__(self, 'assign_mission', 'Assign Mission')


class Challenge(Action):
    def __init__(self):
        Action.__init__(self, 'challenge', 'Challenge')


class Combat(Action):
    def __init__(self):
        Action.__init__(self, 'combat', 'Combat')


class CreateMission(Action):
    def __init__(self):
        Action.__init__(self, 'create_mission', 'Create Mission')


class Equip(Action):
    def __init__(self):
        Action.__init__(self, 'equip', 'Equip')


class Gift(Action):
    def __init__(self):
        Action.__init__(self, 'gift', 'Gift')


class JoinConflict(Action):
    def __init__(self):
        Action.__init__(self, 'join_conflict', 'Join')


class Talk(Action):
    def __init__(self):
        Action.__init__(self, 'talk', 'Talk')


class Trade(Action):
    def __init__(self):
        Action.__init__(self, 'trade', 'Trade')


class ViewActor(Action):
    def __init__(self):
        Action.__init__(self, 'view_actor', 'View Actor')


class ViewConflict(Action):
    def __init__(self):
        Action.__init__(self, 'view_conflict', 'View')
