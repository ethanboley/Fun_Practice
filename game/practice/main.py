
from things_stuff import *
from actions import * 
from stuffs_that_do import *
from misc import *
from monsters import *
from players import *
from worlds import *


# # Initialize Pygame
# initialize_pygame()

# Main game logic
def main_game():
    xp_thresholds = define_xp_thresholds()
    input('Press enter to start . . . ')

    world_1 = WorldOne('The Kobold Wood')
    world_1.introdction()
    world_1.world_loop(xp_thresholds)


if __name__ == "__main__":
    main_game()
