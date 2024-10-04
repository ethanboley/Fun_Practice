
import random
import math
from actions import *
from things_stuff import init_skills, init_spalls, Inventory
from stuffs_that_do import init_spells


class Player:
    def __init__(self, name, gender, hp, atk, xp, level, accuracy, col, progress=0):
        self.name = name
        self.gender = gender
        self.maxhp = hp
        self.hp = hp
        self.atk = atk
        self.xp = xp
        self.level = level
        self.accuracy = accuracy
        self.col = col
        self.asleep = False # skip turn
        self.poisoned = False # -hp over time
        self.blessed = False # +hp over time
        self.confused = False # can't choose turn
        self.frightened = False # run attempt each turn or nothing
        self.enranged = False # +damage and -accuracy
        self.focussed = False # +accuracy
        self.defended = False # ???
        self.empowered = False # +atk
        self.energized = False # +mag
        self.auto_battle = False
        self.location = '1-0' # see location dictionary in notes
        self.progress = progress
        if self.gender == 'Female':
            self.grammer = {'subjective':'she', 'objective':'her', 'possessive':'hers', 'reflexive':'herself'}
        else: 
            self.grammer = {'subjective':'he', 'objective':'him', 'possessive':'his', 'reflexive':'himself'}


    def attack(self, enemy, xp_thresholds):
        if self.auto_battle:

            if random.random() < self.accuracy:
                enemy.hp -= self.atk - random.randint(0, self.atk // 5)
                dprint(f'{self.name} attacks {enemy.name} for {self.atk} damage!')
                if enemy.is_alive():
                    dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
                else:
                    if enemy.has_phases:
                        enemy.next_phase(self)
                    else:
                        dprint(f'{self.name} has defeated {enemy.name}!')
                        self.gain_xp(enemy.xp, xp_thresholds)
                        self.gain_col(enemy.col)
                        enemy.drop(self)

            else:
                dprint(f'{self.name} misses their attack!')

        else:
            attack_value = attack_timing_window(enemy, self, self.accuracy)
            if attack_value > self.accuracy:
                enemy.hp -= self.atk - random.randint(0, self.atk // 5)
                dprint(f'{self.name} attacks {enemy.name} for {self.atk} damage!')
                if enemy.is_alive():
                    dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
                else:
                    dprint(f'{self.name} has defeated {enemy.name}!')
                    self.gain_xp(enemy.xp, xp_thresholds)
                    self.gain_col(enemy.col)
                    enemy.drop(self)

            else:
                dprint(f'{self.name} misses their attack!')

    def gain_xp(self, xp, xp_thresholds):
        dprint(f'{self.name} gained {xp} experience points, ')
        self.xp += xp
        for threshold in xp_thresholds:
            if self.xp >= threshold:
                self.level += 1
                dprint(f'{self.name} has leveled up to level {self.level}!')
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
            if enemy.is_alive():
                dprint(f'{enemy.name} is willing to keep going.')
            else:
                dprint(f'{enemy.name} is fed up with all these issues.')
    
    def special_attack():
        pass


class Fighter(Player):
    def __init__(self, name, gender, hp, atk, xp, level, accuracy, col, progress=0):
        super().__init__(name, gender, hp, atk, xp, level, accuracy, col, progress)
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
        self.allies = []

    def attack(self, enemy, xp_thresholds):
        if self.auto_battle:
            if random.random() < self.accuracy:
                if self.empowered:
                    damage = self.atk + random.randint(0, self.atk // 5)
                else:
                    damage = self.atk - random.randint(0, self.atk // 5)
                enemy.hp -= damage
                dprint(f'{self.name} attacks {enemy.name} for {damage} damage!')
                if enemy.is_alive():
                    dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
                else:
                    dprint(f'{self.name} has defeated {enemy.name}!')
                    self.gain_xp(enemy.xp, xp_thresholds)
                    self.gain_col(enemy.col)
                    enemy.drop(self)
            else:
                dprint(f'{self.name} misses their attack!')
        else:
            dprint('Ready?', .05)
            time.sleep(.75)
            input()
            attack_value = attack_timing_window(enemy, self, self.accuracy)
            if attack_value > self.accuracy:
                if self.empowered:
                    damage = self.atk + random.randint(0, self.atk // 5)
                else:
                    damage = self.atk - random.randint(0, self.atk // 5)
                enemy.hp -= damage
                dprint(f'{self.name} attacks {enemy.name} for {damage} damage!')
                if enemy.is_alive():
                    dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
                else:
                    if enemy.has_phases:
                        enemy.next_phase(self)
                    else:
                        dprint(f'{self.name} has defeated {enemy.name}!')
                        self.gain_xp(enemy.xp, xp_thresholds)
                        self.gain_col(enemy.col)
                        enemy.drop(self)
            else:
                dprint(f'{self.name} misses their attack!')

    def gain_xp(self, xp, xp_thresholds:dict):
        dprint(f'{self.name} gained {xp} experience points, ')
        self.xp += xp
        # level_key_to_remove = None
        for level_key, threshold in xp_thresholds.items():
            if self.xp >= threshold:
                self.level = level_key + 1
                ascci_fireworks()
                dprint(f'{self.name} has leveled up to level {self.level}!')
                self.level_up()
                level_key_to_remove = level_key
        try:
            xp_thresholds.pop(level_key_to_remove) # Remove the threshold we just crossed
        except UnboundLocalError as err:
            # print(f'it works to do nothing here : {err}')
            pass
        dprint(f'{self.name} now has {self.xp} xp. ')

    def level_up(self):
        self.maxhp += 5 + round(self.level * 1.025)
        self.atk += (self.level // 8) if self.level > 20 else 1 + (self.level // 5)
        self.accuracy += .0025 if self.accuracy < 1 else self.accuracy == 1
        self.hp += 5 + round(self.level * 1.025)
        self.skill_slots = 1 + int(math.log(self.level, 1.85))
        self.maxmag += 1 + (self.level // 40) if self.level % 5 == 0 else (self.level // 40)
        self.agi -= 1 if self.level % 12 == 0 else 0
        self.learn_skill()

    def special_attack(self, enemy, xp_thresholds):
        if self.mag <= 0:
            dprint('You\'re out of magic!')
            return self.attack(enemy, xp_thresholds)
        
        # update skill downtime (this method requires that all action methods need these lines at the begining)
        for skill in self.known_skills:
            if skill.downtime < skill.cooldown: # if downtime is less than cooldown
                skill.downtime += 1 # bring the 2 closer together

        # that way when this line comes along the number of usable skills is accurate
        skill = self.choose_skill([skill for skill in self.known_skills if skill.is_usable()])
        if skill == None:
            dprint('No skills to use.')
            for skill in self.known_skills:
                print(f'Skill: {skill.name}, cooldown: {skill.cooldown - skill.downtime} (turns remaining).')
            return self.attack(enemy, xp_thresholds)

        attack_value = 0.0

        if self.empowered:
            strong_damage = self.atk + (self.atk // 5) + skill.damage
            weak_damage = self.atk
        else:
            strong_damage = self.atk + random.randint(1, (self.atk // 5) + 1) + skill.damage # 272
            weak_damage = self.atk - random.randint(1, (self.atk // 5) + 1) # 180
        if self.auto_battle:
            self.mag -= skill.cost
            if random.random() < self.accuracy + self.acu:
                enemy.hp -= strong_damage
                skill.set_downtime() # downtime, to make sure the skills aren't used too fast. 
                dprint(f'{self.name} connects with the sword skill {skill.name}!')
                dprint(f'the attack hits {enemy.name} for {strong_damage} damage!')
                if enemy.is_alive():
                    dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
                else:
                    dprint(f'{skill.name} obliterated {enemy.name}!')
                    self.gain_xp(enemy.xp, xp_thresholds)
                    self.gain_col(enemy.col)
                    enemy.drop(self)
            elif random.random() < self.accuracy:
                enemy.hp -= weak_damage
                skill.set_downtime() # downtime
                dprint(f'{self.name} dealt a weak hit of the skill {skill.name}.')
                dprint(f'The attack dealt {weak_damage} damage to {enemy.name}.')
                if enemy.is_alive():
                    dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
                else:
                    dprint(f'Despite the weak hit with {skill.name}, {enemy.name} has died!')
                    self.gain_xp(enemy.xp, xp_thresholds)
                    self.gain_col(enemy.col)
                    enemy.drop(self)
            else:
                dprint(f'{self.name} executed the skill {skill.name} but missed! ')
                skill.set_downtime() # even though it was a miss, its still a use.

        else:
            dprint('ready?', .05)
            time.sleep(.75)
            input()
            attack_value = attack_timing_window(enemy, self, self.accuracy + self.acu)
            if attack_value > self.accuracy + self.acu: # TODO or 1 - attack_timer_score_thingy < self.accuracy + self.acu
                enemy.hp -= strong_damage
                skill.set_downtime() # downtime, to make sure the skills aren't used too fast. 
                dprint(f'{self.name} connects with the sword skill {skill.name}!')
                dprint(f'the attack hits {enemy.name} for {strong_damage} damage!')
                if enemy.is_alive():
                    dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
                else:
                    dprint(f'{skill.name} obliterated {enemy.name}!')
                    self.gain_xp(enemy.xp, xp_thresholds)
                    self.gain_col(enemy.col)
                    enemy.drop(self)
            elif attack_value > self.accuracy:
                enemy.hp -= weak_damage
                skill.set_downtime() # downtime
                dprint(f'{self.name} dealt a weak hit of the skill {skill.name}.')
                dprint(f'The attack dealt {weak_damage} damage to {enemy.name}.')
                if enemy.is_alive():
                    dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
                else:
                    dprint(f'Despite the weak hit with {skill.name}, {enemy.name} has died!')
                    self.gain_xp(enemy.xp, xp_thresholds)
                    self.gain_col(enemy.col)
                    enemy.drop(self)
            else:
                dprint(f'{self.name} executed the skill {skill.name} but missed! ')
                skill.set_downtime() # even though it was a miss, its still a use.

    def learn_skill(self):
        skills = init_skills()
        learnables = [skill for skill in skills if skill.level <= self.level and skill.type == 0]
        dprint('You have an available skill slot')
        while len(self.known_skills) < self.skill_slots: 
            dprint('would you like to learn or replace a skill?')
            lorp = ['learn', 'replace', 'nope'] # lorp: Learn or Replace
            for i in range(3):
                print(f'{i + 1}: {lorp[i]}')
            ans = input()
            if ans in ['0', '1', 'l', 'L', 'Learn', 'learn','LEARN']: # if learn new
                self.add_skill(learnables)
            elif ans in ['2', 'r', 'R', 'replace', 'Replace', 'repl', 'Repl','REPLACE','REPL']: # if replace known
                self.remove_skill()
                self.add_skill(learnables)
            elif ans in ['3','n','N','NO','no','No','nope','Nope','NOPE','4','absolutely not!']:
                dprint('Ok maybe next time!')
                break
            else:
                continue
    
    def remove_skill(self):
        skill_int = get_validated_input('Replace which skill? ', self.known_skills)
        self.known_skills.remove(self.known_skills[skill_int - 1]) # remove the chosen skill at valid position

    def add_skill(self, learnables):
        skill_int = get_validated_input('Add which skill', learnables)
        self.known_skills.append(learnables[skill_int - 1]) # append the selected choice to known skills
        dprint(f'{self.name} has learned the skill {self.known_skills[-1].name}!')

    def choose_skill(self, skills):
        if skills == []:
            return
        user = get_validated_input('Which skill do you want to use? ', skills)
        if user == None:
            return
        return skills[user - 1]
    
    def use_item(self, enemy, xp_thresholds):
        # Update skill downtime
        for skill in self.known_skills:
            if skill.downtime < skill.cooldown:
                skill.downtime += 1

        useables = [item for item in self.inventory.contents if item.can_use]
        if len(useables) != 0:
            list_int = get_validated_input('choose an item', useables)
            to_use = useables[list_int - 1]
            to_use.use(self, enemy, xp_thresholds)
            self.inventory.remove_item(to_use)
        else:
            dprint('Your inventory is empty. ')

    def run(self):
        # update skill downtime
        for skill in self.known_skills: 
            if skill.downtime < skill.cooldown:
                skill.downtime += 1

        small = int((self.accuracy * 100) + (20 - self.agi))
        big = int(80 + self.agi)
        if random.randint(0, small) > random.randint(0, big):
            return True
        return False
