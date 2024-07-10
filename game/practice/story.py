
from actions import *
from things_stuff import *
from monsters import init_enemies, init_allies
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
        self.all_allies = init_allies()

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
    
    def story_reward(self):
        self.player.progress += 1
        self.player.hp += (self.player.maxhp - self.player.hp) // 2 if self.player.hp < self.player.maxhp else 0
        self.player.gain_xp((self.player.level * 2) + (self.player.progress * 2) + 1, self.xp_thresholds)


    def adjust_team(self, to_modify:str, add_or_remove='add'):
        """
        Modifies the player's team by adding or removing allies based on their desigantion.
        Also removes duplicate allies with the same desigantion.

        Args:
            to_modify (str, required): Desigantion of the ally to add or remove.
            add_or_remove (str, optional): 'add' to add an ally, 'remove' to remove. Defaults to 'add'.
        """

        # print(f'to_modify: {to_modify}, add_or_remove: {add_or_remove}')
        # print(f'0 __ player.allies: {self.player.allies}')
        ally_designations = set()
        # print(f'initial ally_designations: {ally_designations}')
        for i in range(len(self.player.allies)): # This performs the remove operation but records the unique names of
            ally_designations.add(self.player.allies[i].designation) # all that were in it the list of allies before
        # if len(ally_designations) != len(self.player.allies):
            # print(f'OH NO! THE FIRST LOOP DIDN\'T WORK {len(ally_designations)} != {len(self.player.allies)}')
        self.player.allies.clear() # allies list should be empty now
        # print(f'0 -- ally_designations set: {ally_designations}')
        # print(f'1 __ player.allies (which has now been emptied): {self.player.allies}')

        for ally in self.all_allies: # iterate through all allies in existence
            # print(f'ally.designation: {ally.designation}, to_modify: {to_modify}, add_or_remove: {add_or_remove}')
            if ally.designation == to_modify: # find the ally matching the desired ally
                # print(f'1 -- ally_designations set: {ally_designations}')

                if add_or_remove == 'add': # if the ally is to be added

                    ally_designations.add(ally.designation)

                else:
                    # print(f'Else (remove): {ally.designation}')
                    # print(f'2 __ player.allies: {self.player.allies}')
                    # print(f'2 -- ally_designations set: {ally_designations}')
                    ally_designations.discard(ally.designation)

                    # try:
                    #     ally_designations.remove(ally.designation)
                    # except KeyError as key_error:
                    #     ally_designations.add(ally.designation)
                    #     ally_designations.remove(ally.designation)
        
        # print(f'3 __ player.allies: {self.player.allies}')
        # print(f'3 -- ally_designations set: {ally_designations}')
        for ally in self.all_allies: # iterate through all allies in existence
            # print(f'{ally.designation} is being checked to be in ally_designations set')
            if ally.designation in ally_designations: # find only the names that are to be in the new team
                # print(f'4 -- ally_designations set: {ally_designations}, current ally: {ally.designation}')
                # print(f'4 __ player.allies before: {self.player.allies}')
                self.player.allies.append(ally) # add all those guys
                # print(f'5 __ player.allies after: {self.player.allies}')
                # print(f'5 -- ally_designations set: {ally_designations}')
        # print(f'Final results: ally_designations set: {ally_designations} player.allies: {self.player.allies}')




    def ch_0(self):
        mon_list = self.config_monsters({'brown worm':1,'slime':1})
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.zero_encounter(),collective=True)
        if player_lives:
            self.zero_victory()
            self.story_reward()
            self.adjust_team('Robin 0', 'add')
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


    def ch_1(self):
        mon_list1 = self.config_monsters({'windworm':1,'cykloone':1,'greedy badger':1})
        mon_list2 = self.config_monsters({'greedy badger': 3, 'frenzy boar':1})
        self.adjust_team('Robin 0', 'add')
        self.one_intro()
        player_lives = self.battle.story(mon_list=mon_list1, dialog=self.one_encounter0(), collective=True)
        if player_lives:
            self.one_victory0()
            player_lives = self.battle.story(mon_list=mon_list2, dialog=self.one_encounter1())
            if player_lives:
                self.one_victory1()
                self.story_reward()
                self.adjust_team('Robin 0', 'remove')
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

    def one_victory0(self): # Thy got my sword, or did they
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


    def ch_2(self):
        mon_list0 = self.config_monsters({'field wolf':2})
        mon_list1 = self.config_monsters({'field wolf':2, 'small kobold':2})
        mon_list2 = self.config_monsters({'refuse':1})
        self.adjust_team('Robin 0', 'add')
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
                    self.adjust_team('Robin 0','remove')
                    return True
                else: 
                    return False
            else:
                return False
        else:
            return False
    
    def two_intro(self): # LOOOOOOOOORRRRE dump
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


    def ch_3(self):
        mon_list1 = self.config_monsters({'slime':2,'awakened shrub':1,'barkling':1})
        mon_list2 = self.config_monsters({'small kobold': 3})
        self.adjust_team('Robin 0', 'add')
        self.three_intro()
        player_lives = self.battle.story(mon_list=mon_list1, dialog=self.three_encounter0(), collective=True)
        if player_lives:
            self.three_victory0()
            player_lives = self.battle.story(mon_list=mon_list2, dialog=self.three_encounter1(), collective=True)
            if player_lives:
                self.three_victory1()
                self.story_reward()
                self.adjust_team('Robin 0', 'remove')
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


    def ch_4(self):
        mon_list = self.config_monsters({'little nepenth':1})
        self.four_intro()
        self.adjust_team('Robin 0', 'remove')
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.four_encounter0())
        if player_lives:
            self.four_victory0()
            self.story_reward()
            self.adjust_team('Robin 0', 'remove')
            return True
        else:
            return False

    def four_intro(self): # that one scene from SAO in the amphitheater
        dprint('The report to the captain of the guard, Outh Gurenge, went well')
        dprint('enough. He informaed you that he has recieved similar reports')
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
        dprint('case. After a short pause, he raises hs had and volunteers you')
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
        dprint('south of there, we usually use them to test new recruits so')
        dprint('good luck to ya!"')

    def four_victory0(self): # victory, the lion roars once more!
        dprint('.  .  .',.25)
        dprint('Having passed the captain\'s test and standing over the')
        dprint('dissolving form of the Nepenth, you hear a short cheer from the')
        dprint('anxiously spectating Robin as wells as an impressed slow clap')
        dprint('from the captain who welcomes you to the ranks with open arms.')


    def ch_5(self):
        mon_list0 = self.config_monsters({'dire wolf':3, 'small kobold':3, 'kobold slave':2, 'kobold guard':1})
        mon_list1 = self.config_monsters({'dire wolf':1, 'small kobold':2, 'kobold slave':2, 'kobold soldier':1})
        mon_list2 = self.config_monsters({'dire wolf':2, 'small kobold':2, 'kobold guard':1})
        self.adjust_team('Henry','add')
        self.adjust_team('Liliyah','add')
        self.adjust_team('Tiffey','add')
        self.adjust_team('Kajlo Sohler','add')
        self.adjust_team('Officer Jerrimathyus','add')
        self.adjust_team('Robin 0', 'remove')
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
                    self.adjust_team('Henry','remove')
                    self.adjust_team('Liliyah','remove')
                    self.adjust_team('Tiffey','remove')
                    self.adjust_team('Kajlo Sohler','remove')
                    self.adjust_team('Officer Jerrimathyus','remove')
                    self.adjust_team('Robin 0', 'remove')
                    return True
                else: 
                    return False
            else:
                return False
        else:
            return False

    def five_intro(self): # OMG multi lined strings, YES! also henry's a jerk. 
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


    def ch_6(self):
        mon_list = self.config_monsters({'little nepenth':1, 'awakened shrub':1, 'barkling':1, 'green worm':1, 'shrubent':1})
        self.six_intro()
        self.adjust_team('Kajlo Sohler','add')
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.six_encounter0())
        if player_lives:
            self.six_victory0()
            self.story_reward()
            self.adjust_team('Kajlo Sohler','remove')
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
"Wow, you certainly are natural! It is almost unnatural, how gifted you are."
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

    def six_victory0(self): # Ifninite dialogue, p1: oh, shoot. pt2: A new mission. 
        dprint(
            f'''
The fight is won and without further wait, you continue your marathon back to 
Greentown. Finaly after nearly 7 hours of running laden with your important 
letters. Here, you split off from Kajlo, you take the letter informing Henry's 
family of the dire situation while your companion takes the note requesting aid. 
It doesn't take you long to find the adress on the note what with Greentown 
being the size it is. You take one more deep breath thinking about what to say
before giving a hardy knock on the door. Moments later a boy no older than 
Robin's age opens to you and looks you up and down for at least 10 
seconds before locking his eyes on the letter. Without, change in tone or so 
much as a blink he says.
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
Upon arriving, you near the main office of the captain and hear raised voices. 
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
through you rather than at you. 
Moments later Captain Gurenge peeks his head out the door too and says
"Ah, {self.player.name}, um, please wait outside for a moment."
"No need captain, I will be taking my leave now, but please take some time to 
consider the true import of this matter before you send this boy off. Good day!"
the man leaves the office places a cap atop his bald head and strolls out the 
door leaving both you and the Captian with mouths agape. 
"Um, if now is not a good time..."
"*sigh* no, no, please come in." 
With those words you are reminded of the last time someone less than happy 
asked you to come in and the request of Han reenters your mind at top speed. 
You ask about Henry's family but before you finish Captain Gurenge tells you 
that he cannot do anything until Henry is legally dead and even after that it 
would be him just sending the request up to Mayor Swendil. "What I can do is 
give him a big bonus if... when he does come back."
Thanking your captian in behalf of Henry and his family and detecting that there 
was nothing more to do on that front, you ask about the man who was just in here 
and the mission that needed to be done at which point any ammount of positivity 
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


    def ch_7(self): # the cave
        mon_list0 = self.config_monsters({'nepenth':1})
        mon_list1 = self.config_monsters({'awakened shrub':10})
        mon_list2 = self.config_monsters({'cave bear':1})
        self.seven_intro()
        player_lives = self.battle.story(mon_list=mon_list0, dialog=self.seven_encounter0(), collective=True)
        if player_lives:
            self.seven_victory0()
            player_lives = self.battle.story(mon_list=mon_list1, dialog=self.seven_encounter1(), collective=True)
            if player_lives:
                self.seven_victory1()
                player_lives = self.battle.story(mon_list=mon_list2, dialog=self.seven_encounter2(), collective=True)
                if player_lives:
                    self.seven_victory2()
                    self.story_reward()
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
Yesterday, Spring 26th, at dusk, a team of scouts followed a group of armed
Kobolds into a forest. The team sent a report of their findings by pigeon mail 
back to Greentown while they continued following the Kobolds. The original team 
has yet to come back and the return pigeon came back having failed to deliver 
his note indicating the scout team is still on the search but in a separate 
location. The mission for {self.player.name} is now to find the scouts and if 
possible look further into the followed kobolds. For this reason this mission 
is to be executed in utmost stealth and caution. Follow the provided map for 
location details and return and report if possible before spring 32nd at midday. 
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
After probably the most heebee geebee worthy fight of your life minus that big 
rat you got rid of when you were Robin's age you continue onwards. Following 
the trail leads you to a long fissure in the ground. The darkness inside seems 
all consuming as you peer into its depths. After a few breaths of encouragement, 
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


    def ch_8(self): # red herring of some kind 
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
                return True
            else:
                return False
        else:
            return False
        
    def eight_intro(self): # little cave camp
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
A less than thurough search of the rest of the small hideout reveals another 
note in common detailing instructions to carry a small group of human scouts
they apparently had as prisoners to somewhere in the north. You also find more 
and more signs that this camp was abandoned in haste. almost as if to flee some
approaching threat. 
Either way you feel like you have the information you need and more, so you 
turn now to your map for directions for an equally hasty flight back home. . . 
'''
        )


    def ch_9(self): # returning home
        mon_list = self.config_monsters({'frenzy boar':7})
        self.nine_intro()
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.nine_encounter0(), collective=False)
        if player_lives:
            self.nine_victory0()
            self.story_reward()
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
your way back night falls, and the morning approaches without even seeing snout
or long lizardy tail of even one kobold! As the sun rises you feel the need to 
vent all your bottled up worries and fears upon something. Aaaand wouldn't you 
have it a perfectly good herd of frenzy boars stands ready to take it in stride!
'''
        )

    def nine_victory0(self): # Meet Milo and report some ominus news
        dprint(
            f'''
