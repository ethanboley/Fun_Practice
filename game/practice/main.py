
from worlds import *

def main_game():
    xp_thresholds:dict = define_xp_thresholds()

    initialize_pygame()

    world_1 = WorldOne('Mainenkedren', xp_thresholds)
    world_1.introdction()
    world_1.world_loop()

if __name__ == "__main__":
    main_game()
