
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
        self.embalmed = False # +hp over time
        self.confused = False # can't choose turn
        self.frightened = False # run attempt each turn or nothing
        self.enranged = False # +damage and -accuracy
        self.blessed = False # +accuracy
        self.defended = False # ???
        self.empowered = False # +atk
        self.energized = False # +mag
        self.location = '1-0'
        self.progress = progress
        if self.gender == 'Female':
            self.grammer = {'subjective':'she', 'objective':'her', 'possessive':'hers', 'reflexive':'herself'}
        else: 
            self.grammer = {'subjective':'he', 'objective':'him', 'possessive':'his', 'reflexive':'himself'}


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
        else:
            dprint(f"{self.name} misses their attack!")
    
    def gain_xp(self, xp, xp_thresholds:dict):
        dprint(f'{self.name} gained {xp} experience points, ')
        self.xp += xp
        # level_key_to_remove = None
        for level_key, threshold in xp_thresholds.items():
            if self.xp >= threshold:
                self.level = level_key + 1
                dprint(f"{self.name} has leveled up to level {self.level}!")
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
            return
        
        # update skill downtime (this method requires that all action methods need these lines at the begining)
        for skill in self.known_skills:
            if skill.downtime < skill.cooldown: # if downtime is less than cooldown
                skill.downtime += 1 # bring the 2 closer together

        # that way when this line comes along the number of usable skills is accurate
        skill = self.choose_skill([skill for skill in self.known_skills if skill.is_usable()])
        if skill == None:
            dprint('No skills to use.')
            for skill in self.known_skills:
                print(f'Skill: {skill.name}, cooldown {skill.cooldown - skill.downtime} (turns remaining).')
            self.attack(enemy, xp_thresholds)
            return

        while not skill.is_usable():
            dprint('That skill is on cooldown.')
            skill = self.choose_skill([skill for skill in self.known_skills if skill.is_usable()])
        
        self.mag -= skill.cost
        strong_damage = self.atk + random.randint(1, (self.atk // 5) + 1) + skill.damage # 272
        weak_damage = self.atk - random.randint(1, (self.atk // 5) + 1) # 180
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


class Mage(Player):
    def __init__(self, name, gender, hp, atk, xp, level, accuracy, col):
        super().__init__(name, gender, hp, atk, xp, level, accuracy, col)
        self.title = 'Mage'
        self.acu = .05 # attack acuracy modifier
        self.agi = 20 # used for battle order like a speed stat (out of 20?)
        self.mag = 25 # used to calculate skill cost
        self.maxmag = self.mag
        self.mod = 1 + self.level // 4
        self.spell_slots = 1
        self.known_spells = []
        self.spells = init_spells()
        self.known_spells.append(self.spells[0])
        self.inventory = Inventory()
        self.allies = []

    def attack(self, enemy, xp_thresholds):
        if random.random() < self.accuracy:
            damage = self.atk - random.randint(0, self.atk // 4)
            enemy.hp -= damage
            dprint(f"{self.name} attacks {enemy.name} for {damage} damage!")
            if enemy.is_alive():
                dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
            else:
                dprint(f'{self.name} has defeated {enemy.name}!')
                self.gain_xp(enemy.xp, xp_thresholds)
                self.gain_col(enemy.col)
                enemy.drop(self)                
        else:
            dprint(f"{self.name} misses their attack!")
    
    def gain_xp(self, xp, xp_thresholds:dict):
        dprint(f'{self.name} gained {xp} experience points, ')
        self.xp += xp
        for level_key, threshold in xp_thresholds.items():
            if self.xp >= threshold:
                self.level = level_key
                dprint(f"{self.name} has leveled up to level {self.level}!")
                self.level_up()
                level_key_to_remove = level_key
        xp_thresholds.pop(level_key_to_remove)  # Remove the threshold we just crossed
        dprint(f'{self.name} now has {self.xp} xp. ')

    def level_up(self):
        self.maxhp += 3 + (self.level // 6)
        self.atk += (self.level // 5)
        self.accuracy += .0025 if self.accuracy < 1 else self.accuracy == 1
        self.hp = self.maxhp
        self.spell_slots = int(math.log(self.level + 6, 1.18) - 10)
        self.maxmag += 3 + (self.level // 6)
        self.agi -= ((self.level // 20) - 1)
        self.learn_spell()

    def special_attack(self, enemy, xp_thresholds):
        if self.mag <= 0:
            dprint('You\'re out of magic!')
            return
        # update spell cooldown
        for spell in self.known_spells:
            if spell.downtime < spell.cooldown:
                spell.downtime += 1

        spell = self.choose_spell([spell for spell in self.known_spells if spell.is_usable()])
        if spell == None:
            dprint('No spells to use.')
            for spell in self.known_spells:
                print(f'Spell: {spell.name}, cooldown {spell.cooldown - spell.downtime} (turns remaining).')
            self.attack(enemy, xp_thresholds)
            return

        self.mag -= spell.cost
        strong_damage = self.atk + random.randint(1, (self.atk // 4) + 1) + spell.damage
        weak_damage = self.atk - random.randint(1, (self.atk // 4) + 1) + spell.damage

        spell.effect(enemy, self, weak_damage=weak_damage, strong_damage=strong_damage)
        if not enemy.is_alive():
            self.gain_xp(enemy.xp, xp_thresholds)
            self.gain_col(enemy.col)
            enemy.drop(self)

        elif spell.nature == 3: # escaping
            pass
    
    def learn_spell(self):
        spells = init_spells()
        learnables = [spell for spell in spells if spell.level <= self.level and spell.type == 1]
        while len(self.known_spells) < self.spell_slots:
            dprint('You have an available spell slot')
            dprint('would you like to learn or replace a spell?')
            lorp = ['learn', 'replace', 'nope'] # lorp: Learn or Replace
            for i in range(3):
                print(f'{i + 1}: {lorp[i]}')
            ans = input()
            if ans in ['0', '1', 'l', 'L', 'Learn', 'learn']: # if learn new
                self.add_spell(learnables)
            elif ans in ['2', 'r', 'R', 'replace', 'Replace', 'repl', 'Repl']: # if replace known
                self.remove_spell()
                self.add_spell(learnables)
            else:
                dprint('Ok maybe next time!')
                break
    
    def remove_spell(self):
        # dprint('Replace which spell? ') # ask
        spell_int = get_validated_input('replace which spell?', self.known_spells)
        self.known_spells.remove(self.known_spells[spell_int - 1]) # remove the chosen spell at valid position

    def add_spell(self, learnables):
        # dprint('Add which spell? ') # ask
        spell_int = get_validated_input('Add which spell?', learnables)
        self.known_spells.append(learnables[spell_int - 1]) # append the selected choice to known spells
        dprint(f'{self.name} has learned the spell {self.known_spells[-1].name}!')

    def choose_spell(self, spells):
        user = get_validated_input('Which spell do you want to use? ', spells)
        if user == None:
            return
        return self.known_spells[user - 1]
    
    def use_item(self, enemy, xp_thresholds):
        useables = [item for item in self.inventory.contents if item.can_use]
        if len(useables) != 0:
            list_int = get_validated_input('Which item?', list=useables)
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
    

class Pugilist(Player):
    def __init__(self, name, gender, hp, atk, xp, level, accuracy, col):
        super().__init__(name, gender, hp, atk, xp, level, accuracy, col)
        self.title = 'Pugilist'
        self.acu = .04 # attack acuracy modifier
        self.agi = 18 # used for battle order like a speed stat (out of 20?)
        self.mag = 10 # used to calculate skill cost
        self.maxmag = self.mag
        self.mod = 1 + self.level // 4
        self.spall_slots = 1
        self.known_spalls = []
        self.spalls = init_spalls()
        self.known_spalls.append(self.spalls[0])
        self.inventory = Inventory()
        self.allies = []

    def attack(self, enemy, xp_thresholds):
        if random.random() < self.accuracy:
            damage = self.atk - random.randint(0, self.atk // 5)
            enemy.hp -= damage
            dprint(f'{self.name} hits {enemy.name} dealing {damage} damage!')
            if enemy.is_alive():
                dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
            else:
                dprint(f'{self.name} has defeated {enemy.name}!')
                self.gain_xp(enemy.xp, xp_thresholds)
                self.gain_col(enemy.col)
                enemy.drop(self)
        else:
            dprint(f"{self.name} misses their attack!")
    
    def gain_xp(self, xp, xp_thresholds:dict):
        dprint(f'{self.name} gained {xp} experience points, ')
        self.xp += xp
        for level_key, threshold in xp_thresholds.items():
            if self.xp >= threshold:
                self.level = level_key
                dprint(f"{self.name} has leveled up to level {self.level}!")
                self.level_up()
                level_key_to_remove = level_key
        xp_thresholds.pop(level_key_to_remove)  # Remove the threshold we just crossed
        dprint(f'{self.name} now has {self.xp} xp. ')

    def level_up(self):
        self.maxhp += 4 + (self.level // 5)
        self.atk += 1 + (self.level // 5)
        self.accuracy += .004 if self.accuracy < 1 else self.accuracy == 1
        self.hp = self.maxhp
        self.spall_slots = 1 + int(math.log(self.level, 1.7))
        self.maxmag += 1 + (self.level // 15)
        self.agi -= ((self.level // 8) - 1)
        self.learn_spall()

    def special_attack(self, enemy, xp_thresholds):
        if self.mag <= 0:
            dprint('You\'re out of magic!')
            return
        
        # update spall downtime (this method requires that all action methods need these lines at the begining)
        for spall in self.known_spalls:
            if spall.downtime < spall.cooldown: # if downtime is less than cooldown
                spall.downtime += 1 # bring the 2 closer together

        # that way when this line comes along the number of usable spalls is accurate
        spall = self.choose_spall([spall for spall in self.known_spalls if spall.is_usable()])
        if spall == None:
            dprint('No spalls to use.')
            for spall in self.known_spalls:
                print(f'spall: {spall.name}, cooldown {spall.cooldown - spall.downtime} (turns remaining).')
            self.attack(enemy, xp_thresholds)
            return

        while not spall.is_usable():
            dprint('That spall is on cooldown.')
            spall = self.choose_spall([spall for spall in self.known_spalls if spall.is_usable()])
        
        self.mag -= spall.cost
        strong_damage = self.atk + random.randint(1, (self.atk // 5) + 1) + spall.damage
        weak_damage = self.atk - random.randint(1, (self.atk // 5) + 1)
        if random.random() < self.accuracy + self.acu:
            enemy.hp -= strong_damage
            spall.set_downtime() # downtime, to make sure the spalls aren't used too fast. 
            dprint(f'{self.name} connects with the sword spall {spall.name}!')
            dprint(f'the attack hits {enemy.name} for {strong_damage} damage!')
            if enemy.is_alive():
                dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
            else:
                dprint(f'{spall.name} obliterated {enemy.name}!')
                self.gain_xp(enemy.xp, xp_thresholds)
                self.gain_col(enemy.col)
                enemy.drop(self)
        elif random.random() < self.accuracy:
            enemy.hp -= weak_damage
            spall.set_downtime() # downtime
            dprint(f'{self.name} dealt a weak hit of the spall {spall.name}.')
            dprint(f'The attack dealt {weak_damage} damage to {enemy.name}.')
            if enemy.is_alive():
                dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
            else:
                dprint(f'Despite the weak hit with {spall.name}, {enemy.name} has died!')
                self.gain_xp(enemy.xp, xp_thresholds)
                self.gain_col(enemy.col)
                enemy.drop(self)
        else:
            dprint(f'{self.name} executed the spall {spall.name} but missed! ')
            spall.set_downtime() # even though it was a miss, its still a use. 
    
    def learn_spall(self):
        spalls = init_spalls()
        learnables = [spall for spall in spalls if spall.level <= self.level and spall.type == 1]
        while len(self.known_spalls) < self.spall_slots:
            dprint('You have an available spall slot')
            dprint('would you like to learn or replace a spall?')
            lorp = ['learn', 'replace', 'nope'] # lorp: Learn or Replace
            for i in range(3):
                print(f'{i + 1}: {lorp[i]}')
            ans = input()
            if ans in ['0', '1', 'l', 'L', 'Learn', 'learn']: # if learn new
                self.add_spall(learnables)
            elif ans in ['2', 'r', 'R', 'replace', 'Replace', 'repl', 'Repl', '3']: # if replace known
                self.remove_spall()
                self.add_spall(learnables)
            else:
                dprint('Ok maybe next time!')
                break
    
    def remove_spall(self):
        spall_int = get_validated_input('Replace which spall? ',self.known_spalls)
        self.known_spalls.remove(self.known_spalls[spall_int - 1]) # remove the chosen spall at valid position

    def add_spall(self, learnables):
        spall_int = get_validated_input('Add which spall? ',learnables)
        self.known_spalls.append(learnables[spall_int - 1]) # append the selected choice to known spalls
        dprint(f'{self.name} has learned the spall {self.known_spalls[-1].name}!')

    def choose_spall(self, spalls):
        user = get_validated_input('Which spall do you want to use? ', spalls)
        if user == None:
            return
        return spalls[user - 1]
    
    def use_item(self, enemy, xp_thresholds):
        useables = [item for item in self.inventory.contents if item.can_use]
        if len(useables) != 0:
            list_int = get_validated_input('',useables)
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
        big = int(60 + self.agi)
        if random.randint(0, small) > random.randint(0, big):
            return True
        return False

