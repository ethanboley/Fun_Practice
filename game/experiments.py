
import math
import time
import sys
import msvcrt
import random
from colorama import ansi, Fore, Style
import pygame as pg
import sys
from math import ceil
from fractions import Fraction
import win32gui as wg
import win32com.client as wcc
from pynput import keyboard as kb




# ---------- player (fighter) stats by level -------------



# Set Initial Stats
# def display_stats():
#     max_hp = 10
#     atk = 2
#     accuracy = 0.75
#     skill_slots = 1
#     max_mag = 10
#     agi = 19
#     prog = 0

#     # Iterate through levels 1-n
#     for level in range(1, 101):
#         # Update stats for each level
#         max_hp += 5 + round(level * 1.025)
#         atk += (level // 8) if level > 20 else 1 + (level // 5)
#         accuracy += 0.0025 if accuracy < 1 else 0
#         skill_slots = 1 + int(math.log(level, 1.85))
#         max_mag += 1 + (level // 40) if level % 5 == 0 else (level // 40)
#         agi -= 1 if level % 12 == 0 else 0
#         prog += 4 if level % 3 == 0 else 3

#         # Print the stats for the current level
#         print(f'Level {level + 1}:')
#         print(f'\tMax HP: {max_hp}; ATK: {atk}; Accuracy: {accuracy:.4f}; Skill Slots: {skill_slots}; Max MAG: {max_mag}; AGI: {agi}; stpry progress: {prog}')





# -------------- dprint ------------------



def dprint(text='', speed:float | None = 0.035, end:str | None = '\n'):
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

    sys.stdout.write(end)  # Add the correct end when done






# ---------------------- xp thresholds testing ---------------




# def define_xp_thresholds():
#     base_xp = 100
#     xp_thresholds = []
#     for i in range(105):
#         xp_thresholds.append(base_xp)
#         thresh = round((base_xp * 1.25) + (100 + (i + 1))) # 100, 125 + 101, ...
#         base_xp = thresh
#     return xp_thresholds


# def define_xp_thresholds_d():
#     """
#     Calculates and returns a dictionary mapping level (1 to n) to XP thresholds.

#     Returns:
#         dict: Dictionary containing level-based XP thresholds.
#     """

#     base_xp = 100
#     xp_thresholds = {1:base_xp}  # Use a dictionary to store level-XP pairs

#     for i in range(1, 104):  # Iterate from 1 to 104 (inclusive) for 104 levels
#       thresh = round((base_xp * 1.25) + (100 + i))
#       xp_thresholds[i + 1] = thresh  # Set level (i+1) as key, XP threshold as value
#       base_xp = thresh

#     return xp_thresholds


# def display_xp_thresholds_d(xp_thresholds:dict):
#     for key, value in xp_thresholds.items():
#         print(f'level: {key}, \n\tthreshold: {value}')

# def display_xp_thresholds(xp_thresholds:list):
#     for i in range(len(xp_thresholds)):
#         print(f'level: {i + 1}, \n\tthreshold: {xp_thresholds[i]}          requirement: {xp_thresholds[i] - xp_thresholds[i - 1]}')

# def display_both_thresh(xp_thresholds:list, xp_thresholds_dict:dict):
#     for key, value in xp_thresholds_dict.items():
#         print(f'dict level: {key}          dict thresh: {value}')
#         print(f'list level: {key}          list thresh: {xp_thresholds[key - 1]}')




# ---------- fun colored health bars --------------------

class Player:
    def __init__(self):
        self.hp = 112
        self.maxhp = 100
        self.level = 3
        self.name = 'Rulid'
        self.acu = 0.70
        self.allies = []
    
    def test(self):
        # for _ in range(120):
        #     display_health(self)
        #     self.hp -= 1
        # # display_health(self)
        # display_health(self)
        pass


tpc = Player()

# def display_health(player):
#     percent = (player.hp / player.maxhp) * 100 # __ what about a situation where the player max = 33 and the hp = 7?
#     # that would make percent = 21.2121212121212121...
#     # Therefore the next line would do some funky things because it is not working with int. 

