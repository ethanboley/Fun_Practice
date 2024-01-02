
import random
import math
from actions import *
from things_stuff import init_skills, Inventory


class Player:
    def __init__(self, name, hp, atk, xp, level, accuracy, col):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.atk = atk
        self.xp = xp
        self.level = level
        self.accuracy = accuracy
        self.col = col

    def attack(self, enemy, xp_thresholds):
        if random.random() < self.accuracy:
            enemy.hp -= self.atk - random.randint(0, self.atk // 5)
            dprint(f"{self.name} attacks {enemy.name} for {self.atk} damage!")
            if enemy.hp > 0:
                dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
            else:
                dprint(f'{self.name} has defeated {enemy.name}!')
                self.gain_xp(enemy.xp, xp_thresholds)
                self.gain_col(enemy.col)
                enemy.drop(self)

        else:
            dprint(f"{self.name} misses their attack!")

    def gain_xp(self, xp, xp_thresholds):
        dprint(f'{self.name} gained {xp} experience points, ')
        self.xp += xp
        for threshold in xp_thresholds:
            if self.xp >= threshold:
                self.level += 1
                dprint(f"{self.name} has leveled up to level {self.level}!")
                self.level_up()
                xp_thresholds.remove(threshold)  # Remove the threshold we just crossed
        dprint(f'{self.name} now has {self.xp} xp. ')

    def level_up(self):
        self.maxhp += 4 + (self.level // 4)
        self.atk += 1 + (self.level // 5)
        self.accuracy += .02 if self.accuracy != 1 else self.accuracy == 1
        self.hp = self.maxhp
        self.learn_skill()

    def is_alive(self):
        return self.hp > 0
    
    def gain_col(self, col):
        if col:
            dprint(f'{self.name} gained {col} col! ')
            self.col += col
            dprint(f'{self.name} now has {self.col} col!')

    def hattack(self, enemy):
        if random.random() < self.accuracy:
            enemy.hp -= self.atk
            if enemy.hp > 0:
                dprint(f'{enemy.name} is willing to keep going. ')
            else:
                dprint(f'{enemy.name} is fed up with all these issues. ')
    
    def special_attack():
        pass


class Fighter(Player):
    def __init__(self, name, hp, atk, xp, level, accuracy, col):
        super().__init__(name, hp, atk, xp, level, accuracy, col)
        self.title = 'Fighter'
        self.acu = .06 # attack acuracy modifier
        self.agi = 19 # used for battle order like a speed stat (out of 20?)
        self.mag = 10 # used to calculate skill cost
        self.maxmag = self.mag
        self.mod = 1 + self.level // 4
        self.skill_slots = 1
        self.known_skills = []
        self.skills = init_skills()
        self.known_skills.append(self.skills[0])
        self.inventory = Inventory()

    def attack(self, enemy, xp_thresholds):
        if random.random() < self.accuracy:
            damage = self.atk - random.randint(0, self.atk // 5)
            enemy.hp -= damage
            dprint(f"{self.name} attacks {enemy.name} for {damage} damage!")
            if enemy.is_alive():
                dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
            else:
                dprint(f'{self.name} has defeated {enemy.name}!')
                self.gain_xp(enemy.xp, xp_thresholds)
                self.gain_col(enemy.col)
                enemy.drop(self)
                # print(self.inventory.contents) # for debugging
                
        else:
            dprint(f"{self.name} misses their attack!")
    
    def gain_xp(self, xp, xp_thresholds):
        dprint(f'{self.name} gained {xp} experience points, ')
        self.xp += xp
        for threshold in xp_thresholds:
            if self.xp >= threshold:
                self.level += 1
                dprint(f"{self.name} has leveled up to level {self.level}!")
                self.level_up()
                xp_thresholds.remove(threshold)  # Remove the threshold we just crossed
        dprint(f'{self.name} now has {self.xp} xp. ')

    def level_up(self):
        self.maxhp += 4 + (self.level // 4)
        self.atk += 1 + (self.level // 5)
        self.accuracy += .02 if self.accuracy != 1 else self.accuracy == 1
        self.hp = self.maxhp
        self.skill_slots = 1 + int(math.log(self.level, 1.85))
        self.maxmag += 1 + (self.level // 40)
        self.agi -= (self.level // 16)
        self.learn_skill()

    def special_attack(self, enemy, xp_thresholds):
        if self.mag <= 0:
            dprint('You\'re out of magic!')
            return 0
        skill = self.choose_skill()
        self.mag -= skill.cost
        strong_damage = self.atk + random.randint(1, (self.atk // 5) + 1) + skill.damage
        weak_damage = self.atk - random.randint(1, (self.atk // 5) + 1)
        if random.random() < self.accuracy + self.acu:
            enemy.hp -= strong_damage
            dprint(f'{self.name} connects with the sword skill {skill.name}!') # TODO define skills
            dprint(f'the attack hits {enemy.name} for {strong_damage} damage!')
            if enemy.is_alive():
                dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
            else:
                dprint(f'{skill.name} obliterated {enemy.name}!') # for spells: '{} blasted {} to bits!'
                self.gain_xp(enemy.xp, xp_thresholds)
                self.gain_col(enemy.col)
                enemy.drop(self)
                # print(self.inventory.contents) # for debugging
        elif random.random() < self.accuracy:
            enemy.hp -= weak_damage
            dprint(f'{self.name} dealt a weak hit of the skill {skill.name}.')
            dprint(f'The attack dealt {weak_damage} damage to {enemy.name}.')
            if enemy.is_alive():
                dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
            else:
                dprint(f'Despite the weak hit with {skill.name}, {enemy.name} has died!')
                self.gain_xp(enemy.xp, xp_thresholds)
                self.gain_col(enemy.col)
                enemy.drop(self)
                # print(self.inventory.contents) # for debugging
        else:
            dprint(f'{self.name} executed the skill {skill.name} but missed! ')
        return skill.cooldown
    
    def learn_skill(self):
        skills = init_skills()
        learnables = [skill for skill in skills if skill.level <= self.level and skill.type == 0]
        while len(self.known_skills) < self.skill_slots: 
            dprint('You have an available skill slot')
            dprint('would you like to learn or replace a skill?')
            lorp = ['learn', 'replace', 'nope'] # lorp: Learn or Replace
            for i in range(3):
                print(f'{i + 1}: {lorp[i]}')
            ans = input()
            if ans in ['', '0', '1', 'l', 'L', 'Learn', 'learn']: # if learn new
                self.add_skill(learnables)
            elif ans in ['2', 'r', 'R', 'replace', 'Replace', 'repl', 'Repl', '3']: # if replace known
                self.remove_skill()
                self.add_skill(learnables)
            else:
                dprint('Ok maybe next time!')
                break
    
    def remove_skill(self):
        dprint('Replace which skill? ') # ask
        skill_int = check_user_input('s',list=self.known_skills)
        self.known_skills.remove(self.known_skills[skill_int - 1]) # remove the chosen skill at valid position

    def add_skill(self, learnables):
        dprint('Add which skill? ') # ask
        skill_int = check_user_input('s',list=learnables)
        self.known_skills.append(learnables[skill_int - 1]) # append the selected choice to known skills
        dprint(f'{self.name} has learned the skill {self.known_skills[-1].name}!')

    # def translate_skill(self, alias, skills):  # uncomment and add where needed (converts Skill.name to Skill)
    #     for skill in skills:
    #         if skill.name == alias:
    #             return skill

    def choose_skill(self):
        dprint('which skill do you want to use? ')
        user = check_user_input('s',list=self.known_skills)
        return self.known_skills[user - 1]
    
    # def check_user_input(self, skill_list):
    #     user_in = '' # set the while loop start case
    #     while not str(user_in).isdigit(): #  check if the user input can be converted into a number. 
    #         for i in range(len(skill_list)): # print out the available values. <--+vvv
    #             print(f'{i + 1}: {skill_list[i].name}; cost: {skill_list[i].cost}, cooldown: {skill_list[i].cooldown}, power: {skill_list[i].damage}') 
    #         print('Enter the number') # prompt the user
    #         user_in = input() # take in user input to be checked by the while condition. 
    #     user_int = int(user_in) # set second loop start case
    #     while user_int not in [x + 1 for x in range(len(skill_list))]: # once the user inputs a number, check if it's a good number
    #         user_int = self.check_user_input(skill_list) # if it isn't, restart by recursively calling the function. 
    #     else: # otherwise it is a good input 
    #         return user_int # therefore return the good value to be further processed. 
    
    def use_item(self, enemy, xp_thresholds):
        useables = [item for item in self.inventory.contents if item.can_use]
        if len(useables) != 0:
            list_int = check_user_input(list=useables)
            to_use = useables[list_int - 1]
            to_use.use(self, enemy, xp_thresholds)
            if to_use == 0:
                self.inventory.remove_item(to_use)
            else:
                self.inventory.contents[to_use] -= 1
        else:
            dprint('Your inventory is empty. ')

    def run(self):
        small = int((self.accuracy * 100) + (20 - self.agi))
        big = int(80 + self.agi)
        if random.randint(0, small) > random.randint(0, big):
            return True
        return False

