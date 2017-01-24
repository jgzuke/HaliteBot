import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import logging
import numpy as np
logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")

myID, game_map = hlt.get_init()
hlt.send_init("MyPythonBot")

def get_random_momentum():
    momentum = [NORTH, EAST, SOUTH, WEST]
    random.shuffle(momentum)
    return momentum

momentum_map = [[get_random_momentum() for i in range(30)] for j in range(30)]
# Frame returned as list of Square(x=0, y=0, owner=0, strength=93, production=2)

def add_movement_to_momentum(square, direction):
    momentum = momentum_map[square.x][square.y]
    momentum.insert(0, momentum.pop(momentum.index(direction)))

movements = ((0, -1), (1, 0), (0, 1), (-1, 0))
def assign_move(square):
    for direction in momentum_map[square.x][square.y]:
        neighbor = game_map.get_target(square, direction)
        if neighbor.owner != myID and neighbor.strength < square.strength:
            add_movement_to_momentum(square, direction)
            return Move(square, direction)

    for direction in momentum_map[square.x][square.y]:
        neighbor = game_map.get_target(square, direction)
        if neighbor.owner == myID and square.strength > neighbor.strength > 1.5 and square.strength > 100:
            add_movement_to_momentum(square, direction)
            return Move(square, direction)

    return Move(square, STILL)

while True:
    game_map.get_frame()
    moves = [assign_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
