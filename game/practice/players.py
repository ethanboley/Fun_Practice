
import random
import math
from actions import *
from things_stuff import init_skills, init_spalls, Inventory
from stuffs_that_do import init_spells, weapons


class Player:
    def __init__(self, name, gender, hp, atk, xp, level, accuracy, col,
                 location='1-1', progress=0, asleep=False, poisoned=False,
                 blessed=False, confused=False, frightened=False,
                 enraged=False, focused=False, defended=False,
                 empowered=False, weakened=False, energized=False,
                 auto_battle=False):
        self.name = name
        self.gender = gender
        self.maxhp = hp
        self.hp = hp
        self.atk = atk
        self.xp = xp
        self.level = level
        self.accuracy = accuracy
        self.col = col
        self.location = location # see location dictionary in notes
        self.progress = progress
        self.asleep = asleep # skip turn
        self.poisoned = poisoned # -hp over time
        self.blessed = blessed # +hp over time
        self.confused = confused # can't choose turn
        self.frightened = frightened # run attempt each turn or nothing
        self.enraged = enraged # +damage and -accuracy
        self.focused = focused # +accuracy
        self.defended = defended # ???
        self.empowered = empowered # +atk
        self.weakened = weakened # -atk
        self.energized = energized # +mag
        self.auto_battle = auto_battle
        if self.gender == 'Female':
            self.grammer = {'subjective':'she', 'objective':'her', 'possessive':'hers', 'reflexive':'herself'}
        else: 
            self.grammer = {'subjective':'he', 'objective':'him', 'possessive':'his', 'reflexive':'himself'}


    def attack(self, enemy, xp_thresholds):
        if self.auto_battle:
            hit_value = random.randint(0, 1000)
            if hit_value < self.accuracy:
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
            hit_value = attack_timing_window(enemy, self)
            if hit_value < self.accuracy:
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
        pass

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
    def __init__(self, name, gender, hp, atk, xp, level, accuracy, col,
                 location='1-1', progress=0, asleep=False, poisoned=False,
                 blessed=False, confused=False, frightened=False,
                 enraged=False, focused=False, defended=False,
                 empowered=False, weakened=False, energized=False,
                 auto_battle=False, title='Fighter', acu=60, agi=999, mag=10,
                 maxmag=None, skill_slots=1, known_skills=[], allies=[]):
        super().__init__(name, gender, hp, atk, xp, level, accuracy, col, location,
                         progress, asleep, poisoned, blessed, confused,
                         frightened, enraged, focused, defended, empowered,
                         weakened, energized, auto_battle)
        self.title = title
        self.acu = acu # attack acuracy modifier
        self.agi = agi # used for battle order like a speed stat (out of 20?)
        self.mag = mag # used to calculate skill cost
        self.total_points = 0
        self.points = 0
        self.hpp = 0
        self.atkp = 0
        self.acup = 0
        self.magp = 0
        self.agip = 0
        self.sklp = 0
        if maxmag == None:
            self.maxmag = self.mag
        else:
            self.maxmag = maxmag
        self.skill_slots = skill_slots
        self.known_skills = known_skills
        self.allies = allies
        self.skills = init_skills()
        if len(self.known_skills) == 0:
            self.known_skills.append(self.skills[0])
        else:
            self.known_skills=known_skills
        self.inventory = Inventory()
        self.weapon = weapons[0]
        self.armor = None
        self.defense = 0 # to be automatically adjusted with changes in self.armor
        # self.shield = None # introduced in kedren main

    def attack(self, enemy, xp_thresholds):
        if self.auto_battle:
            hit_value = random.random()
            if hit_value < self.accuracy:
                condition_modifier = self.get_cond_mod()
                crit = self.is_crit(hit_value)
                damage = damage_calculator(self.atk, self.level, power=0, f=self.weapon.force, d=enemy.defense, num_targets=1, crit=crit, special=False, condition=condition_modifier, other=1)
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
            hit_value = attack_timing_window(enemy, self)
            if hit_value < self.accuracy:
                condition_modifier = self.get_cond_mod()
                crit = self.is_crit(hit_value)
                damage = damage_calculator(self.atk, self.level, power=0, f=self.weapon.force, d=enemy.defense, num_targets=1, crit=crit, special=False, condition=condition_modifier, other=1)
                enemy.hp -= damage
                dprint(f'{self.name} attacks {enemy.name} for {damage} damage!')
                dprint('A critical hit!') if crit else print()
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
        for level_key, threshold in xp_thresholds.items():
            if self.xp >= threshold:
                if self.level < level_key + 1: # if there are ever xp related problems in the future, 
                    self.level = level_key + 1 # the big question here is the + 1 on the previous line
                    ascci_fireworks() # or just the logic in general within that conditional.
                    dprint(f'{self.name} has leveled up to level {self.level}!')
                    self.level_up()
                level_key_to_remove = level_key
        try:
            xp_thresholds.pop(level_key_to_remove)
        except UnboundLocalError as err:
            pass
        dprint(f'{self.name} now has {self.xp} xp. ')

    def level_up(self):
        hpp, atkp, acup, magp, agip, sklp = self.point_allocation()
        self.maxhp += 4 + round(1.03 ** self.level) + hpp #
        self.hp += 4 + round(1.03 ** self.level) + hpp #
        self.atk += (self.level // 8) + atkp if self.level > 20 else 1 + (self.level // 5) + atkp
        self.accuracy += 2 * acup if self.accuracy < 1000 else self.accuracy == 1000 #
        self.sklp += sklp #
        self.skill_slots = 1 + int(math.log(self.level, 1.85) + (self.sklp * 0.015)) #
        self.maxmag += 1 + (self.level // 40) + magp if self.level % 5 == 0 else (self.level // 40) + magp #
        self.agi -= 1 + agip if self.agi > 400 else ceil(agip / 1.5) #
        self.learn_skill()

    def point_allocation(self):
        self.points += 5 + (self.level // 10)
        self.total_points += 5 + (self.level // 10)
        allocations = {'Hit Points': 0, 'Attack Power': 0, 'Accuracy': 1,
                       'Magic': 0, 'Speed': 0, 'Skill Learn Rate': 0}

        dprint(f'You have {self.points} points to spend!')
        dprint(f'Choose wisely. You can\'t unspend points!')

        options = ['None this time', *allocations.keys()]

        # Display options
        for i, option in enumerate(options):
            print(f'{i}: {option}')

        # Spend points
        while self.points > 0:
            choice = input('Enter the number: ').strip()

            if not choice.isdigit():
                dprint('Invalid choice. Exiting allocation.')
                break

            choice = int(choice)
            if choice == 0:  # Exit if "None this time" is chosen
                break
            elif 1 <= choice <= len(allocations):
                key = list(allocations.keys())[choice - 1]
                allocations[key] += 1
                self.points -= 1
                dprint(f'Allocated 1 point to {key}. Points remaining: {self.points}')
            else:
                dprint('Invalid choice. Try again.')

        # Return allocated points as a tuple
        return tuple(allocations[key] for key in allocations)

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

        condition_modifier = self.get_cond_mod()
        if self.weakened:
            dprint('You can\'t use any skills right now.')
            return self.attack(enemy, xp_thresholds)
        if self.auto_battle:
            hit_value = random.randint(0, 1000)
            crit = self.is_crit(hit_value)
            self.mag -= skill.cost
            if hit_value < self.accuracy:
                strong_damage = damage_calculator(self.atk, level=self.level, power=skill.damage, f=self.weapon.force, d=enemy.defense, num_targets=1, crit=crit, special=True, condition=condition_modifier, other=1)
                enemy.hp -= strong_damage
                skill.set_downtime() # downtime, to make sure the skills aren't used too fast. 
                dprint(f'{self.name} connects with the sword skill {skill.name}!')
                dprint('A critical hit!') if crit else print()
                dprint(f'the attack hits {enemy.name} for {strong_damage} damage!')
                if enemy.is_alive():
                    dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
                else:
                    dprint(f'{skill.name} obliterated {enemy.name}!')
                    self.gain_xp(enemy.xp, xp_thresholds)
                    self.gain_col(enemy.col)
                    enemy.drop(self)
            elif hit_value < self.accuracy + self.acu:
                weak_damage = damage_calculator(self.atk, level=self.level, power=0, f=self.weapon.force, d=enemy.defense, num_targets=1, crit=crit, special=True, condition=condition_modifier, other=1)
                enemy.hp -= weak_damage
                skill.set_downtime() # downtime
                dprint(f'{self.name} dealt a weak hit of the skill {skill.name}.')
                dprint('A critical hit!') if crit else print()
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
            hit_value = attack_timing_window(enemy, self)
            crit = self.is_crit(hit_value)
            if hit_value < self.accuracy:
                strong_damage = damage_calculator(self.atk, level=self.level, power=skill.damage, f=self.weapon.force, d=enemy.defense, num_targets=1, crit=crit, special=True, condition=condition_modifier, other=1)
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
            elif hit_value < self.accuracy + self.acu:
                weak_damage = damage_calculator(self.atk, level=self.level, power=0, f=self.weapon.force, d=enemy.defense, num_targets=1, crit=crit, special=True, condition=condition_modifier, other=1)
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

    def is_crit(self, hit_val):
        # Calculate crit value based on conditions
        crit_val = (
            (2 if self.focused else 0) +
            (1 if self.enraged else 0) +
            (1 if self.blessed else 0) -
            (1 if self.confused else 0) +
            (1 if self.empowered else 0) -
            (2 if self.frightened else 0) -
            (1 if self.weakened else 0) +
            (1 if (self.accuracy + self.acu) / 8 > hit_val else 0) +
            (1 if hit_val <= 0.04 else 0))

        crit_thresholds = {0: 95, 1: 85, 2: 65, 3: 50}
        threshold = crit_thresholds.get(crit_val, 35)
        return random.randint(1, 100) > threshold if crit_val >= 0 else False

    def learn_skill(self):
        skills = init_skills()
        learnables = [skill for skill in skills if skill.level <= self.level and skill.type == 0]
        if len(self.known_skills) < self.skill_slots:
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
    
    def add_skill_by_name(self, skills, s_name):
        skill_names = [skill.name for skill in self.known_skills]
        if s_name not in skill_names:
            for skill in skills:
                if skill.name == s_name:
                    self.known_skills.append(skill)

    def add_ally_by_name(self, allies, a_des):
        a_dees = [ally.designation for ally in allies]
        if a_des not in a_dees:
            for ally in allies:
                if ally.designation == a_des:
                    self.allies.append(ally)
    
    def gain_xp_quietly(self, xp, xp_thresholds:dict):
        self.xp += xp

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

        small = int((self.accuracy / 10) + (1000 - self.agi))
        big = int(80 + self.agi)
        if random.randint(0, small) > random.randint(0, big):
            return True
        return False
    
    def get_cond_mod(self) -> float:
        if self.asleep:
            return 0

        modifier = 1.0

        if self.poisoned:
            modifier *= 0.95
        if self.blessed:
            modifier *= 1.1
        if self.confused:
            modifier *= 1.05
        if self.frightened:
            modifier *= 0.85
        if self.enraged:
            modifier *= 1.2
        if self.focused:
            modifier *= 1.35
        if self.defended:
            modifier *= 0.98
        if self.empowered:
            modifier *= 1.5
        if self.weakened:
            modifier *= 0.75
        if self.energized:
            modifier *= 1.05

        return modifier
