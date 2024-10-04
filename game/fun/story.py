
from actions import *
from things_stuff import *
from monsters import init_enemies, init_allies
from battle import *
from stuffs_that_do import init_items
import time
import copy


class BookOne:
    def __init__(self, player, xp_thresholds):
        self.name = 'Begin story'
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
        self.player.gain_xp((self.player.level * 2) + (self.player.progress * 2) + 1, self.xp_thresholds)

    def story_prep(self, location='1-1', name='continue'):
        self.player.location = location
        self.name = name

    # def adjust_team(self, to_modify:str, add_or_remove='add'):
    #     """
    #     Modifies the player's team by adding or removing allies based on their desigantion.
    #     Also removes duplicate allies with the same desigantion with the use of a set.

    #     Args:
    #         to_modify (str, required): Desigantion of the ally to add or remove.
    #         add_or_remove (str, optional): 'add' to add an ally, 'remove' to remove. Defaults to 'add'.
    #     """
    #     ally_designations = set()

    #     # The following loop records the unique designations (not names) of all
    #     # the allies that are currently in the player's list of allies into the
    #     # set called ally_designations defined just before. 
    #     for i in range(len(self.player.allies)):
    #         ally_designations.add(self.player.allies[i].designation)
        
    #     # The player's allies list is then emptied completely (should equal []).
    #     self.player.allies.clear()

    #     # The following loop iterates through all the allies defined in the entire game
    #     for ally in self.all_allies: 
    #         # each iteration, it checks the current ally's designation attribute against
    #         # the to_modify argument of the same type (str)
    #         if ally.designation == to_modify: 

    #             # when the ally is found in the list of all allies in the game, it
    #             # adds or removes that ally's designation to or from the built
    #             # set of designations.
    #             if add_or_remove == 'add':
    #                 ally_designations.add(ally.designation)
    #                 # stop looping after having found the ally
    #                 break

    #             else:
    #                 ally_designations.discard(ally.designation)
    #                 # stop looping after having found the ally
    #                 break

    #     # Finally, again iterate through all allies in the game
    #     for ally in self.all_allies: 
    #         # find only the designations that are to be in the new list of player allies
    #         if ally.designation in ally_designations:
    #             # add, by designation, all the new allies that are to populate the list
    #             self.player.allies.append(ally)

    def adjust_team(self, to_modify:str, add:bool | None = True):
        """
        Modifies the player's team by adding or removing allies based on their designation.
    
        Args:
            to_modify (str, required): Designation of the ally to add or remove.
            add (bool, optional): Determines whether to add or remove the ally.
                False to remove, True or leave empty to add. Defaults to True.
        """
        # Find the ally in the list of all allies
        ally_to_modify = next((ally for ally in self.all_allies if ally.designation == to_modify), None)
    
        # If no such ally exists, return early
        if not ally_to_modify:
            return
    
        if add:
            # Only add if the ally is not already in the player's allies list
            if ally_to_modify not in self.player.allies:
                self.player.allies.append(ally_to_modify)
        else:
            # Remove the ally if they exist in the player's allies list
            self.player.allies = [ally for ally in self.player.allies if ally.designation != to_modify]


    def ch_0(self): # Spring 11th, 3044, 6th age
        mon_list = self.config_monsters({'brown worm':1,'slime':1})
        # mon_list = self.config_monsters({'test_boss':1})
        self.adjust_team('robin_0')
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.zero_encounter(),collective=True) # changed to boss
        if player_lives:
            self.zero_victory()
            self.story_reward()
            self.story_prep(location='1-0')
            return True
        else:
            return False

    def zero_encounter(self): # bubble and churn first fight
        dprint('The ground below you suddenly seems to bubble and churn.')
        dprint('Monsters begin appearing all around you! "Prepare to fight!"')
        dprint('says your little brother Robin pulling out a sword of his own.')
        dprint('"I know you might still be a little out of it but do you best!"')
    
    def zero_victory(self): # Robin marvles almost too much
        input()
        dprint('  .  .  .  ')
        time.sleep(.75)
        dprint(f'Wow {self.player.name}, why have you never fought like that')
        dprint('before!? I mean, those weren\'t that bad but they hardly even')
        dprint('touched you! I was sure, I\'d be doing all the fighting as')
        dprint('usual but boy have I never been more wrong!')
        dprint('Your right, your right, enough. Let\'s get back to town, were')
        dprint('not out of here yet!')


    def ch_1(self): # Spring 11th, 3044, 6th age
        mon_list1 = self.config_monsters({'windworm':1,'cykloone':1,'greedy badger':1})
        mon_list2 = self.config_monsters({'greedy badger': 3, 'frenzy boar':1})
        self.adjust_team('robin_0', False)
        self.one_intro()
        player_lives = self.battle.story(mon_list=mon_list1, dialog=self.one_encounter0(), collective=True)
        if player_lives:
            self.one_victory0()
            self.adjust_team('robin_0', True)
            player_lives = self.battle.story(mon_list=mon_list2, dialog=self.one_encounter1())
            if player_lives:
                self.one_victory1()
                self.story_reward()
                self.story_prep(location='1-0', name='Continue to the town')
                self.adjust_team('robin_0', add=False)
                return True
            else:
                return False
        else:
            return False
    
    def one_intro(self): # How many fingers, heading home
        dprint('You and Robin pick up the pace. On your way your conversation')
        dprint('turns to why you collapsed and why you can\'t remember much')
        dprint('anymore. Robin is visibly concerned, wonders about a')
        dprint('concussion and begins waving 3 finger in your face! "How many')
        dprint(f'fingers {self.player.name}? How many!!?"')
        dprint('You really don\'t feel very off and you assure him so. You are')
        dprint('a little concerned about the memory loss thing but your sure')
        dprint('it\'ll all come back to you soon.')
    
    def one_encounter0(self): # bug distraction and thieving badgers
        dprint('A few minutes at a light jog brings you both within sight of the')
        dprint('town walls. Right at that moment though, you are both attacked')
        dprint('by giant bugs from the nearby trees. In the chaos, a pack of')
        dprint('theiving rodents snatch Robin\'s sword away. Its all up to you!')

    def one_victory0(self): # They got my sword... or did they
        dprint(' . . .')
        time.sleep(.4)
        dprint('AAAAAH! NOOO! This is bad. Those Badgers ran off with my sword,')
        dprint('well, I guess it\'s mom\'s sword, but honestly that makes it')
        dprint('worse. We\'ve got to get it back!')
        dprint('You both sprint after the thieves all the while Robin ensures')
        dprint('you he\'ll back you up in any way he can without his sword.')

    def one_encounter1(self): # cornered a bunch of badgers
        dprint('A good 10 minute chase finally leaves the little bandits')
        dprint('cornered. They begin to turn and prepare to fight!')

    def one_victory1(self): # Robin says flippin
        dprint(' . . .')
        time.sleep(.75)
        dprint('"You sure you didn\'t just become a whole different person? You')
        dprint('NEVER fought so well before! Not that I\'m complaining!')
        dprint('Normally, a gaggle of greedy badgers and a flippin FRENZY BOAR,')
        dprint('for crying out loud, would have done us in! Well, anyway, I\'ve')
        dprint('got mom\'s sword back so we should be ... well, at least more')
        dprint('fine than we already were..."')


    def ch_2(self): # Spring 11th, 3044, 6th age
        mon_list0 = self.config_monsters({'field wolf':2})
        mon_list1 = self.config_monsters({'field wolf':2, 'small kobold':2})
        mon_list2 = self.config_monsters({'refuse':1})
        self.adjust_team('robin_0', True)
        self.two_intro()
        player_lives = self.battle.story(mon_list=mon_list0, dialog=self.two_encounter0())
        if player_lives:
            self.two_victory0()
            player_lives = self.battle.story(mon_list=mon_list1, dialog=self.two_encounter1(), collective=True)
            if player_lives:
                self.two_victory1()
                player_lives = self.battle.story(mon_list=mon_list2, dialog=self.two_encounter2())
                if player_lives:
                    self.two_victory2()
                    self.story_reward()
                    self.story_prep()
                    self.adjust_team('robin_0',False)
                    return True
                else: 
                    return False
            else:
                return False
        else:
            return False
    
    def two_intro(self): # LOOOOOOOOORRRRE dump, Spring 11th, 3044, 6th age
        dprint('The siblings continue towards the town as the evening sky')
        dprint('grows from blue to orange. On your way Robin begins giving you')
        dprint('a quick rundown of everything you may have forgotten and, sure')
        dprint('enough and to your great relief, as he speaks, recolection')
        dprint('washes over you. If only peice by peice.')
        dprint(f'You are 17 years old, your Father, Rulid Sr. runs')
        dprint('a shipping guild and is often away. Annabell, your mother, is')
        dprint('at home near the outskirts of the very town you and Robin left')
        dprint('this morning, taking care of your 9 year old little sister, Rosie')
        dprint(f'and worrying about her 3 older children, Robin, 14 years old; {self.player.name},')
        dprint('17 years old; and Elond, 22 years old who has worked with your')
        dprint('father in the shipping guild for the past 3 years.')
        dprint('Robin reminds you to your sorrow, that just over 12 years ago')
        dprint('now, the brother that would have been the oldest at 24 now,')
        dprint('vanished and hasn\'t been seen since. As he says this, you')
        dprint('remember the face of your long lost brother from the few years')
        dprint('you knew him; kind and energetic with hair just like the rest')
        dprint('of your family, wild and a light shade of oak wood brown.')
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

    def two_encounter0(self): # A gift of Life Potions
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

    def two_victory0(self): # Really?
        dprint('. . .')
        time.sleep(.5)
        dprint('You still good!?')

    def two_encounter1(self): # strategic dprint(), first kobolds
        dprint('Good, because I think were in for a round 2', .04)
        dprint(' . . . .       ',.1)
        dprint('Wait, are those Kobolds with them? Armed Kobolds?! But I', .05)
        dprint('thought, well, nevermind, they\'re here now and I heard they')
        dprint('can be mighty tricky in a fight so be careful and use those')
        dprint('life potions!')

    def two_victory1(self): # kobolds? How strange. . . 
        dprint('. . .')
        time.sleep(.7)
        dprint('*pant* "Well, that was ... strange! I\'ve never even seen let')
        dprint('alone fought a kobold! I heard they\'re around these woods')
        dprint('sometimes but they always keep to themselves... Right! sorry,')
        dprint('they\'re little goblin like creatures that supposedly have dragon')
        dprint('blood and will USUALLY do nothing but steal food from farmers or')
        dprint('other Kobolds in the dead of night. These ones appear to be,')
        dprint('attacking random passers by in, well, I can\'t really call this')
        dprint('\'broad daylight\' anymore but its still weird.')

    def two_encounter2(self): # robin says GAAAH!
        dprint('"Makes me wonder if somethi... GAAAH! ...Oh, its just a refuse.')
        dprint('That scared the jive out of me!')

    def two_victory2(self): # a nice warm ending
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


    def ch_3(self): # Spring 12th-17th, 3044, 6th age
        mon_list1 = self.config_monsters({'slime':2,'awakened shrub':1,'barkling':1})
        mon_list2 = self.config_monsters({'small kobold': 3})
        self.adjust_team('robin_0', add=True)
        self.story_prep('1-1')
        self.three_intro()
        player_lives = self.battle.story(mon_list=mon_list1, dialog=self.three_encounter0(), collective=True)
        if player_lives:
            self.three_victory0()
            player_lives = self.battle.story(mon_list=mon_list2, dialog=self.three_encounter1(), collective=True)
            if player_lives:
                self.three_victory1()
                self.story_reward()
                self.adjust_team('robin_0', False)
                return True
            else:
                return False
        else:
            return False
        
    def three_intro(self): # a weak passes and now fight for fun!!! 
        dprint('. . .', .15)
        time.sleep(.5)
        dprint('About a week passes and your family members and people you know')
        dprint('bring you up to speed about many things in you life. You wish')
        dprint('this strange phenomenon hadn\'t happened but you\'re at least')
        dprint('glad you memories are coming back to you so easily.')
        dprint('Your brother Robin was always a fighter and now that you\'ve')
        dprint('shown this new combat prowess, he\'s been excited to show you')
        dprint('what he knows when it comes to fighting.')
        dprint('One day you two have some free time after finishing your chores')
        dprint('and you decide to go out into the forest and give yourself some')
        dprint('practical training.')
        pass # nothing super crazy happens but more kobolds appear

    def three_encounter0(self): # Now you fight for fun.
        dprint('Rather sooner than you expected, you come across a few monsters')
        dprint('upon which to practice but dispite the surprise, you\'re both')
        dprint('ready to go!')

    def three_victory0(self): # ok back home now
        dprint('Upon achieving victory in what turned out to be a more dificult')
        dprint('fight than expected, you about face and make your way back')
        dprint('towards home.')

    def three_encounter1(self): # Its a trap! second kobolds. 
        dprint('Moments later, however, you feel your body imediately entangled')
        dprint('in a thick net accompaied by several high screams and jeers of')
        dprint('a group of ambushing kobolds.')
        dprint('Robin acts quickly, narrowly avoiding getting caught as well.')
        dprint('you watch as he deftly cuts his entangled leg free and follows')
        dprint('through swipping at an aproaching kobold with a masterful')
        dprint('execution of the sword skill, slant, one you had both been')
        dprint('working on that same day.')
        dprint('The recieving kobold is blasted out of sight over a clump of')
        dprint('bushes but the others close in quickly. Robin leaps past two')
        dprint('other kobolds getting hit on the way but manages with little')
        dprint('more than a wince, take a swing at your net cutting you free.')
        dprint('a few moments of awkward struggling later while Robin defends')
        dprint('you, you both stand ready to fight.')

    def three_victory1(self): # important detour
        dprint('more than a little tired, you both hurry home in the mid')
        dprint('afternoon sun to report what has now become a seriously')
        dprint('worrying problem.')
        dprint('With little issue, you make it back and head, not home, but to')
        dprint('the town garrison to report the two kobold attacks. . .', .04)


    def ch_4(self): # Spring 17th-22nd, 3044, 6th age
        mon_list = self.config_monsters({'little nepenth':1})
        self.four_intro()
        self.adjust_team('robin_0', add=False)
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.four_encounter0())
        if player_lives:
            self.four_victory0()
            self.adjust_team('robin_0', add=False)
            self.story_prep(name='first mission')
            self.story_reward()
            return True
        else:
            return False

    def four_intro(self): # that one scene from SAO in the amphitheater
        dprint('The report to the captain of the guard, Outh Gurenge, went well')
        dprint('enough. He informed you that he has recieved similar reports')
        dprint('from various people over the past few weeks now and, after')
        dprint('thanking you again, tells you that he will keep the both of you')
        dprint('in the loop concerning the issue.')
        dprint('Five days pass in silence before you recieve a summons from the')
        dprint('captain to both of you, telling you also to invite anyone you')
        dprint('know around town who knows how to fight to a meeting in the')
        dprint('amphitheater by the barracks that next afternoon.')
        dprint('At high noon, the next day you both find yourselves seated in')
        dprint('the meeting place surrounded by several armed adults. The')
        dprint('meeting begins addressing the issue of repeated and increasing')
        dprint('kobold attacks outside the town. Requests for aid from the')
        dprint('capital have been denied due to similar problems all across the')
        dprint('realm. For this reason the captain of the guard is putting')
        dprint('together a group of willing and able adult fighters to')
        dprint('investigate different aspects of the situation.')
        dprint('Robin turns to you and complains that neither of them are adult')
        dprint('fighters but then ponders why they were summoned here in that')
        dprint('case. After a short pause, he raises his had and volunteers you')
        dprint('to join. You\'re a little embarrassed but you hear the captain')
        dprint('tell you to speak with him afterwords.')
        dprint('In answer to your questioning Robin as to why he did that, he')
        dprint('simply shruggs and tells you that your nearly old enough and')
        dprint('could probably beat each and every one of those other volunteers')
        dprint('up there anyways.')

    def four_encounter0(self): # a minor test of strength
        dprint('You and Robin stay after and speak with the captain who tells')
        dprint('you that he is willing to bring someone your age on if you can')
        dprint('prove yourself in a fight. A few minutes later, Robin is')
        dprint('sitting in the stands watching you armed and ready to fight')
        dprint('whatever the captain brings through that portcullis ahead.')
        dprint('"These suckers can be found in the deeper forests to the far')
        dprint('south of here, we usually use them to test new recruits so')
        dprint('good luck to ya!"')

    def four_victory0(self): # victory, the lion roars once more!
        dprint('.  .  .',.25)
        dprint('Having passed the captain\'s test and standing over the')
        dprint('dissolving form of the Nepenth, you hear a short cheer from the')
        dprint('anxiously spectating Robin as wells as an impressed slow clap')
        dprint('from the captain who welcomes you to the ranks with open arms.')


    def ch_5(self): # Spring 22nd and 23rd, 3044, 6th age
        mon_list0 = self.config_monsters({'dire wolf':3, 'small kobold':3, 'kobold slave':2, 'kobold guard':1})
        mon_list1 = self.config_monsters({'dire wolf':1, 'small kobold':2, 'kobold slave':2, 'kobold soldier':1})
        mon_list2 = self.config_monsters({'dire wolf':2, 'small kobold':2, 'kobold guard':1})
        self.adjust_team('Henry',add=True)
        self.adjust_team('Liliyah',add=True)
        self.adjust_team('Tiffey',add=True)
        self.adjust_team('Kajlo Sohler',add=True)
        self.adjust_team('Officer Jerrimathyus',add=True)
        self.adjust_team('robin_0', add=False)
        self.five_intro()
        player_lives = self.battle.story(mon_list=mon_list0, dialog=self.five_encounter0(), collective=True)
        if player_lives:
            self.five_victory0()
            player_lives = self.battle.story(mon_list=mon_list1, dialog=self.five_encounter1(), collective=True)
            if player_lives:
                self.five_victory1()
                player_lives = self.battle.story(mon_list=mon_list2, dialog=self.five_encounter2(), collective=True)
                if player_lives:
                    self.five_victory2()
                    self.story_reward()
                    self.adjust_team('Henry',add=False)
                    self.adjust_team('Liliyah',add=False)
                    self.adjust_team('Tiffey',add=False)
                    self.adjust_team('Kajlo Sohler',add=False)
                    self.adjust_team('Officer Jerrimathyus',add=False)
                    self.adjust_team('robin_0', add=False)
                    self.story_prep(location='1-2', name='Hurry home')
                    return True
                else: 
                    return False
            else:
                return False
        else:
            return False

    def five_intro(self): # OMG multi lined strings YES! also henry's a jerk. 
        dprint(
            '''
That evening you are sent a note requesting your first mission
with someone named Henry, a seasoned and official member of the
town guard, which will begin the next morning at dawn. 
That next morning you find yourself with your new teammate Henry
who promptly informs you that you should have arrived 10 minutes
early and begins walking away without another word.
Hours in, you have only exchanged a few words and you get the 
feeling he's not taking you too seriously.
Either way, nearly the rest of the day passes in rather 
uncomfortable silence before around twighlight, you enter the
northern outpost where you have been stationed with 2 other pairs
for the night. 
'''
        )

    def five_encounter0(self): # Its an ambush!
        dprint(
            '''
You are awoken before dawn with a soft shake and a whisper. Armed
Kobolds were spotted near the outpost. 
Soon enough you and 5 other fighters are stalking in the bushes
about 100 yards behind your quary which appears to be a gaggle of
a dozen or so Kobolds some armed, some less so. The more dangerous
ones also appear to be riding large black wolves which you are
informed are dire wolves. 
After about an hour, the kobolds make to stop for a rest. Not five
minutes later and without warning, 4 kobolds among the group 
hurl javelins right at your group. A that moment 3 more armed
Dire Wolf riders jump you from behind while the group you thought
you were following in stealth runs at you to participate in the
ambush!
'''
        )

    def five_victory0(self): # theres no way theres another one of these fights right? 
        dprint(
            '''
Blood was spilt on both sides in this battle that was never
supposed to happen, but you can't go home yet, this was
the reason you came out here in the first place. Most of you are
still able to keep fighting and the monsters are on the run. You
all need rest but you need answers more. 
'''
        )

    def five_encounter1(self): # right?!
        dprint(
            '''
You and those with you give chase, hunting the fleeing ambushers.
Across a long dark prarie, into a sparse woodland and across a
river. You pursue for over an hour before about half of their
number peel off in a different direction. In a split second
decision, you and your entire group head for the larger group
heading to the south-east. You only need one to talk anyways.
Mere minutes later you catch them and a battle breaks out again.
'''
        )

    def five_victory1(self): # Jer is good cop. *shunk*
        dprint(
            '''
Finally, after 2 brutal battles you have a captive bound and ready
for interrogation. It's rough but you can distinguish a little of
the thick accented Common tongue amongst snarls and cries of your
captive. 
"Tell us who your current boss is NOW or your guts get spilt, 
RIGHT NOW! RIGHT NOW!!!"
Bellowed Jerrimathyus brandishing Tiffey's knife inches from the
kobold's belly.
"AAAhhhchhh, aaahI NOooOohtt knooOhhwh *squeel* Naeeimme!"
The interrogation continued for only a few minutes before the
kobold was ready to talk. 
"AhhhhhlraaaIghTch, aAaHiy teehl eeEu, AaahhIeE TEEHL eEue, 
faaiene! ...Naeeimme ihz... Naeeimme IhZz... Ih-"
*shunk*
'''
        )
    
    def five_encounter2(self): # its an ambush-waaait. 
        dprint(
            '''
At the very moment of it telling, a crude, savage arrow seemed to
materialize in its head from its crown through its lower jaw 
instantly killing it.
Jerrimathyus acted the quickest, shielding himself and tackling 
Kajlo to take cover. A few more arrows narrowly missed you and one
struck Tiffey in her forearm. It seems the group that separated
earlier was back and ready to fight!
'''
        )
    
    def five_victory2(self): # rush back to town
        dprint(
            '''
Once again, you're not sure how you managed to escape yet again, 
but there is another problem, Henry appears to be teetering on the
threshold of death! Jerrimathyus takes quick notice and with you
and a wounded Liliyah, hoist up Henry's unmoving body and begin the 
long dark treck back to the outpost.
Finally you arrive and Henry's treatment is begun while
Jerrimathyus composes a letter to Henry's family and yet another to
the town physicians for emergency medical aid.
"Rulid, as Henry's teammate, I'm tasking you with delivering these
letters with as much speed as you can muster. Kajlo will accompany
you, follow his lead."
Without much more than a 'good luck' or a breather, you again find
yourself sprinting with all you have southward back to town. . .
'''
        )


    def ch_6(self): # Spring 24th, 3044, 6th age
        mon_list = self.config_monsters({'little nepenth':1, 'awakened shrub':1, 'barkling':1, 'green worm':1, 'shrubent':1})
        self.story_prep('1-1')
        self.six_intro()
        self.adjust_team('Kajlo Sohler',add=True)
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.six_encounter0())
        if player_lives:
            self.six_victory0()
            self.adjust_team('Kajlo Sohler',add=False)
            self.story_reward()
            self.story_prep(location='1-0', name='The cave')
            return True
        else:
            return False
    
    def six_intro(self): # No way a super dope breathing technique
        dprint(
            '''
You feel like your lungs are going to burst. Kajlo Sohler your newly assigned
team mate seems to have an unending well of stamina. After nearly 5 hours of 
non-stop running, you feel like you might just pass out. 
Just then, the both of you come around a bend in the path and see afar off, the
town of Greentown, sparkling in the early morning darkness. Kajlo stops so 
suddenly you collide with his back and collapse flat on your back grasping at 
any oxygene you can get. He takes notice of your desparation for air and says
"Ooh *pant* sorry, we can stop here for now, *pant* town is still *pant* ways 
off" He takes several deep breaths and continues ". . . You know, you are quite 
impressive fighter for one your age! Heres trick that may help you. Same magic 
that one expells through their sword skills or magic spells and like, can be 
used within own body as well! I have been using it to assist
me in our long dark mission here." 
He explains to you a way to access the magic wthin you through a nifty 
breathing technique and its necessarily accompanying state of mind. After a few 
tries you pull it off with incredible results. Your shredded lungs seem to fill 
with the sweetest air and you blood seems to flow into all the right places 
quickly recovering your energy. 
"Wow, you certainly are natural! It is almost unnatural, how gifted you are!"
*chuckle*
Shortly after, you continue onward. 20 minutes later Kajlo suggests a short-cut 
through a forest almost guaranteeing a fight, but you're both ready for 
anything. 
'''
        )

    def six_encounter0(self): # a momentary story intermission
        dprint(
            '''
Jumping and dashing through the woodland, you focus you mind on the magic 
within you, keeping you energized. You also with your ally, notice occasional
motion between the trees. 
At last the battle comes as the creatures of the woods attack the intruders! 
'''
        )

    def six_victory0(self): # Ifninite dialogue, p1: oh... shoot. pt2: A new mission.
        dprint(
            f'''
The fight is won and without further wait, you continue your marathon back to 
Greentown. Finaly after nearly 7 hours of running laden with your important 
letters. Here, you split off from Kajlo, you take the letter informing Henry's 
family of the dire situation while your companion takes the note requesting aid. 
It doesn't take you long to find the address on the note what with Greentown 
being the size it is. You take one more deep breath thinking about what to say
before giving a hardy knock on the door. Moments later a boy no older than 
Robin's age opens to you and looks you up and down for at least ten secconds 
before locking his eyes on the letter. Without, change in tone or so much as a
blink he says,
"So then, are we orphans now?"
Your short preparation did not ready you for this and you merely stand there 
reeling. Henry was so short with you while he was your team mate and you 
thought he was just unhappy being paired with someone under-aged. 
You quickly interrupt your thoughts to ensure the boy that his only parent is
in good hands but has been badly injured and will likely not return home for a
few days. After this, another boy around 4 by the looks of it toddles up to the 
threshold. 
"Come here Berr..." 
Without taking the now outstreched letter, the Boy takes his younger brother 
and walks into the house. 
"Come in, please."
Tentatively, you enter the dim cottege after the boy and his brother. Once 
inside he gestures for you to sit at a table before introducing himself as Han, 
the son of Henry and begins telling you that his mother died of sickness about 
6 and a half seasons ago on the eve of her 30th birthday. Henry soon after 
joined the guard to earn more money leaving Han, the eldest child, to care for 
the family while their father was away. The few times Henry was home he was 
much more quiet and distant than usual but caring supportive and strong as a 
father all tha same. At this point Han looks down as tears begin sliding down 
his face. 
Before this most recent mission Henry reported that this mission was going 
to be a dangerous one and asked Han to contact the guard's if anything happened. 
You promise that you will do what you can and let Captain Gurenge know about 
Henry and Han's pricarious family situation. Han thanks you coarsely and you 
leave heading straight for the barracks. . . '''
        )

        input()
        dprint(
            f'''
Upon arriving near the main office of the captain, you hear raised voices. 
"That's not the point, sir! This has nothing to do with man power..!" came the 
voice of your captain Outh Gurenge. 
"But it will never get done without it!" came another voice, tenor with a 
slight rasp. 
"You don't understand, thats why weve been requesting aid in the first place!
We need the numbers but weve been denied, so we need to get this done without 
it!"
"Captain..."
"SOOO, if you would be willing to make another request, that would be 
wonderful! Otherwise, it needs to be done with what little we have!"
"...very well, captain... I believe you have at least one particular young 
recruit who would be very willing to take on this mission standing at the ready 
just outside."
At that moment the other man's head appears around the corner and stares 
directly at you with startlingly solid, inky black, eyes which seem to look 
more in your general direction than at you.
Moments later Captain Gurenge peeks his head out the door too and says
"Ah, {self.player.name}, um, please wait outside for a moment."
"No need captain, I will be taking my leave now, but please take some time to 
consider the true import of this matter before you send this boy off. Good day!"
the man leaves the office places a cap atop his bald head and strolls out the 
door leaving both you and the Captian with mouths agape. 
"Um, if now is not a good time..."
*sigh* "no, no, please come in." 
With those words you are reminded of the last time someone less than happy 
asked you to come in and the request of Han reenters your mind at top speed. 
You ask about Henry's family but before you finish Captain Gurenge tells you 
that he cannot do anything until Henry is legally dead and even after that it 
would be him just sending the request up to Mayor Swendil. "What I can do is 
give him a big bonus if... when he does come back."
Thanking your captian in behalf of Henry and his family and detecting that there 
was nothing more to do on that front, you ask about the man who was just in here 
and the mission that needed to be done at which point any amount of positivity 
left in his demeanor dissolves and he lets out a long sigh before continuing. 
He explains that a separate recon group to the one you were in found the 
remains of what looked like an actual organized kobold military camp. No other 
available teams were back yet and no remaining guardsmen were available to go 
out and investigate further. In other words only you and Kajlo Sohler were 
available for an emergency reassignment. 
"I was planning on sending Kajlo, he being somewhat older and more experienced 
but if you are willing to go, yourself..."
You ask why he can't send you both to which he says he needs more available 
back up incase more things like this happen. 
"Pick your poison in other words."
The captain gives you 4 hours to think it over before finalizing your choice 
and sends you off. . .
'''
        )


    def ch_7(self): # the cave, Spring 24th-25th, 3044, 6th age
        mon_list0 = self.config_monsters({'nepenth':1})
        mon_list1 = self.config_monsters({'awakened shrub':10})
        mon_list2 = self.config_monsters({'cave bear':1})
        self.seven_intro()
        player_lives = self.battle.story(mon_list=mon_list0, dialog=self.seven_encounter0(), collective=False)
        if player_lives:
            self.seven_victory0()
            player_lives = self.battle.story(mon_list=mon_list1, dialog=self.seven_encounter1(), collective=True)
            if player_lives:
                self.seven_victory1()
                player_lives = self.battle.story(mon_list=mon_list2, dialog=self.seven_encounter2(), collective=False)
                if player_lives:
                    self.seven_victory2()
                    self.story_reward()
                    self.story_prep(location='1-2')
                    return True
                else: 
                    return False
            else:
                return False
        else:
            return False
        
    def seven_intro(self): # oooh new potions!
        loot = self.config_loot({'vermilion life potion':2})
        dprint(
            f'''
At home you tell your axious mother and your eager brother Robin of the mission
leaving out several key details so as not to set either one off. They both 
worry about the state of Henry and the strangness of the increased kobold 
activity. They both encourage you to be as careful as possible on this next 
mission and before long, the breakfast you all helped your mother prepare is eaten 
and you find yourself preparing to head out again to the barracks. Before you 
go your mother sends you off with a rather expensive 2 vermilion life potions, 
she insists you take them dispite you ensuring her that the captain will likely
send you off with some supplies anyway. 
'''
        )
        dprint(f'{self.player.name} gained the following items from Annabell!')
        for l in loot:
            print(f'{l.name}')
            self.player.inventory.add_item(l)
        print()

    def seven_encounter0(self): # a minor test of strength+
        dprint(
            f'''
Back at the barracks you inform Captain Outh of your decision to which he nods
and tells you that if you are to take this mission, he's going to need to test 
you again. Soon enough you find yourself once again waiting for the 
portcullis in the amphitheater to unleash whatever monster it holds within. 
"Brace yourself, this ones a lot bigger than last time!"
'''
        )

    def seven_victory0(self): # oh really more potions? ok!
        loot = self.config_loot({'life potion':2})
        dprint(
            f'''
After the battle, Outh, congratulates you considering you a worthy candidate
for this mission. You inform him that you happened to encounter one of those 
creatures before along side Kajlo. 
"Hmm, well I suppose it already wasn't much of a suprise anyway, well, just 
incase, I'll send you off with 1 extra life potion than you were getting 
already."
'''
        )
        dprint(f'{self.player.name} gained the following items from Captain Outh Gurenge!')
        for l in loot:
            print(f'{l.name}')
            self.player.inventory.add_item(l)
        print()
        dprint('. . .', .1)
        dprint(
            f'''
The captain then gives you a map and the general rundown of the mission 
objectives which were also written on a paper sealed to the back of the map as 
follows: 
Yesterday, Spring 23th, at dusk, a team of scouts followed a group of armed
Kobolds into a forest. The team sent a report of their findings by pigeon mail 
back to Greentown while they continued following the Kobolds. The original team 
has yet to come back and the return pigeon came back having failed to deliver 
his note indicating the scout team has likely been captured and taken off site.
The mission for {self.player.name} is now to find the scouts and if possible
look further into the followed kobolds. For this reason this mission is to be
executed in utmost stealth and caution. Follow the provided map for location
details and return and report if possible before spring 29th at midday.
Good Luck.
'''
        )

    def seven_encounter1(self): # traveling and a trees worth of monsters
        dprint(
            f'''
After the official send off, You head in the direction of the cave to the east 
of the town and carry on at a light jog for nearly the rest of the day thinking 
to yourself that you must have loged about 100 miles of running over the last 
24 hours. Well past dark, you arrive at the edge of a forest matching the 
description into which the scout team vanished nearly 30 hours ago now. 
You enter the blackness of the wood looking for movement or signs of recent
kobold or human activity. Soon you find a set of helpfully quite obvious tracks 
in the forest floor. You, have no experience in tracking but you estimate this 
trail was made by anywhere between 30 and 50 individual kobolds and humans. 
Suddenly, the entire tree imediately to your left excluding the trunk drops to 
the ground and begins scuttling towards you like a 10,000 legged leafy spider! 
 '''
        )

    def seven_victory1(self): # Ooh they glow! 
        dprint(
            f'''
After probably the most heebee geebee worthy fight of your life, minus that big 
rat you got rid of when you were eleven, you continue onwards. Following the
trail leads you to a long fissure in the ground. The darkness inside seems all
consuming as you peer into its depths. After a few breaths of encouragement, 
you follow the path half walking half sliding downwards into total darkness. 
After only about 10 seconds crawling blindly you open your supply sack for 
anything that might help you navigate without giving away your position too 
much. Immediately upon opening your bag you are greeted with faint light 
coming from somewhere inside. A quick search reveals that the vermilion life 
potions your mother gave you give off a faint glow! Not quite enough to fully 
light your way but enough to barely help you know where the walls and ceiling 
of this cave are. Silently offering your heart-felt thanks to your omnicient 
Mother, you carry on deeper and deeper into the void of blackness. . . 
'''
        )

    def seven_encounter2(self): # thats not a rock! 
        dprint(
            f'''
After nearly an hour, your eyes manage to adjust due to the faintest of faint 
organic luminance eminating strangely from parts of the cave walls allowing you
to stow your, much brighter by comparison, bottle of potion. The cold down here
is also quite penetrating and leaves your fingers stiff and your skin pocked 
with goosebumps. 
You can make out a rather larger opening up ahead with a prominent boulder in 
the center. After rounding the boulder, you come to a big problem. The cave 
splits into a right-flat tunnel and a left-downward tunnel. You decide that
the vantage point of large boulder in the center would help you think. You
make to climb on the boulder and imediately leap back as you feel not icy stone 
but the warm thick prickly hide of an enormous and breathing beast which begins 
to stir and wake from its disturbed slumber. . .
'''
        )

    def seven_victory2(self): # ah, time to leave. 
        dprint(
            f'''
You're not sure how much longer you can survive against this 15 foot beast of
pure thick skin and muscle but thankfully at this point, the hardly scratched 
bear begins to back away before finally slinking backwards down the right path 
having met a worthy foe. 
You muse that it wasn't exactly the way you pictured that "boulder" helping you 
decide which path to take, but take the left path anyway. The only path that 
does not now contain a giant cave bear. . . 
'''
        )


    def ch_8(self): # red herring of some kind, Spring 25th, 3044, 6th age
        mon_list1 = self.config_monsters({'cave slime':2,'swarm of bats':1})
        mon_list2 = self.config_monsters({'refuse':3})
        self.eight_intro()
        player_lives = self.battle.story(mon_list=mon_list1, dialog=self.eight_encounter0(), collective=True)
        if player_lives:
            self.eight_victory0()
            player_lives = self.battle.story(mon_list=mon_list2, dialog=self.eight_encounter1(), collective=True)
            if player_lives:
                self.eight_victory1()
                self.story_reward()
                self.story_prep(location='1-2', name='back to greentown')
                return True
            else:
                return False
        else:
            return False
        
    def eight_intro(self): # little cave camp, a family trait
        dprint(
            f'''
. . .
Mere minutes into this cave, the claustrophobia starts to get to you. The walls 
are much tighter and the ceiling, much lower. You're not the tallest person 
ever, a family trait, and yet you still have to duck sometimes to avoid head 
injury. You quickly find that you can't stop either the thought of being 
surrounded in rock for close to a mile in all directions gets worse. You press 
forward for another long while before FINALLY, just before you decide to give 
up, head back and report a mission failure, you see something different through 
the darkness ahead!
'''
        )

    def eight_encounter0(self): # definitely shouldn't have done that
        dprint(
            f'''
It looks like a fire-pit and what could be the rest of its acompanying 
abandoned camp. Just to be sure nothing is hiding, you throw a small rock into 
the camp to alert any stragglers.
Instantly several things happen. Your rock never hits the cave floor as a 
gelatinous psudopod-like apendage catches and obsorbs it. At the same moment a
deafening cacophony of fluttering and screeching hits your ears. 
'''
        )

    def eight_victory0(self): # burned at the stake
        dprint(
            f'''
. . . 
Fairly certain now that the rest of the camp is empty, you enter and take out 
your potion for more light. As the more clear sight of the camp hits your 
acclimated eyes, you are startled to see what is clearly the remains of a 
kobold who was burnt at the stake. Among the debris and ashes, lies a semi-
charred plank with a message written helpfully in common. 
"An example to those disloyal the the new Boss"
With that chilling statement. You continue to search the remainder of the camp 
finding little help clues or evidence other than more to lead you onward 
through more of the cave. Though it was good to discover that there were 
Kobolds, (and kobolds capable of murder) somewhere up ahead. . . 
'''
        )

    def eight_encounter1(self): # greatfully blinded eyes
        dprint(
            f'''
Soon, the cave begins climbing rapidly and it becomes more a free climbing 
excercise than an effort to simply walk ahead and avoid the ever increasing 
claustrophobia. 
Then, glorious, wonderful daylight meets your greatfully blinded eyes! For what 
is hopefully the last time, you stow your liquid light away and continue the 
climb. For a few minutes more and around several more bends the light steadilly 
grows brighter and brighter before you see your first tree under the sky since 
you entered this wreched cave. And true to its nature, the first thing the 
world greets you with is a fight. 
'''
        )

    def eight_victory1(self): # Lord Luxkhanna and the kobold plans
        dprint(
            f'''
. . .
Back in the light of what appears to be mid-morning sun, you strike out again 
following the much more traceble path left behind by the kobolds. You follow 
this trail breathing in every bit of the surface atmosphere, for nearly an hour 
before you come to a series of low hills between which you find yet another 
clearly abandoned kobold camp. This time it is very expansive with several rings 
of tents each around a pile of once burning coals (none of which fortunately
had burnt kobold bones amid them). You search first the largest tent at the 
north end of the camp. Inside you find an empty desk and a large round kobold 
cot. This camp appears to be more on the permanent side so it's strange to see
that much of the kobolds who once lived here did not leave more than a few cots
behind. The only thing written in common in the tent is a torn up peice of 
paper which looked like it belonged once to a letter. 
It takes you a while to find and piece together the letter and you can't find 
about half of it but after you do put together what you have, it reads: 
"....ver be victorious again. To se .. e th .. you are hereby commanded dir .. tly 
from the new Boss to gather  ..  one of the 7 gr .. hideouts in the area to meet 
and recieve further instr .. tions from the new Bos .. ere you and your clan will
be further infor .. d of Lord Luxkhanna's plan t .. aid the .. earest 3 human 
s .. ments. This will take place imediate .. following the gathe .. g...."
A lot of the letter is ripped off here but one final small peice says the words 
"...only human chi .. ren as captives..." and you git the gist. 
Kobolds in large number are planning to outright attack nearby human towns and 
villages. You're not certain if this includes Greentown but you're sure the 
missing part of the letter would say where, when and maybe even why. Whatever 
the case this new Boss Luxkhanna seems to be the one steering all these kobolds 
down this more outright violent path and by the sounds of it this plan may well 
be happening soon! 
A less than thorough search of the rest of the small hideout reveals another
note in common detailing instructions to carry a small group of human scouts
they apparently had as prisoners to somewhere in the north. You also find more 
and more signs that this camp was abandoned in haste. almost as if to flee some
approaching threat. 
Either way you feel like you have the information you need and more, so you 
turn now to your map for directions for an equally hasty flight back home. . . 
'''
        )


    def ch_9(self): # returning home, Spring 25th-26th, 3044, 6th age
        mon_list = self.config_monsters({'frenzy boar':7})
        self.nine_intro()
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.nine_encounter0(), collective=False)
        if player_lives:
            self.nine_victory0()
            self.story_reward()
            self.story_prep(location='1-3')
            return True
        else:
            return False

    def nine_intro(self): # Run back home
        dprint(
            f'''
You left the hasitlly abandoned camp hours ago to first find a vantage point
from which to orient yourself on the map and next to run all the way home 
to report what you've seen and discovered on your mission. 
The road home is long and you're sure that you'll encounter a bunch of kobolds 
on your way back but you know they have a bigger plan that you must tell the 
captain about maybe even the mayor, heck, this effects more than just Greentown
it might be wise to send a letter to the capital! Either way, you have to make 
it back no matter how many kobolds try to stop you. 
'''
        )

    def nine_encounter0(self): # litteraly just attacked for no reason
        dprint('. . . ', .25)
        dprint(
            f'''
Surprisingly, not to mention unnervingly, you never do meet any kobolds along 
your way back. Night falls, and the morning approaches without even seeing snout
or long lizardy tail of even one kobold! As the sun rises you feel the need to 
vent all your bottled up worries and fears upon something. Aaaand wouldn't you 
have it a perfectly good herd of frenzy boars stands ready to take it in stride!
'''
        ) 

    def nine_victory0(self): # Meet Milo and report some ominus news
        dprint(
            f'''
Leaving the battle field behind without a second glance, you make your way to 
town finally arriving just before noon on what you find out to be the 26th of 
Spring meaning you were only gone for 2 full days making that 3 days faster 
than expected. 
You run all the way to the barracks and find Outh out in the yard sparring with 
a boy about your age. As you approach, he notices you and all attention is
clearly diverted from the spar as the boy follows through with a strike he 
was expecting to be blocked and clobbers the captian's shin with a heavy 
looking wooden training sword.
"Oh {self.player.name[:4]}-" *WHACK* "GAH!"
The boy drops his training weapon and crouches at the side of the collapsed 
captain still yelling and gripping his shin while the boy apologizes copiously. 
After a some time and numerous ice bags. The Captian is back to normal sporting
a gigantic bruise where the training accident had occurred for which the boy 
(intruduced as Romilontius Nuor Filipius Nix Alabian Groves Titor Jr, or just 
Milo) continues to apologize. 
Captian Gurenge asks about your mission and the reason for you returning so soon
and you imediately begin telling him about the abandoned kobold camp; this new 
boss of theirs, Luxkhanna; and their plans to raid human settlments likely 
quite soon. 
"That is very interesting intelligence, because I happen to have just heard 
from yet another returning scouting group that the kobolds are in fact planning 
something big but that it would come in nearly a full season from now. Did you 
happen to bring this note back with you?"
You didn't think to take the letter with you and now you find yourself mentally 
kicking yourself that you didn't. You try explaining this to the Captian who 
assures you that he believes you but that he will need to speak with the scouts 
who brought back the conflicting intel and invites you to a meeting the next 
morning. 
"One more thing Rulid before you go! Did you encounter any Kobolds on your way
back, no actually, on your whole mission?"
Thinking back you are stunned to realize that, no, you have not actually seen a
living kobold since the night Henry was hurt. You report this and the Captain 
responds by saying "Hm, that's very interesting, and a little worrying. No one
has seen a kobold for a few days now. I fear your intel may be the true one and
their big move could be sooner than we would like... Well, good day, see me at 
about mid morning tomorow. I have a bit more training to give this lad here."
finishes the captain with a little extra emfasis on the word "training" Milo 
srinks at this comment and automatically apologizes again. To which Captian 
Gruenge chuckles and dismisses the apology and you make your way out of the 
barracks and onto the road back home to see your family. . . 
'''
        )


    def ch_10(self): # wake in flames, robin abducted, single fight giving chase, Spring 27th, 3044, 6th age
        mon_list = self.config_monsters({'kobold soldier':4})
        self.adjust_team('Liliyah', add=True)
        self.adjust_team('Bulli', add=True)
        self.adjust_team('milo_0', add=True)
        self.adjust_team('Gaffer', add=True)
        self.adjust_team('Holt', add=True)
        self.ten_intro()
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.ten_encounter0(), collective=True)
        if player_lives:
            self.ten_victory0()
            self.story_reward()
            self.adjust_team('Liliyah', add=False)
            self.adjust_team('Bulli', add=False)
            self.adjust_team('milo_0', add=False)
            self.adjust_team('Gaffer', add=False)
            self.adjust_team('Holt', add=False)
            self.story_prep(location='1-3', name='Give chase')
            return True
        else:
            return False

    def ten_intro(self): # The kobold attack, relapse, vision
        dprint(' . . . . . . ', .2)
        dprint(' . . . . . . ', .1)
        dprint(' . . . . . . ', .05)
        dprint(
            f'''
. . . *crash* . . . 
. . . {self.player.name[-4:]} . . 
. . *SCREAM* . . . {self.player.name.upper()}!!!
          *SHATTER* 
You wake suddenly to the sounds of screaming and breaking glass, the wavering 
orange glow of fires luminate your bedroom through your window, through which a 
thick wooden support beam crashes in from the outside. The terrible sound that 
meets the fresh opening of your window is like nothing you ever want to hear 
again, a sound that rocks you to your center. 
Your mother, Annabell, screaming and pleading with something just out front.
Again she screams your name and you leap into action, straight out your freshly
made entrance. The sight that meets your eyes is a complete nightmare. In the 
darkness of the night, you can easily pick out multiple buildings in flames and 
by that light you can make out more than one motionless human body and many 
armed cackling kobolds throwing more objects through windows, hurling torches 
and fireballs into shops and homes, fighting people and dragging a few people 
out of sight. The pair of Kobolds who smashed in your window appear to have 
just ended a fit of cackling having not expected something to exit the window 
they just destroyed. 
''', .05)
        if self.player.title == 'Fighter':
            dprint(
                f'''
Without more than a second hesitation while you take all this in, you execute 
the skill, {self.player.known_skills[-1].name} with power somehow far above 
your normal standard. 
''', .05)
        elif self.player.title == 'Mage':
            dprint(
                f'''
Without more than a second hessitation while you take all this in, you cast
{self.player.known_spells[-1].name} with power somehow far above your normal 
standard. 
''', .5)
        elif self.player.title == 'Pugilist':
            dprint(
                f'''
Without more than a second hessitation while you take all this in, you use
{self.player.known_spalls[-1].name} with power somehow far above your normal 
standard.
''', .05)

        dprint(
            f'''
You don't stop though, you can still hear you mother just around the front hedge.
On the other side, you see her on her knees crying into the dirt. You fight off
another kobold and she notices you. Her eyes grow wide. 
"{self.player.name}, they took Robin and Rosie!"
at the sound of that sentence, all seemed to fade away, sounds became muffled, 
your vision blurred, the grazes on your skin seemed to fade into the background. . . 
'''
        )
        dprint('''. . .''', .15)
        dprint(
            f'''
For the briefest moment right as your vision fades to black, a perfectly clear 
vew of some kind of strange dim room full of old books, papers, strange 
instruments and tools of all kinds, fills your vision. But as if a blindfold 
was suddenly appled, all goes dark again. 
'''
        )
        dprint(' . . . ', .15)
        dprint(
            f'''
"Master, are you well . . ?"
". . ."
"My Lord?"
'''
        , .085)
        dprint('. . . khhiiill . . .', .105)
        dprint(
            f'''
Instantly, you find yourself back in reality, and on the ground. Jumping to 
your feet, you're startled mother backs away briefly. You share a meaningful
glance after which she mouths, "{self.player.name}, please come back." to 
which you nod and promise to return with Robin and Rosie, more to yourself,
than anything before begining the chase.
'''
        )

    def ten_encounter0(self): # begin the pursuit
        dprint('. . . ', .075)
        dprint(
            f'''
Sprinting in the direction of the chaos, you review what has transpired thus 
far, you woke up, jumped through your smashed window to help your mother, and saw
a small figure of what you now realize was likely one of your younger siblings 
being dragged away! 
At that thought, you put as much strength into your stride as you can and dart 
through the raid. Ignoring all other things that might sue for your attention. 
"{self.player.name}! What are you?! Hey, wait!"
No one mattered but your siblings and the kobolds that took them. You round a 
corner and run straight into an intense battle. 
'''
        )

    def ten_victory0(self): # a new team
        dprint(
            f'''
Just as you finish up, you catch a glimse of a pair of Kobolds carying what 
looks like Robin or some other smaller human away. 
"Alright, now {self.player.name} where you going in such a hurry? Hey! Hey no, 
slow down! WHEre yoU gOinG . . ?"
Your already bolting full steam ahead after Robin. Moments later, you hear a 
distant voice call again, but not to you this time. 
"Oi! Cap! I think {self.player.name}s on to something again!"
"You two, follow {self.player.grammer['objective']} and help {self.player.grammer['objective']} out! You three stay here!" came the voice of 
Captian Gurenge. 
Another minute later, just moments after you pursue the kobolds outside the 
crumbling Town gates, two figures appear dashing astride you, Milo the boy you 
met with the Captian and a woman you've seen but never really met before. A 
member of the guard. As the three of you continue to run none speaks a word you
all just keep running . . . 
'''
        )


    def ch_11(self): # the hunt begins, Spring 27th, 3044, 6th age
        mon_list0 = self.config_monsters({'small kobold':1, 'kobold slave':1, 'kobold soldier':2, 'kobold guard':1})
        mon_list1 = self.config_monsters({'small kobold':4, 'kobold slave':2, 'kobold soldier':1})
        mon_list2 = self.config_monsters({'kobold soldier':2, 'kobold slave':1, 'kobold soldier':1, 'small kobold':1, 'kobold soldier':1})
        mon_list3 = self.config_monsters({'kobold soldier':4, 'small kobold':2})
        self.adjust_team('milo_0', add=True)
        self.adjust_team('Suphia', add=True)
        self.eleven_intro()
        player_lives = self.battle.story(mon_list=mon_list0, dialog=self.eleven_encounter0(), collective=False)
        if player_lives:
            self.eleven_victory0()
            self.adjust_team('Electo', add=True)
            player_lives = self.battle.story(mon_list=mon_list1, dialog=self.eleven_encounter1(), collective=True)
            if player_lives:
                self.eleven_victory1()
                player_lives = self.battle.story(mon_list=mon_list2, dialog=self.eleven_encounter2(), collective=False)
                if player_lives:
                    self.eleven_victory2()
                    self.adjust_team('milo_0', add=False)
                    player_lives = self.battle.story(mon_list=mon_list3, dialog=self.eleven_encounter3(), collective=True)
                    if player_lives:
                        self.eleven_victory3()
                        self.adjust_team('Suphia', add=False)
                        self.adjust_team('milo_0', add=False)
                        self.adjust_team('Electo', add=False)
                        self.story_reward()
                        self.story_prep(location='1-0', name='Rescue your siblings')
                        return True
                    else:
                        return False
                else: 
                    return False
            else:
                return False
        else:
            return False
        
    def eleven_intro(self): # not gaining much ground
        dprint(
            f'''
Very, soon into pursuit, the 3 of you begin finding it very dificult to make
any real ground on these nimble, hot-footed kobold kidnappers. It becomes even 
more so as you have to avoid fights resulting in a serpentine path through 
kobold forces. 
'''
        )

    def eleven_encounter0(self): # "some fights ... are unavoidable"
        dprint(
            f'''
Some fights, however, are unavoidable. 
'''
        )

    def eleven_victory0(self): # Electo-Suphia not to be confused with Electrosphere
        dprint(
            f'''
Bursting through your final foe and narrowly evading others bent on lengthening 
the confrontation, you look ahead and see your quary much farther ahead than 
before having gained a lot of ground during the fight. On the upside, a new 
fighter appears at Suphia's side. A man with the same straight black hair as 
Suphia. 
"Brother! Captain sent you?"
The man nods.
"{self.player.name}, this is my brother Electo, he's not in the guard but he 
was in town for the weekend from Pompon!"
The man nodds again.
'''
        )

    def eleven_encounter1(self): # oh boy another fight ... PSYCHE! lol! Nope!
        dprint(
            f'''
Electo quickly turns out to be a big help both in power and tactics, though he 
doesn't speak very much, he is fast enough to lead the group and he does so to
great effect, leading you through groups of kobolds which you wouldn't have 
dared to before. All this leads to you gaining on the kobold with Robin and 
Rosie. 
This again doesn't last forever as several kobolds surround you trapping you 
and leaving no alternative to a fight. 
'''
        )
        dprint('Enemies move in to attack!')
        print('Round 1, FIGHT!')
        input('1: attack\n2: special\n3: item\n4: run\n5: auto/controlled\n')
        dprint(
            f'''
Before anything can happen, Electo blasts a hole in the surrounding kobolds with 
a thunder wave spell and keeps running with you and the rest following closely 
behind. 
You keep running narrowly avoiding a few more fights and gaining ground before 
finally you find yourself cornered by sheer numbers. 
'''
        )

    def eleven_victory1(self): # lol actually empty
        dprint(
            f'''
'''
        )

    def eleven_encounter2(self): # "You win but more just keep coming"
        dprint(
            f'''
You clear the first group but more just keep coming in to fight! 
'''
        )

    def eleven_victory2(self): # Milo's sacrifice. 
        dprint(
            f'''
"{self.player.name} just go, I can keep them off your tail!"
Milo turns his back on you keeping the continuous stream of kobolds at bay. 
You thank him and he briefly looks back grinning and sending you a thumbs up 
before returning to the fight. 
'''
        )

    def eleven_encounter3(self): # Oh gosh theres more!?
        dprint(
            f'''
Quite distantly and only through by the flickering light of torches, you spot 
your quary still fleeing at top speed and gaining still more distance by the 
second. 
But as if to laugh in your increasingly frustrated face, the forces of the 
enemy corner you yet again soon after. 
'''
        )

    def eleven_victory3(self): # Electo's turn to hold them off
        dprint(
            f'''
This time, Electo stays behind, blasting the remaining and approaching kobolds
into each other opening up a window you are silently ordered to take. Suphia
hesitates for a moment but Electo gives both of you a look that seems to
magically compel both of you to turn and run. 
As you do so you see why it was made so urgent. Right on the outside of this 
fight the sporadic crowds of kobolds seems to break leaving you open and able 
to continue mostly unresisted towards the retreating kobolds. 
... But where were the retreating kobolds?
As you and Suphia hurry through the night, you strain your senses to detect the
signature movement of kobold capters, but try as you might, neither of you 
have any idea without the light you had before of where your quary might be. 
The kobold forces you have now left behind, seem to care very little about a 
few escaped victims and pay you little heed. This grants you the ability to 
slow down and put more energy into scanning the landscape. But no, neither of 
your eyes can spot them, they must have gotten mere feet too far. 
Your frustration is apparently written on your face as Suphia tells you that 
even if they were sure to be lost at this point, she would not abandon the 
mission because of her brother's sacrifice to help them make it this far. 
Agreeing with your newest teammate, you both reason about the most likely 
direction they were heading in and resume full speed. 
Let the hunt begin. . . 
'''
        )


    def ch_12(self): # alone int he woods pt 1, Spring 27th, 3044, 6th age
        mon_list1 = self.config_monsters({'sappent':1,'shrubent':2,'awakened shrub':3})
        mon_list2 = self.config_monsters({'blue worm':1})
        self.twelve_intro()
        self.adjust_team('Suphia', add=True)
        player_lives = self.battle.story(mon_list=mon_list1, dialog=self.twelve_encounter0(), collective=True)
        if player_lives:
            self.twelve_victory0()
            player_lives = self.battle.story(mon_list=mon_list2, dialog=self.twelve_encounter1(), collective=False)
            if player_lives:
                self.twelve_victory1()
                self.story_reward()
                self.story_prep(location='1-4', name='Head to the smoke')
                return True
            else:
                return False
        else:
            return False

    def twelve_intro(self): # Ok, lets review. . . 
        dprint(
            f'''
A mild glow from the soon to be rising sun casts a red to blue gradiant above 
you to your left. The freezing early wind ruffles your clothing, made more so 
as your run. Your companion Suphia, continues head of you about 50 feet with 
long quick strides. The smell of smoke and terror still lingers in both of your 
minds among far to many things to verbalize. 
In your mind you go over the things you heard and discovered about the kobolds
and their plans, that could have prevented this terrible catastrophy. 
You heard from the Captain that kobolds had been increasing in activity for 
weeks before you and Robin even encountered them. Even as far back as the late 
Winter.
You and Robin were ambushed by a group of kobolds which initiated increased 
action against the kobolds by the Greentown guard resulting in your recruitment.
Each team discovered some ominous news about the kobolds and their recent 
increase in activity the most concerning of which was the report of an entire 
missing team. 
Upon further investigation, you discovered possibly erroneus inteligence that 
the enemy was planning an attack of some sort on nearby human settlments, 
possibly including greentown, Pompon, Farthe Outpost and Tolbantha or maybe 
villages in the farther east like Kyoma or Uten. This combined with the lack of 
concrete evidence and the discovery of contradicting intel at about the same time 
resulted in indecision and crucial preparation time spent strategising and
reasoning about next steps. 
Whether it was a well orcestrated attack strategy, which Suphia pointed out 
was incongruent with usual kobold nature; or, the work of some human 
traitor or mole, it had worked and the kobolds had, counter to their normal 
behavior, orchestrated a combined attack on Greentown and more than likely, 
several other towns in the area.
There was one other important piece of inteligence that you and at least one 
other source discovered. The kobold called Luxkhanna. That kobold was 
supposedly the leader who orchestrated all this. 
If, and you hated even giving this idea any ground in your mind, but if you 
were never able to find and rescue Rosie and Robin, you did at least have an 
alternative goal: Find that monster and destroy him. . . 
'''
        )

    def twelve_encounter0(self): # lets hope its just shrubs
        dprint(
            f'''
Your thoughts as you run turn to grattitude for Kajlo Sohler who taught you to 
use magic to inprove your stamina. You can't help but be impressed at Suphia, 
however, as she looks to hardly have broken a sweat dispite still striding 
ahead of pace in this now nearly 4 hour run. 
You both enter a grove of trees and take a quick breather. Almost imedieatly 
upon stopping, however, you hear the sound of nearby creatures rustling their 
way invisibly through the trees. 
"shrubs...maybe?" guessed Suphia, drawing her blade.
Readying yourself as well, you follow closely behind her as you both begin to 
breathlessly stalk through the woods towards the sound.
'''
        )

    def twelve_victory0(self): # grassy noll mentioned
        dprint(
            f'''
After the fight you continue forward slightly slower due to the increasing 
thickness of the woods. By about midday, a few hours later you find yourselves
resting again atop a grassy noll for a view above the thick treeline. From that
vantage point, and between the 2 of you, you find not 1, nor even 2 but 3 
interesting things a ways off. The first, to the north close to the way you 
came, is a glassy lake with an unusually large tree stump at its center. The 
second is a feint column of smoke to the north-west and last you spot an old 
stone tower in the southward distance. After some discussion you decide that your
time would be best spent moving in the same direction but that any signs of 
structure or inteligent life should be top priority. For this reason you decide 
that backtracking toward the smoke would be the best course of action before 
moving on to the tower further south. 
'''
        )

    def twelve_encounter1(self): # worm
        dprint(
            f'''
On your way again you both navigate your way through the trees and decide that 
now that you're close enough you might as well check out the lake and fallen tree
as well. Shortly upon arriving at the shoreline you spot the island in the 
middle but at the same time something else spots you. 
'''
        )

    def twelve_victory1(self): #
        dprint(
            f'''
Having seen the kinds of things that swim in these waters, and seeing nothing
more than a gigantic hollow stump as your destination. You both change your
minds again and make your way south west towards the smoke primed and ready for
anything.
'''
        )


    def ch_13(self): # alone int he woods pt 2, Spring 27th, 3044, 6th age
        mon_list = self.config_monsters({'little nepenth':3})
        self.thirteen_intro()
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.thirteen_encounter0(), collective=False)
        if player_lives:
            self.thirteen_victory0()
            self.story_reward()
            self.story_prep(location='1-4', name='Continue to the tower')
            return True
        else:
            return False

    def thirteen_intro(self): # outward camp observations
        dprint(
            f'''
Upon arriving near the site of the smoke, you both see several things. The 
smoke originated from a small camp of some sort, a little more orderly than a 
kobold camp is usually, but Suphia observes that first of all kobolds in 
general have been acting differently anyway, and secondly who else would be 
just casually camping in these woods at times like these, barring themselves in 
a few hours. 
'''
        )

    def thirteen_encounter0(self): # oop, theres a nepenth there
        dprint(
            f'''
The next imediate thing you both notice is a singular nepenth standing with its 
gaping bulbous mouth wide and lashing vines relaxed as if simply enjoying a 
moment in the sun. Upon a closer look though you see what is clearly a semi-
skeletal foot of some poor creature about human sized sticking out the edge of 
the nepenth's mouth. It was simply digesting a recent meal, likely the reason 
this camp was so hastilly abandoned. After a quick plan of attack and a warning 
from Suphia that these things usually move in groups, you move in for the attack. 
'''
        )

    def thirteen_victory0(self): # aha evidence, capper Luxkhanna
        dprint(
            f'''
The camp itself, now that you're inside, appears quite a bit more kobold-like and 
is more expansive than you both perceived it to be from the outside. You find 
remains of tents and old scraps of food. Another abandoned and half dissolved 
kobold foot rests near the smothered fire. Upon a short wooden table lays half 
of a map detailing current locations and movements of kobold batalions. You 
call Suphia over and you both begin to scour the map remains for evidence of 
prisoner troops or leaders. Seconds later you eyes fall upon the fine printed 
words: "Hail Capper Luxkhanna" above a camp symbol far the the south. 
After a few more minutes searching you scrape off the map and make your way 
south towards your hopeful camp for the night that is the stone tower and after
that, the camp of Capper Luxkhanna.
'''
        )


    def ch_14(self): # alone int he woods pt 3, Spring 28th, 3044, 6th age
        mon_list1 = self.config_monsters({'skeleton':1})
        mon_list2 = self.config_monsters({'refuse':3})
        self.fourteen_intro()
        player_lives = self.battle.story(mon_list=mon_list1, dialog=self.fourteen_encounter0(), collective=False)
        if player_lives:
            self.fourteen_victory0()
            player_lives = self.battle.story(mon_list=mon_list2, dialog=self.fourteen_encounter1(), collective=True)
            if player_lives:
                self.fourteen_victory1()
                self.story_reward()
                self.story_prep(location='1-5', name='Head towards Luxkhanna\'s camp')
                return True
            else:
                return False
        else:
            return False

    def fourteen_intro(self): # into the dungeon
        dprint(
            f'''
You both find your way to the tower and, having found it mostly safe, set camp
for the night just below the top level. That morning you decide to check out 
the rest of the tower which you found extended at least a few levels below 
ground too. Soon you are both below ground in a rather elaborate and dark 
dungeon. Each turn leads you further into the unknown, and sometimes still
deeper with each level lower the air seems to chill and grow thicker. 
'''
        )

    def fourteen_encounter0(self): # First real dungeon loot! whoop whoop!
        loot = self.config_loot({'grand col':1, 'glass bottle':1, 'agiros sheet':1})
        dprint(
            f'''
Four levels down and about 20 minutes in you enter a chamber with five altars 
connecting a pentagon in the center of the room. In the far corner is a very 
human skeleton in a leather cap and clutching a long cutlas in one hand and a 
round bottle in the other. Each of the altars but one carries a box in the 
shape of a five sided pyramid. Upon careful inspection, 3 of the 4 remaining 
boxes have been emptied already but one at the far side of the room holds one 
giganic silver coin, an empty glass bottle of similar shape as the one the 
skeleton holds in his hand, and a sheet of some thick but surprisingly light 
fabric. Suphia lets you keep the loot. . .
'''
        )
        dprint(f'{self.player.name} gained the following items from the dungeon box!')
        for l in loot:
            print(f'{l.name}')
            self.player.inventory.add_item(l)
        print()
        dprint('. . .', .1)
        dprint(
            '''
Imediately upon extracting the items from the chest, the interior of the 
pentagon glows a dim pale purple and the skeleton in the corner moves. After a 
few stiff moments it's joints begin to glow and it stands confidently upon its 
feet brandishing its cutlas. 
'''
        )

    def fourteen_victory0(self): # omg dungeons AND dragons? 
        loot = self.config_loot({'col coin':4, 'magic glass':1})
        dprint(
            f'''
The skeleton's bones scatter with the final blow and all traces of magic fades
from its joints. A dark shadow, moving like slow black flames rises from the 
skull. The chamber is suddenly filled with a piercing disonant scream which 
lingers for several seconds before the tormented ghost steadily dissipates, 
leaving the room steeped in an unnerving silence. Neither of you dare disturb
the stillness and so simply sneak back to the chamber's entrance having seen
all you needed.
You carry on much more cautious than before but find little more of interest, a 
few thankfully inanimate kobold skeletons, a few more empty boxes, some mild 
booby-traps and a fair few rats. Finaly you reach a room at the end of what you 
imagine (and somewhat hope) to be the final chamber at the lowest dungeon at 
9 levels below the surface.
The chamber houses but one thing of interest, that being a large pile of bones
that look, upon closer inspection, to be that of a small dragon. roughly the size
of a large draft horse, the main body lies broken and chipped evidence of a battle. 
The nearly 30 foot wings lay both separated from the main body at different 
points in the room. The long neck and tail bear spiked horns as well as deep 
grooves in the dragon's bones. 
"I didn't think there was a dragon in this region let alone one so close to 
home! I'm just glad we found it after it was killed rather than before!"
remarks Suphia.
You both tiptoe your way through a quick inspection of the dragon bones before
noticing a single open and mostly emptied chest under the dragon's upper 
ribcage. Inside lies a few small coins and 2 dusty bottles of a reddish gold 
liquid which Suphia identifies as magic glasses, bottles of drinkable pure 
magic energy. She hands you one and keeps the other. She also lets you keep the
col. 
'''
        )
        dprint(f'{self.player.name} gained the following items from the dragon\'s chest!')
        for l in loot:
            print(f'{l.name}')
            self.player.inventory.add_item(l)
        print()
        dprint('. . .', .1)

    def fourteen_encounter1(self): # a few odd discoveries
        dprint(
            f'''
You both leave the chamber and begin to make your way back up to the surface. 
A few levels up Suphia points out something interesting. At about level six 
below the surface she points at a rickety door made of poor quality wood and 
gives two observations. First that this is the only wooden door in the entire 
dungeon and second that its made of wood that would not have lasted as long as
anything else in this dungeon. You decide to make a quick double check of this
room and find, just like last time, an empty room containing nothing 
interesting but a few scraps of old paper.
"...paper? That wouldn't last long either." Suphia remarks picking up one of 
the old dry sheets. "I can't read any of these though, they look to be written 
in kobold tongue. Find one in common!"
A quick search of the few papers in the room yealded nothing but kobold and one 
in gobldeeguk of all things, the language of goblins. There was however a rough 
drawing of another map upon which showed several old camp locations in the area
but at least 2 of which were confirmed to be destroyed since whenever this was 
drawn up. Alltogether not the most helpful find but it was good to know that 
they were walking comfortably in historically kobold territory. 
Heading further up again, you pass the chamber where you fought the skeleton 
and still further before anything else happens. At just level two below the 
surface, three hitherto inanimate piles of refuse spring into action.
'''
        )

    def fourteen_victory1(self): # Susume!
        dprint(
            f'''
After the fight you make your way to the surface and from there to the top of 
the stone tower. From that vantage point you can see far into the distance. Now
with greater confirmation that you are on the right path, you set your sights 
south towards the distant rolling hills and eventual low mountains that roll 
into being on the faint horrizon. This being the general location of Luxkhanna's 
base camp as detailed on the other map you found. Suphia gives one last warning 
before you set off that those woods farther south are notoiously dangerous for
more reasons than just kobolds but you have no alternative and either way, 
there is nothing that could turn you back from this mission until you reunite
with your brother and sister.
'''
        )


    def ch_15(self): # following the trail, Spring 28th-30th, 3044, 6th age
        mon_list0 = self.config_monsters({'small kobold':3})
        mon_list1 = self.config_monsters({'ruin kobold':1})
        mon_list2 = self.config_monsters({'treent':1, 'ruin kobold':1, 'kobold soldier':3, 'small kobold':1})
        self.fifteen_intro()
        player_lives = self.battle.story(mon_list=mon_list0, dialog=self.fifteen_encounter0(), collective=True)
        if player_lives:
            self.fifteen_victory0()
            player_lives = self.battle.story(mon_list=mon_list1, dialog=self.fifteen_encounter1(), collective=False)
            if player_lives:
                self.fifteen_victory1()
                player_lives = self.battle.story(mon_list=mon_list2, dialog=self.fifteen_encounter2(), collective=False)
                if player_lives:
                    self.fifteen_victory2()
                    self.story_reward()
                    self.story_prep(location='1-4')
                    return True
                else: 
                    return False
            else:
                return False
        else:
            return False

    def fifteen_intro(self): # Geography!
        dprint(
            f'''
The rest of that day and another pass swiftly with a few mild battles and a
slower pace to conserve energy and keep a lower profile as you hunt in enemy
territory. As far as you can tell by the remains of the kobold map, you are
rapidly aproaching your destination which appears to lie just beyond the
mountains.
The Amn mountain range is not the tallest, widest nor the most treacherous to
cross physically but few people have dared to settle near it because of rampant
monsters and the rumors of things like wild goblins and, of course, kobolds
making these more rocky regions their homes. 
'''
        )

    def fifteen_encounter0(self): # woken again by kobolds
        dprint(
            f'''
One night you are woken by Suphia during her watch. She tells you she heard
something or a few somethings nearby and you quickly hear what she means. 
Easilly less than 100 paces away you hear the rythmic crunching of undergrowth
and fallen twiggs. 
Silently the two of you rise and peer through the trees to see in the darkness,
a passing troop of kobolds. Its hard to tell in the dark but there appears to
be 5 or less among them. With a quick look and nod you both decide to confront
them for information. 
Suphia tosses a well aimed stone between the kobolds and a point about 15 feet
to your right. Just as you had hoped the kobolds stop and a brief silence is
broken by a quiet murmer in kobold. Then what you didn't quite want happens. 
After some brief deliberation, the entire troop begins walking towards the 
sound.
Withoout a moment's hessitation, you both duck backwards and left to avoid the 
path and eyesight of the kobolds. Sheer luck and another well cast stone leads
you eventually right behind the perplexed troop of five all murmuring softly 
just loud enough to mask your approaching footsteps. 
Then, you lunge. 
Your combined and coordinated attacks together with the element of surprise
easilly drop the two you both aimed for but now the battle was in full
array!
'''
        )

    def fifteen_victory0(self): # pilot test of the basic response function
        prompts = ('What does that mean for us?','Should we hide?',
                   'does that mean more are coming?')
        dprint(
            f'''
Unfortunately interrogation would have to wait as the 2 who still managed to
cling to life after your assault seem to have passed out. You bind them and
return to camp to tend to wounds. Shortly after doing so, Suphia stands
suddenly. In a low tone she says "They were Mahouts."
After a glance at your puzzled look she explained in a hushed but alarmed, 
almost scared tone, "They're pathfinders or scouts that lead a carravan or...
or military brigade..." she finished. 
'''
        )
        response = basic_player_prompt(*prompts)
        if response == 1:
            dprint(
                '''
"Sh-" she hissed gesturing you into a crouching position, "They're already here."
'''
            )
        elif response == 2:
            dprint(
                '''
She nods guesturing for you to crouch as she silently does the same. Once 
sufficiently low, she points through the trees before bringing her finger to
her lips again. 
'''
            )
        elif response == 3:
            dprint(
                '''
"They already are..." she hissed pointing through the trees. 
'''
            )
        dprint(
            '''
Sure enough as you look, you can see something moving through the darkness with
the signature glowing eyes of many kobolds.
'''
        )

    def fifteen_encounter1(self): # Ruin Kobold, kobold tongue
        dprint(
            '''
Their path seems to pass by you but it will lead them directly through the
remains of the battle you just won. Freshly killed kobold bodies were sure to
tip them off if, or rather, when they found them. 
You needed to move, now.
Both of you seemed to come to this conclusion simultaneously as without even
a shared look, you both slink backwards as silently as possible.
Moments later, a much louder and heavier set of footsteps come to your attention
much closer and heading directly towards you. This time, you did share a glance.
The look conveyed nothing but urgency and caution as you both turn and pick up
the pace.
*Snap*
At the worse possible moment, a fallen tree branch you hadn't noticed breaks
under your foot. 
"Iikaah-" came a voice unlike the usual whine of kobolds, deeper and heavier.
You both take a few more quick strides from the scene desperate to avoid
the inevetable conflict. The only thing you can hope for now, as the large 
being stumbles into your obviously just abandoned camp, would be to attempt to
fight only this thing and avoid the rest of them. 
What was this thing anyway? You both think as you now have a clearer view of
it.
It looked like a regular kobold but nearly three feet taller and longer with a
thicker snout, sharper teeth and a much more muscular build. It was armed with
a short crude mace clearly meant for something much smaller than itself.
"Tuo comm, tuo comm, yeb ii combit r bringbom gob, ya sonch uou. . . or are you
puny humans? Havin' a li'le fun out in the dark of night R we? Come out. I
hear that, I could shoot you in the dark if I...wan'ed teh."
His low talking was giving you both just enough cover to continue slinking
backwards, but it wouldn't last forever. Just as he said, he was clearly
sniffing his way right to you.
At about 12 feet away, Suphia looked at you and using some cleaver hand
gestures pantamimed a plan of attack. You were to hide in bushes on either side
of the beastly kobold and pounce when the moment was right. That way at least
one of you would get a surprise attack on it whoever was found first.
Five feet appart now you both wait for the kobold to near close enough or to
find one of you. It was only 8 feet away, 7, 6, 5, right then there came a cry
from the main group, they had clearly found the bodies. 
The kobold turns back, and you both leap into action!
'''
        )

    def fifteen_victory1(self): # RRRUUUUN!
        dprint(
            f'''
"Run!","Go!" you both say as soon as the battle ends and the fleeting
opportunity presents itself. You now have an entire kobold brigade fully aware
of the two of you. The chances of you surviving that were slim and you both
knew it so running and hiding at the soonest chance was the plan. 
You dart through the trees as crude arrows and javelins wizz past you on both
sides and the howls and jeers of your gleeful pursuers sound behind you. You
run monstly west for several minutes and gain little ground.
Finally, you spot a shallow and narrow ravine up ahead and with just enough
distance on your pursuers, you leap in unnoticed and crawl further out of
the kobold's path. Seconds later the ground rumbles around you as only 20 paces
past your feet, nearly 50 armed kobolds and several of those gigantic ones
surge over the ravine. 
Unfortunately though, one near the very back of the troop spots you and howls
alearting several of his nearest comrades who in turn begin alearting the rest
of the entire troop. 
You scramble to your feet as another arrow zips so close to your head, you feel
a few sliced hairs fall into your eyes. 
'''
        )

    def fifteen_encounter2(self): # Treent saves the day
        dprint(
            '''
You've managed to thin their numbers by your little hiding spot. Now less than
half are still following you, but thats still half including at least
six of the huge Kobolds. 
"DUCK!" screams Suphia suddenly.
You do so just in time as a foot thick limb, bellonging to the oak tree next
to you, swings inches from your lowered head. The force of the tree limb's
movement passing so close still knocks you off your feet. 
From the ground you see the oak tree next to you, nearly 100 feet tall and well
over 3 feet thick at the trunk, pull itself from the forest floor with a sound
deep and echoing, like thunder rolling across the sky. It stands upon powerful
thick and curlled roots which tear themselves free of the old forest floor with
a series of sharp, cracking sounds, like the splintering of a ship's hull. The
scent of damp earth and old wood fills the air. New spring leaves flutter down
like dark confetti as it shakes with anger. An aura of rage emenating from its
thick bark washes over the entire scene filling you and all present with a deep
primal fear. The entire tree looms above you its branches, each smaller trees of
their own moving and swaying with purpose accompanied by a haunting melody of
creaking groaning wood.
'''
        )

    def fifteen_victory2(self): # escape and flight
        dprint(
            f'''
Suphia's eyes meet yours, and without a word, you both know what you have to do.
This is your chance to escape. The treent, though terrifying, is a distraction
you can use to your advantage. You block an attack from a kobold that strays
too close and Suphia does the same, her movements quick and precise as she cuts
down another kobold and hacks another chip of bark off the much larger foe, 
still thrashing its gigantic limbs. Another limb swings past you and collides
with a kobold parting it from its left leg and sending the rest of it flying
through the trees. 
Seeing your opportunity, you both leap backwards and break into a run, weaving
through the trees and underbrush, the sounds of battle fading behind you. The 
forest around you is dark, but you trust your instincts, moving swiftly and
silently. You glance back only once, just in time to see the treant lift a
massive branch, sweeping it through a group of kobolds with terrifying force,
toppling two smaller trees in the process.
You keep running for a few minutes until the sounds of the fight die away
completely, though the ground still occasionally rumbles. Suphia flashes you a
quick grin. "That was close."
You agree with a little laugh. The The treant's unexpected appearance had been
both a blessing and a curse, but you had made it out alive. And now, with the
kobolds likely too occupied to follow, you can finally continue farther south
towards the kobold camp thinking and wishing, if only you could have taken the
treent with you to face the kobolds instead. 
'''
        )


    def ch_16(self): # following the trail pt 2, Spring 30th-31st, 3044, 6th age
        mon_list1 = self.config_monsters({'onikuma':3})
        mon_list2 = self.config_monsters({'small kobold':3})
        self.sixteen_intro()
        player_lives = self.battle.story(mon_list=mon_list1, dialog=self.sixteen_encounter0(), collective=False)
        if player_lives:
            self.sixteen_victory0()
            player_lives = self.battle.story(mon_list=mon_list2, dialog=self.sixteen_encounter1(), collective=False)
            if player_lives:
                self.sixteen_victory1()
                self.story_reward()
                self.story_prep(location='1-5', name='To the wall')
                return True
            else:
                return False
        else:
            return False

    def sixteen_intro(self): # traveling to the river
        dprint(
            f'''
It was still the middle of the night but sleep had fled far from you and so you
both decided to continue and call it an early day. According to the map, you
still had another few days ahead of you before reaching Luxkhanna and your
siblings, so it would probably be a good idea to keep moving anyway. 
Your first stop early that morning as the sun came up over the horrizon was one
of the increasingly common hills in this area. The top was bare of trees
allowing a good vantage point. The hill, however, was nowhere near the tallest
in the area and so you couldn't see far in a few directions especially farther
south as the hills continued to merge into mountain foothils. You did see, just
beyond a hill to your west, a wide river carving a valley that would likely
lead you right up to the distant mountains. 
Reasoning that that route would be far less treacherous and much more straight
forward, you both spend the rest of the day heading to the river and following
it along the valley. Because of your early start to the day, you agree to make
camp shortly after the sun sets and, thankfully, an uneventfull night passes. 
'''
        )

    def sixteen_encounter0(self): # Illegal food, Spirit Bears
        dprint(
            f'''
The next morning you are woken by a welcome smell. Suphia had cooked up a
gigantic salmon she had apparently caught earlier. Spit roasted and seasoned
from the wild herbs nearby, the the meat smelt devine and made you realize how
long it had been since you had had real food. She portioned out the fish and
together you dug in. 
The first bite takes you away as the flaky texture dizolves in you mouth. The
flavor is rich and buttery, with a subtle hint of saltiness from the distant
ocean. The smoke from its flame cooking added a depth and complexity that
elevates the taste to a whole new level and leaves your palette satisfied long
after each bite. 
This fish was massive too. Enough to fill you both completely with a little
extra for later. With a well enjoyed meal finished and the remainders packed
away, you refocus your attention on the task as hand.
Out of the corner of your eye you see something big and dark move through the
trees under the morning sun. Instantly a blinding flash fills the scene and
when it fades and instant later, three gigantic bears stand in your camp, one
holds its face an inch from yours. You leap back and the bear speaks. 
"Who are you?" comes its voice deep but soft almost like a whisper. 
A second later it makes a swipe for you which you avoid by again leaping
backwards. 
"You can...?" begins Suphia facing a bear of her own, "We don't want any
trouble!"
"Yet, you seem perfectly fine bringing it yourselves," answers the bear closest
to her, winding up for another swipe. 
"You take our food, we take you... as food," quips your bear before snapping
its jaws meanacingly.
"You can't expect us to have known it was your salmon!" reasons Suphia.
The bear in the back stands upon its hind legs and its head morphs shape. Its
snout flattens and brown fur dissapears. Within seconds an almost human face
rests where the bears snout once was. The only differing features being that of
its curved upward tusks and unnaturally wide eyes.
"You likewise cannot expect us to hunger for your sakes."
With those words it raises its arms as if conducting music before swiping
forward with both of the others initiating their attack.
'''
        )

    def sixteen_victory0(self): # Foreshadowing? 
        dprint(
            f'''
Just before the final blow, the last bear creature wails in an unearthly rage.
"FOUL... WRECHED! We will haunt your next life until your debt is paid!"
It sceams another terrible distorted unnatural scream, wailing like a tormented
spirit before falling backwards, still.
You both sit in silence for several moments before Suphia breaks it. 
"That was... actually, I have no idea what that was."
You agree and make your way further along the valley, sure to check your
surroundings before traveling far.
'''
        )

    def sixteen_encounter1(self): # Roll intimidation... 20!
        dprint(
            f'''
Hours later, you stumble upon a gaggle of kobolds seemingly digging in the side
of a hill. Having lost your last interrogation opportunity, you decide to
capture one or two and question them about the map among other things. Thirty
minutes later, you follow a group of about a dozen or so leaving the mine on
their usual set route. 
Tossing a stone as a diversion, you hunker down and watch their actions for the
perfect opportunity. Three stop briefly at the sound of the rock hitting the 
forest floor but they do nothing and continue on, catching up with the others
quickly a little more on guard. 
"Well that didn't work," you say. 
You continue to follow them for a minute or so before one of them clearly see
you or at least evidence of you as he points directly at your bush and says
something to the kobold next to him who glances briefly at your hiding place
too before turning the first kobold away and whispering something to it.
"Their either planning an ambush or discounting what they saw," remarks Suphia
in an undertone. 
You decide to stay where you are and let the kobold band continue back to the
mine. A few minutes pass and, true to Suphias prediction, you both detect two
separate kobold bands behind you as well as a third looking similar to the
group that just passed. 
"What should we do?" Suphia asks.
Quickly counting up the opposing numbers in your head and seeing none of the
giant Ruin Kobolds, you agree to make it clear to the enemy that this is no
longer an ambush. Maybe trying your had at intimidation? 
Steadilly, confidantly, you rise from your hiding place and look directly into
the faces of each kobold group. Neither you nor Suphia are the most
intimidating people ever, but as you stare them down and draw your weapons, the
atmosphere in the wood completely changes. Rather than also come out of their
hiding places, make kobolds slink down further and maybe even take a few silent
shuffles backward. Suphia brandishes her weapon in the direction of the closest
group and takes a steady step in their direction. You follow suit at the same
moment as she takes another and that seems to break them. 
First comes a nervous jitter from the group and then a high scream before they
all scatter. Several kobolds from the two groups behind you think it a good
opportunity to attack from behind but before they get too close, you both turn
on your heels causing the attackers to skid to a halt in the undergrowth. 
Finally, one kobold in the front stands its ground, looks to its kobold
companions on either side of it, glares at the ground with its eyes closed
tight, gives with the others a strong battle cry and finally they charge in,
weapons raised.
'''
        )

    def sixteen_victory1(self): # interrogation, bigger dialogue test
        prompts = ('Well...?!','Spill it then!',
                   'We know he\'s further south, but where in the south and how far?',
                   'I\'ll give you to the count of three...ONE!...',
                   'Is this map accurate?','Answer or die...that simple.',
                   'Spit it out!','Look, we really don\'t want to hurt you...')
        dprint(
            f'''
Several other kobolds seem to have been spurred on to courage by the battle,
but after seeing how quickly and efficiently you dispatched three of their
number, they were now in full retreat. Fortunately, due to a little healing
magic on Suphia's part, you had three perfectly fine kobolds ready for
interrogation. Well, maybe not perfectly fine. 
You mostly had four questions to ask the kobolds as you were now and Suphia
began with the first as soon as the first kobolds woke and found himself bound
to a tree. 
"Alright, can you understand me?" she began in a calm tone. 
After a few moments the kobold shook its head back and fourth nervously,
clearly not realizing that that as good as meant "yes!"
"Aww man!" Said Suphia in mock exasperation, looking to you with big sad eyes,
"looks like weve got another dud!" she said bringing a knife to the kobolds
throat. 
"Waaiiiet! Waiiet! No, I do, I doo! Don kill mii!" screamed the kobold. 
"Fantastic! Where's Capper Luxkhanna?! If you don't know or don't tell, I'll
kill you too!"
The kobolds looked around for a few moments before nodding. 
"I yam onli digger...BUT..!" it shouted as suphia sighed and pressed the blade
into the kobolds scaily neck, "But, I tink I may still nou..."
'''
        )
        response = basic_player_prompt(*prompts)
        if response == 1:
            dprint(
                '''
The kobold winces at the threat of a second interrogator and responds, "I think
Capper is south. There is a wall, yes, yes, wooden wall, south of here, cross
it. You will find him beyond it, yes, cross the wall."
'''
            )
        elif response == 2:
            dprint(
                '''
The kobold glares briefly at you, but winces soon after meeting your gaze.
"Capper is south. There is a wall, yes, yes, wooden wall, south of here, cross
it. You will find him beyond it, yes, cross the wall. hehehe heh heh!"
*cough* *cough*
'''
            )
        elif response == 3 or response == 5:
            dprint(
                '''
You pull out the map and the kobolds eyes narrow upon a point you gesture to,
the camp icon with the words "Hail Capper Luxkhanna" above it. 
"Hmmmm... yes, that looks, yeeeehs" the most fleeting shadow of a smirk flies
across his face before he continues, "but it is a long journey, make sure to
stay in the wuuds beyond the wall there." 
The kobold gestures with its snout to a thin brown line about a day south of
your current location before going as dead silent as possible, fixing his gaze
on some point about thirty feet past you both.
You and Suphia exchange looks deciding not to acknowledge the obvious trap in
his words. It was good to know that those woods were dangerous somehow and also
that average kobolds were extremely dim.
'''
            )
        elif response == 4:
            dprint(
                '''
*Screee*
"South capper is south past a mountain!" said the kobold ending in a wimper.
"Great!" said Suphia, stowing the knife and pulling out the map you had found
at the abandoned kobold camp. The kobolds eyes narrow upon a point she gestures
to, the camp icon with the words "Hail Capper Luxkhanna" above it. 
"Hmmmm... yes, that looks, yeeeehs" the most fleeting shadow of a smirk flies
across his face before he continues, "but it is a long journey, make sure to
make camp in the wuuds beyond the woooden wal ther." 
The kobold gestures with its snout to a thin brown line about a day south of
your current location before going as dead silent as possible, fixing his gaze
on some point about thirty feet past you both.
You and Suphia share a knowing look, choosing not to reveal how transparent the
trap in his words is. At least now you know that the woods beyond the wall are
dangerous somehow, and also that ordinary kobolds are quite dim.
'''
            )
        elif response == 6:
            dprint(
                '''
Suphia supresses a snort and the kobolds eyes widen before rattling off a
quick, "South capper is south past a mountain!" ending in a wimper. 
"Great!" said Suphia, stowing the knife and pulling out the map you had found
at the abandoned kobold camp. The kobolds eyes narrow upon a point she gestures
to, the camp icon with the words "Hail Capper Luxkhanna" above it. 
"Hmmmm... yes, that looks, yeeeehs" the most fleeting shadow of a smirk flies
across his face before he continues, "but it is a long journey, make sure to
make camp in the wuuds beyond the woooden wal ther." 
The kobold gestures with its snout to a thin brown line about a day south of
your current location before going as dead silent as possible, fixing his gaze
on some point about thirty feet past you both.
You and Suphia share a knowing look, choosing not to reveal how transparent the
trap in his words is. At least now you know that the woods beyond the wall are
dangerous somehow, and also that ordinary kobolds are quite dim.
'''
            )
        elif response == 7:
            dprint(
                '''
The kobold winces at the threat of a second interrogator and responds, "I think
Capper is south. There is a wall, yes, yes, wooden wall, south of here, cross
it. You will find him beyond it, yes, cross the wall."
'''
            )
        else:
            dprint(
                '''
The kobold and Suphia both give you the same look for different reasons.
"Hand me the map." She says holding out her dagger hand. 
You pull out the old kobold map you had found at the abandoned camp and hand it
to her. Relinquishing her grip on the kobold she unravels the paper and
gestures to a point on the map with her knife. 
"Is this where he is?"
"Hmmmm... yes, that looks, yeeeehs" the most fleeting shadow of a smirk flies
across his face before he continues, "but it is a long journey, make sure to
make camp in the wuuds beyond the woooden wal ther." 
The kobold gestures with its snout to a thin brown line about a day south of
your current location before going as dead silent as possible, fixing his gaze
on some point about thirty feet past you both. Clearly trying not to smile
again. 
You and Suphia share a knowing look, choosing not to reveal how transparent the
trap in his words is. At least now you know that the woods beyond the wall are
dangerous somehow, and also that ordinary kobolds are pretty dumb.
'''
            )
        dprint(
                '''
Either way you continue to interrogate the kobold until soon the other kobolds
wake and enter the interrogation too. Funnily enough, the other two talk about
the wooden wall and the forest beyond with the exact same tone as the first.
As Subtly as they can muster, trying to convince you that those woods are a
fantastic place to camp and stay for a while.
Next, you ask the kobolds about what they know on the recent attack on
Greentown. They seem truthfully enough to not know much about it other than
that it happened and that Pompon to the south-west and Tolbantha to the west
were likely the other two settlements targeted. 
Just as you suspect from their answers to the previous question you get little
information about prisoners and prison routes after the attacks leaving you
still with the same goal and hope that finding the kobold leader will also find
you your abducted siblings.
The kobolds give one more closing remark encouraging you to camp in the woods
as soon as you cross beyond the wooden wall each sharing a smirk that could not
possibly give away their plan more to which Suphia says, "Alrighty then...lead
the way!"
Having not expected this the kobolds merely sit in dreaded silence even after
their bindings are removed. 
"Go on," she says holding back a smile, "It sounds like those woods are just
great so lets go!"
Slowly, silently, the kobolds rise to their feet the one in the center flashes
the briefest emotionless smile before leading the way. 
'''
            )


    def ch_17(self): # surrounded by nepenths (pre-boss), Spring 31st-32nd, 3044, 6th age
        mon_list0 = self.config_monsters({'little nepenth':1, 'barkling':1, 'windwasp':1, 'little nepenth':1})
        mon_list1 = self.config_monsters({'little nepenth':2, 'nepenth':1, 'pod nepenth':1})
        mon_list2 = self.config_monsters({'Pod Nepenth':1, 'flower nepenth':2, 'big nepenth':1, 'nepenth':4, 'little nepenth':3})
        mon_list3 = self.config_monsters({'flower nepenth':1, 'nepenth':1,'little nepenth':3})
        mon_list4 = self.config_monsters({'flower nepenth':1, 'big nepenth':1, 'nepenth':2, 'little nepenth':1})
        self.seventeen_intro()
        player_lives = self.battle.story(mon_list=mon_list0, dialog=self.seventeen_encounter0(), collective=False)
        if player_lives:
            self.seventeen_victory0()
            player_lives = self.battle.story(mon_list=mon_list1, dialog=self.seventeen_encounter1(), collective=False)
            if player_lives:
                self.seventeen_victory1()
                player_lives = self.battle.story(mon_list=mon_list2, dialog=self.seventeen_encounter2(), collective=True)
                if player_lives:
                    self.seventeen_victory2()
                    self.adjust_team('Suphia', add=False)
                    player_lives = self.battle.story(mon_list=mon_list3, dialog=self.seventeen_encounter3(), collective=True)
                    if player_lives:
                        self.seventeen_victory3()
                        player_lives = self.battle.story(mon_list=mon_list4, dialog=self.seventeen_encounter4(), collective=False)
                        if player_lives:
                            self.seventeen_victory4()
                            self.story_reward()
                            self.story_prep(location='1-6', name='Leave the nepenth woods')
                            return True
                        else:
                            return False
                    else:
                        return False
                else: 
                    return False
            else:
                return False
        else:
            return False

    def seventeen_intro(self): # let them go, outside the wall
        dprint(
            f'''
For the rest of the day, your captives make several attempts to derail the
situation or remove themselves from it. First they begin leading you east
rather then farther south like they has said. Next, one suddenly realizes that
he had forgotten that the wall was actually to the west not the south until you
point to the wall as it appeared on the map and he conceeds. At about nightfall,
one of the kobolds tries to make a break for it but is quickly recaptured. Soon
you realize that the desperate escape attempt was made because they could make
out the wall from a few miles away due to their mild dark vision and they knew
that soon after you would see it as well. Their dread was palpable and you both
exchange a quiet word behind the quavering backs of your captive kobolds,
agreeing to let them go at their next escape attempt which comes almost
imediately. 
Having noticed your quiet conversation and seeing it as the slightest of
distractions, they take their chance, bolting in three seperate directions.
Even if you hadn't just agreed to let them off, you probably would have been
hard pressed to recapture all three of them. So, considering it fortunate
timing, you watch them skitter out of sight with many whoops and high
kackles of relief and success.
Less than an hour later you arrive within natural human eyesight of the wooden
wall. It was made up of cored trees sharpened into spikes near each tip. For
this reason it was variable in height from less than twenty feet to nearly
fifty feet in places. Up close you found that it continued without break or
entrance point as far as you could see to both sides. 
You withdraw a few hundred paces from the wall and make a light camp for the
night. With the kobolds' words about the woods beyond the wall lingering in
your mind, you spend the night preparing for the dangers ahead and maintain a
vigilant watch throughout.
'''
        )

    def seventeen_encounter0(self): # Suphia's reason why
        prompts = ('Distance is no problem, it\'s time I\'m worried about.',
                   'I don\'t want to burden you, if you want to return to Electo and the town...',
                   'Let\'s go through!',
                   'I think whatever comes at us in those woods, we can handle.')
        dprint(
            f'''
A while after sunrise, you break camp and make your way back to the wall. 
"Alright, according to the kobolds, these woods are definitely something to be
wary of," began Suphia, "I mean why else would there be a whole wall keeping
whatever dangers these woods hold in? ... But, according to the map it really
looks like this is the most direct way to Luxkhanna. If you think it would be
better not to risk it we can go around, but it is quite a fair distance. What
Do you think?"
'''
        )
        response = basic_player_prompt(*prompts)
        if response == 1:
            dprint(
                '''
"I concur. I don\'t believe the kobolds would be so terrible as to kill their
prisoners but I would like to get to them sooner than later..."
'''
            )
            dprint(f'. . . "{self.player.name}"', .06)
            dprint(
                '''
"I know you must think this is a mission for you alone as it is your siblings
that were taken. Starting out I thought similarly, but traveling, fighting, 
strategizing with you, I have come to view you in a similar light as my own
brother Electo. In my mind, Robin and Rosie have become mine as well and I
would go through Avernus itself for them just as I know you would."
'''
            )
        if response == 2:
            dprint(
                '''
"You know... it's strange, over the course of our travels, battles, experiences,
it feels almost like I am traveling with my own brother Electo. I would venture
into the fires of Avernus itself to liberate him from captivity and I know you
woud do the same for Robin and Rosie. This mission is not a burden to me, I
know Electo is safe in Greentown awaiting our triumphant return, so I will do
everything in my power to make that happen. But my greatest desire above that
is the rescue of your siblings, siblings who, in my mind have become my own in
spirit."
'''
            )
        if response == 3:
            dprint(
                '''
"I admire your resolve, you have reminded me of my own brother Electo. I know
he would want to rescue prisoners as soon as possible as well. Let's go!"
'''
            )
        if response == 4:
            dprint(
                '''
Suphia smiles, "Your probably right, and honestly, I have become quite mentally
invested in recovering Robin and Rosie. I find it difficult now to believe
there can be anything in this world able to stand in our way."
'''
            )
        dprint(
            '''
With that you begin skirting the wall looking for an easier way through before
resorting to digging, climbing or breaching by force. Fortunately, about a half
mile to the west, you do find a shallow dip in the earth and a gap in the posts 
alligned just so that you could squeeze through. 
On the other side the woods look and feel little different from before. The
difference does come soon enough though as you hear several quick, skittery
movements between the trees and through the brush. 
With the morning sun still low in the sky, visibility is less than ideal, but
enough to spot a few smaller woodland creatures like rabits, foxes, squirels
and pikas scurrying out of sight. Only about two hours in do things start
becoming ominous. You spot a large skeleton through the trees and only realize
up close that it's the broken remains of a gigantic bear. The skeleton was not
quite the size of the cave bear you encountered before, but was still easilly 
larger and more powerful looking than a common grizzly.
"What kind of bear-" you begin.
"Nepenths." interrupted Suphia.
"I don't think that's a Nepenth," you say pointing to the carcas.
"No I mean, Nepenths did this. look at the slashes in the bones. Nepenths
killed this bear and picked it clean. As for the variety of bear... it almost
looks like a juvenile Ursaring but I'm pretty sure those mostly inhabit the
mountanous regions in the far east. Whatever it is we should get out of he- 
WATCH OUT!"
'''
        )
            
    def seventeen_victory0(self): # o fricc these things are everywhere
        dprint(
            f'''
"We need to leave were attracting to much attention!" 
You both spring away from the sound of more approaching monsters, It wasn't a
bad fight but it looked like one that could keep going indefinietly if the
situation wasn't vacated quickly.
"Wait, theres another Nepenth ahead."
You both skidd to a halt several yards before the Nepenth, it was another small
one and it just stood there on its roots almost perfectly blending in to the
folliage, you turn to go around but Suphia grabs your shoulder hard, keeping
you in place. You look around following her gaze and spot another two nepenths
through the trees similarly camaflaged. Suphia puts a finger to her lips and
points back the direction you came. Your weapon begins to quiver as you do at
the sight she points out to you. 
Less than ten paces back, you passed less than five feet from the largest
nepenth you had ever seen, easilly twice the height and width of a little
nepenth with its barbed vines as thick as your arm relaxed at its side... 
"Sleeping" you conclude in a whisper. 
Suphia nods and points at three different points through the trees confirming
your fears that these woods were utterly crawling with nocturnal nepenths of
all shapes and sizes. Not only were you surrounded, but you had also been
surrounded for likely the last several minutes before the fight. 
*Flump*
The big nepenth behind you flops its heavy left vine on the forest floor in its
slumber. It was time to go again. It was only a matter of time before sleeping
nepenths smelled your presence and woke. Taking care to avoid fallen twiggs and
branches, you both make your way again swiftly and silently through the forest,
passing close to slumbering nepenth after slumbering nepenth. 
Doing so, you see some interesting features on some of the nepenths. Most were
simply the large and smaller varieties of the basic nepenth with its ever
gaping maw, no eyes, plant-like features and the large bulb hanging like a lamp
over their head. Some Nepenths though had bulbs that had apparently bloomed
into large scentless flowers, others has strange large fruits hanging there
instead. Oddly enough the fruits were the ones that stunk. 
'''
        )

    def seventeen_encounter1(self): # so it begins
        dprint(
            f'''
As you continue to sneak past the monsters, you come to the realization that
you had better get out of these woods before nightfall or it would turn into a
drawn out battle until the next dawn and likely beyond and you really didn't
know how many of these nepenths you could realisticly take. But picking up the
pace just makes too much noise.
'''
        )

    def seventeen_victory1(self): # oo YIIIIIKES! its empty!
        dprint(
            f'''
. . .
'''
        , .1)

    def seventeen_encounter2(self): # The fight
        dprint(
            f'''
The fruit above the pod nepenth's head shatters, releasing a stench so thick it stings
your eyes and smoke so dense it covers the scene in seconds, burning your lungs,
obscuring everything. Then you hear it, the sound of slow, deliberate movements
through the haze. The unmistakable shamblings of far too many nepenths. As the
smoke begins to thin and your vision adjusts, the nightmare takes shape.
Nepenths, twenty or more of them, of every twisted variety, emerge from the
shadows, lured by the smell of fresh death. There will be no where to run or
hide this time. Every possible exit is filled with their monstrous forms,
closing in from all directions.
'''
        )

    def seventeen_victory2(self): # victory? no not victory. 
        dprint(
            f'''
You've done the impossible, merely surviving longer than you had any right to
against the relentless swarm. But its not enough, The nepenths are endless, and
your strength is fading fast. You steal a glance at Suphia and your world
crumbles. An acid-green vine, as thick as your neck and covered in jagged barbs
pierces her lower chest and bursts out from her back pulling her body along
like a ragdoll, the sound of tearing flesh ringing in your ears.
The world seems to slow to nothing, but it doesn't stop. Reality presses on
mercilessly, with more strikes from the nepenths raining down on your back, tearing
you appart. Her dying eyes find yours, pain and resignation written in her
gaze. She mouths the begining of your name, but the words die before they reach
you. She is lifted high into the air, suspended like a trophy before the
gigantic monster. Her eyes open one final time, and with a last surge of effort,
she reaches out to you, her hand trembling.
A ball of golden light blasts out from her open hand and collides with your
collapsed form. A moment later, the nepenth's jaws close taking with it most of
her upper body.
'''
        )

    def seventeen_encounter3(self): # Magic!
        dprint(
            f'''
The sounds coming from your throat are drowned by a rushing like a wide
shoreline. The light from Suphia's last spell fills the scene and causes a few
of the monsters to pause for a moment. The warm trickling down your back stops
as a numb sensation briefly overtakes you. Your wounds begin to heal.
'''
        )
        dprint('. . . ', .1)
        self.player.hp += (self.player.maxhp // 2) + self.player.hp
        self.player.empowered = True
        display_health(self.player)
        dprint(
            f'''
Not only had Suphia lost her life in your aid, she had also used the last of
her strength and cast her final spell in hopes that you would make it through.
A flash of Rosie and Robin enters your minds eye and at the same moment, you
feel much more than healing energy within you. Somehow you can feel Suphia's
strength behind your blade now. You rise feeling beyond whole, filled with a
determination to fulfill Suphia's shared desire to get out of here and find
your siblings and bring justice to the monsters that brought these events to
pass.
'''
        )
        dprint(f'{self.player.name} is now EMPOWERED!', .1)
        
    def seventeen_victory3(self): # ehh might as well finish them off
        dprint(
            f'''
Plowing your way through nepenth after nepenth, you work you way towards your
target all while bringing their numbers down significantly. You havent seen
another pod nepenth yet and so determine that these nepenths around you must
be most of the ones around. You really couldn't care any less though, with
Suphia's last strength coursing through every fiber of your being, you know you
have a good chance of just taking them all down now.
'''
        )

    def seventeen_encounter4(self): # a taste of revenge
        dprint(
            f'''
There is however, one nepenth you want dead above all others, standing there,
just a couple nepenths away, as if mocking you after its victory. 
Never before in your life have you understood what revenge meant to people,
always seeing it as just a pointless way to cause unnecessary fights and
discord. Now you see that in some cases, especailly in this case, you couldn't
have been more wrong.
'''
        )

    def seventeen_victory4(self): # At last its over
        dprint(
            f'''
Finally, you stand, gasping for breath above your final foe. The woods are
finally silent again beyond the ringing in your ears. Without much pause, you
feel the last energy Suphia bestowed upon you fade swiftly away as she does. 
Your weapong falls to the forest floor and you follow suit soon after falling
to your knees, you body finally realizing what it was just put through. 
Victory, could not be more bitter to you as, minutes later you find the
strength to crawl to the remains of the mostly evaporated big nepenth, the
demise of your first real companion.
You don't even have the energy to mourn, your eyes and mouth both dry from over
use. After some time you gather the strength again to stand knowing that
spending the night here would likely be fatal; however, as you turn to go, your
eyes fall upon the now exposed remains of Suphia, her monstrous prison
dissipated. You know the risk but can't even entertain the thought of leaving 
her here.
You spend some time binding her up before beginning your way further south
carrying what you know is much more than a broken body, but a strong will,
faithful heart, cunning mind, and indominable spirit. 
After nearly an hour you begin seeing nepenths again, sleeping as before, as
well as the same familiar cautious woodland creatures, but it's like the wood
itself finally understands what is happening. The weight behind this single
person prosession is far to great to disturb and dispite the smell of death and
the soft crunching of topsoil and undergrowth at each step, nothing stirs as if
knowing full well what will most definitely befall them should they do so. 
'''
        )


    def ch_18(self): # scouting the Kosaur's lair, Spring 32nd-34rd, 3044, 6th age
        mon_list = self.config_monsters({'bandit':1})
        self.six_intro()
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.six_encounter0())
        if player_lives:
            self.six_victory0()
            self.story_reward()
            self.story_prep(location='1-6', name='Into the canyon')
            return True
        else:
            return False

    def eighteen_intro(self): # The funeral of Suphia
        dprint(
            f'''
Just as you suspected, Night begins to fall much sooner than you would have
liked and right as you begin to fear for the potential fights ahead, the forest
begins to stir. 
You pick up the pace and to your relief, the trees begin to thin soon after.
Now that you think about it, though, you haven't actually seen any nepenths for
a while anyway. It looks like the monsters perfer to stear clear of the edge of
these woods. Or maybe its the foothills you are now climbing, maybe it was
both. Either way, night falls quickly and sure enough nothing springs out at
you from the darkness. Tall pointed gray boulders begin jutting up from the
hillside in the place of trees and the dark mass of the mountain lies less than
a mile or so ahead of you. A bit of a way to the west the mountain seems to
melt away at the canyon. Luxkhanna's camp lies just beyond these mountains
through the canyon, but you have business to attend to first. 
At about what you estimate to be midnight, or maybe slightly after, you find a
level clearing surrounded by those jutting boulders and consider it as good a
place as any. 
You spend the rest of the knight working gathering materials and building. By
the time the sky begins to brighten again you have dug as deep a pit as you
could with what you had on hand and placed Suphia inside. 
After several moments of silence full of grattitude for her life and help and
remorse for its swift and sudden end, you then covered her wraped form, eyes
and hands stinging all the while before finally laying the flat stones you had
gathered in a sort of altar over the top. As it turns out you had never
actually attended a funeral in living memory but based on the circumstances
and current situation you felt this was the best you could do.
After another few moments of silence paying last respects, you again move a bit
of a ways down the mountain and turn your gaze west, more determined than ever
before, towards the canyon and what likely lies beyond.
'''
        )

    def eighteen_encounter0(self): # A survivor
        dprint(
            f'''
As the sun finally begins to rise in earnest over the elevated horrizon your
exhastion again begins to catch up to you. Every step takes a toll on your
mental and physical being. At about midday, you decide to make an early camp
and head into the canyon the next morning. The canyon mouth is narrow and sharp
only wide enough for the river to run through before ending in steep, sudden,
vertical walls of light gray stone on both sides. 
Over the last day or so you realize to both your relief and mounting axiety
that you haven't seen any kind of monsters in the area be they nepenths or
otherwise. It reminds you ominously of the strange calm before the storm that
was the kobold's inexplicable sudden attack on Greentown. 
Despite these thoughts, you take advantage of the calm and set up a lazy camp
under the stars on the banks of the river at the mouth of the canyon. 
That night, soreness and grief again set in and you get little rest before
nearly midnight again when exhastion overtakes you completely. You wake with
the midmorning sun shining into you eyes from above. Mere minutes after
breaking camp, you hear movement that sounds very different from the regular
babbling of the river. Heavy, hurried, irregular splashing is coming from a
short way inside the canyon and rapidly approaching. 
You quickly ready yourself on the shoreline ready for anything. What burst into
view, you are surprised to see, is a human clothed in a girdle of various skins
and with paints of a variety of colors on their face and other parts of their
skin. They came rushing out of the canyon club bared with a battle cry at the
ready as soon as you came into its view. You hold up your hands for peace but
it seems that a battle is inevetable as they just keep coming, brandishing
their club all the while. 
'''
        )

    def eighteen_victory0(self): # seen the mid-boss
        dprint(
            f'''
To what is likely both of your reliefs, the bandit withdraws after your last
hit, tossing his club behind him and screaming something in a strange language
you havent heard before. An then it hits you, the look in his eyes as he came
in for the attack, it was one not of anger or of much surprise, but of a deep
primal fear. You wish you noticed sooner as you now hear a new sound over the
river. A long drawn out roar. It was not a high call but it was not deep like a
lion's either. It rang out through the canyon walls for a long while before
trailing away there was clearly something big in this canyon. Something that
was keeping the local monsters away, something that bandit may have disturbed.
You spend a few minutes deliberating with yourself what to do and determine
that an aerial view would be the best scouting approach to find out what this
thing might be and what kind of a threat it poses. 
Soon enough you find a tricky way up but a way up no less and by the early
afternoon you find yourself crawling and climbing around rocks, boulders and
slipery patches of gravel to get further along the top of the canyon wall to
maybe spot the beast. You find a decently flat spot to take a break and notice
something strange about a small puddle towards the mountain wall. Every second
or so you notice regular circular ripples form along the outside of the puddle.
They are small and dissipate quickly but are just large enough to be noticeable
from your resting place. You crouch down for a better look and sure enough,
every about one and half seconds the glassy surface of the water is broken by
those circular rings. With the river far below you now, the air is nearly
silent allowing you to strain your ears for the sounds that may accompany the
ripples. 
*brrr* *brrr* *brrr*
The sound you hear as you press your ear against the cold rock seems to vibrate
and reverberate through the whole earth. A deep boom accompanied by a distant
rumble.
The route you picked out along the side of the canyon wall seems to come to an
end a few hundren feet later but that ends up being all you need. As you peer
around your dead end and into the canyon, you see it, more than see it, you
smell it too, the stench of blood and decay. The bodies of a few dozen human
bandits, just like the one you fought earlier today, lay strewn across the
banks of the river. And their killer stalking just beyond. 
A gigantic orange and brown, scaly biped, with horns like pointed battlements
along its head and spine, tipping a massive muscular body designed for
devastation. A set of wings spanning easily thirty feet still seemed almost
comically small when compared to the rest of its hulking frame, tipped with a
clubbed tail, huge powerful claws and a disproportionately large
head and jaws that looked capable of crunching entire houses in one go. 
In its entirety, the dinosaur like creature was over fifty feet tall and about
that long including its tail. Truly a powerful looking beast. It was a
relatively safe distance away and you had good cover but the sight still left
your heart thumping in your chest.
It didn't look like there was any way around besides finding another canyon
somewhere and you weren't about to go back now. This left the only real option
of fighting your way past it.
You carefully make your way back to the mouth of the canyon and as evening
approaches you steel yourself for the next morning in which you would challenge
the king of the canyon.
'''
        )


    def ch_19(self): # Kosaur boss fight, Spring 35th, 3044, 6th age
        mon_list = self.config_monsters({'Kosaur':1})
        self.six_intro()
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.six_encounter0())
        if player_lives:
            self.six_victory0()
            self.story_reward()
            return True
        else:
            return False

    def nineteen_intro(self): # 
        dprint(
            f'''
You wake, fully rested and ready to go now for the first time since before the
wall. Today was the day, probably the biggest, riskiest fight so far and that
was saying something considering the devastating outcome of the last big fight
in the woods now far behind you. Preparing youself for what was to follow, you
wash briefly in the river to wake up more before heading into the canyon trying
to stay as dry and light on your feet as possible. 
In your head you go over the brief plan you had fassioned the last night:
"Try to sneak as far past it as possible. Keep a constant eye on it and your
surroundings. Look for possible advantages in the landscape, hiding places,
vantage points. Fight defensively when the time comes, use all available
resources. During the fight, try to confuse it, get behind it and make your
escape only at the opportune moment, it doesn't have to end with a death, I
have too much on the line, too much more to lose."
Far sooner than you had thought, you find yourself edging along the eastern
wall, crouched low, both eyes fixed on the collosal creature digging and
scratching at the dirt fewer than a hundred steps away, steps for you anyway,
maybe three or four steps for it. 
You edge closer and closer farther and farther along the wall, hoping beyond
hope that it just never spots you, knowing that those odds are very slim. There
are no trees in this part of the canyon, little undergrowth or large rocks to
hide behind, just you and the wall you hope you can blend into enough. That and
a river you hope can continue to mask your careful steps. 
You are almost level with it before the worst happens, it pauses to sniff the
air and apparently imediately notices something. 
'''
        )

    def nineteen_encounter0(self): # 
        dprint(
            f'''
Just the act of it turning directly towards you made it seem twice its normally
gargantuan size. Its forward facing black eyes aimed hungrilly at its next
prospective meal. It raises it head and body to its full height in a motion
that could almost be surprise before it arches backwards and bellows an ear
splitting roar that shakes your bones and causes your feet to glue themselves
in place. Again it looks at you, apraising you, waiting. 
You draw your sword, and you both spring into action!
'''
        , .045)

    def nineteen_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_20(self):
        pass # kosaur boss recovery

    def twenty_intro(self): #
        dprint(
            f'''

'''
        )

    def twenty_encounter0(self): # 
        dprint(
            f'''

'''
        )

    def twenty_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_21(self):
        pass # following the trail pt 3

    def twenty_one_intro(self): #
        dprint(
            f'''

'''
        )

    def twenty_one_encounter0(self): # 
        dprint(
            f'''

'''
        )

    def twenty_one_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_22(self):
        pass # following the trail pt 4

    def twenty_two_intro(self): #
        dprint(
            f'''

'''
        )

    def twenty_two_encounter0(self): # 
        dprint(
            f'''

'''
        )

    def twenty_two_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_23(self):
        pass # found the kobold camp and spot Robin

    def twenty_three_intro(self): #
        dprint(
            f'''

'''
        )

    def twenty_three_encounter0(self): # 
        dprint(
            f'''

'''
        )

    def twenty_three_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_24(self):
        pass # infiltrate, encounter with Illfang

    def twenty_four_intro(self): #
        dprint(
            f'''

'''
        )

    def twenty_four_encounter0(self): # 
        dprint(
            f'''

'''
        )

    def twenty_four_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_25(self):
        pass # the kobold plans

    def twenty_five_intro(self): #
        dprint(
            f'''

'''
        )

    def twenty_five_encounter0(self): # 
        dprint(
            f'''

'''
        )

    def twenty_five_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_26(self):
        pass # rush back to warn the town

    def twenty_six_intro(self): #
        dprint(
            f'''

'''
        )

    def twenty_six_encounter0(self): # 
        dprint(
            f'''

'''
        )

    def twenty_six_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_27(self):
        pass # rush back to warn the town pt 2

    def twenty_seven_intro(self): #
        dprint(
            f'''

'''
        )

    def twenty_seven_encounter0(self): # 
        dprint(
            f'''

'''
        )

    def twenty_seven_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_28(self):
        pass # plan is to attack first

    def twenty_eight_intro(self): #
        dprint(
            f'''

'''
        )

    def twenty_eight_encounter0(self): # 
        dprint(
            f'''

'''
        )

    def twenty_eight_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_29(self):
        pass # heading out

    def twenty_nine_intro(self): #
        dprint(
            f'''

'''
        )

    def twenty_nine_encounter0(self): #
        dprint(
            f'''

'''
        )

    def twenty_nine_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_30(self):
        pass # the boss' lair

    def thirty_intro(self): #
        dprint(
            f'''

'''
        )

    def thirty_encounter0(self): #
        dprint(
            f'''

'''
        )

    def thirty_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_31(self):
        pass # the boss' lair pt 2

    def thirty_one_intro(self): #
        dprint(
            f'''

'''
        )

    def thirty_one_encounter0(self): #
        dprint(
            f'''

'''
        )

    def thirty_one_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_32(self):
        pass # Illfang boss fight

    def thirty_two_intro(self): #
        dprint(
            f'''

'''
        )

    def thirty_two_encounter0(self): #
        dprint(
            f'''

'''
        )

    def thirty_two_victory0(self): #
        dprint(
            f'''

'''
        )

