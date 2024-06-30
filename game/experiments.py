
import math
import time
import sys
import msvcrt
import random
from colorama import ansi, Fore, Style



# ---------- player (fighter) stats by level -------------



# Set Initial Stats
def display_stats():
    max_hp = 10
    atk = 2
    accuracy = 0.75
    skill_slots = 1
    max_mag = 10
    agi = 19
    prog = 0

    # Iterate through levels 1-n
    for level in range(1, 101):
        # Update stats for each level
        max_hp += 5 + round(level * 1.025)
        atk += (level // 8) if level > 20 else 1 + (level // 5)
        accuracy += 0.0025 if accuracy < 1 else 0
        skill_slots = 1 + int(math.log(level, 1.85))
        max_mag += 1 + (level // 40) if level % 5 == 0 else (level // 40)
        agi -= 1 if level % 12 == 0 else 0
        prog += 4 if level % 3 == 0 else 3

        # Print the stats for the current level
        print(f'Level {level + 1}:')
        print(f'\tMax HP: {max_hp}; ATK: {atk}; Accuracy: {accuracy:.4f}; Skill Slots: {skill_slots}; Max MAG: {max_mag}; AGI: {agi}; stpry progress: {prog}')





# -------------- dprint ------------------



def dprint(text='', sleep_time=.035):
    skip_slow_display = False

    for char in text:
        if not skip_slow_display:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(sleep_time) # lower value is faster
        else:
            sys.stdout.write(char) # really puts in perspective how fast .write() is

        if msvcrt.kbhit():  # Check if a key is pressed
            key = msvcrt.getch().decode('utf-8')
            if key == '\r':  # Press Enter to skip
                skip_slow_display = True

    sys.stdout.write('\n')  # Add a newline when done




# ---------------------- xp thresholds testing ---------------




def define_xp_thresholds():
    base_xp = 100
    xp_thresholds = []
    for i in range(105):
        xp_thresholds.append(base_xp)
        thresh = round((base_xp * 1.25) + (100 + (i + 1))) # 100, 125 + 101, ...
        base_xp = thresh
    return xp_thresholds


def define_xp_thresholds_d():
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


def display_xp_thresholds_d(xp_thresholds:dict):
    for key, value in xp_thresholds.items():
        print(f'level: {key}, \n\tthreshold: {value}')

def display_xp_thresholds(xp_thresholds:list):
    for i in range(len(xp_thresholds)):
        print(f'level: {i + 1}, \n\tthreshold: {xp_thresholds[i]}          requirement: {xp_thresholds[i] - xp_thresholds[i - 1]}')

def display_both_thresh(xp_thresholds:list, xp_thresholds_dict:dict):
    for key, value in xp_thresholds_dict.items():
        print(f'dict level: {key}          dict thresh: {value}')
        print(f'list level: {key}          list thresh: {xp_thresholds[key - 1]}')




# ---------- fun colored health bars --------------------

# class Player:
#     def __init__(self):
#         self.hp = 112
#         self.maxhp = 100
#         self.name = 'Rulid'
    
#     def test(self):
#         for _ in range(120):
#             display_health(self)
#             self.hp -= 1
#         # display_health(self)
#         display_health(self)

            

# tpc = Player()

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
        ansi_code = '\033[38;2;160;0;30m' # Red RGB:160,0,30
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



# print(Fore.LIGHTMAGENTA_EX + "This text is printed in red color!" + Style.RESET_ALL)

# print("\033[38;2;0;255;40mThis text is a custom green\033[0m")
# print("\033[38;2;255;235;0mThis text is a custom yellow\033[0m")
# print("\033[38;2;255;105;50mThis text is a custom orange\033[0m")
# print("\033[38;2;255;0;60mThis text is a custom red\033[0m")



# ------ tests -------



# display_stats()
# display_xp_thresholds(define_xp_thresholds())
# display_both_thresh(define_xp_thresholds(), define_xp_thresholds_d())
# tpc.test()
