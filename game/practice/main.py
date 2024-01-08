
from actions import * 
from misc import *
from monsters import *
from players import *
from things_stuff import *
from worlds import *


# # Initialize Pygame
# initialize_pygame()

# Main game logic
def main_game():
    xp_thresholds = define_xp_thresholds()
    input('Press enter to start . . . ')

    world_1 = WorldOne('The Kobold Wood')
    pc = world_1.create_character()
    world_1.world_loop(pc, xp_thresholds)

if __name__ == "__main__":
    main_game()
