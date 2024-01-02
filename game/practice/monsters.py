
import random
from actions import *
from things_stuff import init_items


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
    def __init__(self, name, hp, atk, xp, level, accuracy, col, agi):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.xp = xp
        self.level = level
        self.accuracy = accuracy
        self.col = col
        self.agi = agi

    def attack(self, player):
        if random.random() < self.accuracy:
            player.hp -= self.atk
            dprint(f"{self.name} attacks {player.name} for {self.atk} damage!")
            if player.is_alive():
                display_health(player)
            else:
                dprint('You have died!')
        else:
            dprint(f"{self.name} misses their attack!")

    def is_alive(self):
        return self.hp > 0
    
    def drop(self, player):
        pass


class Boss:
    def __init__(self, name, hp, atk, xp, level, acu, col, agi):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.xp = xp
        self.level = level
        self.acu = acu
        self.col = col
        self.agi = agi
    
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi) -> None:
        super().__init__(name, hp, atk, xp, level, acu, col, agi)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi) -> None:
        super().__init__(name, hp, atk, xp, level, acu, col, agi)
        self.acu_mod = .03
        self.title = 'the Kobold Lord'
    
    def talwar():
        pass


class Barran(Boss):
    def __init__(self, name, hp, atk, xp, level, acu, col, agi):
        super().__init__(name, hp, atk, xp, level, acu, col, agi)
        self.acu_mod = .03
        self.title = 'the General Tarus'

    def lance():
        pass


class Asterios(Boss):
    def __init__(self, name, hp, atk, xp, level, acu, col, agi):
        super().__init__(name, hp, atk, xp, level, acu, col, agi)
        self.acu_mod = .04
        self.title = 'the Tarus King'

    def mace():
        pass


# ----------- Monsters


class Beastoid(Enemy):
    def __init__(self, name, hp, atk, xp, level, acu, col, agi):
        super().__init__(name, hp, atk, xp, level, acu, col, agi)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi):
        super().__init__(name, hp, atk, xp, level, acu, col, agi)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi):
        super().__init__(name, hp, atk, xp, level, acu, col, agi)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi):
        super().__init__(name, hp, atk, xp, level, acu, col, agi)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi):
        super().__init__(name, hp, atk, xp, level, acu, col, agi)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi):
        super().__init__(name, hp, atk, xp, level, acu, col, agi)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi):
        super().__init__(name, hp, atk, xp, level, acu, col, agi)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi):
        super().__init__(name, hp, atk, xp, level, acu, col, agi)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi):
        super().__init__(name, hp, atk, xp, level, acu, col, agi)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi):
        super().__init__(name, hp, atk, xp, level, acu, col, agi)
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
    def __init__(self, name, hp, atk, xp, level, acu, col, agi):
        super().__init__(name, hp, atk, xp, level, acu, col, agi)
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
    dr_ed_bmed = Doctor('Dr. Ed B.med.', 2, 2, 1, 1, .4)
    dr_doug_bmbs = Doctor('Dr. Doug BMBS', 3, 3, 2, 1, .55)
    dr_steven_int = Doctor('Dr. Steven Intern', 3, 1, 2, 1, .35)
    dr_sye_bsrg = Doctor('Dr. Sye B.Srg.', 4, 4, 3, 1, .8)
    dr_tom_mbbs = Doctor('Dr. Tom MBBS', 5, 3, 3, 1, .5)
    dr_van_mph = Doctor('Dr. Van MPH', 6, 4, 4, 1, .5)
    dr_al_mphil = Doctor('Dr. Al M.Phil.', 7, 2, 3, 1, .6)
    dr_bill_mcm = Doctor('Dr. Bill MCM', 7, 5, 4, 1, .65)
    dr_red_mmsc = Doctor('Dr. Red MMSc.', 9, 3, 3, 2, .7)
    dr_greg_msc = Doctor('Dr. Greg MSc', 10, 4, 4, 2, .75)
    dr_rick_msrg = Doctor('Dr. Rick M.Srg.', 11, 5, 5, 2, .95)
    dr_lars_mm = Doctor('Dr. Lars MM', 11, 6, 5, 2, .75)
    dr_ford_da = Doctor('Dr. Ford DA', 13, 4, 4, 3, .9)
    dr_phil_dn = Doctor('Dr. Phill DN', 14, 3, 4, 3, .85)
    dr_hal_dhms = Doctor('Dr. Hal DHMs', 15, 4, 5, 3, .9)
    dr_paul_phd = Doctor('Dr. Paul Ph.D.', 16, 7, 6, 3, .85)
    dr_fred_dm = Doctor('Dr. Fred DM', 17, 8, 8, 3, .95)
    dr_bert_gp = Doctor('Dr. Bert GP', 18, 5, 6, 3, .8)
    dr_gord_dcm = Doctor('Dr. Gord DCM', 20, 6, 7, 4, .95)
    dr_boe_dsrg = Doctor('Dr. Boe D.Srg.', 21, 6, 7, 4, .99)
    dr_jerry_do = Doctor('Dr. Jerry DO', 23, 8, 8, 4, .95)
    dr_dan_md = Doctor('Dr. Dan MD', 24, 9, 9, 4, .9)
    dr_russ = Doctor('Dr. Russ', 30, 10, 15, 5, .99)
    dr_the = Doctor('The Doctor', 35, 10, 16, 5, .99)
    
    doc_list = [dr_ed_bmed, dr_doug_bmbs, dr_steven_int, dr_sye_bsrg, 
                dr_tom_mbbs, dr_van_mph, dr_al_mphil, dr_bill_mcm, 
                dr_red_mmsc, dr_red_mmsc, dr_greg_msc, dr_rick_msrg, 
                dr_lars_mm, dr_ford_da, dr_phil_dn, dr_hal_dhms, dr_paul_phd,
                dr_fred_dm, dr_bert_gp, dr_gord_dcm, dr_boe_dsrg, 
                dr_jerry_do, dr_dan_md, dr_russ, dr_the]

    return doc_list

