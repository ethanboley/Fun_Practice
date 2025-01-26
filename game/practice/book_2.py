
from actions import *
from things_stuff import *
from monsters import init_enemies, init_allies
from battle import *
from stuffs_that_do import init_items
import time
import copy


class BookTwo():
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
        chapter_name = f"ch_{progress}"  # Create chapter function name string
        if hasattr(self, chapter_name):  # Check if function exists
            return getattr(self, chapter_name)()  # Call the function dynamically

    def config_monsters(self, monsters_to_include:dict={}) -> list:
        """
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
        """
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
        """
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
        """
        configured_loot = []

        for name, count in loot_to_include.items():
            for _ in range(count): # Loop to add duplicates based on count
                configured_loot.append([l for l in self.all_loot if l.name == name][0])

        return configured_loot
    
    def story_reward(self):
        self.player.progress += 1
        self.player.hp += (self.player.maxhp - self.player.hp) // 2 if self.player.hp < self.player.maxhp else 0
        self.player.gain_xp(round(self.player.level * 1.5) + self.player.progress + 5, self.xp_thresholds)

    def story_prep(self, location='2-0', name='continue'):
        self.player.location = location
        self.name = name
        for ally in self.player.allies:
            ally.hp = ally.maxhp

    def adjust_team(self, to_modify:str, add:bool | None = True):
        """
        Modifies the player's team by adding or removing allies based on their designation.
    
        Args:
            to_modify (str, required): Designation of the ally to add or remove.
            add (bool, optional): Determines whether to add or remove the ally.
                False to remove, True or leave empty to add. Defaults to True.
        """

        ally_to_modify = next((ally for ally in self.all_allies if ally.designation == to_modify), None)
    
        if not ally_to_modify:
            return
    
        if add:
            if ally_to_modify not in self.player.allies:
                self.player.allies.append(ally_to_modify)
        else:
            self.player.allies = [ally for ally in self.player.allies if ally.designation != to_modify]