#     if 50 < percent <= 100:
#         ansi_code = '\033[38;2;0;160;10m' # Green RGB:0,160,10
#     elif 25 < percent <= 50:
#         ansi_code = '\033[38;2;255;200;0m' # Yellow RGB:255,200,0
#     elif 10 < percent <= 25:
#         ansi_code = '\033[38;2;255;90;0m' # Orange RGB:255,90,0
#     elif 0 < percent <= 10:
#         ansi_code = '\033[38;2;160;0;30m' # Red RGB:160,0,30
#     else:
#         ansi_code = '\033[38;2;60;0;180m' # Blue RGB:60,0,180
#     ansi_end = '\033[0m'

#     bars_to_print = u'\u2588' * int(percent // 2)

#     if percent % 2 == 0: # the percentage is even
#         if percent > 0: # even and greater than 0
#             fitting_end = ' ' * int(50 - (percent // 2)) + u'\u258f'
#         elif percent > 100 or percent <= 0: # even and greater than 100
#             fitting_end = ''
#     else: # the percentage is odd
#         if 0 < percent <= 100: # odd and between (0,100]
#             fitting_end = u'\u258c' + ' ' * int((50 - (percent // 2)) - 1) + u'\u258f'
#         elif percent < 0: # odd and below 0
#             fitting_end = ''
#         else: # odd and above 100
#             fitting_end = u'\u258c'

#     numeric_representation = f'{player.hp}/{player.maxhp}'
    
#     print(ansi_code + bars_to_print + fitting_end + ansi_end, end='')
#     print(f'{numeric_representation:>10}   {player.name}')



# print(Fore.LIGHTMAGENTA_EX + "This text is printed in red color!" + Style.RESET_ALL)

# print("\033[38;2;0;255;40mThis text is a custom green\033[0m")
# print("\033[38;2;255;235;0mThis text is a custom yellow\033[0m")
# print("\033[38;2;255;105;50mThis text is a custom orange\033[0m")
# print("\033[38;2;255;0;60mThis text is a custom red\033[0m")




# ------- Pygame stuffs --------

class Monster:
    def __init__(self) -> None:
        self.ac = (200, 6, 480, 2) # rail size, hit dc, speed, chances
        self.level = 31

tmon = Monster()

# Initialize Pygame
pg.init()

