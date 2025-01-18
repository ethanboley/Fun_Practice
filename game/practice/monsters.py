
import random
from actions import *
from stuffs_that_do import init_items, SpellAttack, Healing


drops = init_items()

class Doctor:
    def __init__(self, name, hp, heal, xp, level, accuracy):
        self.name = name
        self.hp = hp
        self.heal = heal
        self.xp = xp
        self.level = level
        self.accuracy = accuracy

    def attack(self, player):
        if random.random() < self.accuracy:
            player.hp += self.heal
            dprint(f"{self.name} heals {player.name} for {self.heal} hp!")
        else:
            dprint(f"{self.name} has no clue how to fix {player.name}\'s injury!")
    
    def is_alive(self):
        return self.hp > 0


class Enemy:
    def __init__(self, name, malice, hp, atk, xp, level, accuracy, col, agi, defense, force, world, ac):
        self.name = name
        self.malice = malice
        self.hp = hp
        self.atk = atk
        self.xp = xp
        self.level = level
        self.accuracy = accuracy
        self.col = col
        self.agi = agi
        self.defense = defense
        self.force = force
        self.world = world
        self.ac = ac
        self.has_phases = False

    def attack(self, target):
        hit_value = random.randint(0,1000)
        if target == None:
            pass
        elif hit_value < self.accuracy:
            damage = damage_calculator(self.atk, self.level, f=self.force, d=target.defense, num_targets=1, mon=self.malice)
            target.hp -= damage
            dprint(f'{self.name} attacks {target.name} for {damage} damage!')
            if target.is_alive():
                display_health(target)
            else:
                if isinstance(target, Ally):
                    dprint(f'{target.name} is unable to battle!')
                else:
                    dprint(f'{target.name} has died!')
        else:
            dprint(f'{self.name} misses their attack!')
    
    def choose_target(self, targets:list):
        if len(targets):
            return random.choice(targets)
        else:
            return None

    def is_alive(self):
        return self.hp > 0
    
    def drop(self, player):
        pass