Leaving the battle field behind without a second glance, you make your way to 
town finally arriving just before noon on what you find out to be the 29th of 
Spring meaning you were only gone for 2 full days making that 3 days faster 
than expected. 
You run all the way to the barracks and find Outh out in the yard sparring with 
a boy about your age. As you approach, he notices you and clearly diverts all 
attention from the what his spar as the boy follows through with a strike he 
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
"One more thing Rulid before you go! did you encounter any Kobolds on your way
back, no, on your whole mission?"
Thinking back you are stunned to realize that, no, you have not actually seen a
living kobold since the night Henry was hurt. You report this and the Captain 
responds by saying "Hm, that's very interesting, and a little worrying. No one
has seen a kobold for a few days now. I fear your intel may be the true one and
their big move could be sooner than we would like... Well, good day, see me at 
about mid morning tomorow. I have a bit more training to give this lad here."
finishes the captain with a little extra emfasis ot eh word "training" Milo 
srinks at this comment and automatically apologizes again. To which Captian 
Gruenge chuckles and dismisses the apology and you make your way out of the 
barracks and onto the road back home to see your family. . . 
'''
        )


    def ch_10(self): # wake in flames robin abducted single fight giving chase
        mon_list = self.config_monsters({'kobold soldier':4})
        self.adjust_team('Liliyah', 'add')
        self.adjust_team('Bulli', 'add')
        self.adjust_team('Milo 0', 'add')
        self.adjust_team('Gaffer', 'add')
        self.adjust_team('Holt', 'add')
        self.ten_intro()
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.ten_encounter0(), collective=True)
        if player_lives:
            self.ten_victory0()
            self.story_reward()
            self.adjust_team('Liliyah', 'remove')
            self.adjust_team('Bulli', 'remove')
            self.adjust_team('Milo 0', 'remove')
            self.adjust_team('Gaffer', 'remove')
            self.adjust_team('Holt', 'remove')
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
orange glow of fires luminate your bedroom through you window through which a 
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
slow down! WHEre You gOing . . ?"
Your already bolting full steam ahead after Robin. Moments later, you hear a 
distant voice call again, but not to you this time. 
"Oi! Cap! I think {self.player.name}s on to something again!"
"You two, follow {self.player.grammer['objective']} and help {self.player.grammer['objective']} out! You three stay here!" came the voice of 
Captian Gurenge. 
Another minute later, just moments after you pursue the kobolds outside the 
crumbling Town gates, 2 figures appear dashing astride you, Milo the boy you 
met with the Captian and a woman you've seen but never really met before. A 
member of the guard. As the 3 of you continue to run none speaks a word you all 
just keep running . . . 
'''
        )


    def ch_11(self): # the hunt begins
        mon_list0 = self.config_monsters({'small kobold':1, 'kobold slave':1, 'kobold soldier':2, 'kobold guard':1})
        mon_list1 = self.config_monsters({'small kobold':4, 'kobold slave':2, 'kobold soldier':1})
        mon_list2 = self.config_monsters({'kobold soldier':2, 'kobold slave':1, 'kobold soldier':1, 'small kobold':1, 'kobold soldier':1})
        mon_list3 = self.config_monsters({'kobold soldier':4, 'small kobold':2})
        self.adjust_team('Milo 0', 'add')
        self.adjust_team('Suphia', 'add')
        self.eleven_intro()
        player_lives = self.battle.story(mon_list=mon_list0, dialog=self.eleven_encounter0(), collective=False)
        if player_lives:
            self.eleven_victory0()
            self.adjust_team('Electo', 'add')
            player_lives = self.battle.story(mon_list=mon_list1, dialog=self.eleven_encounter1(), collective=True)
            if player_lives:
                self.eleven_victory1()
                player_lives = self.battle.story(mon_list=mon_list2, dialog=self.eleven_encounter2(), collective=False)
                if player_lives:
                    self.eleven_victory2()
                    self.adjust_team('Milo 0', 'remove')
                    player_lives = self.battle.story(mon_list=mon_list3, dialog=self.eleven_encounter3(), collective=True)
                    if player_lives:
                        self.eleven_victory3()
                        self.adjust_team('Suphia', 'remove')
                        self.adjust_team('Milo 0', 'remove')
                        self.adjust_team('Electo', 'remove')
                        self.story_reward()
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

    def eleven_encounter1(self): # oh boy, another fight ... PSYCHE! lol! Nope!
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
        print('1: attack\n2: special\n3: item\n4: run\n')
        input()
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
... But where are the retreating kobolds? 
As you and Suphia hurry through the night, you strain your senses to detect the
signature movement of kobold captures, but try as you might, neither of you 
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


    def ch_12(self): # alone int he woods pt 1
        mon_list1 = self.config_monsters({'cave slime':2,'swarm of bats':1})
        mon_list2 = self.config_monsters({'refuse':3})
        self.twelve_intro()
        player_lives = self.battle.story(mon_list=mon_list1, dialog=self.twelve_encounter0(), collective=True)
        if player_lives:
            self.twelve_victory0()
            player_lives = self.battle.story(mon_list=mon_list2, dialog=self.twelve_encounter1(), collective=True)
            if player_lives:
                self.twelve_victory1()
                self.story_reward()
                return True
            else:
                return False
        else:
            return False

    def twelve_intro(self): # 
        dprint(
            f'''
A mild glow from the soon to be rising sun casts a red to blue gradiant above 
you to your left. The freezing early wind ruffles your clothing, made more so 
as your run. Your companion Suphia, continues head of you about 50 feet with 
long quick strides. The smell of smoke and terror still lingers in both of your 
minds among far to many things to verbalize. 
In your mind you go over the things you heard and discovered about the kobolds
and their plans, that could have led prevention of this terrible catastrophy. 
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
possibly including greentown, Pompon, Farthe Outpost or maybe villages in the 
farther east like Kyoma or Uten. This combined with the lack of concrete 
evidence and the discovery of contradicting intel at about the same time 
resulted in indecision and crucial time spent strategising and reasoning about
next steps. 
Whether it was a well orcestrated attack strategy, which Suphia pointed out 
was incongruent with the usual kobold nature; or, the work of some human 
traitor or mole, it had worked and the kobolds had, counter to their normal 
behavior, orchestrated a combined attack on Greentown and more than likely, 
several other towns in the area.
There was one other important piece of inteligence that you and at least one 
other source discovered. The kobold called Luxkhanna. That kobold was 
supposedly the leader who orchestrated all this. 
If, and you hated even giving this idea any ground in your mind, but if you 
were never able to find and rescue Rosie and Robin, you did atleast have an 
alternative goal: Find that monster and destroy him. . . 
'''
        )

    def twelve_encounter0(self): # 
        dprint(
            f'''
Your thought as you run turn to grattitude for Kajlo Sohler who taught you to 
use magic to inprove your stamina. You can help but be impressed at Suphia, 
however, as she looks to hardly have broken a sweat. 
'''
        )

    def twelve_victory0(self): #
        dprint(
            f'''

'''
        )

    def twelve_encounter1(self): # 
        dprint(
            f'''

'''
        )

    def twelve_victory1(self): #
        dprint(
            f'''

'''
        )


    def ch_13(self): # alone int he woods pt 2
        mon_list = self.config_monsters({'frenzy boar':7})
        self.thirteen_intro()
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.thirteen_encounter0(), collective=False)
        if player_lives:
            self.thirteen_victory0()
            self.story_reward()
            return True
        else:
            return False

    def thirteen_intro(self): # 
        dprint(
            f'''

'''
        )

    def thirteen_encounter0(self): # 
        dprint(
            f'''

'''
        )

    def thirteen_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_14(self): # alone in the woods pt 3 (found a clue)
        mon_list1 = self.config_monsters({'cave slime':2,'swarm of bats':1})
        mon_list2 = self.config_monsters({'refuse':3})
        self.fourteen_intro()
        player_lives = self.battle.story(mon_list=mon_list1, dialog=self.fourteen_encounter0(), collective=True)
        if player_lives:
            self.fourteen_victory0()
            player_lives = self.battle.story(mon_list=mon_list2, dialog=self.fourteen_encounter1(), collective=True)
            if player_lives:
                self.fourteen_victory1()
                self.story_reward()
                return True
            else:
                return False
        else:
            return False

    def fourteen_intro(self): # 
        dprint(
            f'''

'''
        )

    def fourteen_encounter0(self): # 
        dprint(
            f'''

'''
        )

    def fourteen_victory0(self): #
        dprint(
            f'''

'''
        )

    def fourteen_encounter1(self): # 
        dprint(
            f'''

'''
        )

    def fourteen_victory1(self): #
        dprint(
            f'''

'''
        )


    def ch_15(self):
        pass # following the trail

    def fifteen_intro(self): # 
        dprint(
            f'''

'''
        )

    def fifteen_encounter0(self): # 
        dprint(
            f'''

'''
        )

    def fifteen_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_16(self):
        pass # following the trail pt 2

    def sixteen_intro(self): # 
        dprint(
            f'''

'''
        )

    def sixteen_encounter0(self): # 
        dprint(
            f'''

'''
        )

    def sixteen_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_17(self): # surrounded by nepenths (pre-boss)
        mon_list0 = self.config_monsters({'little nepenth':1, 'barkling':1, 'windwasp':1, 'little nepenth':1})
        mon_list1 = self.config_monsters({'little nepenth':2, 'nepenth':1, 'pod nepenth':1})
        mon_list2 = self.config_monsters({'Pod Nepenth':1, 'flower nepenth':2, 'big nepenth':2, 'nepenth':3, 'little nepenth':4})
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
                    player_lives = self.battle.story(mon_list=mon_list3, dialog=self.seventeen_encounter3(), collective=True)
                    if player_lives:
                        self.seventeen_victory3()
                        player_lives = self.battle.story(mon_list=mon_list4, dialog=self.seventeen_encounter4(), collective=False)
                        if player_lives:
                            self.seventeen_victory4()
                            self.story_reward()
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

    def seventeen_intro(self): # 
        dprint(
            f'''

'''
        )

    def seventeen_encounter0(self): # 
        dprint(
            f'''

'''
        )

    def seventeen_victory0(self): #
        dprint(
            f'''

'''
        )

    def seventeen_encounter1(self): # 
        dprint(
            f'''

'''
        )

    def seventeen_victory1(self): #
        dprint(
            f'''

'''
        )

    def seventeen_encounter2(self): # 
        dprint(
            f'''

'''
        )

    def seventeen_victory2(self): #
        dprint(
            f'''

'''
        )

    def seventeen_encounter3(self): # 
        dprint(
            f'''

'''
        )

    def seventeen_victory3(self): #
        dprint(
            f'''

'''
        )

    def seventeen_encounter4(self): # 
        dprint(
            f'''

'''
        )

    def seventeen_victory4(self): #
        dprint(
            f'''

'''
        )


    def ch_18(self): # scouting the Kosaur's lair
        mon_list = self.config_monsters({'red worm':1, 'shrubent':1})
        self.six_intro()
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.six_encounter0())
        if player_lives:
            self.six_victory0()
            self.story_reward()
            return True
        else:
            return False

    def eighteen_intro(self): # no
        dprint(
            f'''

'''
        )

    def eighteen_encounter0(self): # 
        dprint(
            f'''

'''
        )

    def eighteen_victory0(self): #
        dprint(
            f'''

'''
        )


    def ch_19(self): # Kosaur boss fight
        mon_list = self.config_monsters({'Kosaur (F-Boss)':1})
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

'''
        )

    def nineteen_encounter0(self): # 
        dprint(
            f'''

'''
        )

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

