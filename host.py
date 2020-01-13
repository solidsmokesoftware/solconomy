
from source.server.server import Server


server = Server('localhost', 65535, b"join")
server.start()
