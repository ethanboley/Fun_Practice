
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
    def __init__(self, name, hp, atk, xp, level, accuracy, col, agi, world, ac):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.xp = xp
        self.level = level
        self.accuracy = accuracy
        self.col = col
        self.agi = agi
        self.world = world
        self.ac = ac
        self.has_phases = False

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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.atk = atk
        self.xp = xp
        self.level = level
        self.acu = acu
        self.col = col
        self.agi = agi
        self.world = world
        self.ac = ac
        self.has_phases = True
        self.phases = 0
    
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
    
    def choose_target(self, targets:list):
        if len(targets):
            return random.choice(targets)
        else:
            return None

    def is_alive(self):
        return self.hp > 0 or self.phases > 0


# ----------- Bosses

class BossTest(Boss):
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
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
            strong_damage = self.atk + random.randint(-2, (self.atk // 3)) + 6
            weak_damage = self.atk
            if random.random() < self.acu + self.acu_mod:
                player.hp -= strong_damage
                dprint(f'{self.name} {self.title} big attack {player.name} with big attackness!')
                dprint(f'the attack hits {player.name} for {strong_damage} damage!')
                if player.is_alive():
                    display_health(player)
                else:
                    dprint(f'The big attack kilt {player.name}!')
            elif random.random() < self.acu:
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac) -> None:
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
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
            else:
                self.bite(player)
    
    def claw(self, player):
        can_use = random.randint(1,5) in [3, 4, 5]
        if can_use:
            strong_damage = self.atk + random.randint(-2, (self.atk // 3)) + 6
            weak_damage = self.atk
            if random.random() < self.acu + self.acu_mod:
                player.hp -= strong_damage
                dprint(f'{self.name} {self.title} slashes {player.name} with it\'s steel claws!')
                dprint(f'the attack hits {player.name} for {strong_damage} damage!')
                if player.is_alive():
                    display_health(player)
                else:
                    dprint(f'The claws split {player.name} in two!')
            elif random.random() < self.acu:
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
            strong_damage = self.atk + random.randint(1, self.atk + 1) + 2
            weak_damage = self.atk - random.randint(0, 1)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac) -> None:
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
        self.acu_mod = .03
        self.title = 'the Kobold Lord'
    
    def talwar():
        pass

    def odachi():
        pass


class Barran(Boss):
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
        self.acu_mod = .03
        self.title = 'the General Tarus'

    def lance():
        pass


class Asterios(Boss):
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
        self.acu_mod = .04
        self.title = 'the Tarus King'

    def mace():
        pass


# ----------- Monsters


class Beastoid(Enemy):
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, acu, col, agi, world, ac)
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
    def __init__(self, name, hp, atk, xp, level, accuracy, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, accuracy, col, agi, world, ac)
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
    def __init__(self, name, hp, atk, xp, level, accuracy, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, accuracy, col, agi, world, ac)
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
    def __init__(self, name, hp, atk, xp, level, accuracy, col, agi, world, ac):
        super().__init__(name, hp, atk, xp, level, accuracy, col, agi, world, ac)
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
    test_boss = BossTest('test_boss', 12, 2, 600, 1, .6, 20, 24, [1], (750, 50, 120, 5))
    windworm = Worm('windworm', 1, 1, 3, 1, .15, 0, 33, [1], (500, 26, 180, 8)) 
    brown_worm = Worm('brown worm', 2, 1, 4, 1, .2, 0, 44, [1], (450, 3, 60, 20)) # limit ratio 450:95
    slime = Slime('slime', 2, 1, 5, 1, .35, 0, 31, [1], (600, 8, 200, 10))
    refuse = Construct('refuse', 3, 1, 4, 1, .2, 1, 25, [1,3,6,9], (400, 15, 300, 12))
    cykloone = Insect('cykloone', 3, 1, 3, 1, .15, 0, 16, [1], (250, 20, 500, 6))
    frenzy_boar = Beast('frenzy boar', 4, 1, 6, 1, .55, 0, 18, [1,2,3,4], (600, 8, 420, 10))
    field_wolf = Beast('field wolf', 5, 1, 6, 1, .7, 0, 15, [1,2], (300, 9, 360, 10))
    greedy_badger = Beastoid('greedy badger', 5, 1, 5, 1, .35, 2, 13, [1,2,3], (200, 8, 400, 8))
    awakened_shrub = Plant('awakened shrub', 5, 1, 5, 1, .6, 0, 22, [1,4,5], (600, 9, 460, 10))
    small_kobold = Koboldoid('small kobold', 6, 2, 8, 1, .45, 1, 21, [1], (700, 8, 510, 4))
    barkling = Plant('barkling', 8, 1, 7, 1, .4, 0, 27, [1], (500, 4, 200, 10))
    swarm_of_bats = Beast('swarm of bats', 8, 1, 9, 1, .9, 0, 16, [1,2,3,4,5], (800, 4, 400, 30))
    little_nepenth = Nepenth('little nepenth', 14, 2, 13, 2, .6, 0, 13, [1], (400, 8, 300, 2))
    kobold_slave = Koboldoid('kobold slave', 13, 1, 12, 2, .75, 1, 19, [1], (750, 9, 490, 4))
    windwasp = Insect('windwasp', 12, 2, 10, 2, .55, 0, 11, [1,2], (700, 10, 800, 7))
    dire_wolf = Beast('dire wolf', 15, 1, 13, 2, .85, 0, 19, [1,3,4], (300, 9, 400, 10))
    green_worm = Worm('green worm', 21, 1, 10, 2, .35, 0, 30, [1], (300, 4, 65, 19))
    nepenth = Nepenth('nepenth', 20, 2, 14, 2, .6, 0, 14, [1], (400, 10, 300, 2))
    onikuma = Beast('onikuma', 17, 3, 14, 2, .7, 0, 25, [1], (760, 32, 760, 4))
    cave_slime = Slime('cave slime', 13, 3, 11, 2, .55, 0, 29, [1], (600, 8, 200, 10))
    kobold_soldier = Koboldoid('kobold soldier', 21, 2, 13, 2, .75, 2, 19, [1], (800, 12, 500, 4))
    Kobold_guard = Koboldoid('kobold guard', 20, 2, 14, 2, .8, 3, 17, [1], (800, 12, 560, 4))
    shrubent = Plant('shrubent', 27, 1, 14, 3, .9, 0, 24, [1], (600, 11, 400, 10))
    cave_bear = Beast('cave bear', 25, 4, 15, 3, .55, 1, 21, [1], (900, 48, 1000, 6))
    pre_pod_nepenth = Nepenth('pod nepenth', 7, 1, 14, 3, .5, 0, 17, [1], (400, 80, 300, 2))
    post_pod_nepenth = Nepenth('Pod Nepenth', 21, 1, 14, 3, .5, 0, 17, [1], (400, 11, 300, 2))
    flower_nepenth = Nepenth('flower nepenth', 32, 2, 18, 3, .75, 0, 14, [1], (400, 11, 300, 2))
    red_worm = Worm('red worm', 35, 1, 14, 3, .40, 0, 28, [1], (250, 3, 70, 18))
    kosaur = Kosaur('Kosaur', 144, 6, 300, 3, .75, 3, 21, [1], (900, 80, 1200, 5))
    big_nepenth = Nepenth('big nepenth', 35, 2, 19, 3, .7, 0, 19, [1], (350, 12, 300, 2))
    sappent = Plant('sappent', 37, 2, 19, 3, .95, 0, 25, [1], (600, 14, 360, 10))
    ruin_kobold = Koboldoid('ruin kobold', 38, 3, 20, 3, .7, 4, 20, [1,3], (600, 10, 600, 4))
    sly_srewman = Beastoid('sly shrewman', 39, 1, 17, 3, .99, 6, 4, [1,2,3,5,9], (200, 6, 480, 2))
    human_bandit = Humanoid('bandit', 21, 7, 20, 4, .8, 3, 20, [1,2,3,6], (600, 10, 500, 4))
    kobold_chief = Koboldoid('kobold chief', 40, 2, 18, 4, .75, 5, 18, [1], (750, 12, 620, 4))
    blue_worm = Worm('blue worm', 54, 2, 19, 4, .55, 0, 27, [1,2], (225, 12, 80, 17))
    treent = Plant('treent', 66, 4, 22, 4, .65, 0, 30, [1,4], (600, 20, 300, 5))
    ruin_kobold_trooper = Koboldoid('ruin kobold trooper', 52, 3, 22, 4, .85, 5, 15, [1,3], (600, 10, 640, 3))
    skeleton = Undead('skeleton', 38, 9, 26, 4, .7, 1, 19, [1,2,3,4,5,6,7,8,9,10], (500, 10, 300, 6))
    bark_golem = Plant('bark golem', 61, 2, 21, 4, .90, 1, 27, [1], (500, 8, 360, 10))
    flying_kobold = Koboldoid('flying kobold', 47, 3, 25, 4, .5, 4, 9, [1], (850, 14, 480, 2))
    ruin_kobold_sentinel = Koboldoid('ruin kobold sentinel', 67, 4, 26, 5, .75, 6, 14, [1], (600, 10, 720, 3))
    # ac: (dist or def, size ratio, actual speed, balance)    (rail_size600px, hit_dc10px, speed480fps, chances10i)
    illfang = Enemy('Illfang the Kobold Lord (Boss)', 140, 11, 1000, 5, .9, 15, 20, [1], (980, 18, 840, 6))

    jackelope = Beast('jackelope', 9, 1, 8, 2, .8, 0, 12, [1], (600, 7, 200, 10))
    borogrove = Beast('borogrove', 30, 3, 20, 3, .7, 1, 22, [1,2,3], (600, 16, 255, 10))
    silver_fish = Insect('silverfish', 8, 2, 5, 1, .6, 0, 20, [1,3,4,9], (500, 5, 180, 16))
    moamwrath = Monstrosity('moamwrath', 99, 7, 34, 6, .666, 0, 17, [1,2,3,5], (720, 22, 720, 22))
    bryllyg = Monstrosity('bryllyg', 37, 5, 22, 4, .9, 1, 20, [1], (600, 18, 200, 10))
    slythy_tove = Monstrosity('slythy tove', 66, 4, 26, 5, .7, 0, 20, [1], (600, 14, 190, 10))
    borogove = Monstrosity('borogove', 41, 4, 26, 4, .62, 0, 17, [1], (800, 14, 118, 10))
    marzeedote = Beast('marzeedote', 40, 3, 20, 4, .75, 0, 20, [1], (600, 14, 200, 6))
    doezeedote = Beast('doezeedote', 80, 9, 55, 6, .81, 0, 19, [1], (500, 18, 210, 8))
    little_amzedivie = Monstrosity('little amzedivie', 164, 24, 119, 9, .675, 0, 20, [1], (600, 9, 125, 11))
    kiddleydivie = Monstrosity('kiddleydivie', 70, 5, 30, 5, .7, 0, 20, [1], (100, 8, 100, 8))
    woodenchew = Construct('woodenchew', 12, 12, 12, 3, .65, 1, 12, [1,2], (300, 5, 70, 9))
    condemned_goblin = Goblinoid('condemned goblin', 50, 6, 23, 5, .74, 0, 17, [1], (700, 9, 194, 4))
    goblin = Goblinoid('goblin', 50, 4, 19, 5, .7, 8, 20, [1,2,3], (600, 12, 160, 10))
    goblin_king = Goblinoid('goblin king', 100, 8, 32, 7, .88, 0, 26, [1], (500, 13, 180, 5))
    shinigami = Astral('shinigami', 44, 3, 17, 4, .595, 0, 14, [1,6,8,9,10], (995, 10, 205, 2))
    large_cave_slime = Slime('large cave slime', 26, 6, 26, 4, .775, 0, 25, [1,2], (800, 16, 400, 20))
    owlbear = Beast('owlbear', 32, 3, 16, 4, .685, 1, 18, [1,2], (750, 20, 300, 12))
    irrawrtzus = Beastoid('irrawrtzus', 55, 4, 35, 6, .89, 5, 20, [2,3,4,6], (800, 12, 700, 6))

    black_worm = Worm('black worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (210, 5, 90, 16))
    bronze_worm = Worm('bronze worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (200, 6, 100, 15))
    white_worm = Worm('snow worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (185, 6, 120, 14))
    yellow_worm = Worm('yellow worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (175, 7, 145, 13))
    fall_worm = Worm('fall worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (160, 7, 160, 12))
    blood_worm = Worm('blood worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (145, 8, 180, 11))
    midnight_worm = Worm('midnight worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (130, 8, 210, 10))
    purple_worm = Worm('purple worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (115, 8, 240, 9))
    water_worm = Worm('water worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (100, 6, 260, 9))
    fire_worm = Worm('fire worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (100, 5, 280, 8))
    wyrm_worm = Worm('wyrm worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (200, 4, 320, 7))
    giant_brown_worm = Worm('giant brown worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (400, 15, 360, 6))
    giant_green_worm = Worm('giant green worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (415, 16, 400, 6))
    giant_red_worm = Worm('giant red worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (430, 17, 440, 5))
    giant_blue_worm = Worm('giant blue worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (445, 18, 480, 5))
    giant_black_worm = Worm('giant black worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (460, 19, 500, 4))
    giant_bronze_worm = Worm('giant bronze worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (480, 20, 520, 4))
    giant_white_worm = Worm('giant snow worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (500, 21, 540, 4))
    giant_yellow_worm = Worm('giant yellow worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (520, 22, 560, 3))
    giant_fall_worm = Worm('giant fall worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (540, 23, 580, 3))
    giant_blood_worm = Worm('giant blood worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (560, 24, 600, 3))
    giant_midnight_worm = Worm('giant midnight worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (580, 25, 620, 2))
    giant_purple_worm = Worm('giant purple worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (600, 26, 640, 2))
    giant_wyrm_worm = Enemy('giant wyrm worm', 54, 1, 19, 4, .55, 0, 28, [1,2], (990, 24, 720, 2)) # side boss
    
    


    mon_list = [test_boss, windworm, brown_worm, slime, refuse, cykloone, frenzy_boar, field_wolf, 
                greedy_badger, awakened_shrub, small_kobold, barkling, swarm_of_bats,
                little_nepenth, kobold_slave, windwasp, dire_wolf, green_worm, nepenth, onikuma,
                cave_slime, kobold_soldier, Kobold_guard, shrubent, cave_bear, pre_pod_nepenth,
                post_pod_nepenth, flower_nepenth, red_worm, kosaur, big_nepenth, sappent, 
                ruin_kobold, sly_srewman, human_bandit, kobold_chief, blue_worm, black_worm, 
                treent, ruin_kobold_trooper, bark_golem, skeleton, flying_kobold, 
                ruin_kobold_sentinel, illfang, jackelope, borogrove, silver_fish]

    return mon_list


def init_allies(): # designations use snake case and numerals
    robin_0 = Ally('Robin', 1, 14, 1, 22, .7, Skill('slant', 0, 1, 1, 2, 1), 'robin_0')
    henry = Ally('Henry', 2, 11, 3, 19, .65, Skill('reverse pull', 0, 2, 5, 4, 3))
    liliyah = Ally('Liliyah', 2, 15, 5, 18, .78, Skill('parallel sting', 0, 2, 2, 2, 2))
    tiffey = Ally('Tiffey', 2, 19, 1, 20, .7, Skill('cross hatch', 0, 3, 2, 4, 3))
    kajlo_sohler = Ally('Kajlo Sohler', 2, 17, 3, 19, .76, Skill('cork screw', 0, 1, 1, 3, 1))
    officer_jerrimathyus = Ally('Officer Jerrimathyus', 3, 26, 5, 26, .75, Skill('uppercut', 0, 3, 1, 4, 3))
    bulli = Ally('Bulli', 2, 18, 2, 20, .76, Skill('mega poke', 0, 1, 2, 2, 1))
    milo_0 = Ally('Milo', 2, 15, 3, 19, .82, Skill('linear', 0, 2, 1, 3, 3), 'milo_0')
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

