
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
        self.asleep = False # skip turn
        self.poisoned = False # -hp over time
        self.confused = False # can't choose turn
        self.frightened = False # run attempt each turn or nothing
        self.enranged = False # +damage and -accuracy
        self.blessed = False # +accuracy
        self.defended = False # ???
        self.empowered = False # +atk
        self.energized = False # +mag


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
        self.accuracy += .02 if self.accuracy <= 1 else self.accuracy == 1
        self.hp = self.maxhp
        self.skill_slots = 1 + int(math.log(self.level, 1.85))
        self.maxmag += 1 + (self.level // 40)
        self.agi -= (self.level // 16)
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
        strong_damage = self.atk + random.randint(1, (self.atk // 5) + 1) + skill.damage
        weak_damage = self.atk - random.randint(1, (self.atk // 5) + 1)
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
            if ans in ['', '0', '1', 'l', 'L', 'Learn', 'learn']: # if learn new
                self.add_skill(learnables)
            elif ans in ['2', 'r', 'R', 'replace', 'Replace', 'repl', 'Repl', '3']: # if replace known
                self.remove_skill()
                self.add_skill(learnables)
            else:
                dprint('Ok maybe next time!')
                break
    
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
    def __init__(self, name, hp, atk, xp, level, accuracy, col):
        super().__init__(name, hp, atk, xp, level, accuracy, col)
        self.title = 'Mage'
        self.acu = .05 # attack acuracy modifier
        self.agi = 20 # used for battle order like a speed stat (out of 20?)
        self.mag = 25 # used to calculate skill cost
        self.maxmag = self.mag
        self.mod = 1 + self.level // 4
        self.spell_slots = 1
        self.known_spells = []
        self.spells = init_skills()
        self.known_spells.append(self.spells[83])
        self.inventory = Inventory()
        self.allies = []

    def attack(self, enemy, xp_thresholds):
        if random.random() < self.accuracy:
            damage = self.atk - random.randint(1, self.atk // 4)
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
        self.maxhp += 3 + (self.level // 6)
        self.atk += (self.level // 5)
        self.accuracy += .02 if self.accuracy <= 1 else self.accuracy == 1
        self.hp = self.maxhp
        self.spell_slots = 1 + int(math.log(self.level, 1.5))
        self.maxmag += 2 + (self.level // 8)
        self.agi -= (self.level // 20)
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

        spell.effect(enemy, strong_damage, xp_thresholds, self)
        if not enemy.is_alive():
            self.gain_xp(enemy.xp, xp_thresholds)
            self.gain_col(enemy.col)
            enemy.drop(self)
        
        if spell.nature == 1: # healing
            dprint(f'A wave of healing energy surges through {self.name}')
            # dprint('Target\n1: Self\n2: ally')
            # user = input()
            # if user in ['2','a','A','Ally','ally','ALLY','friend']:
            #     pass
            # else
            self.hp += weak_damage
            if self.hp > self.maxhp:
                self.hp = (self.hp - self.maxhp) // 2 + self.hp
            dprint(f'{self.name} feels vitality returning.')
            display_health(self)

        elif spell.nature == 3: # escaping
            pass
    
    def learn_spell(self):
        spells = init_skills()
        learnables = [spell for spell in spells if spell.level <= self.level and spell.type == 1]
        while len(self.known_spells) < self.spell_slots:
            dprint('You have an available spell slot')
            dprint('would you like to learn or replace a spell?')
            lorp = ['learn', 'replace', 'nope'] # lorp: Learn or Replace
            for i in range(3):
                print(f'{i + 1}: {lorp[i]}')
            ans = input()
            if ans in ['', '0', '1', 'l', 'L', 'Learn', 'learn']: # if learn new
                self.add_spell(learnables)
            elif ans in ['2', 'r', 'R', 'replace', 'Replace', 'repl', 'Repl', '3']: # if replace known
                self.remove_spell()
                self.add_spell(learnables)
            else:
                dprint('Ok maybe next time!')
                break
    
    def remove_spell(self):
        dprint('Replace which spell? ') # ask
        spell_int = check_user_input('s',list=self.known_spells)
        self.known_spells.remove(self.known_spells[spell_int - 1]) # remove the chosen spell at valid position

    def add_spell(self, learnables):
        dprint('Add which spell? ') # ask
        spell_int = check_user_input('s',list=learnables)
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
    

class Pugilist(Player):
    def __init__(self, name, hp, atk, xp, level, accuracy, col):
        super().__init__(name, hp, atk, xp, level, accuracy, col)
        self.title = 'Pugilist'
        self.acu = .04 # attack acuracy modifier
        self.agi = 16 # used for battle order like a speed stat (out of 20?)
        self.mag = 10 # used to calculate skill cost
        self.maxmag = self.mag
        self.mod = 1 + self.level // 4
        self.skill_slots = 1
        self.known_skills = []
        self.skills = init_skills()
        self.known_skills.append(self.skills[83])
        self.inventory = Inventory()
        self.allies = []

    def attack(self, enemy, xp_thresholds):
        if random.random() < self.accuracy:
            damage = self.atk - random.randint(1, self.atk // 5)
            enemy.hp -= damage
            dprint(f"{self.name} hits {enemy.name} dealing {damage} damage!")
            if enemy.is_alive():
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
        self.maxhp += 4 + (self.level // 5)
        self.atk += 1 + (self.level // 5)
        self.accuracy += .03 if self.accuracy <= 1 else self.accuracy == 1
        self.hp = self.maxhp
        self.skill_slots = 1 + int(math.log(self.level, 1.7))
        self.maxmag += 1 + (self.level // 15)
        self.agi -= (self.level // 8)
        self.learn_skill()

    def special_attack(self, enemy, xp_thresholds):
        if self.mag <= 0:
            dprint('You\'re out of magic!')
            return 0
        skill = self.choose_skill()
        self.mag -= skill.cost
        strong_damage = self.atk + random.randint(1, (self.atk // 4) + 1) + skill.damage
        weak_damage = self.atk - random.randint(1, (self.atk // 4) + 1) + skill.damage
    
    def learn_skill(self):
        skills = init_skills()
        learnables = [skill for skill in skills if skill.level <= self.level and skill.type == 1]
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

    def choose_skill(self):
        dprint('which skill do you want to use? ')
        user = check_user_input('s',list=self.known_skills)
        return self.known_skills[user - 1]
    
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
        big = int(60 + self.agi)
        if random.randint(0, small) > random.randint(0, big):
            return True
        return False
