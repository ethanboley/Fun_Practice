
from actions import *
from things_stuff import *
from monsters import init_enemies
import time


class BookOne:
    def __init__(self, player, xp_thresholds):
        self.player = player
        self.xp_thresholds = xp_thresholds
        self.monsters = init_enemies()
        self.battle = Battle(self.player,self.xp_thresholds)

    def play_story(self, progress):
        chapters = {
            0:self.ch_0, 1:self.ch_1, 2:self.ch_2, 3:self.ch_3, 4:self.ch_4,
            5:self.ch_5, 6:self.ch_6, 7:self.ch_7, 8:self.ch_8, 9:self.ch_9,
            10:self.ch_10, 11:self.ch_11, 12:self.ch_12, 13:self.ch_13,
            14:self.ch_14, 15:self.ch_15, 16:self.ch_16, 17:self.ch_17,
            18:self.ch_18, 19:self.ch_19, 20:self.ch_20, 21:self.ch_21,
            22:self.ch_22, 23:self.ch_23, 24:self.ch_24, 25:self.ch_25,
            26:self.ch_26, 27:self.ch_27, 28:self.ch_28, 29:self.ch_29,
            30:self.ch_30, 31:self.ch_31, 32:self.ch_32
        }

        if progress in chapters:
            return chapters[progress]()

        # if progress == 0:
        #     self.ch_0()
        # elif progress == 1:
        #     self.ch_1()
        # elif progress == 2:
        #     self.ch_2()
        # elif progress == 3:
        #     self.ch_3()
        # elif progress == 4:
        #     self.ch_4()
        # elif progress == 5:
        #     self.ch_5()
        # elif progress == 6:
        #     self.ch_6()
        # elif progress == 7:
        #     self.ch_7()
        # elif progress == 8:
        #     self.ch_8()
        # elif progress == 9:
        #     self.ch_9()
        # elif progress == 10:
        #     self.ch_10()
        # elif progress == 11:
        #     self.ch_11()
        # elif progress == 12:
        #     self.ch_12()
        # elif progress == 13:
        #     self.ch_13()
        # elif progress == 14:
        #     self.ch_14()
        # elif progress == 15:
        #     self.ch_15()
        # elif progress == 16:
        #     self.ch_16()
        # elif progress == 17:
        #     self.ch_17()
        # elif progress == 18:
        #     self.ch_18()
        # elif progress == 19:
        #     self.ch_19()
        # elif progress == 20:
        #     self.ch_20()
        # elif progress == 21:
        #     self.ch_21()
        # elif progress == 22:
        #     self.ch_22()
        # elif progress == 23:
        #     self.ch_23()
        # elif progress == 24:
        #     self.ch_24()
        # elif progress == 25:
        #     self.ch_25()
        # elif progress == 26:
        #     self.ch_26()
        # elif progress == 27:
        #     self.ch_27()
        # elif progress == 28:
        #     self.ch_28()
        # elif progress == 29:
        #     self.ch_29()
        # elif progress == 30:
        #     self.ch_30()
        # elif progress == 31:
        #     self.ch_31()
        # elif progress == 32:
        #     self.ch_32()

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
                configured_monsters.append([mon for mon in self.monsters if mon.name == name][0])
        
        return configured_monsters
    

    def ch_0(self):
        # mon_list = [mon for mon in self.monsters if mon.name in ['brown worm','slime']]
        mon_list = self.config_monsters({'brown worm':1,'slime':1})
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.zero_encounter())
        if player_lives:
            self.zero_victory()
            self.player.progress += 1
            return True
        else:
            return False

    def zero_encounter(self):
        dprint('The ground below you suddenly seems to bubble and churn.')
        dprint('Monsters begin appearing all around you! "Prepare to fight!"')
        dprint('says your little brother pulling out a sword of his own. "I know')
        dprint('you might still be a little out of it but do you best!"')
    
    def zero_victory(self):
        input()
        dprint('  .  .  .  ')
        time.sleep(.75)
        dprint(f'Wow {self.player.name}, why have you never fought like that')
        dprint('before!? I mean, those weren\'t that bad but they hardly even')
        dprint('touched you! I was sure, I\'d be doing all the fighting as')
        dprint('usual but boy have I never been more wrong!')
        dprint('Your right, your right, enough. Let\'s get back to town, were')
        dprint('not out of here yet!')


    def ch_1(self):
        mon_list1 = [mon for mon in self.monsters if mon.name in ['windworm','cykloone','greedy badger']]
        mon_list2 = [mon for mon in self.monsters if mon.name in ['greedy badger', '']]
        self.player.progress =+ 1
        return True

    def ch_2(self):
        pass

    def ch_3(self):
        pass

    def ch_4(self):
        pass

    def ch_5(self):
        pass

    def ch_6(self):
        pass

    def ch_7(self):
        pass

    def ch_8(self):
        pass

    def ch_9(self):
        pass

    def ch_10(self):
        pass

    def ch_11(self):
        pass

    def ch_12(self):
        pass

    def ch_13(self):
        pass

    def ch_14(self):
        pass

    def ch_15(self):
        pass

    def ch_16(self):
        pass

    def ch_17(self):
        pass

    def ch_18(self):
        pass

    def ch_19(self):
        pass

    def ch_20(self):
        pass

    def ch_21(self):
        pass

    def ch_22(self):
        pass

    def ch_23(self):
        pass

    def ch_24(self):
        pass

    def ch_25(self):
        pass

    def ch_26(self):
        pass

    def ch_27(self):
        pass

    def ch_28(self):
        pass

    def ch_29(self):
        pass

    def ch_30(self):
        pass

    def ch_31(self):
        pass

    def ch_32(self):
        pass

