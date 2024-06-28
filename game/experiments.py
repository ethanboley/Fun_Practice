
import math
import time
import sys
import msvcrt
import random


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


display_stats()