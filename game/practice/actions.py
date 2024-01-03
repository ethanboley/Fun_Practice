
import random
import time
import sys
import msvcrt
from things_stuff import Skill
# import pygame as pg


def choose_monster(player, monsters):
    one_worthy = [mon for mon in monsters if mon.level <= player.level]
    return random.choice(one_worthy)

def dprint(text=''):
    skip_slow_display = False

    for char in text:
        if not skip_slow_display:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)  # lower value is faster
        else:
            sys.stdout.write(char) # really puts in perspective how fast .write() is

        if msvcrt.kbhit():  # Check if a key is pressed
            key = msvcrt.getch().decode('utf-8')
            if key == '\r':  # Press Enter to skip
                skip_slow_display = True

    sys.stdout.write('\n')  # Add a newline when done

def display_health(player):
    percent = (player.hp / player.maxhp) * 100
    if percent % 2 == 0: # the percentage is even
        print(u'\u2588' * int(percent // 2), end='')
        print(' ' * int(50 - (percent // 2)) + u'\u258f', end='')
        print(f'{player.hp}/{player.maxhp}   {player.name}')
    else: # the percentage is odd
        print(u'\u2588' * int(percent // 2) + u'\u258c', end='')
        print(' ' * int((50 - (percent // 2)) - 1) + u'\u258f', end='')
        print(f'{player.hp}/{player.maxhp}   {player.name}')

def battle(player, monster, xp_thresholds, monsters, type=0): # TODO add a list of friends (teamates)
    battle_options = ['fight', 'skill', 'item', 'run']
    if type:
        # play the boss music
        pass
    else:
        dprint(f'you encounter a {monster.name}')
        round_num = 1
        seconds = 1
        cooldown = 0
        if player.mag != player.maxmag:
            player.mag += 1 + player.level
            if player.mag >= player.maxmag:
                player.mag = player.maxmag
        active_monsters = []
        active_monsters.append(monster)

        while player.is_alive() and len(active_monsters) != 0:

            if seconds % 20 == 1:
                dprint(f'Round {round_num}, FIGHT! ')
                round_num += 1

            if seconds % player.agi == 0:
                if cooldown:
                    cooldown -= 1
                dprint('Target which monster?')
                target = get_list_option(active_monsters)
                for i in range(4):
                    print(f'{i + 1}: {battle_options[i]}')
                option = input()
                if option in ['2', 'Skill', 'skill', 's', 'S'] and (not cooldown):
                    cooldown = player.special_attack(target, xp_thresholds)
                    if not target.is_alive():
                        active_monsters.remove(target)
                elif option in ['3', 'item', 'Item', 'i', 'I', 'bag', 'Bag', 'b', 'B']:
                    player.use_item(target, xp_thresholds)
                    if not target.is_alive():
                        active_monsters.remove(target)
                elif option in ['4', 'Run', 'run', 'r', 'R', 'nigerundaio!', '5', 'flee']:
                    if player.run():
                        dprint(f'{player.name} made a narrow escape!')
                        break
                    else:
                        dprint(f'{player.name} fails their escape attempt!')
                else:
                    player.attack(target, xp_thresholds)
                    if not target.is_alive():
                        active_monsters.remove(target)
            
            # for friend in friends:
            #     if seconds % friend.agi == 0:
            #         friend.attack(monster)
            #         if not target.is_alive():
            #             active_monsters.remove(target) # TODO see function def line

            for monster in active_monsters:
                if seconds % monster.agi == 0:
                    monster.attack(player)
                    if not player.is_alive():
                        return False
            
            if seconds % 120 == 0:
                active_monsters.append(choose_monster(player, monsters))
                dprint('The sound of battle and the smell of blood atracts')
                dprint(f'a {active_monsters[-1].name} which joins the fight!')

            seconds += 1
    
    return True


class Battle:
    def __init__(self, active_player, xp_thresholds):
        self.active_player = active_player
        self.xp_thresholds = xp_thresholds
        self.type = 0
        self.active_monsters = []
        self.active_teamates = []
        self.name = 'battle'
        self.battle_options = ['fight', 'skill', 'item', 'run']

    def regular(self, mon_list):
        # basically the same as the battle function defined above
        # define the initial participants of this particular battle
        self.init_parti(mon_list)
        # set seconds to 1
        seconds = 1
        # set round num to 1
        round_num = 1
        # reset player skill cooldown
        cooldown = 0
        # set player mag val
        if self.active_player.mag != self.active_player.maxmag:
            self.active_player.mag += 1 + self.active_player.level
            if self.active_player.mag >= self.active_player.maxmag:
                self.active_player.mag = self.active_player.maxmag
        # describe the encounter
        dprint(f'you encounter a {self.active_monsters[-1].name}!')
    
        # begin battle
        while self.active_player.is_alive() and len(self.active_monsters) != 0:
            # handle the rounds
            if seconds % 20 == 1:
                dprint(f'Round {round_num}, FIGHT! ')
                round_num += 1
            # handle the player's turn
            cooldown = self.handle_player_turn(seconds, cooldown)
            # go through the allie's turns
            self.handle_ally_turns(seconds)
            # handle the monster's turns
            self.handle_monster_turns(seconds)
            if not self.active_player.is_alive():
                return False # tell the game the player is dead
            # add monsters to the battle if it lasts too long
            self.handle_additional_monsters(seconds, mon_list)
            # increment seconds
            seconds += 1
        
        return True # tell the game the player is still alive

    def boss(self, mon_list):
        self.init_parti(mon_list)
    
    def handle_player_turn(self, seconds, cooldown):
        if seconds % self.active_player.agi == 0:
            # reduce skill cooldown if applicable
            if cooldown:
                cooldown -= 1
            # prompt for battle option
            for i in range(4):
                print(f'{i + 1}: {self.battle_options[i]}')    
            option = input()

            if option in ['','1','0','f','F','fight','Fight','FIGHT','attack','a','A','Y','y','yes']:
                # define target
                if len(self.active_monsters) == 1:
                    target = self.active_monsters[-1]
                else:
                    dprint('target which monster')
                    target = get_list_option(self.active_monsters)
                # attack
                self.active_player.attack(target, self.xp_thresholds)
                # update active monsters
                if not target.is_alive():
                    self.active_monsters.remove(target)

            elif option in ['2','Skill','skill','s','S','spell','Spell','SKILL','SPELL'] and (not cooldown):
                # define the target
                if len(self.active_monsters) == 1:
                    target = self.active_monsters[-1]
                else:
                    dprint('target which monster')
                    target = get_list_option(self.active_monsters)
                # special attack
                cooldown = self.active_player.special_attack(target, self.xp_thresholds)
                # update active monsters
                if not target.is_alive():
                    self.active_monsters.remove(target)
            
            elif option in ['3', 'item', 'Item', 'i', 'I', 'bag', 'Bag', 'b', 'B']:
                # define the target
                if len(self.active_monsters) == 1:
                    target = self.active_monsters[-1]
                else:
                    dprint('target which monster')
                    target = get_list_option(self.active_monsters)
                # use item
                self.active_player.use_item(target, self.xp_thresholds)
                # update active monsters
                if not target.is_alive():
                    self.active_monsters.remove(target)
            
            else:
                escape = 0
                for i in range(len(self.active_monsters)):
                    if self.active_player.run():
                        escape += 1
                if len(self.active_monsters) == 1 and escape == 1:
                    dprint(f'{self.active_player.name} escaped!')
                    self.active_monsters.clear()
                elif len(self.active_monsters) == 2:
                    if escape == 1:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 2:
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                elif len(self.active_monsters) == 3:
                    if escape == 2:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 3:
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                elif len(self.active_monsters) == 4:
                    if escape == 2:
                        dprint(f'{self.active_player.name} barely escaped with their life!')
                        self.active_monsters.clear()
                    elif escape == 3:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 4: 
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                elif len(self.active_monsters) > 4:
                    if escape >= 6:
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                    elif escape == 5:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 4:
                        dprint(f'{self.active_player.name} barely escaped with their life!')
                        self.active_monsters.clear()
                    elif escape == 3:
                        dprint('Wow... miracles really do happen!')
                        self.active_monsters.clear()
                else:
                    dprint(f'{self.active_player.name} failed their escape attempt.')
            return cooldown
    
    def handle_ally_turns(self, seconds):
        for ally in self.active_teamates:
            if seconds % ally.agi == 0:
                target = ally.take_turn()
                if not target.is_alive:
                    self.active_monsters.remove(target)

    def handle_monster_turns(self, seconds):
        for monster in self.active_monsters:
            if seconds % monster.agi == 0:
                monster.attack(self.active_player)

    def handle_additional_monsters(self, seconds, mon_list):
        if seconds % 120 == 0:
            self.active_monsters.append(choose_monster(self.active_player, mon_list))
            dprint('The sound of battle and the smell of blood atracts')
            dprint(f'a {self.active_monsters[-1].name} which joins the fight!')

    def init_parti(self, mon_list):
        for ally in self.active_player.allies:
            self.active_teamates.append(ally)
        self.active_monsters.append(choose_monster(self.active_player,mon_list))


def check_user_input(type='l', list=[], dict={}):
    if type == 'l': # type l means a list of objects with .name attributes
        user_in = '' # set the while loop start case
        while not str(user_in).isdigit(): #  check if the user input can be converted into a number. 
            for i in range(len(list)): # print out the available values. <--+vvv
                print(f'{i + 1}: {list[i].name}') 
            print('Enter the number') # prompt the user
            user_in = input() # take in user input to be checked by the while condition. 
            if user_in == '': # allow a default enter
                user_in = '1'
        user_int = int(user_in) # set second loop start case
        while user_int not in [x + 1 for x in range(len(list))]: # once the user inputs a number, check if it's a good number
            user_int = check_user_input('l',list=list) # if it isn't, restart by recursively calling the function. 
        # else: # otherwise it is a good input
        return user_int
    elif type == 'd': # type d means dictionaries with count or other incrementing integer vlaues and keys with .name attributes
        user_in = '' # set the while loop start case
        while not str(user_in).isdigit(): # check if the user input can be converted into a number. 
            i = 0 # set the index for the display loop
            for key in dict: # print out the available values. <--+vvv
                print(f'{i + 1}: item, {key.name}; count, {dict[key]}') # mind this will only work if the key of the dict has a .name property
                i += 1 # increment the index
            print('Enter the number') # prompt the user
            user_in = input() # take in user input to be checked by the while condition.
            if user_in == '': # allow a default enter
                user_in = '1'
        user_int = int(user_in) # set second loop start case
        while user_int not in [x + 1 for x in range(len(dict))]: # once the user inputs a number, check if it's a good number
            user_int = check_user_input('d',dict=dict) # if it isn't, restart by recursively calling the function. 
        # else: # otherwise it is a good input
        return user_int
    elif type == 's': # type s is the same as type l exclusively for type:Skill objects
        user_in = '' # set the while loop start case
        while not str(user_in).isdigit(): #  check if the user input can be converted into a number. 
            for i in range(len(list)): # print out the available values. <--+vvv
                print(f'{i + 1}: {list[i].name}; cost: {list[i].cost}, cooldown: {list[i].cooldown}, power: {list[i].damage}')
            print('Enter the number') # prompt the user
            user_in = input() # take in user input to be checked by the while condition. 
            if user_in == '': # allow a default enter
                user_in = '1'
        user_int = int(user_in) # set second loop start case
        if user_int not in [x + 1 for x in range(len(list))]: # once the user inputs a number, check if it's a good number
            print('test1') # debugging
            user_int = check_user_input('s',list=list) # if it isn't, restart by recursively calling the function. 
        # else: # otherwise it is a good input
        return user_int


def get_validated_input(prompt, options):
    if not options:
        return None
    
    dprint(prompt)
    while True:
        for i, option in enumerate(options, start=1):
            if isinstance(option, Skill):  # Assuming Skill is the class name for the skill type
                print(f'{i}: {option.name}; cost: {option.cost}, cooldown: {option.cooldown}, power: {option.damage}')
            else:
                print(f'{i}: {option.name}')
        
        user_in = input("Enter the number: ").strip()
        
        if user_in == '':
            user_in = '1'  # Default to the first option
        
        if user_in.isdigit():
            user_int = int(user_in)
            if 1 <= user_int <= len(options):
                return user_int

# Usage Example for List of Options
def get_list_option(options):
    ans = get_validated_input('Choose an option:',options)
    if ans == None:
        print('No options available.' )
        return
    return options[ans - 1]

# Usage Example for Dictionary Options
def get_dict_option(options):
    ans = get_list_option(list(options.keys()))
    if ans == None:
        return
    key = ans
    return options[key]



# def initialize_pygame():
#     pg.init()
#     pg.mixer.init()

