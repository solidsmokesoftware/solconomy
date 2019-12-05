from source.common.manager import Manager

class Battle:
	def __init__(self):
		return


class BattleMan(Manager):
	def __init__(self, game):
		Manager.__init__(self)
		self.game = game

	def update(self):
		for battle in self.items:
			pass