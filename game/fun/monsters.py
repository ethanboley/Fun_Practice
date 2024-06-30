
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
    def __init__(self, name, hp, atk, xp, level, accuracy, col, agi, world):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.xp = xp
        self.level = level
        self.accuracy = accuracy
        self.col = col
        self.agi = agi
        self.world = world

    def attack(self, target):
        if target == None:
            pass
        elif random.random() < self.accuracy:
            target.hp -= self.atk
            dprint(f'{self.name} attacks {target.name} for {self.atk} damage!')
            if target.is_alive():
                display_health(target)
            else:
                if isinstance(target, Ally):
                    dprint(f'{target.name} has been mortally wounded!')
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
    def __init__(self, name, level, hp, atk, agi, acu, skill, designation=None) -> None:
        self.name = name
        self.level = level
        self.maxhp = hp
        self.hp = hp
        self.atk = atk
        self.agi = agi
        self.acu = acu
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
        if random.random() < self.acu:
            damage = self.atk - random.randint(0, self.atk // (self.level + 15))
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
            damage = self.atk + random.randint(0, self.atk // (self.level + 15)) + self.skill.damage
            if self.cooldown <= 0:
                active_damage = damage if random.random() < self.acu else (damage // 5) + 1
                target.hp -= active_damage
                dprint(f'{self.name} used {self.skill.name} and dealt {active_damage} damage to {target.name}!')
                if target.is_alive():
                    dprint(f'{target.name} has {target.hp} hp remaining.')
                else:
                    dprint(f'{self.name} has defeated {target.name}!')
        
        elif self.skill.type == 1: # if its a spell
            damage = self.atk + random.randint(0, self.atk // (self.level + 15)) + self.skill.damage
            if self.skill.nature == 0: # if its a spellattack
                pass # keep target the same
                if self.cooldown <= 0:
                    active_damage = damage if random.random() < self.acu else (damage // 5) + 1
                    target.hp -= active_damage
                    dprint(f'{self.name} used {self.skill.name} and dealt {active_damage} damage to {target.name}!')
                    if target.is_alive():
                        dprint(f'{target.name} has {target.hp} hp remaining.')
                    else:
                        dprint(f'{self.name} has defeated {target.name}!')

            elif self.skill.nature == 1: # if its a healing spell
                target = random.choice(player.allies)
                if self.cooldown <= 0:
                    active_damage = damage if random.random() < self.acu else (damage // 5) + 1
                    target.hp += active_damage
                    dprint(f'{self.name} healed {target.name}!')
                

        self.cooldown += 4
            

    def is_alive(self):
        return self.hp > 0


class Boss:
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.xp = xp
        self.level = level
        self.acu = acu
        self.col = col
        self.agi = agi
        self.world = world
    
    def attack(self, player):
        if random.random() < self.acu:
            player.hp -= self.atk
            dprint(f"{player.name} is hit for {self.atk} damage from {self.name}\'s attack!")
            if player.is_alive():
                dprint(f'{player.name} takes the hit like a boss!')
                display_health(player)
            else:
                dprint(f'{player.name} was slain at the hand of {self.name}!')
        else:
            dprint(f"{self.name} attacks but misses {player.name}!")


# ----------- Bosses


class Kosaur(Boss):
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world) -> None:
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world)
        self.acu_mod = .02
        self.title = 'Scourge of the Kobold Wood'

    def bite(self, player):
        can_use = random.randint(1,6) in [5, 6]
        if can_use:
            strong_damage = self.atk + random.randint(1, (self.atk // 5) + 1) + 2
            weak_damage = self.atk - random.randint(1, (self.atk // 5) + 1)
            if random.random() < self.acu + self.acu_mod:
                player.hp -= strong_damage
                dprint(f'{self.title} attacks with it\'s massive jaws!')
                dprint(f'the attack hits {player.name} for {strong_damage} damage!')
                if player.is_alive():
                    display_health(player)
                else:
                    dprint(f'{player.name} was eaten alive!')
        elif random.random() < self.acu:
            player.hp -= weak_damage
            dprint(f'{self.name} just got a bit of {player.name}')
            dprint(f'the attack dealt {weak_damage} damage to {player.name}.')
            if player.is_alive():
                display_health(player)
            else:
                dprint(f'but that was all {player.name} could take!')
        else:
            dprint(f'{self.name} tried to eat {player.name} but missed! ')


class Illfang(Boss):
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world) -> None:
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world)
        self.acu_mod = .03
        self.title = 'the Kobold Lord'
    
    def talwar():
        pass


class Barran(Boss):
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world)
        self.acu_mod = .03
        self.title = 'the General Tarus'

    def lance():
        pass


class Asterios(Boss):
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world)
        self.acu_mod = .04
        self.title = 'the Tarus King'

    def mace():
        pass


# ----------- Monsters


class Beastoid(Enemy):
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world)
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


class Tarusoid(Enemy): # world 2 (cows)
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world)
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


# -------------------------------------------------------------------------------------------------------------------------------------------------------------


def init_doctors():
    dr_ed_bmed = Doctor('Dr. Ed B.med.', 2, 1, 1, 1, .4)
    dr_doug_bmbs = Doctor('Dr. Doug BMBS', 3, 2, 2, 1, .55)
    dr_steven_int = Doctor('Dr. Steven Intern', 3, 1, 1, 1, .35)
    dr_sye_bsrg = Doctor('Dr. Sye B.Srg.', 4, 3, 3, 1, .8)
    dr_tom_mbbs = Doctor('Dr. Tom MBBS', 5, 2, 3, 2, .5)
    dr_van_mph = Doctor('Dr. Van MPH', 6, 3, 4, 2, .5)
    dr_al_mphil = Doctor('Dr. Al M.Phil.', 7, 1, 3, 2, .6)
    dr_bill_mcm = Doctor('Dr. Bill MCM', 7, 4, 4, 3, .65)
    dr_red_mmsc = Doctor('Dr. Red MMSc.', 9, 2, 3, 4, .7)
    dr_greg_msc = Doctor('Dr. Greg MSc', 10, 3, 4, 5, .75)
    dr_rick_msrg = Doctor('Dr. Rick M.Srg.', 11, 4, 5, 6, .95)
    dr_lars_mm = Doctor('Dr. Lars MM', 11, 5, 5, 7, .75)
    dr_ford_da = Doctor('Dr. Ford DA', 13, 3, 4, 8, .9)
    dr_phil_dn = Doctor('Dr. Phill DN', 14, 2, 4, 9, .85)
    dr_hal_dhms = Doctor('Dr. Hal DHMs', 15, 3, 5, 10, .9)
    dr_paul_phd = Doctor('Dr. Paul Ph.D.', 16, 6, 6, 12, .85)
    dr_fred_dm = Doctor('Dr. Fred DM', 17, 7, 8, 13, .95)
    dr_bert_gp = Doctor('Dr. Bert GP', 18, 4, 6, 15, .8)
    dr_gord_dcm = Doctor('Dr. Gord DCM', 20, 5, 7, 16, .95)
    dr_boe_dsrg = Doctor('Dr. Boe D.Srg.', 21, 5, 7, 18, .99)
    dr_jerry_do = Doctor('Dr. Jerry DO', 23, 7, 8, 20, .95)
    dr_dan_md = Doctor('Dr. Dan MD', 24, 9, 8, 24, .9)
    dr_russ = Doctor('Dr. Russ', 30, 10, 15, 30, .99)
    dr_the = Doctor('The Doctor', 35, 10, 16, 40, .99)
    
    doc_list = [dr_ed_bmed, dr_doug_bmbs, dr_steven_int, dr_sye_bsrg, 
                dr_tom_mbbs, dr_van_mph, dr_al_mphil, dr_bill_mcm, 
                dr_red_mmsc, dr_red_mmsc, dr_greg_msc, dr_rick_msrg, 
                dr_lars_mm, dr_ford_da, dr_phil_dn, dr_hal_dhms, dr_paul_phd,
                dr_fred_dm, dr_bert_gp, dr_gord_dcm, dr_boe_dsrg, 
                dr_jerry_do, dr_dan_md, dr_russ, dr_the]

    return doc_list

def init_enemies(): 
    windworm = Worm('windworm', 1, 1, 3, 1, .15, 0, 33, [1])
    brown_worm = Worm('brown worm', 2, 1, 4, 1, .2, 0, 44, [1])
    slime = Slime('slime', 2, 1, 5, 1, .35, 0, 31, [1])
    refuse = Construct('refuse', 3, 1, 4, 1, .2, 1, 25, [1,3,6,9])
    cykloone = Insect('cykloone', 3, 1, 3, 1, .15, 0, 16, [1])
    frenzy_boar = Beast('frenzy boar', 4, 1, 6, 1, .55, 0, 18, [1,2,3,4])
    field_wolf = Beast('field wolf', 5, 1, 6, 1, .7, 0, 15, [1,2])
    greedy_badger = Beastoid('greedy badger', 5, 1, 5, 1, .35, 2, 13, [1,2,3])
    awakened_shrub = Plant('awakened shrub', 5, 1, 5, 1, .6, 0, 22, [1,4,5])
    small_kobold = Koboldoid('small kobold', 6, 2, 8, 1, .45, 1, 21, [1])
    barkling = Plant('barkling', 8, 1, 7, 1, .4, 0, 27, [1])
    swarm_of_bats = Beast('swarm of bats', 8, 1, 9, 1, .9, 0, 16, [1,2,3,4,5])
    little_nepenth = Nepenth('little nepenth', 14, 2, 13, 2, .6, 0, 13, [1])
    kobold_slave = Koboldoid('kobold slave', 13, 1, 12, 2, .75, 1, 19, [1])
    windwasp = Insect('windwasp', 12, 2, 10, 2, .55, 0, 11, [1,2])
    dire_wolf = Beast('dire wolf', 15, 1, 13, 2, .85, 0, 19, [1,3,4])
    green_worm = Worm('green worm', 21, 1, 10, 2, .35, 0, 30, [1])
    nepenth = Nepenth('nepenth', 20, 2, 14, 2, .6, 0, 14, [1])
    cave_slime = Slime('cave slime', 13, 3, 11, 2, .55, 0, 29, [1])
    kobold_soldier = Koboldoid('kobold soldier', 21, 2, 13, 2, .75, 2, 19, [1])
    Kobold_guard = Koboldoid('kobold guard', 20, 2, 14, 2, .8, 3, 17, [1])
    shrubent = Plant('shrubent', 27, 1, 14, 3, .9, 0, 24, [1])
    cave_bear = Beast('cave bear', 20, 3, 15, 3, .45, 1, 17, [1])
    pre_pod_nepenth = Nepenth('pod nepenth', 7, 1, 14, 3, .5, 0, 17, [1])
    post_pod_nepenth = Nepenth('Pod Nepenth', 21, 1, 14, 3, .5, 0, 17, [1])
    flower_nepenth = Nepenth('flower nepenth', 32, 2, 18, 3, .75, 0, 14, [1])
    red_worm = Worm('red worm', 35, 1, 14, 3, .40, 0, 28, [1])
    kosaur = Enemy('Kosaur (F-Boss)', 60, 5, 30, 3, .7, 3, 20, [1])
    big_nepenth = Nepenth('big nepenth', 35, 2, 19, 3, .7, 0, 19, [1])
    sappent = Plant('sappent', 37, 2, 19, 3, .95, 0, 25, [1])
    ruin_kobold = Koboldoid('ruin kobold', 38, 3, 20, 3, .7, 4, 18, [1,3])
    sly_srewman = Beastoid('sly shrewman', 39, 1, 17, 3, .99, 6, 4, [1,2,3,5,9])
    human_bandit = Humanoid('bandit (human)', 39, 3, 21, 4, .8, 3, 20, [1,2,3,6])
    kobold_chief = Koboldoid('kobold chief', 40, 2, 18, 4, .75, 5, 18, [1])
    black_worm = Worm('black worm', 54, 1, 19, 4, .55, 0, 28, [1,2])
    treent = Plant('treent', 50, 3, 22, 4, .65, 0, 30, [1,4])
    ruin_kobold_trooper = Koboldoid('ruin kobold trooper', 52, 3, 22, 4, .85, 5, 15, [1,3])
    bark_golem = Plant('bark golem', 61, 2, 21, 4, .90, 1, 27, [1])
    flying_kobold = Koboldoid('flying kobold', 47, 3, 25, 4, .5, 4, 9, [1])
    ruin_kobold_sentinel = Koboldoid('ruin kobold sentinel', 67, 4, 26, 5, .75, 6, 14, [1])
    illfang = Enemy('Illfang the Kobold Lord (Boss)', 140, 9, 60, 5, .9, 15, 20, [1])

    mon_list = [windworm, brown_worm, slime, refuse, cykloone, frenzy_boar, field_wolf, 
                greedy_badger, awakened_shrub, small_kobold, barkling, swarm_of_bats,
                little_nepenth, kobold_slave, windwasp, dire_wolf, green_worm, nepenth, 
                cave_slime, kobold_soldier, Kobold_guard, shrubent, cave_bear, pre_pod_nepenth,
                post_pod_nepenth, flower_nepenth, red_worm, kosaur, big_nepenth, sappent, 
                ruin_kobold, sly_srewman, human_bandit, kobold_chief, black_worm, 
                treent, ruin_kobold_trooper, bark_golem, flying_kobold, ruin_kobold_sentinel, 
                illfang]

    return mon_list


def init_allies():
    robin_0 = Ally('Robin', 1, 14, 1, 22, .7, Skill('slant', 0, 1, 1, 2, 1), 'Robin 0')
    henry = Ally('Henry', 2, 11, 3, 19, .65, Skill('reverse pull', 0, 2, 5, 4, 3))
    liliyah = Ally('Liliyah', 2, 15, 5, 18, .78, Skill('parallel sting', 0, 2, 2, 2, 2))
    tiffey = Ally('Tiffey', 2, 19, 1, 20, .7, Skill('cross hatch', 0, 3, 2, 4, 3))
    kajlo_sohler = Ally('Kajlo Sohler', 2, 17, 3, 19, .76, Skill('cork screw', 0, 1, 1, 3, 1))
    officer_jerrimathyus = Ally('Officer Jerrimathyus', 3, 26, 5, 26, .75, Skill('uppercut', 0, 3, 1, 4, 3))
    bulli = Ally('Bulli', 2, 18, 2, 20, .76, Skill('mega poke', 0, 1, 2, 2, 1))
    milo_0 = Ally('Milo', 2, 15, 3, 19, .82, Skill('linear', 0, 2, 1, 3, 3), 'Milo 0')
    gaffer = Ally('Gaffer', 1, 9, 1, 20, .6, Skill('pitch fork', 0, 1, 2, 4, 1))
    holt = Ally('Holt', 3, 27, 2, 23, .72, Skill('back rush', 0, 4, 1, 5, 4))
    suphia = Ally('Suphia', 4, 28, 3, 19, .7, Healing('quick tonic', 1, 3, 4, 4, 2, 1))
    electo = Ally('Electo', 4, 27, 3, 19, .72, SpellAttack('thunder wave', 1, 3, 4, 4, 2, 0))
    hesh = Ally('Hesh', 3, 24, 2, 19, .76, SpellAttack('fire bolt', 1, 3, 4, 3, 3, 0))
    # coef = Ally('Coef')
    # deg = Ally('Deg')
    # virabela  = Ally('Virabela')
    # polly = Ally('Polly')


    allies = [robin_0,henry,liliyah,tiffey,kajlo_sohler,officer_jerrimathyus,
              bulli,milo_0,gaffer,holt,suphia,electo,hesh]

    return allies

