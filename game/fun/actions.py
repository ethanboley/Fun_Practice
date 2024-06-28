
import random
import time
import sys
import msvcrt
from things_stuff import Skill, Spell, Spall
# import pygame as pg


def define_xp_thresholds():
    base_xp = 100
    xp_thresholds = []
    for i in range(100):
        xp_thresholds.append(base_xp)
        thresh = round((base_xp * 1.25) + (100 + (i + 1))) # 100, 125 + 101, ...
        base_xp = thresh
    return xp_thresholds

def choose_monster(player, monsters):
    one_worthy = [mon for mon in monsters if mon.level <= player.level]
    return random.choice(one_worthy)

def dprint(text='',speed=0.035):
    skip_slow_display = False

    for char in text:
        if not skip_slow_display:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed) # lower value is faster
        else:
            sys.stdout.write(char) # really puts in perspective how fast .write() is

        if msvcrt.kbhit():  # Check if a key is pressed
            key = msvcrt.getch().decode('utf-8')
            if key == '\r':  # Press Enter to skip
                skip_slow_display = True

    sys.stdout.write('\n')  # Add a newline when done

def display_health(player):
    percent = (player.hp / player.maxhp) * 100 # what about a situation where the player max = 33 and the hp = 7?
    # that would make percent = 21.21212121212121...
    # Therefore the next line would do some funky things because it is not working with int. 
    if percent % 2 == 0: # the percentage is even
        print(u'\u2588' * int(percent // 2), end='')
        print(' ' * int(50 - (percent // 2)) + u'\u258f', end='')
        print(f'{player.hp}/{player.maxhp}   {player.name}')
    else: # the percentage is odd
        print(u'\u2588' * int(percent // 2) + u'\u258c', end='')
        print(' ' * int((50 - (percent // 2)) - 1) + u'\u258f', end='')
        print(f'{player.hp}/{player.maxhp}   {player.name}')

def get_validated_input(prompt, options):
    if not options:
        dprint('No options to choose from. ')
        return None
    
    dprint(prompt)
    while True:
        for i, option in enumerate(options, start=1):
            if isinstance(option, Skill):
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
    ans = get_validated_input('Choose an option:', options)
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

