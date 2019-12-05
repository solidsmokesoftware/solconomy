from source.server.game import Game
from source.common.network import Server


game = Game()
server = Server('localhost', 65535, game)

game.start()
server.start()
