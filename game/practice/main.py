
from worlds import *

def main_game():

    initialize_pygame()

    world_1 = WorldOne('Mainenkedren')
    world_1.introdction()
    complete = world_1.world_loop()
    if complete:
        world_2 = WorldTwo('Mainenkedren', pc=world_1.pc, xp_thresholds=world_1.xp_thresholds)
        complete = world_2.world_loop()
        if complete:
            pass # complete = world_3.world_loop() # etc... vvv

if __name__ == "__main__":
    main_game()
