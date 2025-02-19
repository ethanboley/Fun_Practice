
from actions import *
from things_stuff import *
from monsters import init_enemies, init_allies
from battle import *
from stuffs_that_do import init_items
import time
import copy


class BookTwo:
    def __init__(self, player, xp_thresholds):
        self.name = 'Story'
        self.player = player
        self.xp_thresholds = xp_thresholds
        self.monsters = init_enemies()
        self.battle = Battle(self.player,self.xp_thresholds)
        self.all_loot = init_items()
        self.all_allies = init_allies()
    
    def run(self, player=None, world=None, xp_thresholds=None):
        return self.play_story(player.progress)

    def play_story(self, progress):
        chapter_name = f'ch_{progress}'  # Create chapter function name string
        if hasattr(self, chapter_name):  # Check if function exists
            return getattr(self, chapter_name)()  # Call the function dynamically

    def config_monsters(self, monsters_to_include:dict={}) -> list:
        '''
        A method to set up the monsters to fight in the chapter

        Arguments: 
            monsters_to_include:
                A dictionary containing keys of type str which is the name of 
                the monster and values of type int which is the count of that 
                monster to include in the chapters monsters.

        returns:
            configured_monsters:
                A list containing the monsters of type Enemy to include in the
                chapter. 
        '''
        configured_monsters = []

        for name, count in monsters_to_include.items():
            for _ in range(count):  # Loop to add duplicates based on count
                try:
                    monster = [mon for mon in self.monsters if mon.name == name][0]
                except IndexError as err:
                    print('Oops, that monster doesn\'t exist!')
                    print(err)
                configured_monsters.append(copy.deepcopy(monster))  # Deepcopy and append
        
        return configured_monsters

    def config_loot(self, loot_to_include:dict={}):
        '''
        A method to set up the loot to gain in the chapter

        Arguments: 
            loot_to_include:
                A dictionary containing keys of type str which is the name of 
                the item and values of type int which is the count of that 
                item to include in the chapters monsters.

        returns:
            configured_loot:
                A list containing the items of type Item to include in the 
                chapter. 
        '''
        configured_loot = []

        for name, count in loot_to_include.items():
            for _ in range(count): # Loop to add duplicates based on count
                configured_loot.append([l for l in self.all_loot if l.name == name][0])

        return configured_loot
    
    def chapter_end(self, location='2-0', name='continue'):
        self.player.progress += 1
        self.player.hp += (self.player.maxhp - self.player.hp) // 2 if self.player.hp < self.player.maxhp else 0
        self.player.gain_xp(round(self.player.level * 1.5) + self.player.progress + 5, self.xp_thresholds)
        self.player.location = location
        self.name = name
        for ally in self.player.allies:
            ally.hp = ally.maxhp

    def adjust_team(self, to_modify:dict | None = None):
        '''
        
        '''
        if to_modify is None:
            return
        
        for tmate, do in to_modify.items():
            ally_to_modify = next((ally for ally in self.all_allies if ally.designation == tmate), None)
        
            if not ally_to_modify:
                continue

            if do:
                if ally_to_modify not in self.player.allies:
                    self.player.allies.append(ally_to_modify)
            else:
                self.player.allies = [ally for ally in self.player.allies if ally.designation != tmate]

    def chapter_loop(self, ch_num, part, parts, battles):
        alive = self.player.is_alive()
        while alive:
            if part % 2 == 0:
                alive = getattr(self, f'passage_{ch_num}_{part}')()
            else:
                alive = self.battle.battle(*battles[part // 2])
            part += 1
            if part == parts:
                self.chapter_end(location='2-0', name='continue')
                break
        return alive

    '''
    def ch00(self): # example chapter (unused)
        ch_num, part, parts = (00, 0, 13)
        self.adjust_team(to_modify={'Person':True, 'personage_3':True, 'Individual':False, 'sample_desigantion_4':False})
        battles = {
            0:(self.config_monsters({'monster':2}), getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')), False, False, ['']),
            1:(self.config_monsters({'monster':2}), getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')), True, False, ['']),
            2:(self.config_monsters({'boss':1}), getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')), True, False, [getattr(self, f'boss_{ch_num}_0')(), getattr(self, f'boss_{ch_num}_1')]), 
            3:(self.config_monsters({'monster':1}), getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')), False, False, ['']),
            4:(self.config_monsters({'monster':3}), getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')), False, True, ['']),
            5:(self.config_monsters({'person':1}), getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')), True, False, [''])}
        return self.chapter_loop(ch_num, part, parts, battles)
    '''


    def ch0(self):
        ch_num, part, parts = (0, 0, 2)
        battles = { # part:(mon_list, dialog, collective=False, surprise=False, boss_dialog=[''])
            0:(self.config_monsters({'monster':2}),
               getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')),
               False, False)}
        return self.chapter_loop(ch_num, part, parts, battles)

    def passage_0_0(self):
        dprint('', story=True)
    
    def prefight_0_1(self):
        dprint('', story=True)

    def passage_0_2(self):
        dprint('', story=True)