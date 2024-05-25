
from actions import *
from things_stuff import *
from monsters import init_enemies
from battle import *
from stuffs_that_do import init_items
import time
import copy


class BookOne:
    def __init__(self, player, xp_thresholds):
        self.player = player
        self.xp_thresholds = xp_thresholds
        self.monsters = init_enemies()
        self.battle = Battle(self.player,self.xp_thresholds)
        self.all_loot = init_items()

    def play_story(self, progress):
        chapter_name = f"ch_{progress}"  # Create chapter function name string
        if hasattr(self, chapter_name):  # Check if function exists
            return getattr(self, chapter_name)()  # Call the function dynamically



        # chapters = {
        #     0:self.ch_0, 1:self.ch_1, 2:self.ch_2, 3:self.ch_3, 4:self.ch_4,
        #     5:self.ch_5, 6:self.ch_6, 7:self.ch_7, 8:self.ch_8, 9:self.ch_9,
        #     10:self.ch_10, 11:self.ch_11, 12:self.ch_12, 13:self.ch_13,
        #     14:self.ch_14, 15:self.ch_15, 16:self.ch_16, 17:self.ch_17,
        #     18:self.ch_18, 19:self.ch_19, 20:self.ch_20, 21:self.ch_21,
        #     22:self.ch_22, 23:self.ch_23, 24:self.ch_24, 25:self.ch_25,
        #     26:self.ch_26, 27:self.ch_27, 28:self.ch_28, 29:self.ch_29,
        #     30:self.ch_30, 31:self.ch_31, 32:self.ch_32
        # }

        # if progress in chapters:
        #     return chapters[progress]()



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
                monster = [mon for mon in self.monsters if mon.name == name][0]
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

    

    def ch_0(self):
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
        dprint('says your little brother Robin pulling out a sword of his own.')
        dprint('"I know you might still be a little out of it but do you best!"')
    
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
        mon_list1 = self.config_monsters({'windworm':1,'cykloone':1,'greedy badger':1})
        mon_list2 = self.config_monsters({'greedy badger': 3, 'frenzy boar':1})
        self.one_intro()
        player_lives = self.battle.story(mon_list=mon_list1, dialog=self.one_encounter0())
        if player_lives:
            self.one_victory0()
            player_lives = self.battle.story(mon_list=mon_list2, dialog=self.one_encounter1())
            if player_lives:
                self.one_victory1()
                self.player.progress += 1
                return True
            else:
                return False
        else:
            return False
    
    def one_intro(self):
        dprint('You and Robin pick up the pace. On your way your conversation')
        dprint('turns to why you collapsed and why you can\'t remember much')
        dprint('anymore. Robin is visibly concerned, wonders about a')
        dprint('concussion and begins waving 3 finger in your face! "How many')
        dprint(f'fingers {self.player.name}? How many!!?"')
        dprint('You really don\'t feel very off and you assure him so. You are')
        dprint('a little concerned about the memory loss thing but your sure')
        dprint('it\'ll all come back to you soon.')
    
    def one_encounter0(self):
        dprint('A few minutes at a light jog brings you both within sight of the')
        dprint('town walls. Right at that moment though, you are both attacked')
        dprint('by giant bugs from the nearby trees. In the chaos, a pack of')
        dprint('theiving rodents snatch Robin\'s sword away. Its all up to you!')

    def one_victory0(self):
        dprint(' . . .')
        time.sleep(.4)
        dprint('AAAAAH! NOOO! This is bad. Those Badgers ran off with my sword,')
        dprint('well, I guess it\'s mom\'s sword, but honestly that makes it')
        dprint('worse. We\'ve got to get it back!')
        dprint('You both sprint after the thieves all the while Robin ensures')
        dprint('you he\'ll back you up in any way he can without his sword.')

    def one_encounter1(self):
        dprint('A good 10 minute chase finally leaves the little bandits')
        dprint('cornered. They turn and prepare to fight!')

    def one_victory1(self):
        dprint(' . . .')
        time.sleep(.75)
        dprint('"You sure you didn\'t just become a whole different person? You')
        dprint('NEVER fought so well before! Not that I\'m complaining!')
        dprint('Normally, a gaggle of greedy badgers and a flippin FRENZY BOAR,')
        dprint('for crying out loud, would have done us in! Well, anyway, I\'ve')
        dprint('got mom\'s sword back so we should be ... well, at least more')
        dprint('fine than we already were..."')


    def ch_2(self):
        mon_list0 = self.config_monsters({'field wolf':2})
        mon_list1 = self.config_monsters({'field wolf':3, 'small kobold':2})
        mon_list2 = self.config_monsters({'refuse':1})
        self.two_intro()
        player_lives = self.battle.story(mon_list=mon_list0, dialog=self.two_encounter0())
        if player_lives:
            self.two_victory0()
            player_lives = self.battle.story(mon_list=mon_list1, dialog=self.two_encounter1())
            if player_lives:
                self.two_victory1()
                player_lives = self.battle.story(mon_list=mon_list2, dialog=self.two_encounter2())
                if player_lives:
                    self.two_victory2()
                    self.player.progress += 1
                    return True
                else: 
                    return False
            else:
                return False
        else:
            return False
    
    def two_intro(self):
        dprint('The siblings continue towards the town as the evening sky')
        dprint('grows from blue to orange. On your way Robin begins giving you')
        dprint('a quick rundown of everything you may have forgotten and, sure')
        dprint('enough and to your great relief, as he speaks, recolection')
        dprint('washes over you. If only peice by peice.')
        dprint(f'You are 17 years old, your Father, {self.player.name} Sr. runs')
        dprint('a shipping guild and is often away. Annabell, your mother, is')
        dprint('at home near the outskirts of the very town you and Robin left')
        dprint('this morning, taking care of your 9 year old little sister, ')
        dprint(f'Rosie and worrying about her 3 sons, Robin, 14 years old; {self.player.name},')
        dprint('17 years old; and Elond, 22 years old who has worked with your')
        dprint('father in the shipping guild for the past 3 years.')
        dprint('Robin reminds you to your sorrow, that just over 12 years ago')
        dprint('now, the brother that would have been the oldest at 24 now,')
        dprint('vanished and hasn\'t been seen since. As he says this, you')
        dprint('remember the face of your long lost brother from the few years')
        dprint('you knew him; kind and energetic with hair just like the rest')
        dprint('of your brothers, wild and a light shade of brown.')
        dprint('Robin reminds you that the town you have lived in all your life')
        dprint('is called Greentown named for the rolling hills of grass and')
        dprint('sparse woodlands surrounding it.')
        dprint('Greentown lies about 5 miles inland of the coast of the realm of')
        dprint('Mainenkedren. The capital, Kedren Main, lies to the north-west')
        dprint('along the same coastline.')
        dprint('This morning, Spring 11th, 3044, 6th age, you and Robin left')
        dprint('Greentown to an outpost 15 miles due south-east to meet with')
        dprint('a high speed delivery service. You took some letters and a')
        dprint('gift pack for your Father and Elond. About 30 minutes ago,')
        dprint('You unexpectedly passed out and woke minutes later with very')
        dprint('limitded memories and notably improved combat skills. This')
        dprint('inexplicable change has already come in handy and appears now')
        dprint('to be especially so as the night draws near and the monsters')
        dprint('come out of their holes. . . ')

    def two_encounter0(self):
        loot = self.config_loot({'life potion':3})
        dprint('Sure enough, the conversation is cut short as a pair of wolves')
        dprint('catch your scent and move in for the kill. ')
        dprint(f'"Here {self.player.name} take these!" Robin throws you 3 red')
        dprint('bottles.')
        dprint(f'{self.player.name} gained the following items from Robin!')
        for l in loot:
            print(f'{l.name}')
            self.player.inventory.add_item(l)
        print()

    def two_victory0(self):
        dprint('. . .')
        time.sleep(.5)
        dprint('You still good!?')

    def two_encounter1(self):
        dprint('Good, because I think were in for a round 2', .04)
        dprint(' . . . .       ',.1)
        dprint('Wait, are those Kobolds with them? Armed Kobolds?! But I')
        dprint('thought, well, nevermind, they\'re here now and I heard they')
        dprint('can be mighty tricky in a fight so be careful and use those')
        dprint('life potions!')

    def two_victory1(self):
        dprint('. . .')
        time.sleep(.7)
        dprint('*pant* "Well, that was ... strange! I\'ve" never even seen let')
        dprint('alone fought a kobold! I heard they\'re around these woods')
        dprint('sometimes but they always keep to themselves... Right! sorry,')
        dprint('little goblin like creatures that supposedly have dragon blood')
        dprint('and will USUALLY do nothing but steal food from farmers or')
        dprint('other Kobolds in the dead of night. These ones appear to be,')
        dprint('attacking random passers by in, well, I can\'t really call this')
        dprint('\'broad daylight\' anymore but its still weird.')

    def two_encounter2(self):
        dprint('"Makes me wonder if somethi... GAAAH! ...Oh, its just a refuse.')
        dprint('That scared the jive out of me!')

    def two_victory2(self):
        dprint('. . .', .4)
        time.sleep(.3)
        dprint('The two of you continue back to Greentown definitely worse for')
        dprint('ware, but you drink the remaining life potions your mother left')
        dprint('for you and you feel much better heading home. You have a few')
        dprint('close encounters with an awakened shrub or two but nothing to')
        dprint('bad and soon enough the sun sets completely and just in time')
        dprint('you cross the gate into town. Another minute later you catch a')
        dprint('glimpse of your mother Annabell, pacing up and down on the')
        dprint('darkened porch of your home. After a warm embrace and a quick')
        dprint('scan for open wounds, you head inside for a semi warm meal and')
        dprint('a much warmer bed.')


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