def attack_timing_window(monster, player, acu) -> float:
    '''
    Creates a Pygame window that simulates an attack timing challenge. Closes
    and returns with enter key or after closing the window.

    Args:
        monster: an Enemy or other object with ac and level attributes
        player: a Player object with acu and level attributes
    
    Returns:
        hit_v (float, between 0 and 1 inclusive): A hit value representing how
        close the user came to hitting the target. 
    '''

    # initialize starting values
    rail_size, hit_dc, speed, chances = monster.ac
    difficulty_mod = abs(player.level - monster.level) * 2

    # initialize fps to the passed speed value and the slider speed to 1
    fps = speed
    adjusted_speed = 1

    # decrease fps until it is between 120 and 240 doubling speed each time
    while fps > 240:
        fps //= 2
        adjusted_speed *= 2
    
    # set the true speed of the slider
    speed = round(adjusted_speed)

    # initialize the hit condition
    hit_v = 0.0

    # Set the width and height of the window
    window_width = 1000
    window_height = 100

    # Panic timer
    passes = 0

    # Create the window
    window = pg.display.set_mode((window_width, window_height))
    pg.display.set_caption(f'ATTACK!!! {chances - passes} chances remaining!')

    # window control 
    # Find the window handle
    hwnd = pg.display.get_wm_info()['window']
    chwnd = wg.GetForegroundWindow()
    
    # Bring the window to the foreground using some butt janky scripting found on stackoverflow
    shell = wcc.Dispatch("WScript.Shell")
    shell.SendKeys(' ') # I have actually non idea why this works but it does
    wg.SetForegroundWindow(hwnd)

    # Define colors
    BLACK = (80, 80, 80) # value to be used for testing
    BROWN = (150, 85, 60) # value to be used for testing
    WHITE = (200, 200, 200) # value to be used for testing
    PURPLE = (35, 0, 60)
    RED_ORANGE = (255, 55, 0)
    YELLOW_ORANGE = (255, 180, 0)
    GREEN = (0, 225, 50)
    YELLOW = (220, 255, 0)
    RED = (200, 0, 40)
    BLUE = (40, 100, 255)

    # Bar properties
    bar_length = rail_size if rail_size < window_width else 600
    bar_height = 20
    bar_x = (window_width - bar_length) // 2
    bar_y = (window_height - bar_height) // 2

    # Target area properties
    target_width = hit_dc + difficulty_mod
    if target_width + (ceil(target_width * 1.85) * 2) > window_width:
        target_width = 30
    target_x = bar_x + (bar_length - target_width) // 2
    target_y = bar_y - 5
    target_height = bar_height + 10

    # Sub-target areas properties'
    sub1_width = ceil(target_width * 1.85) if 1 < ceil(target_width * 1.85) <= (window_width - 10) else 2
    sub1_x = target_x - sub1_width
    sub1_y = bar_y - 3
    sub1_height = bar_height + 6
    
    sub2_width = ceil(target_width * 1.85) if 1 < ceil(target_width * 1.85) <= (window_width - 10) else 1
    sub2_x = target_x + target_width
    sub2_y = bar_y - 3
    sub2_height = bar_height + 6

    # slider properties
    slider_width = 2
    slider_height = 30
    slider_speed = speed if speed < target_width else target_width // 2

    # Initialize the slider position and direction
    slider_x = bar_x
    slider_direction = slider_speed

    # Initialize the clock
    clock = pg.time.Clock()

    # Main loop
    running = True
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                hit_v = 0.0
                running = False
                break
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if target_x <= slider_x <= target_x + target_width:
                        # print('Success!')
                        hit_v = 1.0
                        running = False
                        break
                    elif sub1_x <= slider_x <= sub1_x + sub1_width:
                        distance = slider_x - target_x
                        normalized_distance = distance / sub1_width
                        hit_v = acu + (1 - acu) * (1 + normalized_distance) # a number from .65 to 1.0 that represents how far away slider_x is from target_x
                        running = False
                        break
                    elif sub2_x <= slider_x <= sub2_x + sub2_width:
                        distance = (slider_x + slider_width) - sub2_x
                        normalized_distance = distance / sub2_width
                        hit_v = acu + (1 - acu) * (1 - normalized_distance) # a number from .65 to 1.0 that represents how far away slider_x is from target_x + target_width (or sub2_x)
                        running = False
                        break
                    else:
                        # print('Miss!')
                        hit_v = 0.0
                        running = False
                        break

        # result found; set focus back to console, kill window, return result, do not draw again, do not pass go, do not collect $200.
        if not running:
            wg.SetForegroundWindow(chwnd)
            pg.quit()
            return hit_v

        # Move the slider
        slider_x += slider_direction

        # Reverse the direction if the slider reaches the bar ends
        if slider_x <= bar_x or slider_x + slider_width >= bar_x + bar_length:
            slider_direction = -slider_direction

            # keep track of the number of times this has occured
            passes += 1
        
            # Update the displayed timer
            pg.display.set_caption(f'ATTACK!!! {chances - passes} chances remaining!')
        
        # Check if the player has run out of chances
        if passes >= chances:
            hit_v = 0.0
            running = False

        # Clear the window
        window.fill(PURPLE)

        # Draw the bar
        pg.draw.rect(window, RED, (bar_x, bar_y, bar_length, bar_height))
        
        # Draw the sub_target areas
        pg.draw.rect(window, RED_ORANGE, (sub1_x, sub1_y, sub1_width, sub1_height))
        pg.draw.rect(window, RED_ORANGE, (sub2_x, sub2_y, sub2_width, sub2_height))

        # These bars are just to add a bit more color
        pg.draw.rect(window, YELLOW_ORANGE, ((target_x + sub1_x) // 2, sub1_y, (target_width * 2 + sub1_width * 2) // 2, sub1_height))
        pg.draw.rect(window, YELLOW, ((target_x + ((target_x + sub1_x) // 2)) // 2, sub1_y, (target_width * 2 + sub1_width * 2) // 3, sub1_height))

        # Draw the target area
        pg.draw.rect(window, GREEN, (target_x, target_y, target_width, target_height))

        # Draw the slider
        pg.draw.rect(window, BLUE, (slider_x, bar_y - (slider_height - bar_height) // 2, slider_width, slider_height))

        # Update the display
        pg.display.flip()


        # Set the frame rate to 120 FPS
        clock.tick(fps)


# ----- level up fireworks ------

# def ascci_fireworks():
#     dprint('    COOOOONGRAAAAAAAAAAADUUULATIOOOOOOONNNSS!!!')
#     dprint(
#         '''
#                                                                         *,                  _`Y,           
#            _Y                 `  \ | *                             *  `* .  ` *              >2``           
#             7``                _`_^___`   BOOM!                  ` `* ,* .* `*  `*            2      CRACK! 
#             2      CRACK!     *   /\ `        / |             * *`* *  * ** *, -` `,           2     ` v _  
#              2     ` v _       `\  \   ` \ ` |`// /   ,      * *  * ,*   *`, ** ** *,*_ ` ~      2     7 `  
#     _ ` /      2     7 `  3~, \     \_` -\ \ |,/ /-  _   /   _ * *`, **` # * ``  **  * =*_ -      2   4   3 
#      =*_ -      2   4   3       ----  \ - \ | | / =/ --/----  /  *  , ,`  .  x  *  .  / | \_    *  2 /   3  
#     ~ | \_       2 /   3      --_--- \  ----\ /BANG!/ -------- *` `, *  * *   * ,*          \     \|    3   
#           \      1    3       -----*---`-----X-------_--------  ,- * `,.*, * `. * .          \     1    3   
#            \     1    3     = ---/-_--/ -/ / | \_\- \---_-----     ` /``  * `           SCREE!\    1    3   
#       SCREE!\    1    3         ----  / -- -|||- --` \  ---- _     /        #  POW!           |     `\ 3    
#             |     `\ 3       /      ``--/- /| |\ -\--``   \       /        /                   \   * |3     
#              \      3      POP!    /   /   ||_  `  ' \           `        |             >\V/<   \  |/      
#               \    /                      //     `                                        /`      \V
# '''
#     ,.0005)
#     dprint('           YAAAAAAAAAAAAY!!!')

# --------- dictionary stuff ---------

# def get_validated_input(prompt, options):
#     print(prompt)
#     for i in range(len(options)):
#         print(f'{i + 1}: {options[i]}')
#     return int(input())

# def get_list_option(options):
#     ans = get_validated_input('Choose an option:', options)
#     if ans == None:
#         print('No options available.' )
#         return
#     return options[ans - 1]

# def get_dict_option(options:dict):
#     ans = get_list_option(list(options.keys()))
#     if ans == None:
#         return
#     key = ans
#     return key

# ------ math --------

def calculate_hp_and_attack(cons: float | None = 1.0, level: int | None = 1) -> tuple[int, int]:
    '''
    if the cons == 1:
        atk = level and hp = level * 20 (hp_mod)
    elif the cons == 0:
        atk = level * 2 and hp = level * 10
    
    hp_mod = some int from 10-20 (20 - (cons * 10))
    atk_mod = 2 - cons

    '''
    if level == 1:
        hp_mod = cons * 10
    elif level < 5:
        hp_mod = (level * 2) + (cons * 10)
    else:
        hp_mod = 10 + (cons * 10)
    atk_mod = 2 - cons

    # Multiply the ratio by level
    hp = 2 if int(hp_mod * level) < 2 else int(hp_mod * level)
    atk = int(atk_mod * level)

    return hp, atk


# ------ tests -------

for i in range(500):
    con = random.random()
    # con = 1.0
    # con = 0.0
    # con = 0.5
    hp_atk = calculate_hp_and_attack(cons = con, level = (i // 5) + 1)
    print(f'level {(i // 5) + 1}. Hp -> {hp_atk} <- atk. Consentration = {round(con, 3)}')
