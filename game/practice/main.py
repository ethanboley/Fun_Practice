
# patch/update history
# 
# dev 0.0.0 (base files and code creation)
# dev 0.0.1 (game base objects update)
# dev 0.0.3 (modular code update)
# dev 0.0.4 (music update)
# dev 0.0.7 (skills update)
# dev 0.0.9 (modular and maintainable code update)
# dev 0.0.10 (order of play update)
# dev 0.0.13 (bug patch) Current
# ...
# alpha 0.1.0 
# ...
# beta 0.2.0
# ...
# 1.0.0 - 1.999.999


from actions import * 
from misc import *
from monsters import *
from players import *
from things_stuff import *


# # Initialize Pygame
# initialize_pygame()



# Main game logic
def main_game():
    input('Press enter to start . . . ')
    dprint('What is your name: ')
    pname = input('')
    # base_p = Player(pname, 20, 4, 0, 1, .8, 0)
    pc = Fighter(pname, 20, 4, 0, 1, .8, 0)

    # skills_list = init_skills()

    base_xp = 100
    xp_thresholds = []
    for i in range(100):
        xp_thresholds.append(base_xp)
        thresh = round((base_xp * 1.1) + (100 + (i + 1)))
        base_xp = thresh

    playing = True

    while playing:
        dprint()
        dprint('You\'re in world 1')
        input()

        mon_list = init_enemies() # if moved outside loop repeat monsters will break. 
        options = ['fight','hospital', 'marketplace']

        for i in range(len(options)):
            dprint(f'{i + 1}: {options[i]}')

        action = input()
        
        if action in ['1', '0','','Absolutely!!!','fight','Fight','f','F','1: fight']:
            
            playing = battle(pc, choose_monster(pc, mon_list), xp_thresholds, mon_list)

        elif action in ['2','Hospital','hospital','h','H','HELP I\'M DYING!!!','heal']:
            hospital = Hospital('Greentown', pc.level)
            option = hospital.welcome()
            playing = hospital.resolve(pc, option, xp_thresholds)
        
        elif action in ['3','m','M','marketplace','market','Market','Store','store','shop','Shop','shopping!','s','S']:
            marketplace = Marketplace('justastore', pc.level)
            option = marketplace.welcome()
            marketplace.resolve(pc, option)

        else:
            dprint('Invalid input. ')
            dprint('Keep playing? Y/N')
            user = input()
            if user in ['N','n','Quit','quit','q','Q','Exit','exit','No','no','False','false','f','0','stop']:
                playing = False


if __name__ == "__main__":
    main_game()