class Ally:
    def __init__(self, name, level, hp, atk, agi, acu, defense, force, skill, designation=None) -> None:
        self.name = name
        self.level = level
        self.maxhp = hp
        self.hp = hp
        self.atk = atk
        self.agi = agi
        self.acu = acu
        self.defense = defense
        self.force = force
        self.skill = skill
        self.cooldown = 0
        if designation == None:
            self.designation = self.name
        else:
            self.designation = designation

    def choose_target(self, targets:list):
        if len(targets):
            return random.choice(targets)
        else: 
            return None
    
    def take_turn(self, target, player):
        if self.cooldown > 0:
            available_options = ['attack']
        else:
            available_options = ['attack','special attack','special attack']

        op = random.choice(available_options)
        if op == 'attack':
            self.attack(target)
        elif op == 'special attack':
            self.special_attack(target, player)

    def attack(self, target):
        hit_value = random.randint(0, 1000)
        if hit_value < self.acu:
            crit = random.random() > .85
            damage = damage_calculator(self.atk, level=self.level, f=self.force, d=target.defense, crit=crit)
            target.hp -= damage
            dprint(f'{self.name} attacks {target.name} for {damage} damage!')
            if target.is_alive():
                dprint(f'{target.name} has {target.hp} hp remaining.')
            else:
                dprint(f'{self.name} has defeated {target.name}!')

        else:
            dprint(f"{self.name} misses their attack!")
        self.cooldown -= 1

    def special_attack(self, target, player):
        if self.skill.type == 0: # if its a skill
            crit = random.random() > .85
            damage = damage_calculator(self.atk, level=self.level, power=self.skill.damage, f=self.force, d=target.defense, num_targets=1, crit=crit, special=True)
            if self.cooldown <= 0:
                hit_value = random.randint(0, 1000)
                active_damage = damage if hit_value < self.acu else (damage // 4) + 1
                target.hp -= active_damage
                dprint(f'{self.name} used {self.skill.name} and dealt {active_damage} damage to {target.name}!')
                if target.is_alive():
                    dprint(f'{target.name} has {target.hp} hp remaining.')
                else:
                    dprint(f'{self.name} has defeated {target.name}!')
        
        elif self.skill.type == 1: # if its a spell
            crit = random.random() > .85
            damage = damage_calculator(self.atk, level=self.level, power=self.skill.damage, f=self.force, d=target.defense, num_targets=1, crit=crit, special=True)
            if self.skill.nature == 0: # if its a spellattack
                pass # keep target the same
                if self.cooldown <= 0:
                    hit_value = random.randint(0, 1000)
                    active_damage = damage if hit_value < self.acu else (damage // 4) + 1
                    target.hp -= active_damage
                    dprint(f'{self.name} used {self.skill.name} and dealt {active_damage} damage to {target.name}!')
                    if target.is_alive():
                        dprint(f'{target.name} has {target.hp} hp remaining.')
                    else:
                        dprint(f'{self.name} has defeated {target.name}!')

            elif self.skill.nature == 1: # if its a healing spell
                own_allies = [ally for ally in player.allies]
                own_allies.append(player)
                target = random.choice(own_allies)
                if self.cooldown <= 0:
                    active_damage = damage if random.random() < self.acu else (damage // 4) + 1
                    target.hp += active_damage
                    dprint(f'{self.name} healed {target.name}!')
        
        elif self.skill.type == 2: # spall
            crit = random.random() > .8
            damage = damage_calculator(self.atk, level=self.level, power=self.skill.damage, f=self.force, d=target.defense, num_targets=1, crit=crit, special=True)
            if self.cooldown <= 0:
                hit_value = random.randint(0, 1000)
                active_damage = damage if hit_value < self.acu else (damage // 4) + 1
                target.hp -= active_damage
                dprint(f'{self.name} used {self.skill.name} dealing {active_damage} damage to {target.name}!')
                if target.is_alive():
                    dprint(f'{target.name} is left with {target.hp} hp.')
                else:
                    dprint(f'{self.name} pulverized {target.name} with {self.skill.name}!')

        self.cooldown += 4
            
    def is_alive(self):
        return self.hp > 0


class Boss:
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        self.name = name
        self.malice = malice
        self.maxhp = hp
        self.hp = hp
        self.atk = atk
        self.xp = xp
        self.level = level
        self.acu = acu
        self.col = col
        self.agi = agi
        self.defense = defense
        self.force = force
        self.world = world
        self.ac = ac
        self.has_phases = True
        self.phases = 0
    
    def attack(self, player):
        hit_value = random.randint(0,1000)
        if hit_value < self.acu:
            damage = damage_calculator(self.atk, level=self.level, f=self.force, d=player.defense, mon=self.malice)
            player.hp -= damage
            dprint(f'{player.name} is hit for {damage} damage from {self.name}\'s attack!')
            if player.is_alive():
                dprint(f'{player.name} takes the hit like a boss!')
                display_health(player)
            else:
                dprint(f'{player.name} was slain at the hand of {self.name}!')
        else:
            dprint(f'{self.name} attacks but misses {player.name}!')
    
    def choose_target(self, targets:list):
        if len(targets):
            return random.choice(targets)
        else:
            return None

    def is_alive(self):
        return self.hp > 0 or self.phases > 0


# ----------- Bosses

class BossTest(Boss):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.acu_mod = .02
        self.title = 'Bane of the Programmer'
        self.phases = 2
    
    def fight(self, player):
        if self.phases == 2:
            if random.randint(0,2):
                self.attack(player)
        elif self.phases == 1:
            if random.randint(0,1):
                self.big_attack(player)
        
    def big_attack(self, player):
        can_use = random.randint(1,2) in [1]
        if can_use:
            strong_damage = damage_calculator(self.atk, level=self.level, power=6, f=self.force, d=player.defense, special=True, mon=100)
            weak_damage = damage_calculator(self.atk, level=self.level, f=self.force, d=player.defense, mon=100)
            hit_value = random.randint(0, 1000)
            if hit_value < self.acu:
                player.hp -= strong_damage
                dprint(f'{self.name} {self.title} big attack {player.name} with big attackness!')
                dprint(f'the attack hits {player.name} for {strong_damage} damage!')
                if player.is_alive():
                    display_health(player)
                else:
                    dprint(f'The big attack kilt {player.name}!')
            elif hit_value < self.acu + self.acu_mod:
                player.hp -= weak_damage
                dprint(f'{self.name} just grazed {player.name}!')
                dprint(f'the big attack dealt {weak_damage} damage to {player.name}.')
                if player.is_alive():
                    display_health(player)
                else:
                    dprint(f'It was still too much for {player.name}')
            else:
                dprint(f'{self.name} missed!')
        else:
            dprint(f'{self.name} looks a little tired after its last attack.')

    def next_phase(self, player, dialogues:list):
        if self.phases > 0:
            self.phases -= 1
            self.hp = self.maxhp
            dialogues.pop()
        else:
            dprint(f'CONGRADULATIONS!!! {player.name} defeated {self.name} {self.title}')


class Kosaur(Boss):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac) -> None:
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.acu_mod = .02
        self.title = 'Scourge of the Kobold Canyon'
        self.phases = 2
    
    def fight(self, player):
        if self.phases == 2:
            if random.randint(0,2):
                self.attack(player)
            else:
                self.bite(player)
        elif self.phases == 1:
            if random.randint(0,1):
                self.attack(player)
            elif random.randint(0,1):
                self.claw(player)
            else:
                self.bite(player)
    
    def claw(self, player):
        can_use = random.randint(1,5) in [3, 4, 5]
        if can_use:
            power = random.randint(-2, (self.atk // 3)) + 6
            strong_damage = damage_calculator(self.atk, level=self.level, power=power, f=self.force, d=player.defense, special=True, mon=self.malice)
            weak_damage = damage_calculator(self.atk, level=self.level, f=self.force, d=player.defense, mon=self.malice)
            hit_value = random.randint(0, 1000)
            if hit_value < self.acu:
                player.hp -= strong_damage
                dprint(f'{self.name} {self.title} slashes {player.name} with it\'s steel claws!')
                dprint(f'the attack hits {player.name} for {strong_damage} damage!')
                if player.is_alive():
                    display_health(player)
                else:
                    dprint(f'The claws split {player.name} in two!')
            elif hit_value < self.acu + self.acu_mod:
                player.hp -= weak_damage
                dprint(f'{self.name} just grazed {player.name}!')
                dprint(f'the swipe dealt {weak_damage} damage to {player.name}.')
                if player.is_alive():
                    display_health(player)
                else:
                    dprint(f'It was still too much for {player.name}')
            else:
                dprint(f'{self.name} took a swing at {player.name} but missed!')
        else:
            dprint(f'{self.name} looks a little tired after its last attack.')

    def bite(self, player):
        can_use = random.randint(1,3) in [2, 3]
        if can_use:
            power = random.randint(1, self.atk + 1) + 2
            strong_damage = damage_calculator(self.atk, level=self.level, power=power, f=self.force, d=player.defense, special=True, mon=self.malice)
            weak_damage = damage_calculator(self.atk, level=self.level, f=self.force, d=player.defense, mon=self.malice)
            hit_value = random.randint(0, 1000)
            if hit_value < self.acu:
                player.hp -= strong_damage
                dprint(f'{self.title} attacks with it\'s massive jaws!')
                dprint(f'the attack hits {player.name} for {strong_damage} damage!')
                if player.is_alive():
                    display_health(player)
                else:
                    dprint(f'{player.name} was eaten alive!')
            elif hit_value < self.acu + self.acu_mod:
                player.hp -= weak_damage
                dprint(f'{self.name} just got a bit of {player.name}')
                dprint(f'the attack dealt {weak_damage} damage to {player.name}.')
                if player.is_alive():
                    display_health(player)
                else:
                    dprint(f'but that was all {player.name} could take!')
            else:
                dprint(f'{self.name} tried to eat {player.name} but missed!')
        else:
            dprint(f'{self.name} looks a little tired after its last attack.')
        
    def next_phase(self, player, dialogues:list):
        if self.phases > 0:
            self.phases -= 1
            self.hp = self.maxhp
            dialogues.pop()
        else:
            dprint(f'CONGRADULATIONS!!! {player.name} defeated {self.name} {self.title}')


class Illfang(Boss):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac) -> None:
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.acu_mod = .03
        self.title = 'the Kobold Lord'
        self.phases = 2
    
    def fight(self, player):
        if self.phases == 2:
            if random.randint(0,2):
                self.attack(player)
            else:
                self.talwar(player)
        elif self.phases == 1:
            if random.randint(0,1):
                self.attack(player)
            else:
                self.odachi(player)

    def talwar(self, player):
        can_use = random.randint(0,5) in [2, 3, 4, 5]
        if can_use:
            power = random.randint(-1, (self.atk // 2)) + 10
            hit_value = random.randint(0, 1000)
            crit = hit_value < 250
            strong_damage = damage_calculator(self.atk, level=self.level, power=power, f=self.force, d=player.defense, crit=crit, special=True, mon=self.malice)
            weak_damage = damage_calculator(self.atk, level=self.level, f=self.force, d=player.defense, crit=crit, mon=self.malice)
            if hit_value < self.acu:
                player.hp -= strong_damage
                dprint(f'{self.title} slashes {player.name} with his Talwar!')
                dprint(f'the attack hits {player.name} for {strong_damage} damage!')
                if player.is_alive():
                    display_health(player)
                else:
                    dprint(f'The talwar splits {player.name} in two!')
            elif hit_value < self.acu + self.acu_mod:
                player.hp -= weak_damage
                dprint(f'{self.name} just grazed {player.name} for {weak_damage} damage!')
                if player.is_alive():
                    display_health(player)
                else:
                    dprint(f'It was still too much for {player.name}!')
            else:
                dprint(f'{self.name} took a swing at {player.name} but missed!')
        else:
            dprint(f'{self.name} looks a little tired after its last attack.')
            dprint('time for a counter attack!')

    def odachi(self, player):
        can_use = random.randint(0,3) in [1,2,3]
        if can_use:
            power = random.randint(1, self.atk + 2) + 12
            hit_value = random.randint(0, 1000)
            crit = hit_value < 225
            strong_damage = damage_calculator(self.atk, level=self.level, power=power, f=self.force, d=player.defense, crit=crit, special=True, mon=self.malice)
            weak_damage = damage_calculator(self.atk, level=self.level, f=self.force, d=player.defense, crit=crit, mon=self.malice)
            if hit_value < self.acu:
                player.hp -= strong_damage
                dprint(f'{self.title} attacks with his Odachi!')
                dprint(f'the attack hits {player.name} for {strong_damage} damage!')
                if player.is_alive():
                    display_health(player)
                else:
                    dprint(f'{player.name} was sliced into a hundred tiny pieces!')
            elif hit_value < self.acu + self.acu_mod:
                player.hp -= weak_damage
                dprint(f'{self.name} just got a bit of {player.name} dealing {weak_damage} damage.')
                if player.is_alive():
                    display_health(player)
                else:
                    dprint(f'but that was all {player.name} could take!')
            else:
                dprint(f'{self.name} took a swing {player.name} but missed!')
        else:
            dprint(f'{self.name} looks a little tired after its last attack.')
            dprint('now\'s your chance to strike back hard!')

    def next_phase(self, player, dialogues:list):
        if self.phases > 0:
            self.phases -= 1
            self.hp = self.maxhp
            dialogues.pop()
            self.force += 15
        else:
            dprint('. . . . . ', .06)


class Barran(Boss):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.acu_mod = .03
        self.title = 'the General Tarus'

    def lance():
        pass


class Asterios(Boss):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.acu_mod = .04
        self.title = 'the Tarus King'

    def mace():
        pass


# ----------- Monsters


class Beastoid(Enemy):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.possible_drops = [drop for drop in drops if drop.name in
                               ['col coin', 'mundane scrap metal',
                                'glass bottle', 'onix stone', 'opal', 'grand col']]

    def create_loot_table(self):
        drop_list = [] # define returnable list
        drop_list.append(self.possible_drops[0]) # add default [col coin]
        if self.level > 1 and random.randint(0, 10) > self.possible_drops[1].rarity:
            drop_list.append(self.possible_drops[1])
            if self.level > 3 and random.randint(0, 10) > self.possible_drops[2].rarity:
                drop_list.append(self.possible_drops[2])
                if self.level > 8 and random.randint(0, 10) > self.possible_drops[4].rarity:
                    drop_list.append(self.possible_drops[4])
            elif self.level > 3 and random.randint(0, 10) > self.possible_drops[3].rarity:
                drop_list.append(self.possible_drops[3])
        if self.level > 20 and random.randint(0, 10) > self.possible_drops[5].rarity:
            drop_list.append(self.possible_drops[5])
        return drop_list
    
    def drop(self, player):
        dropses = self.create_loot_table()
        if not len(dropses) == 0:
            dprint(f'{player.name} got the following items')
            for drop in dropses:
                print(drop.name)
                player.inventory.add_item(drop)


class Koboldoid(Enemy):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.possible_drops = [drop for drop in drops if drop.name in
                               ['col coin', 'glass bottle', 'little dagger', 'onix stone']]
        
    def create_loot_table(self):
        drop_list = [] # define returnable list
        drop_list.append(self.possible_drops[0]) # add default [col coin]
        if self.level > 1 and random.randint(0, 10) > self.possible_drops[1].rarity:
            drop_list.append(self.possible_drops[1])
            if self.level > 3 and random.randint(0, 10) > self.possible_drops[2].rarity:
                drop_list.append(self.possible_drops[2])
                if self.level > 15 and random.randint(0, 10) > self.possible_drops[3].rarity:
                    drop_list.append(self.possible_drops[3])
        return drop_list
    
    def drop(self, player):
        dropses = self.create_loot_table()
        if not len(dropses) == 0:
            dprint(f'{player.name} got the following items')
            for drop in dropses:
                print(drop.name)
                player.inventory.add_item(drop)


class Humanoid(Enemy):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.possible_drops = [drop for drop in drops if drop.name in
                               ['col coin', 'glass bottle', 'simple fabric', 'venom glass', 
                                'onix stone', 'life potion']]
        
    def create_loot_table(self):
        drop_list = [] # define returnable list
        drop_list.append(self.possible_drops[0]) # add default [col coin]
        if self.level > 1 and random.randint(0, 10) > self.possible_drops[1].rarity:
            drop_list.append(self.possible_drops[1])
            if self.level > 3 and random.randint(0, 10) > self.possible_drops[2].rarity:
                drop_list.append(self.possible_drops[2])
                if self.level > 8 and random.randint(0, 10) > self.possible_drops[3].rarity:
                    drop_list.append(self.possible_drops[3])
                    if self.level > 13 and random.randint(0, 10) > self.possible_drops[4].rarity:
                        drop_list.append(self.possible_drops[4])
                        if self.level > 17 and random.randint(0, 10) > self.possible_drops[5].rarity:
                            drop_list.append(self.possible_drops[5])
        return drop_list
    
    def drop(self, player):
        dropses = self.create_loot_table()
        if not len(dropses) == 0:
            dprint(f'{player.name} got the following items')
            for drop in dropses:
                print(drop.name)
                player.inventory.add_item(drop)


class Plant(Enemy):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.possible_drops = [drop for drop in drops if drop.name in
                               ['living wood', 'aged teak log', 'droplet of villi'
                                'nawsoth fruit']]
        
    def create_loot_table(self):
        drop_list = [] # define returnable list
        if self.level > 0 and random.randint(0, 10) > self.possible_drops[0].rarity:
            drop_list.append(self.possible_drops[0])
            if self.level > 3 and random.randint(0, 10) > self.possible_drops[1].rarity:
                drop_list.append(self.possible_drops[1])
                if self.level > 9 and random.randint(0, 10) > self.possible_drops[2].rarity:
                    drop_list.append(self.possible_drops[2])
                    if self.level > 15 and random.randint(0, 10) > self.possible_drops[3].rarity:
                        drop_list.append(self.possible_drops[3])
        return drop_list
    
    def drop(self, player):
        dropses = self.create_loot_table()
        if not len(dropses) == 0:
            dprint(f'{player.name} got the following items')
            for drop in dropses:
                print(drop.name)
                player.inventory.add_item(drop)


class Nepenth(Enemy):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.possible_drops = [drop for drop in drops if drop.name in
                               ['living wood', 'monster tooth', 'nepenth fruit',
                                'nepenths ovule', 'droplet of villi', 'ooze jelly']]
        
    def create_loot_table(self):
        drop_list = [] # define returnable list
        if self.level > 0 and random.randint(0, 10) > self.possible_drops[0].rarity:
            drop_list.append(self.possible_drops[0])
            if self.level > 3 and random.randint(0, 10) > self.possible_drops[1].rarity:
                drop_list.append(self.possible_drops[1])
                if self.level > 9 and random.randint(0, 10) > self.possible_drops[2].rarity:
                    drop_list.append(self.possible_drops[2])
                    if self.level > 15 and random.randint(0, 10) > self.possible_drops[3].rarity:
                        drop_list.append(self.possible_drops[3])
                        if self.level > 17 and random.randint(0, 10) > self.possible_drops[4].rarity:
                            drop_list.append(self.possible_drops[4])
                            if self.level > 21 and random.randint(0, 10) > self.possible_drops[5].rarity:
                                drop_list.append(self.possible_drops[5])
        return drop_list
    
    def drop(self, player):
        dropses = self.create_loot_table()
        if not len(dropses) == 0:
            dprint(f'{player.name} got the following items')
            for drop in dropses:
                print(drop.name)
                player.inventory.add_item(drop)


class Beast(Enemy):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.possible_drops = [drop for drop in drops if drop.name in
                               ['mundane organ', 'monster tooth', 'hide']]
        
    def create_loot_table(self):
        drop_list = [] # define returnable list
        if self.level > 1 and random.randint(0, 10) > self.possible_drops[0].rarity:
            drop_list.append(self.possible_drops[0])
            if self.level > 2 and random.randint(0, 10) > self.possible_drops[1].rarity:
                drop_list.append(self.possible_drops[1])
                if self.level > 5 and random.randint(0, 10) > self.possible_drops[2].rarity:
                    drop_list.append(self.possible_drops[2])
        return drop_list
    
    def drop(self, player):
        dropses = self.create_loot_table()
        if not len(dropses) == 0:
            dprint(f'{player.name} got the following items')
            for drop in dropses:
                print(drop.name)
                player.inventory.add_item(drop)


class Worm(Enemy):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.possible_drops = [drop for drop in drops if drop.name in
                               ['prostomium', 'ooze jelly']]
        
    def create_loot_table(self):
        drop_list = [] # define returnable list
        if self.level > 0 and random.randint(0, 10) > self.possible_drops[0].rarity:
            drop_list.append(self.possible_drops[0])
            if self.level > 15 and random.randint(0, 10) > self.possible_drops[1].rarity:
                drop_list.append(self.possible_drops[1])
        return drop_list

    def drop(self, player):
        dropses = self.create_loot_table()
        if not len(dropses) == 0:
            dprint(f'{player.name} got the following items')
            for drop in dropses:
                print(drop.name)
                player.inventory.add_item(drop)


class Slime(Enemy):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.possible_drops = [drop for drop in drops if drop.name in
                               ['slime jelly', 'slime membrane', 'ooze jelly', 
                                'hyper slime jelly']]
        
    def create_loot_table(self):
        drop_list = [] # define returnable list
        if self.level > 0 and random.randint(0, 10) > self.possible_drops[0].rarity:
            drop_list.append(self.possible_drops[0])
            if self.level > 5 and random.randint(0, 10) > self.possible_drops[1].rarity:
                drop_list.append(self.possible_drops[1])
                if self.level > 9 and random.randint(0, 10) > self.possible_drops[2].rarity:
                    drop_list.append(self.possible_drops[2])
                    if self.level > 23 and random.randint(0, 10) > self.possible_drops[3].rarity:
                        drop_list.append(self.possible_drops[3])
        return drop_list
    
    def drop(self, player):
        dropses = self.create_loot_table()
        if not len(dropses) == 0:
            dprint(f'{player.name} got the following items')
            for drop in dropses:
                print(drop.name)
                player.inventory.add_item(drop)


class Insect(Enemy):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.possible_drops = [drop for drop in drops if drop.name in
                               ['carapas', 'venom glass', 'acutite']]
        
    def create_loot_table(self):
        drop_list = [] # define returnable list
        if self.level > 2 and random.randint(0, 10) > self.possible_drops[0].rarity:
            drop_list.append(self.possible_drops[0])
            if self.level > 3 and random.randint(0, 10) > self.possible_drops[1].rarity:
                drop_list.append(self.possible_drops[1])
                if self.level > 11 and random.randint(0, 10) > self.possible_drops[2].rarity:
                    drop_list.append(self.possible_drops[2])
        return drop_list
  
    def drop(self, player):
        dropses = self.create_loot_table()
        if not len(dropses) == 0:
            dprint(f'{player.name} got the following items')
            for drop in dropses:
                print(drop.name)
                player.inventory.add_item(drop)


class Construct(Enemy):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.possible_drops = [drop for drop in drops if drop.name in
                               ['mundane scrap metal', 'onix stone', 
                                'simple fabric', 'glass bottle', 'magic glass', 
                                'aged teak log', 'opal', 'agiros sheet', 'emerald', 
                                'acutite', 'crystalite', 'return_soul_stone', 'ruby', 
                                'sapphire', 'noblewood', 'blue blood diamond', 
                                'living stone', 'solidite', 'diamond', 
                                'super aja stone', 'colossal col']]
        
    def create_loot_table(self):
        drop_list = [] # define returnable list
        if self.level > 0 and random.randint(0, 10) > self.possible_drops[0].rarity:
            drop_list.append(self.possible_drops[0]) # scrap metal
            if self.level > 5 and random.randint(0, 10) > self.possible_drops[1].rarity:
                drop_list.append(self.possible_drops[1]) # onix
        elif self.level > 5 and random.randint(0, 10) > self.possible_drops[2].rarity:
            drop_list.append(self.possible_drops[2]) # fabric
            if self.level > 7 and random.randint(0, 10) > self.possible_drops[3].rarity:
                drop_list.append(self.possible_drops[3]) # bottle
                if self.level > 9 and random.randint(0, 10) > self.possible_drops[4].rarity:
                    drop_list.append(self.possible_drops[4]) # magic glass
                    if self.level > 11 and random.randint(0, 10) > self.possible_drops[5].rarity:
                        drop_list.append(self.possible_drops[5]) # aged teak log
                        if self.level > 14 and random.randint(0, 10) > self.possible_drops[6].rarity:
                            drop_list.append(self.possible_drops[6]) # opal
        elif self.level > 14 and random.randint(0, 10) > self.possible_drops[7].rarity:
            drop_list.append(self.possible_drops[7]) # agiros
            if self.level > 15 and random.randint(0, 10) > self.possible_drops[8].rarity:
                drop_list.append(self.possible_drops[8]) # emerald
        elif self.level > 15 and random.randint(0, 10) > self.possible_drops[9].rarity:
            drop_list.append(self.possible_drops[9]) # acutite
            if self.level > 17 and random.randint(0, 10) > self.possible_drops[10].rarity:
                drop_list.append(self.possible_drops[10]) # crystalite
                if self.level > 19 and random.randint(0, 10) > self.possible_drops[11].rarity:
                    drop_list.append(self.possible_drops[11]) # soul stone
                    if self.level > 20 and random.randint(0, 10) > self.possible_drops[12].rarity:
                        drop_list.append(self.possible_drops[12]) # ruby
        elif self.level > 20 and random.randint(0, 10) > self.possible_drops[13].rarity:
            drop_list.append(self.possible_drops[13]) # sapphire
        elif self.level > 20 and random.randint(0, 10) > self.possible_drops[14].rarity:
            drop_list.append(self.possible_drops[14]) # noblewood
            if self.level > 21 and random.randint(0, 10) > self.possible_drops[15].rarity:
                drop_list.append(self.possible_drops[15]) # blue diamond
        elif self.level > 21 and random.randint(0, 10) > self.possible_drops[16].rarity:
            drop_list.append(self.possible_drops[16]) # living stone
            if self.level > 23 and random.randint(0, 10) > self.possible_drops[17].rarity:
                drop_list.append(self.possible_drops[17]) # solidite
                if self.level > 24 and random.randint(0, 10) > self.possible_drops[18].rarity:
                    drop_list.append(self.possible_drops[18]) # diamond
        elif self.level > 24 and random.randint(0, 10) > self.possible_drops[19].rarity:
            drop_list.append(self.possible_drops[19]) # aja
        elif self.level > 25 and random.randint(0, 10) > self.possible_drops[20].rarity:
            drop_list.append(self.possible_drops[20]) # COLosal
        return drop_list
 
    def drop(self, player):
        dropses = self.create_loot_table()
        if not len(dropses) == 0:
            dprint(f'{player.name} got the following items')
            for drop in dropses:
                print(drop.name)
                player.inventory.add_item(drop)


class Undead(Enemy):
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.possible_drops = [drop for drop in drops if drop.name in
                               ['glass bottle', 'venom glass', 'onix stone', 
                                'simple fabric','dagger', 'grand col', 
                                'rose life potion']]
        
    def create_loot_table(self):
        drop_list = [] # define returnable list
        if self.level > 0 and random.randint(0, 10) > self.possible_drops[0].rarity:
            drop_list.append(self.possible_drops[0])
            if self.level > 3 and random.randint(0, 10) > self.possible_drops[1].rarity:
                drop_list.append(self.possible_drops[1])
                if self.level > 9 and random.randint(0, 10) > self.possible_drops[2].rarity:
                    drop_list.append(self.possible_drops[2])
                    if self.level > 18 and random.randint(0, 10) > self.possible_drops[3].rarity:
                        drop_list.append(self.possible_drops[3])
                        if self.level > 31 and random.randint(0, 10) > self.possible_drops[4].rarity:
                            drop_list.append(self.possible_drops[4])
                    elif self.level > 23 and random.randint(0, 10) > self.possible_drops[5].rarity:
                        drop_list.append(self.possible_drops[5])
                        if self.level > 37 and random.randint(0, 10) > self.possible_drops[6].rarity:
                            drop_list.append(self.possible_drops[6])
        return drop_list
  
    def drop(self, player):
        dropses = self.create_loot_table()
        if not len(dropses) == 0:
            dprint(f'{player.name} got the following items')
            for drop in dropses:
                print(drop.name)
                player.inventory.add_item(drop)


class Tarusoid(Enemy): # world 2 (cows)
    def __init__(self, name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, acu, col, agi, defense, force, world, ac)
        self.possible_drops = [drop for drop in drops if drop.name in 
                               []]
        
    def create_loot_table(self):
        pass
    
    def drop(self, player):
        dropses = self.create_loot_table()
        if not len(dropses) == 0:
            dprint(f'{player.name} got the following items')
            for drop in dropses:
                print(drop.name)
                player.inventory.add_item(drop)

class Monstrosity(Enemy):
    def __init__(self, name, malice, hp, atk, xp, level, accuracy, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, accuracy, col, agi, defense, force, world, ac)
        self.possible_drops = [drop for drop in drops if drop.name in
                               ['scale hide', 'animal hide', 'carapas', 
                                'thicc tendon','monster tooth', 'impish wings', 
                                'return soul stone']]
    
    def create_loot_table(self):
        drop_list = [] # define returnable list
        if self.level > 0 and random.randint(0, 10) > self.possible_drops[0].rarity:
            drop_list.append(self.possible_drops[0])
            drop_list.append(self.possible_drops[1])
            drop_list.append(self.possible_drops[2])
            if self.level > 3 and random.randint(0, 10) > self.possible_drops[3].rarity:
                drop_list.append(self.possible_drops[3])
                if self.level > 20 and random.randint(0, 10) > self.possible_drops[4].rarity:
                    drop_list.append(self.possible_drops[4])
                    if self.level > 30 and random.randint(0, 10) > self.possible_drops[5].rarity:
                        drop_list.append(self.possible_drops[5])
                        if self.level > 95 and random.randint(0, 10) > self.possible_drops[6].rarity:
                            drop_list.append(self.possible_drops[6])
        return drop_list
    
    def drop(self, player):
        dropses = self.create_loot_table()
        if not len(dropses) == 0:
            dprint(f'{player.name} got the following items')
            for drop in dropses:
                print(drop.name)
                player.inventory.add_item(drop)


class Goblinoid(Enemy):
    def __init__(self, name, malice, hp, atk, xp, level, accuracy, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, accuracy, col, agi, defense, force, world, ac)
        self.possible_drops = [drop for drop in drops if drop.name in
                               ['dagger', 'goblin coin', 'onix stone', 
                                'emerald','ruby', 'crystalite', 
                                'life potion']]
    
    def create_loot_table(self):
        drop_list = [] # define returnable list
        if self.level > 0 and random.randint(0, 10) > self.possible_drops[0].rarity:
            drop_list.append(self.possible_drops[0])
            if self.level > 12 and random.randint(0, 10) > self.possible_drops[1].rarity:
                drop_list.append(self.possible_drops[1])
                drop_list.append(self.possible_drops[2])
                if self.level > 16 and random.randint(0, 10) > self.possible_drops[4].rarity:
                    drop_list.append(self.possible_drops[3])
                    drop_list.append(self.possible_drops[4])
                    if self.level > 21 and random.randint(0, 10) > self.possible_drops[5].rarity:
                        drop_list.append(self.possible_drops[5])
                        if self.level > 28 and random.randint(0, 10) > self.possible_drops[6].rarity:
                            drop_list.append(self.possible_drops[6])
        return drop_list
    
    def drop(self, player):
        dropses = self.create_loot_table()
        if not len(dropses) == 0:
            dprint(f'{player.name} got the following items')
            for drop in dropses:
                print(drop.name)
                player.inventory.add_item(drop)


class Astral(Enemy):
    def __init__(self, name, malice, hp, atk, xp, level, accuracy, col, agi, defense, force, world, ac):
        super().__init__(name, malice, hp, atk, xp, level, accuracy, col, agi, defense, force, world, ac)
        self.possible_drops = [drop for drop in drops if drop.name in
                               ['droplet of villi', 'ectoplasm', 'astral shroud', 
                                'spirit lantern']]
    
    def create_loot_table(self):
        drop_list = [] # define returnable list
        if self.level > 4 and random.randint(0, 10) > self.possible_drops[1].rarity:
            drop_list.append(self.possible_drops[1])
            if self.level > 92 and random.randint(0, 10) > self.possible_drops[2].rarity:
                drop_list.append(self.possible_drops[2])
                drop_list.append(self.possible_drops[3])
        elif self.level > 4 and random.randint(0,7) > self.possible_drops[0].rarity:
            drop_list.append(self.possible_drops[0])
        return drop_list
    
    def drop(self, player):
        dropses = self.create_loot_table()
        if not len(dropses) == 0:
            dprint(f'{player.name} got the following items')
            for drop in dropses:
                print(drop.name)
                player.inventory.add_item(drop)


# ---------------------------------------------------------------------------------------


def init_doctors():
    dr_ed_bmed = Doctor('Dr. Ed B.med.', 2, 1, 1, 1, 400)
    dr_doug_bmbs = Doctor('Dr. Doug BMBS', 3, 2, 2, 1, 550)
    dr_steven_int = Doctor('Dr. Steven Intern', 3, 1, 1, 1, 350)
    dr_sye_bsrg = Doctor('Dr. Sye B.Srg.', 4, 3, 3, 1, 800)
    dr_tom_mbbs = Doctor('Dr. Tom MBBS', 5, 2, 3, 2, 500)
    dr_van_mph = Doctor('Dr. Van MPH', 6, 3, 4, 2, 500)
    dr_al_mphil = Doctor('Dr. Al M.Phil.', 7, 1, 3, 2, 600)
    dr_bill_mcm = Doctor('Dr. Bill MCM', 7, 4, 4, 3, 650)
    dr_red_mmsc = Doctor('Dr. Red MMSc.', 9, 2, 3, 4, 700)
    dr_greg_msc = Doctor('Dr. Greg MSc', 10, 3, 4, 5, 750)
    dr_rick_msrg = Doctor('Dr. Rick M.Srg.', 11, 4, 5, 6, 950)
    dr_lars_mm = Doctor('Dr. Lars MM', 11, 5, 5, 7, 750)
    dr_ford_da = Doctor('Dr. Ford DA', 13, 3, 4, 8, 900)
    dr_phil_dn = Doctor('Dr. Phill DN', 14, 2, 4, 9, 850)
    dr_hal_dhms = Doctor('Dr. Hal DHMs', 15, 3, 5, 10, 900)
    dr_paul_phd = Doctor('Dr. Paul Ph.D.', 16, 6, 6, 12, 850)
    dr_fred_dm = Doctor('Dr. Fred DM', 17, 7, 8, 13, 950)
    dr_bert_gp = Doctor('Dr. Bert GP', 18, 4, 6, 15, 800)
    dr_gord_dcm = Doctor('Dr. Gord DCM', 20, 5, 7, 16, 950)
    dr_boe_dsrg = Doctor('Dr. Boe D.Srg.', 21, 5, 7, 18, 995)
    dr_jerry_do = Doctor('Dr. Jerry DO', 23, 7, 8, 20, 955)
    dr_dan_md = Doctor('Dr. Dan MD', 24, 9, 8, 24, 900)
    dr_russ = Doctor('Dr. Russ', 30, 10, 15, 30, 996)
    dr_the = Doctor('The Doctor', 35, 10, 16, 40, 996)
    
    doc_list = [dr_ed_bmed, dr_doug_bmbs, dr_steven_int, dr_sye_bsrg, 
                dr_tom_mbbs, dr_van_mph, dr_al_mphil, dr_bill_mcm, 
                dr_red_mmsc, dr_red_mmsc, dr_greg_msc, dr_rick_msrg, 
                dr_lars_mm, dr_ford_da, dr_phil_dn, dr_hal_dhms, dr_paul_phd,
                dr_fred_dm, dr_bert_gp, dr_gord_dcm, dr_boe_dsrg, 
                dr_jerry_do, dr_dan_md, dr_russ, dr_the]

    return doc_list

'''
A note on monster initialization:
Enemies of all kinds vary in stats but follow a few consistent themes.
According to the lore, the line between monsters and creatures is rather fine.
Monsterism is a sort of essence that imbues itself within either creatures or
raw matterial.
Technically, anything with any amount of this essence is classified as a
monster but the more one has the more monsterous it becomes. What monsterism
does to a creature or a substance is that it grants it with or increases its
intelligence. This is not universal intelligence, only the necessary
intelligence that would make the monster more evil. For example, Slimes are
purely monsters formed out of liquid embued with monster essence, they are
litterally animated liquids that desire nothing but death and destruction
(granted they're not very good at it).
Nepenths and other plant monsters are ordinary plants embued with monster
essence making them nothing more than animated plants that desire death and
distruction. Creature monsters are a little different because they have, asside
from monster essence increasing their evilness, they also have their own
intelligence, their own desire and their own physical needs (until those needs
are not met and they become an animated corpse, an undead monster). This makes
them a little more capable of retreat from a fight they know they cannot win.
Lore asside, the point is that there is a scale of monsterism inside each
enemy that ranges from 0 to 100 percent monsterism concentration. This scale is
the main determiner for their general stats. The closer the enemy is to 100
percent the greater the ratio between attack and hit point max is upon
initialization. Take this hypothetical example given below:
example100 = Enemy('example 100%', 100, 5, ...)
example0 = Enemy('example 0%', 50, 10, ...)
As you can see above, the enemy with 0% monster essence flowing through them
has an Hp:Atk ratio of about 5:1 while the enemy with the full 100%
concentration has a Hp:Atk ratio of around 20:1. This is because of a
blessing/curse granted upon all those with monster essence within them.
The more they have the more Hit points they have but the less attack power they
have per level.
There are two other main determiners of monster stats. Enemy level and the
build/shape/size of the mosnter. The level is actually calculated last after
everything else while the build/shape/size of the mosnter is calculated after
the monster essence bit to tweak those values. Here are a few more examples to
help demonstrate these effects:
stock100 = Enemy('regular monster with 100%', 100, 5, xp, lv, acu=.7, agi=20, ...)
fast100 = Enemy('regular but fast with 100%', 100, 4, xp, lv, acu=.65, agi=16, ...)
hardy100 = Enemy('regular but tanky with 100%', 150, 6, xp, lv, acu=.6, agi=24, ...)
sharp100 = Enemy('reg but sharp shot with 100%', 100, 4, xp, lv, acu=.9, agi=20, ...)
maxdps100 = Enemy('reg but high dps with 100%', 100, 3, xp, lv, acu=.65, agi=10, ...)
As you can see the enemies above are all about the same strength but have their
base stats modified by certain factors like the monster's actual speed, actual
accuracy, the actual hardness of their body's exterior, etc.
Lastly, the final level is calculated based on their stats after all those
things have been done. However, level is also used to initallize the base stats
as well. The examples where the hp was 100 and the attack was 5 represented an
average level 5 monster with 100% monster essence concentration.
The initial values passed to it are the monster essence and the desired level,
if during the later stat tweaks, the stats push the monster to what would
resemble a higher leveled monster than desired, then, all stats, prioritizing
hp and attack are increased or decreased until again, the monster resembles that
of the desired level.
Case:
We want a giant beatle insect type monster. First we pass in the desired
level (we will say level 4 for this case) and also the number from 1 to 100
representing the ammount of monsterism concentrated within said monster in this
case we know that the beatle is also a kind of creature with inteligence of its
own so we will say it has a middle ground concentration of 50% and a ratio of
about 10:1.
These initial calculations bring us to a monster with the following stats:
giant_rhino_beatle = Insect('giant rhino beatle', hp=60, atk=6, xp, lv=4, acu=.7, agi=20, ...)
Now we will adjust the monster stats based on what we know about the creature.
We know that an insect is typically quick but a beatle is more tanky than
quick. Furthermore, we know that beatles can be clumsy in their attacks. We can
take this information and adjust the stats like so:
giant_rhino_beatle = Insect('giant rhino beatle', hp=80, atk=4, xp, lv=?, acu=.55, agi=18, ...)
these adjustments seem to have slightly reduced the monster's over all power
level to nearly below the desired level of 4; therefore, we will increase hp
and/or attack to meet the required level with more accuracy as follows:
giant_rhino_beatle = Insect('giant rhino beatle', hp=86, atk=5, xp, lv=4, acu=.55, agi=18, ...)
This monster now reflects the desired level in its stats accomplished by
increasing the onster's hp and significaltly increasing its attack power.
The final step is to calculate the ammount of xp the player will recieve upon
defeating this monster. To do this we will look at the power level again and
estimate a value within a given range per level, that will be a fitting reward.
Higher powered level 4 monsters will grant more xp than lower powered level 4
monsters.
The first few ranges are calculated below but they are typically slightly
overlapping and increasing range sizes. We can see from our example monster
that the adjusted values left the final monster slightly more powerful within
the level 4 range giving us an xp value above the median value of 25, maybe
something like 29. Now that we have all stats accounted for, we can initailize
the monster as follows:
giant_rhino_beatle = Insect('giant rhino beatle', 86, 5, 29, 4, .55, 18, ...)
note: The two remaining stats after the agi value (18) that are dotted out are
unimportant to these calculations and represent the worlds this particular
enemy appears in and the values to use for the attack minigame when
initiallized during a battle.
Xp ranges per level:
1:{1x10}, 2:{6x16}, 3:{12x24}, 4:{18x32}, 5:{25x40}, 6:{35x50}, 7{48x64},
8:{62x80}, 9:{76x96}, 10:{95x120}, 11:{118x144}, 12:{142x170}, 13:{164x196}, 
14:{195x230}, 15:{228x272}, 16:{270x320}, ...
'''

def init_enemies():
    test_boss = BossTest('test_boss', 100, 12, 2, 600, 1, 600, 20, 1200, 0, 0, [1], (750, 60, 120, 5))
    windworm = Worm('windworm', 70, 1, 1, 3, 1, 150, 0, 1650, 0, 0, [1], (500, 70, 180, 8))
    brown_worm = Worm('brown worm', 65, 2, 1, 4, 1, 200, 0, 1500, 0, 0, [1], (450, 15, 60, 20))
    slime = Slime('slime', 100, 2, 1, 5, 1, 350, 0, 1550, 0, 0, [1], (600, 21, 200, 10))
    refuse = Construct('refuse', 100, 3, 1, 4, 1, 200, 1, 1250, 0, 0, [1,3,6,9], (400, 33, 240, 12))
    cykloone = Insect('cykloone', 70, 3, 1, 3, 1, 150, 0, 800, 0, 0, [1], (250, 27, 400, 6))
    frenzy_boar = Beast('frenzy boar', 55, 4, 1, 6, 1, 550, 0, 900, 0, 0, [1,2,3,4], (600, 18, 280, 10))
    field_wolf = Beast('field wolf', 40, 5, 1, 6, 1, 700, 0, 750, 0, 0, [1,2], (300, 19, 260, 10))
    greedy_badger = Beastoid('greedy badger', 35, 5, 1, 5, 1, 350, 2, 650, 0, 0, [1,2,3], (200, 17, 275, 8))
    awakened_shrub = Plant('awakened shrub', 80, 5, 1, 5, 1, 600, 0, 1100, 0, 0, [1,4,5], (600, 16, 290, 10))
    small_kobold = Koboldoid('small kobold', 25, 14, 2, 8, 2, 435, 1, 1050, 0, 0, [1], (700, 10, 170, 4))
    barkling = Plant('barkling', 85, 16, 1, 7, 2, 450, 0, 1350, 0, 0, [1], (500, 10, 150, 10))
    swarm_of_bats = Beast('swarm of bats', 70, 13, 1, 9, 2, 900, 0, 800, 0, 0, [1,2,3,4,5], (800, 10, 110, 30))
    little_nepenth = Nepenth('little nepenth', 85, 16, 1, 13, 3, 660, 0, 660, 0, 0, [1], (400, 11, 200, 2))
    kobold_slave = Koboldoid('kobold slave', 25, 16, 2, 12, 3, 750, 1, 950, 0, 0, [1], (750, 10, 285, 4))
    windwasp = Insect('windwasp', 70, 13, 1, 10, 3, 550, 0, 550, 0, 0, [1,2], (700, 17, 400, 7))
    dire_wolf = Beast('dire wolf', 65, 17, 1, 13, 3, 850, 0, 950, 0, 0, [1,3,4], (300, 13, 250, 10))
    green_worm = Worm('green worm', 65, 26, 1, 10, 3, 350, 0, 1450, 0, 0, [1], (300, 16, 165, 19))
    nepenth = Nepenth('nepenth', 85, 18, 1, 14, 3, 705, 0, 795, 0, 0, [1], (400, 12, 200, 2))
    onikuma = Beast('onikuma', 90, 30, 2, 14, 4, 755, 0, 1240, 1, 0, [1], (760, 30, 385, 4))
    cave_slime = Slime('cave slime', 100, 35, 2, 11, 4, 550, 0, 1450, 0, 0, [1], (600, 14, 160, 10))
    kobold_soldier = Koboldoid('kobold soldier', 25, 29, 4, 13, 4, 750, 2, 950, 1, 0, [1], (800, 12, 240, 4))
    Kobold_guard = Koboldoid('kobold guard', 25, 27, 4, 14, 4, 800, 3, 850, 2, 0, [1], (800, 13, 250, 4))
    shrubent = Plant('shrubent', 85, 42, 3, 14, 5, 685, 0, 1100, 0, 0, [1], (600, 11, 280, 10))
    cave_bear = Beast('cave bear', 20, 33, 5, 15, 5, 650, 1, 1150, 1, 0, [1], (900, 64, 700, 6))
    pre_pod_nepenth = Nepenth('pod nepenth', 85, 8, 2, 14, 5, 600, 0, 700, 0, 0, [1], (400, 120, 200, 2))
    post_pod_nepenth = Nepenth('Pod Nepenth', 85, 27, 2, 14, 5, 600, 0, 700, 0, 0, [1], (400, 11, 200, 2))
    flower_nepenth = Nepenth('flower nepenth', 85, 35, 2, 18, 5, 600, 0, 700, 0, 0, [1], (400, 11, 200, 2))
    red_worm = Worm('red worm', 65, 55, 1, 14, 5, 400, 0, 1400, 0, 0, [1], (250, 17, 130, 18))
    kosaur = Kosaur('Kosaur', 95, 144, 7, 300, 5, 750, 3, 1050, 1, 0, [1], (900, 70, 800, 5))
    big_nepenth = Nepenth('big nepenth', 85, 48, 3, 19, 6, 680, 0, 920, 0, 0, [1], (350, 16, 200, 2))
    sappent = Plant('sappent', 85, 44, 3, 19, 6, 700, 0, 1415, 0, 0, [1], (600, 14, 320, 10))
    ruin_kobold = Koboldoid('ruin kobold', 30, 38, 5, 20, 6, 700, 4, 1000, 1, 0, [1,3], (600, 18, 296, 4))
    sly_srewman = Beastoid('sly shrewman', 35, 19, 1, 17, 6, 995, 6, 195, 0, 0, [1,2,3,5,9], (200, 10, 400, 2))
    human_bandit = Humanoid('bandit', 0, 30, 6, 20, 6, 800, 6, 1005, 1, 0, [1,2,3,6], (600, 10, 250, 4))
    kobold_chief = Koboldoid('kobold chief', 30, 46, 6, 18, 7, 750, 5, 900, 1, 0, [1], (750, 19, 310, 4))
    blue_worm = Worm('blue worm', 65, 70, 2, 19, 7, 550, 0, 1350, 0, 0, [1,2], (225, 18, 140, 17))
    treent = Plant('treent', 85, 52, 3, 22, 7, 675, 0, 1445, 12, 0, [1,4], (600, 15, 100, 5))
    ruin_kobold_trooper = Koboldoid('ruin kobold trooper', 30, 46, 6, 22, 7, 850, 5, 750, 1, 0, [1,3], (600, 16, 300, 3))
    skeleton = Undead('skeleton', 100, 60, 3, 26, 8, 700, 1, 950, 0, 0, [1,2,3,4,5,6,7,8,9,10], (500, 10, 150, 6))
    bark_golem = Plant('bark golem', 95, 66, 4, 21, 8, 900, 1, 1350, 8, 0, [1], (500, 14, 300, 10))
    flying_kobold = Koboldoid('flying kobold', 30, 52, 7, 25, 8, 500, 4, 450, 0, 10, [1], (850, 13, 300, 2))
    ruin_kobold_sentinel = Koboldoid('ruin kobold sentinel', 30, 61, 8, 26, 9, 750, 6, 700, 2, 0, [1], (600, 21, 480, 3))
    # ac: (dist or def, size ratio, actual speed, balance)  (rail_size600px, hit_dc10px, speed480fps, chances10i) # limit ratio 450:95
    illfang = Illfang('Illfang', 35, 240, 17, 1000, 9, 900, 15, 1000, 3, 5, [1], (980, 18, 640, 6))

    jackelope = Beast('jackelope', 40, 16, 2, 8, 2, 800, 0, 600, 0, 0, [1], (600, 10, 200, 10))
    borogrove = Beast('borogrove', 90, 17, 1, 20, 3, 700, 1, 1100, 0, 0, [1,2,3], (600, 16, 255, 10))
    silver_fish = Insect('silverfish', 80, 8, 1, 5, 1, 600, 0, 1000, 0, 0, [1,3,4,9], (500, 10, 180, 16))
    moamwrath = Monstrosity('moamwrath', 100, 40, 2, 34, 6, 666, 0, 850, 0, 0, [1,2,3,5], (720, 22, 720, 22))
    bryllyg = Monstrosity('bryllyg', 100, 34, 2, 22, 4, 900, 1, 1000, 0, 0, [1], (600, 18, 200, 10))
    slythy_tove = Monstrosity('slythy tove', 100, 40, 2, 26, 5, 700, 0, 1000, 0, 0, [1], (600, 14, 190, 10))
    borogove = Monstrosity('borogove', 100, 36, 2, 26, 4, 620, 0, 850, 0, 0, [1], (800, 14, 118, 10))
    marzeedote = Beast('marzeedote', 65, 33, 3, 20, 4, 750, 0, 1000, 0, 0, [1], (600, 14, 200, 6))
    doezeedote = Beast('doezeedote', 75, 48, 3, 55, 6, 810, 0, 950, 0, 0, [1], (500, 18, 210, 8))
    little_amzedivie = Monstrosity('little amzedivie', 100, 63, 3, 119, 9, 675, 0, 1000, 1, 0, [1], (600, 10, 125, 11))
    kiddleydivie = Monstrosity('kiddleydivie', 100, 40, 2, 30, 5, 700, 0, 1000, 0, 0, [1], (100, 10, 100, 8))
    woodenchew = Construct('woodenchew', 95, 20, 1, 12, 3, 650, 1, 600, 0, 0, [1,2], (300, 10, 70, 9))
    condemned_goblin = Goblinoid('condemned goblin', 35, 34, 4, 23, 5, 740, 0, 850, 0, 0, [1], (700, 10, 194, 4))
    goblin = Goblinoid('goblin', 35, 41, 5, 19, 6, 700, 8, 950, 1, 0, [1,2,3], (600, 12, 160, 10))
    goblin_king = Goblinoid('goblin king', 40, 55, 6, 32, 8, 880, 0, 1000, 2, 0, [1], (500, 13, 180, 5))
    shinigami = Astral('shinigami', 95, 49, 3, 17, 6, 595, 0, 700, 0, 0, [1,6,8,9,10], (995, 12, 205, 2))
    large_cave_slime = Slime('large cave slime', 100, 26, 3, 26, 8, 670, 0, 1250, 0, 0, [1,2], (800, 16, 400, 20))
    owlbear = Beast('owlbear', 20, 26, 4, 16, 4, 685, 1, 900, 1, 0, [1,2], (750, 20, 300, 12))
    irrawrtzus = Beastoid('irrawrtzus', 45, 47, 5, 35, 6, 890, 5, 1000, 0, 0, [2,3,4,6], (800, 12, 700, 6))
    letiche = Beast('letiche', 90, 30, 2, 27, 4, 600, 0, 850, 0, 0, [1], (400, 10, 140, 4))
    bullbous_bow = Beast('bullbous bow', 45, 61, 6, 34, 9, 700, 0, 1000, 15, 3, [1,2], (700, 22, 200, 10))

    black_worm = Worm('black worm', 65, 122, 3, 29, 6, 550, 0, 1300, 0, 0, [1,2], (210, 9, 90, 16))
    bronze_worm = Worm('bronze worm', 65, 54, 1, 19, 4, 550, 0, 1250, 0, 0, [1,2], (200, 9, 100, 15))
    white_worm = Worm('snow worm', 65, 54, 1, 19, 4, 550, 0, 1200, 0, 0, [1,2], (185, 9, 120, 14))
    yellow_worm = Worm('yellow worm', 65, 54, 1, 19, 4, 550, 0, 1150, 0, 0, [1,2], (175, 9, 145, 13))
    fall_worm = Worm('fall worm', 70, 54, 1, 19, 4, 550, 0, 1100, 0, 0, [1,2], (160, 10, 160, 12))
    blood_worm = Worm('blood worm', 70, 54, 1, 19, 4, 550, 0, 1050, 0, 0, [1,2], (145, 10, 180, 11))
    midnight_worm = Worm('midnight worm', 70, 54, 1, 19, 4, 550, 0, 1000, 0, 0, [1,2], (130, 11, 210, 10))
    purple_worm = Worm('purple worm', 70, 54, 1, 19, 4, 550, 0, 975, 1, 0, [1,2], (115, 11, 240, 9))
    water_worm = Worm('water worm', 70, 54, 1, 19, 4, 550, 0, 950, 2, 0, [1,2], (100, 10, 260, 9))
    fire_worm = Worm('fire worm', 70, 54, 1, 19, 4, 550, 0, 925, 2, 0, [1,2], (100, 10, 280, 8))
    wyrm_worm = Worm('wyrm worm', 75, 54, 1, 19, 4, 550, 0, 900, 3, 0, [1,2], (200, 9, 320, 7))
    giant_brown_worm = Worm('giant brown worm', 75, 54, 1, 19, 4, 550, 0, 1100, 5, 0, [1,2], (400, 19, 360, 6))
    giant_green_worm = Worm('giant green worm', 75, 54, 1, 19, 4, 550, 0, 1075, 15, 0, [1,2], (415, 20, 400, 6))
    giant_red_worm = Worm('giant red worm', 75, 54, 1, 19, 4, 550, 0, 1050, 22, 0, [1,2], (430, 22, 440, 5))
    giant_blue_worm = Worm('giant blue worm', 75, 54, 1, 19, 4, 550, 0, 1025, 28, 0, [1,2], (445, 23, 480, 5))
    giant_black_worm = Worm('giant black worm', 75, 54, 1, 19, 4, 550, 0, 1000, 32, 0, [1,2], (460, 24, 500, 4))
    giant_bronze_worm = Worm('giant bronze worm', 75, 54, 1, 19, 4, 550, 0, 980, 35, 0, [1,2], (480, 25, 520, 4))
    giant_white_worm = Worm('giant snow worm', 75, 54, 1, 19, 4, 550, 0, 960, 36, 0, [1,2], (500, 27, 540, 4))
    giant_yellow_worm = Worm('giant yellow worm', 75, 54, 1, 19, 4, 550, 0, 940, 40, 0, [1,2], (520, 28, 560, 3))
    giant_fall_worm = Worm('giant fall worm', 75, 54, 1, 19, 4, 550, 0, 920, 44, 0, [1,2], (540, 30, 580, 3))
    giant_blood_worm = Worm('giant blood worm', 80, 54, 1, 19, 4, 550, 0, 900, 50, 0, [1,2], (560, 32, 600, 3))
    giant_midnight_worm = Worm('giant midnight worm', 80, 54, 1, 19, 4, 550, 0, 880, 60, 0, [1,2], (580, 35, 620, 2))
    giant_purple_worm = Worm('giant purple worm', 85, 54, 1, 19, 4, 550, 0, 860, 92, 0, [1,2], (600, 36, 640, 2))
    giant_wyrm_worm = Enemy('giant wyrm worm', 90, 54, 1, 19, 4, 550, 0, 850, 196, 0, [1,2], (990, 34, 720, 2)) # side boss


    mon_list = [test_boss, windworm, brown_worm, slime, refuse, cykloone, frenzy_boar, field_wolf, 
                greedy_badger, awakened_shrub, small_kobold, barkling, swarm_of_bats,
                little_nepenth, kobold_slave, windwasp, dire_wolf, green_worm, nepenth, onikuma,
                cave_slime, kobold_soldier, Kobold_guard, shrubent, cave_bear, pre_pod_nepenth,
                post_pod_nepenth, flower_nepenth, red_worm, kosaur, big_nepenth, sappent, 
                ruin_kobold, sly_srewman, human_bandit, kobold_chief, blue_worm, black_worm, 
                treent, ruin_kobold_trooper, bark_golem, skeleton, flying_kobold, 
                ruin_kobold_sentinel, illfang, jackelope, borogrove, silver_fish, moamwrath,
                bryllyg, slythy_tove, borogove, marzeedote, doezeedote, little_amzedivie,
                kiddleydivie, woodenchew, condemned_goblin, goblin, goblin_king, shinigami,
                large_cave_slime, owlbear, irrawrtzus, letiche, bullbous_bow]

    return mon_list


def init_allies(): # designations use snake case and numerals
    robin_0 = Ally('Robin', 1, 14, 1, 1111, 700, 0, 0, Skill('slant', 0, 1, 1, 2, 1), 'robin_0')
    henry = Ally('Henry', 2, 11, 3, 960, 650, 0, 0, Skill('reverse pull', 0, 2, 5, 4, 3))
    liliyah = Ally('Liliyah', 2, 15, 2, 865, 790, 0, 0, Skill('parallel sting', 0, 2, 2, 2, 2), 'liliyah_0')
    tiffey = Ally('Tiffey', 2, 16, 2, 820, 700, 0, 0, Skill('cross hatch', 0, 3, 2, 4, 3))
    kajlo_sohler = Ally('Kajlo Sohler', 2, 18, 3, 975, 760, 0, 0, Skill('cork screw', 0, 1, 1, 3, 1))
    officer_jerrimathyus = Ally('Officer Jerrimathyus', 3, 26, 7, 1225, 760, 1, 0, Skill('uppercut', 0, 3, 1, 4, 3))
    bulli = Ally('Bulli', 2, 12, 1, 1000, 750, 0, 0, Skill('mega poke', 0, 1, 2, 2, 1))
    milo_0 = Ally('Milo', 2, 16, 3, 960, 785, 0, 0, Skill('linear', 0, 2, 1, 3, 3), 'milo_0')
    gaffer = Ally('Gaffer', 1, 9, 1, 1030, 635, 0, 0, Skill('pitch fork', 0, 1, 2, 4, 1))
    holt = Ally('Holt', 3, 22, 6, 1150, 760, 0, 0, Skill('back rush', 0, 4, 1, 5, 4))
    suphia = Ally('Suphia', 4, 28, 5, 925, 750, 0, 0, Healing('quick tonic', 1, 3, 4, 4, 2, 1))
    electo = Ally('Electo', 4, 26, 7, 1010, 780, 0, 0, SpellAttack('thunder wave', 1, 3, 4, 4, 2, 0))
    hesh = Ally('Hesh', 3, 19, 7, 840, 760, 0, 0, SpellAttack('fire bolt', 1, 3, 4, 3, 3, 0))
    coef = Ally('Coef', 6, 39, 12, 840, 770, 0, 1, Skill('avalanche', 0, 6, 1, 6, 9))
    deg = Ally('Deg', 5, 34, 7, 990, 765, 0, 0, Skill('triangular', 0, 5, 3, 3, 8))
    virabela  = Ally('Virabela', 5, 30, 10, 1000, 810, 0, 0, SpellAttack('magic arrow', 1, 4, 6, 5, 3, 0))
    polly = Ally('Polly', 4, 28, 5, 900, 800, 0, 0, Skill('streak', 0, 3, 1, 3, 2))
    rivek = Ally('Rivek', 7, 45, 14, 1005, 795, 10, 2, Skill('vertical arc', 0, 8, 2, 7, 11))
    outh_gurenge = Ally('Captain Gurenge', 10, 72, 19, 890, 890, 12, 15, Skill('quad pain', 0, 11, 4, 6, 14))
    robin_1 = Ally('Robin', 9, 54, 18, 1010, 770, 0, 0, Skill('sonic leap', 0, 9, 1, 7, 10), 'robin_1')
    mickle = Ally('Officer Mickle', 10, 67, 20, 905, 865, 10, 10, Skill('flash forward', 0, 9, 4, 4, 9))
    reywyn = Ally('Reywyn', 7, 44, 13, 986, 925, 0, 1, Skill('triangular', 0, 5, 3, 5, 8))
    liliyah_1 = Ally('Liliyah', 7, 50, 15, 830, 810, 0, 0, Skill('parallel sting', 0, 2, 2, 2, 2), 'liliyah_1')
    dykester = Ally('Dykester', 8, 50, 9, 640, 825, 0, 0, Spall('turquoise blue overdrive', 2, 5, 2, 2, 5))
    bellman = Ally('Bellman', 8, 52, 17, 950, 710, 12, 0, Skill('negative cycle', 0, 4, 2, 4, 5))
    ford = Ally('Ford', 8, 52, 17, 950, 710, 0, 12, Skill('loss', 0, 4, 4, 6, 8))
    huffman = Ally('Huffman', 9, 60, 16, 995, 760, 2, 5, SpellAttack('emerald splash', 1, 9, 9, 5, 6, 0))
    dagshor = Ally('Dagshor', 9, 64, 20, 1055, 688, 1, 1, Skill('steel press', 0, 8, 4, 4, 5))


    allies = [robin_0,henry,liliyah,tiffey,kajlo_sohler,officer_jerrimathyus,
              bulli,milo_0,gaffer,holt,suphia,electo,hesh,coef,deg,virabela,polly,
              rivek,outh_gurenge,robin_1,mickle,reywyn,liliyah_1,bellman,huffman,
              dykester,ford,dagshor]

    return allies

