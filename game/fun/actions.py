
import random
import time
import sys
import msvcrt
from things_stuff import Skill, Spell, Spall
# import pygame as pg


def define_xp_thresholds():
    """
    Calculates and returns a dictionary mapping level (1 to n) to XP thresholds.

    Returns:
        dict: Dictionary containing level-based XP thresholds.
    """

    base_xp = 100
    xp_thresholds = {1:base_xp}  # Use a dictionary to store level-XP pairs

    for i in range(1, 104):  # Iterate from 1 to 104 (inclusive) for 104 levels
      thresh = round((base_xp * 1.25) + (100 + i))
      xp_thresholds[i + 1] = thresh  # Set level (i+1) as key, XP threshold as value
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
    percent = (player.hp / player.maxhp) * 100 # __ what about a situation where the player max = 33 and the hp = 7?
    # that would make percent = 21.2121212121212121...
    # Therefore the next line would do some funky things because it is not working with int. 

    if 50 < percent <= 100:
        ansi_code = '\033[38;2;0;160;10m' # Green RGB:0,160,10
    elif 25 < percent <= 50:
        ansi_code = '\033[38;2;255;200;0m' # Yellow RGB:255,200,0
    elif 10 < percent <= 25:
        ansi_code = '\033[38;2;255;90;0m' # Orange RGB:255,90,0
    elif 0 < percent <= 10:
        ansi_code = '\033[38;2;175;0;30m' # Red RGB:160,0,30
    else:
        ansi_code = '\033[38;2;60;0;180m' # Blue RGB:60,0,180
    ansi_end = '\033[0m'

    bars_to_print = u'\u2588' * int(percent // 2)

    if percent % 2 == 0: # the percentage is even
        if percent > 0: # even and greater than 0
            fitting_end = ' ' * int(50 - (percent // 2)) + u'\u258f'
        elif percent > 100 or percent <= 0: # even and greater than 100
            fitting_end = ''
    else: # the percentage is odd
        if 0 < percent <= 100: # odd and between (0,100]
            fitting_end = u'\u258c' + ' ' * int((50 - (percent // 2)) - 1) + u'\u258f'
        elif percent < 0: # odd and below 0
            fitting_end = ''
        else: # odd and above 100
            fitting_end = u'\u258c'

    numeric_representation = f'{player.hp}/{player.maxhp}'
    
    print(ansi_code + bars_to_print + fitting_end + ansi_end, end='')
    print(f'{numeric_representation:>10}   {player.name}')


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

