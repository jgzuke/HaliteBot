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
directions = [NORTH, EAST, SOUTH, WEST]
actions = [NORTH, EAST, SOUTH, WEST, STILL]
action_directions = ((0, -1), (1, 0), (0, 1), (-1, 0), (0, 0))
def get_enemy_closeness(square, direction):
    dx, dy = ((0, -1), (1, 0), (0, 1), (-1, 0), (0, 0))[direction]
    for i in range(20):
        if game_map.contents[(square.y + dy*i) % game_map.height][(square.x + dx*i) % game_map.width].owner != myID:
            return (21. - i) / 22
    return (21. - 21) / 22

def get_closest_enemy_direction(square):
    return directions[np.argmax(get_enemy_closeness(square, direction) for direction in directions)]

def get_square_value(square, direction):
    new_square = game_map.get_target(square, direction)
    if new_square.owner == 0:
        if new_square.strength:
            return float(new_square.production) / new_square.strength
        else:
            return sum(1 for neighbor in game_map.neighbors(new_square) if neighbor.owner != myID)

    if new_square.owner != myID:
        return sum(square.strength for neighbor in game_map.neighbors(new_square) if neighbor.owner != 0 and neighbor.owner != myID)
    return 0

def get_best_target_direction(square):
    values = [get_square_value(square, direction) for direction in directions]
    if sum(values) == 0:
        return None
    return directions[np.argmax(values)]

def get_move_advantage(square, target_direction, action):
    if action == STILL:
        if (square.strength < (square.production * 15)):
            return 14

        return 1

    neighbor = game_map.get_target(square, action)
    # Unowned Space
    if action == target_direction and neighbor.owner == 0:
        if neighbor.strength < square.strength and neighbor.strength > 0:
            return 15

    # Enemy Space
    if action == target_direction and neighbor.owner != myID:
        if neighbor.strength < square.strength:
            return 15

    # My Space
    if target_direction == None and neighbor.owner == myID:
        if square.strength > neighbor.strength > 1.5 and square.strength > 100:
            return 13 + get_enemy_closeness(square, action)

    return 0

def get_best_move(square):
    target_direction = get_best_target_direction(square)
    return actions[np.argmax([get_move_advantage(square, target_direction, action) for action in actions])]

def assign_move(square):
    return Move(square, get_best_move(square))

while True:
    game_map.get_frame()
    moves = [assign_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
