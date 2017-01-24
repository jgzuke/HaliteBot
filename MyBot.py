import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import logging
import numpy as np
logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logging.info('Log Start')

myID, game_map = hlt.get_init()
hlt.send_init("MyPythonBot")

# Frame returned as list of Square(x=0, y=0, owner=0, strength=93, production=2)
actions = [NORTH, EAST, SOUTH, WEST, STILL]
action_directions = ((0, -1), (1, 0), (0, 1), (-1, 0), (0, 0))
def get_move_advantage(square, action):
    if action == STILL:
        return 1

    neighbor = game_map.get_target(square, action)
    # Unowned Space
    if neighbor.owner == 0:
        if neighbor.strength < square.strength and neighbor.strength > 0:
            return 4
        else:
            return 0

    # Enemy Space
    if neighbor.owner != myID:
        if neighbor.strength < square.strength:
            return 3
        else:
            return 0

    # My Space
    if square.strength > neighbor.strength > 1.5 and square.strength > 100:
        return 2
    else:
        return 0

def assign_move(square):
    return Move(square, actions[np.argmax([get_move_advantage(square, action) for action in actions])])

while True:
    game_map.get_frame()
    moves = [assign_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
