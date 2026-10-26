
from worlds import *

def main_game():

    initialize_pygame()

    world_1 = WorldOne('Mainenkedren')
    world_1.introdction()
    world_1.world_loop()

if __name__ == "__main__":
    main_game()