def init_enemies(): 
    windworm = Worm('windworm', 2, 1, 2, 1, .2, 0, 31) # changed from 2 to 55 for debugging puroses
    brown_worm = Worm('brown worm', 4, 1, 3, 1, .35, 0, 42)
    slime = Slime('slime', 4, 1, 4, 1, .65, 0, 28)
    refuse = Construct('refuse', 5, 1, 3, 1, .45, 1, 22)
    cykloone = Insect('cykloone', 6, 1, 2, 1, .3, 0, 14)
    frenzy_boar = Beast('frenzy boar', 9, 2, 5, 1, .55, 0, 18)
    field_wolf = Beast('field wolf', 10, 2, 5, 1, .7, 0, 14)
    greedy_badger = Beastoid('greedy badger', 11, 1, 4, 1, .7, 2, 13)
    awakened_shrub = Plant('awakened shrub', 10, 2, 5, 1, .6, 0, 21)
    small_kobold = Koboldoid('small kobold', 12, 3, 7, 1, .65, 1, 20)
    barkling = Plant('barkling', 17, 1, 6, 1, .8, 0, 27)
    little_nepenth = Nepenth('little nepenth', 21, 3, 9, 2, .8, 0, 12)
    kobold_slave = Koboldoid('kobold slave', 17, 3, 8, 2, .7, 1, 19)
    windwasp = Insect('windwasp', 15, 3, 6, 2, .6, 0, 10)
    dire_wolf = Beast('dire wolf', 19, 2, 9, 2, .85, 0, 17)
    green_worm = Worm('green worm', 31, 2, 6, 2, .4, 0, 30)
    nepenth = Nepenth('nepenth', 31, 3, 10, 2, .8, 0, 14)
    kobold_soldier = Koboldoid('kobold soldier', 30, 4, 9, 2, .75, 2, 18)
    Kobold_guard = Koboldoid('kobold guard', 28, 5, 10, 2, .75, 3, 17)
    shrubent = Plant('shrubent', 37, 3, 7, 3, .9, 0, 25)
    pod_nepenth = Nepenth('pod nepenth', 38, 1, 7, 3, .8, 0, 16)
    flower_nepenth = Nepenth('flower nepenth', 45, 4, 10, 3, .8, 0, 15)
    red_worm = Worm('red worm', 49, 2, 8, 3, .45, 0, 29)
    kosaur = Enemy('Kosaur (F-Boss)', 60, 5, 18, 3, .7, 3, 20)
    big_nepenth = Nepenth('big nepenth', 50, 4, 11, 3, .8, 0, 18)
    sappent = Plant('sappent', 54, 4, 11, 3, .95, 0, 24)
    ruin_kobold = Koboldoid('ruin kobold', 53, 5, 12, 3, .8, 4, 17)
    sly_srewman = Beastoid('sly shrewman', 39, 1, 8, 3, .99, 6, 5)
    human_bandit = Humanoid('bandit (human)', 51, 6, 11, 4, .8, 3, 20)
    kobold_chief = Koboldoid('kobold chief', 62, 5, 8, 4, .7, 5, 18)
    black_worm = Worm('black worm', 78, 3, 9, 4, .5, 0, 28)
    treent = Plant('treent', 70, 5, 12, 4, .8, 0, 32)
    ruin_kobold_trooper = Koboldoid('ruin kobold trooper', 75, 6, 12, 4, .85, 5, 16)
    bark_golem = Plant('bark_golem', 91, 4, 10, 4, .95, 1, 26)
    flying_kobold = Koboldoid('flying kobold', 64, 7, 14, 4, .7, 4, 9)
    ruin_kobold_sentinel = Koboldoid('ruin kobold sentinel', 85, 7, 13, 5, .85, 6, 15)
    illfang = Enemy('Illfang the Kobold Lord (Boss)', 140, 9, 40, 5, .9, 15, 20)

    mon_list = [windworm, brown_worm, slime, refuse, cykloone, frenzy_boar, field_wolf, 
                greedy_badger, awakened_shrub, small_kobold, barkling, little_nepenth, 
                kobold_slave, windwasp, dire_wolf, green_worm, nepenth, 
                kobold_soldier, Kobold_guard, shrubent, pod_nepenth, flower_nepenth, 
                red_worm, kosaur, big_nepenth, sappent, ruin_kobold, sly_srewman, 
                human_bandit, kobold_chief, black_worm, treent, ruin_kobold_trooper, 
                bark_golem, flying_kobold, ruin_kobold_sentinel, illfang]

    return mon_list


