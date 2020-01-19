![Image](https://i.imgur.com/Vbwgvd7.png)

# Solconomy
A very incomplete "game" written in Python with [Pyglet](http://pyglet.org/). The main purpose of this is to serve as an example of using [pysics](https://github.com/solidsmokesoftware/pysics).

Currently the entire tilemap is being simulated by pysics. This is not a very efficent way of doing things but it show what the system can handle

Animation is breaking, need to fix that

## Features:

* Multiplayer with dedicated server and clients.
* Explore Infinite procedurally generated world
* Destroying blocks and teleportation
* Movement and collision in a physics simulation
* Object-oriented entity management system
* Multi-threaded network layer
* Spatial Hash for entity occlusion
* 4-way animated movement

#### Coming Soon:

* Effect processing
* UDP reliability layer

## Instructions:

1. Run host.py to start the server
2. Run join.py to join the server
3. WASD to move
4. Left-click to destroy a block
5. Right-click to teleport
