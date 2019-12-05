from source.server.game import Game
from source.common.network import Server


game = Game()
server = Server('localhost', 45460, game)

game.start()
server.start()
