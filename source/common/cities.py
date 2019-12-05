from random import randint

#### High level overview of city generation ####
'''
Start with a capitol city. Put it in the middle of the map and have it search around for best spot

Spawn out 3-4 cities in a random nsew direction. They search around in thier direction for a best spot.
Distance from an established city is important to keep things seperated a bit. They'll prioritize settling
on resources that are different from those in already established cities. Draw roads back

Each city is connected to 1-3 towns (Including capitol). Spawn in random directions. If they run parallal to
roads that they could intersect, make them do so

Each settlment spawns 1-2 points of interest. +1 for cities and capitols. If the settlement only has one attached
settlement, it may create a village or dungeon. One poi will always be the starting village while another will
be the end dungeon. Settlments will draw from the map around them to pick enviormental based pois such as lakes,
ocean, forest, as well as creating dungeons and what not.


Settlement types:
----------------
Capitol
City
Town
Village

Points of interest:
------------------
Dungeon
Shrine
Lake
Questline
Trail loop
Hunting ground
Trading port
Carvan
Ocean
Forest

'''

class Settler:
    def __init__(self, direction, settlment):
        self.direction = direction
        self.settlement = settlement
        self.pos = None

    def walk(self):
        """Try to walk in thier direction"""
        return

    def survey(self):
        """Evaluate a chunk for its potential as a settlment"""

    def settle(self):
        """Create a settlement at the current location"""