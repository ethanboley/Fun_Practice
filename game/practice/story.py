
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


    def ch_0(self): # Spring 11th, 3044, 6th age
        mon_list = self.config_monsters({'brown worm':1,'slime':1})
        # mon_list = self.config_monsters({'test_boss':1})
        self.adjust_team('robin_0')
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.zero_encounter(),collective=True) # changed to boss
        if player_lives:
            self.zero_victory()
            self.story_reward()
            self.story_prep(location='1-1')
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
        dprint('bad and soon enough the sun sets completely. Just in time')
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
                self.story_prep(location='1-4', name='To the wall')
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
        self.eighteen_intro()
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.eighteen_encounter0())
        if player_lives:
            self.eighteen_victory0()
            self.story_reward()
            self.story_prep(location='1-7', name='Into the canyon')
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
        self.nineteen_intro()
        player_lives = self.battle.boss(mon_list=mon_list, dialog=self.nineteen_encounter0(), boss_dialog=[self.nineteen_boss0()])
        if player_lives:
            self.nineteen_victory0()
            self.story_reward()
            self.story_prep(location='1-7', name='through the canyon')
            return True
        else:
            return False

    def nineteen_intro(self): # Approach
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
hope that it just never spots you, knowing that those odds were very slim. There
are no trees in this part of the canyon, little undergrowth or large rocks to
hide behind, just you and the wall you hope you can blend into enough. That and
a river you hope can continue to mask your careful steps. 
You are almost level with it before the worst happens, it pauses to sniff the
air and apparently imediately notices something. 
'''
        )

    def nineteen_encounter0(self): # first boss intro! we have to defeat it!
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

    def nineteen_boss0(self): # boss dialog test
        dprint(
            f'''
The towering monster reels back in pain, deep wounds from your blade etched
into its stony hide forever. But it isn't over. As it regains its composure,
you see a new flame ignite in its forward facing eyes. You are no longer prey.
Now it just wants you dead. Thinking this is your chance to make your escape,
you dart back along the wall of the canyon, but a deranged look flashes across
the Monster's eyes and it launches after you again!
'''
        )

    def nineteen_victory0(self): # Thanks editor
        dprint(
            f'''
You stagger back, gasping for air, your heart pounding in your chest like a war
drum. The canyon walls loom around you, trapping the sound of your labored
breaths. Before you, the Monster a hulking, dinosaur that seemed indomitable—
collapses to the ground like a toppeling of a great stone tower. Its massive,
reptilian body lies still on the canyon floor and across the river, large
enough to dam the river running through it. You can hardly believe it.
For what feels like an eternity, you just stand there, blood-soaked and
trembling, the sword in your hand hanging by the last thread of strength you
didn't know you still had. Your arms ache from the weight of every swing,
every desperate attempt to fend off its crushing jaws. You didn't come here to
fight this thing, you didn't want to, but it left you no choice.
You were trying to escape, to just get past it, but this monster, this...
Kosaur, as you call it because of its crossed apearance of a Kobold and a
dinosaur, was relentless. No matter how fast you ran, how cleverly you dodged,
it was always there, forcing you back into battle. Every roar, every lunge,
made you feel like you were one mistake away from death. And yet, against the
odds, here you were, standing over its broken form.
In the stillness that follows the battle, the canyon seems eerily quiet, as
though even the wind itself is holding its breath. You can hear the faint echo
of your ragged breathing, but nothing else. No more monstrous growls. No more
thundering footsteps.
With what little strength you have left, you drag yourself back to the rocky
walls, pressing your back against them for support. Your legs feel like they
might give out at any moment, but for now, you have a chance to catch your
breath. The path ahead lies open now, clear of the terror that stood in your
way. The thought of your siblings, of Luxkhanna's camp just beyond the next
ridge, flickers in your mind.
You aren't done yet.
For now, for this brief moment, you allow yourself to breathe. You allow
yourself to feel the small, hollow victory of survival. Because despite
everything that's been taken from you, despite the loss of Suphia, your abducted
siblings and doubtlessly countless others, despite the exhaustion clawing at
your bones—you're still here.
With a job still to do.
'''
        )


    def ch_20(self): # kosaur boss recovery; Spring 35th-42nd, 3044, 6th age
        mon_list0 = self.config_monsters({'red worm':1, 'silverfish':1, 'borogrove':1})
        mon_list1 = self.config_monsters({'bryllyg':1, 'jackelope':1, 'sly shrewman':1})
        mon_list2 = self.config_monsters({'marzeedote':3})
        self.twenty_intro()
        player_lives = self.battle.story(mon_list=mon_list0, dialog=self.twenty_encounter0(), collective=False)
        if player_lives:
            self.twenty_victory0()
            player_lives = self.battle.story(mon_list=mon_list1, dialog=self.twenty_encounter1(), collective=False)
            if player_lives:
                self.twenty_victory1()
                player_lives = self.battle.story(mon_list=mon_list2, dialog=self.twenty_encounter2(), collective=False)
                if player_lives:
                    self.twenty_victory2()
                    self.story_reward()
                    self.story_prep(location='1-8', name='continue')
                    return True
                else: 
                    return False
            else:
                return False
        else:
            return False

    def twenty_intro(self): # word spreads fast
        dprint(
            f'''
Whether it was the birds or the winds themselves, over the next few days, word
seems to spread throughout the wilderness that the Scourge of the Kobold Canyon
is no more. At first it was a surprise to you to see life hopping among
the trees near by. But soon after another, and another, it became quite clear
that the Kosaur had occupied a major choke point in the wilderness that was
clearly disturbing the natural ballance of the area.
'''
        )

    def twenty_encounter0(self): # slowing down
        dprint(
            f'''
By now, at the close of the fourth day following your defeat of the Kosaur, 
Monsters and beasts of all kinds were veritably swarming through the canyon in
both directions causing your pace to slow significantly. It became necessary to
find hard to reach nooks, hollows, caves and shelves along the confining canyon
to set up each camp for the night. Tonight you think you've found just one such
perfect place inside a large cavity obscured in part by a steady trickling of
mountain run-off. 
Unsurprisingly, you are forced to clear out your competitors first.
'''
        )

    def twenty_victory0(self): # purpose
        dprint(
            f'''
Upon settling in for the night, you doze quickly, more force of habbit now than
anything and you dream restlessly of dark towers and deep caves; of monsters
and unnamed creatures of the depths. None of these frighten you much like they
did not long ago, what scares you is their threat to your comfort and
livelihood as well as the lives of those you loved and cared for. 
You wish none of this had ever happened and you wanted to find whoever made
these things so and at the very least ask them why before teaching them all the
lessons you have been forced to learn thus far.
'''
        )

    def twenty_encounter1(self): # aw man 2wice in a row!
        dprint(
            '''
Your thoughts are interrupted, as you are woken with a sharp pain in your
abdomen. For the second night in a row, you are found and attacked by night-
crawling monsters.
'''
        )
    
    def twenty_victory1(self): # another day another fight
        dprint(
            '''
You manage to get some rest after the fight but what seems far too soon, you're
again woken by the morning light and the sound of motion nearby.
Momentarily, you find yourself back out in the canyon sneeking after what might
be your breakfast in a small herd of wild boars.
'''
        )

    def twenty_encounter2(self): # MARZEDOTES! HAHA!
        dprint(
            '''
Just then a herd of something else charges in from the opposite direction,
scattering the boars and at least a few coming after your hiding place. You
recognize these beasts, though you've never seen one before. They looked like
large fat zebras without front legs and talons instead of hooves. 
Marzeedotes.
Having only heard stories of these creatures, you didn't know what to expect,
but you ready yourself for the fight anyway.
'''
        )
    
    def twenty_victory2(self): # oh shoot thats not good
        dprint(
            '''
Now, finding the area cleared of monsters and beasts, you move on again as
slowly as ever, frustrated to think that at this rate, you may still find
yourself in this canyon for another three or even four days more. 
You try to pick up the pace but each time you do without fail, another fight
takes place and you simply cannot affort to continue exhasting your energy like
this especially considering your sleep schedule, which, for the fifth night in
a row yields little true rest. 
On the evening of the seventh day, you are stirred from your approaching
slumber yet again, this time not by mindless monsters or wild animals but by
the sounds of distant raised voices in the midst of what sounded like a battle.
The voices sounded like that of kobolds but there was something else mixed in
with the high grating kobold tones. Something deeper, almost human. 
Eager for the first asurances of being on the right path for the first time in
what feels now like weeks, you slide out of your hole and sneek your way closer
to the fray a good 500 feet farther down the canyon. Once there, you see the
group. They appear to have just won a battle against a couple wargs, a fight
you're glad you didn't have yourself.
To your surprise, though, you see only kobolds. And then you remember, the
giant kobolds from before. What you thought sounded almost like human speech
was actualy just them.
Another surprise, they were speaking common and with little accent. Counting
your fortunes, and making sure to stay hidden, you listen.
"Yeah, I think the capper was right. There are too many of these little
bleeders suddenly comin out o'th'mountains." spoke one of the big ones. 
"Yeah! I thik, we bay dot fide Belby wer we left it!" whinned on of the regular
kobolds in the back who apparantly had a bloody nose or something.
"Ah shut up!" bellowed the first, "Don't you go round takin credit for things
we Ruin Kobolds do for yeh little runts! Ehh if I had my way, I'd see you all-"
"Enough," interrupted an even deeper voiced Ruin Kobold just behind, "Be
careful what you say. If Luxkhanna hears you said some like that..."
"Mhhhh, well still,"
*smack* 
*eep*
"Know your place runt!"
They began to move again. You shrank deeper into the shadows of the bushes,
sure to stay out of sight.
"You may have a point though, I doubted ol' Kluffoot when he was thinkin that
Belby had run off or even died but this is just gettin ludicr-what was that?"
You heard it too, it sounded like a small boulder had been pushed over the
opposite cliff edge and shattered against the canyon floor. 
Moments later, there came another, and then another. 
"There! Goblins!" shouted the last Ruin kobold in the very back of the group. 
With their recognization, there came from the goblins several high screeches
from atop the cliff and several dozen small but lanky dark masses began
scuttling straight down the vertical cliff edge towards the bottom each
accompanied by a pair of radiant green beads if light for their eyes.
The high cackling and screaching of the goblins filled the canyon, echoing from
edge to edge. 
You back slowly, from the scene, knowing that by this point, most sounds you
make will be drowned in the cocophony but also fully aware that everything in
the area, except for you, can see clearly in the dark.
*bong*
All goes black.
'''
        )


    def ch_21(self): # following the trail pt 3, Spring 44th, 3044, 6th age, variant chapter.
        mon_list0 = self.config_monsters({'kobold chief':1, 'ruin kobold trooper':1, 'ruin kobold':1, 'condemned goblin':1})
        mon_list1 = self.config_monsters({'goblin':3})
        mon_list2 = self.config_monsters({'goblin king':1})
        self.twenty_intro()
        player_lives = self.battle.story(mon_list=mon_list0, dialog=self.twenty_encounter0(), collective=False)
        if player_lives:
            self.twenty_victory0()
            player_lives = self.battle.story(mon_list=mon_list1, dialog=self.twenty_encounter1(), collective=False)
            if player_lives:
                alt = self.twenty_victory1()
                if alt == None:
                    pass
                else:
                    return False
                player_lives = self.battle.story(mon_list=mon_list2, dialog=self.twenty_encounter2(), collective=False)
                if player_lives:
                    self.twenty_victory2()
                    self.story_reward()
                    self.story_prep(location='1-8', name='escape')
                    return True
                else: 
                    return False
            else:
                return False
        else:
            return False

    def twenty_one_intro(self): # can you believe it... this is the short one
        self.player.inventory.contents.clear()
        dprint(
            f'''
You wake. The first thing you notice are the lights of a strange combination of
fire and liminant stone casting yellows and greens simultaneously across the
scene. The second thing you notice is a dull pain in the top of you're head,
you were clearly hit hard in the head by something. Then you remember. There
were goblins coming into the canyon. You were about to make your escape but
then you must have recieved a well coordinated sneakstrike because thats all
you remember and now you're here. You make to stand and quickly make your third
observation. Your elbow now hurts just as badly as your head. You were bound
and so your attempt to stand resulted in a sort of wobble and flop ending in
most of your body weight landing onto your now very bruised elbow.
Biting your gag hard out of pain, you, observe more of your surroundings. You
see that you're in a sort of giant basket woven out of reeds and carved tree
branches suspended above, well, nothing as far down as you could see through
the bottom of your prison, you could not make out any bottom. You are relieved
as you look up to see rather sturdy by comparison supports holding you to the
ceiling.
A few moments pass before you make another, more careful attempt to stand,
sliding upwards along the side of your box. Upon doing so, you make your next
observation. There was a goblin nearby, sleeping hither to your motion to stand,
who started awake and scurried off without hessitation. 
Another minute or so passes in silence during which time, you look around and
struggle at your bindings managing only to minorly loosen your wrists before
you hear the sounds of goblins approaching from the apparent only entrance. 
Moments later, you find your cage being opened by the front of five goblins
including the one who had left. 
After a few moments, the surprisingly strong goblins for their size, begin
literally dragging your bound form through the stone halls requiring great
effort not to aggrivate your sore skull. After what seems like miles, the
procession comes to a halt and your gag as well as several other binding are
roughly removed leaving only your wrists and ankles. Before you can do anything
however, you captures lean your body over the edge of a dark pit supported by
nothing but your wrist bindings.
You know your protests will not be heard or even understood by the goblins but
you make known your discomfort either way. Sure enough, the goblins just laugh
at what they hear to be simply worried jibberish before cutting the line. . . 
'''
        )

    def twenty_one_encounter0(self): # A very strategic battle
        dprint(
            f'''
Fortunately the fall is not as far as you thought, only about twenty feet but
still, with your legs still bound, it became very difficult to avoid damage
alltogether. As you scramble to losen your sore ankles, a portion of the far
wall seems to dizolve away revealing a stone passageway beyond. With the
opening of the passageway comes the unmistakable cocophony of an excited goblin
crowd. 
Your bindings come loose well enough and your feet appear uninjured enough to
function properly. With that in mind and no other place to go. You make your
way steadily into what is surely some kind of arena. You are unarmed and
underprepared, but you know you have to survive. Step after step, the sound
grows louder until a light reaches your eyes beyond one final bend and you see
the space before you.
the arena is small and circular only about thirty or fourty feet across with
openings similar to yours every several feet. As you enter the space, the
volume of the goblin crowd increases drastically mixed with jeers, laughs,
excited screeches and the like. 
You appear to be the first party through their entrance and only wonder for a
second or two what else might be coming before you begin scanning every inch of
you perception for an escape. 
The arena walls are little less than 20 feet tall ending in an iron railing and
the packed stands which rise in steep tiers before finally coming to open
stone passageways through which more goblins continue to come and go. The
ceiling appears to be domed begining at about this point and from the ceiling
hangs all the lighting for the chamber consisting of those green luminus
stones. 
Before you can scan much more of the area, another two participants enter from
opposite entrances about five seconds appart from each other. Through the door
on your left, enters three of the very same ruin kobolds you had see before you
were knocked out (however long ago that was). From the right entrance staggers
a single goblin quvering and cowering under the jeers and glares of it peers
clearly under some kind of punishment.
You and the other groups stare each other down for a few moments before several
things happen. Iron portcullises materialize where each entrance was moments
ago, another aperition at the center of the arena takes the form of a large
wooden stand fully equipped with crude, goblin craft weapons of all sorts.
Finally, the briefest thought crosses your mind that if none of the combatants
ever grab the weapons no one needed to get hurt and you could all try to
escape. Well, it really was a short lived thought because as soon as you
thought this, both the goblin and the Kobolds made an instant break for the
center weapons, leaving you in the dust and with a severe dissadvantage. 
"Of course savages like kobolds and goblins woudn't think not to fight at the
closest opportunity!" you think to yourself as you try to catch up. And now
because of that moment's hessitation, your life really could be much more on
the line than it already was.
Before you can get anywhere close to the weapon stand, the kobolds appear to
get there first grabbing weapons and slashing at the goblin and throwing the
entire stand closer to their side of the arena giving them a massive advantage
in both strength and numbers. The spectating goblins howl their approval at
this one sided start to the battle.
The goblin proves to exceed the kobolds in agility, however, as it quickly
after dives past the defending ruin kobolds and just manages to snatch a
viscious looking sickle from the scattered weapons. 
Now it you were the only one unarmed. 
"Tag e lum, ee pikik sha fah ou!" barks the largest of the ruin kobolds clearly
having abandoned their common tongue for the time being. But it doesn't matter,
the message is clear as the other two imediately turn towards you grinning
menacingly and brandishing their weapons while the one that spoke engages the
goblin. 
You back slowly away back the way you came and a bit along the wall edging
slightly closer towards the koblds section. You know agility and more often
than not speed wise the kobolds have humans beat but if you can just catch them
off guard with something, you might be able to snatch a weapon, and then you'll
be in business. 
Before you have time to edge much closer, the kobolds leap at you, full speed
ahead, weapons forward.
First things first, you need more to work with. You leap backwards and scan the
area for anything. It was only a matter of time before the kobolds caught you
and there was only a tiny chance you would be able to slip past them unscathed.
With your mind in overdrive, your eyes fall upon the dueling pair across the
arena and an idea strikes you. 
Peeling off your course you make bee line for the battle. Unfortunately, your
change of course comes too close to one of the ruin kobolds who slashed you
across the back just within reach.
'''
        )
        self.player.hp -= 4 if self.player.hp > 10 else 2
        display_health(self.player)
        dprint(
            '''
You continue forward through the pain having learned your lesson not to let
something distract you in battle. 
Within a few strides of the goblin, the kobold battling it sees you and lunges
causing the goblin to leap back and to the side placing you within its line of
sight as well. But a sneak attack wasn't your goal (allthough now that you
think about it that may also have been a good plan). The goblin turns to defend
itself from you and you dive to the side rolling behind it again but only after
splaying your clearly unarmed hands int he goblin's view.
It worked! The goblin was now completely surrounded, its original opponent, on
one side and the other two kobolds beside him while you were behind. And now
with the goblin aware that you were unarmed and therefore less of a threat, it
did not turn back towards you but stayed essentially defending you from the
kobolds for the time being.
Now for the second part of your plan. 
Focusing your attention on the kobold leader, you reach out your arms wide as
if to say "is that all you got?" and at the exact same moment edging around the
back of the goblin just enough so that all 3 kobolds and yourself were closer
to one side of the goblin. 
Edging this close earned you another swipe but it was worth the risk for the
result. 
'''
        )
        self.player.hp -= 4 if self.player.hp > 10 else 2
        display_health(self.player)
        dprint(
            '''
Your two kobold attackers and the taunted leader all bolt to one side
of the goblin, the side closest to you. Upon seeiing this, you dash around the
goblin at equal speed but not for long and you now finally have a perfect
unobstructed path straight for the weapons.
"AAAAAHHHHG, EOG YIE!" bellows the leader. 
As you make a break for the thrown weapon stand the mildly relieved goblin
takes a hearty swing at one of the other kobolds who turns to defend. It was
just enough. Sliding in low, feet first just out of reach of the gaining
kobold, you grip the unwrapped hilt of a short, crude, iron scimitar and rise
to your feet finally ready to fight. 
'''
        )

    def twenty_one_victory0(self): # Zoo goers' worst nightmare
        dprint(
            f'''
Two kobolds lie dead in pools of orange blood, the goblin also leans against
the far wall not dead but injured beyond continuing. The last ones left
standing are you and the kobold leader who also seems to be on his last leg
none the less. Your blades collide but this time it feel diffenent. Your sword
seems to have hit its last leg too and it snaps right at the point of impact.
'''
        )
        self.player.hp -= 2 if self.player.hp > 10 else 1
        display_health(self.player)
        dprint(
            '''
The bleeding ruin kobold stands over your collapsed body with a mixture of rage
and satisfaction written across his face. You're by mo means unscathed but you,
unlike the kobold, have strength to spare. Employing a move briefly taught you
by Suphia, you sweep your heel across the kobolds ankles causing it not quite
to fall but to reel just enough for you to get grab the only thing you can
nearest to you, a line of rope.
The kobold takes another swing now nothing but wrath on his face. The blade
slices the end of rope you haphazardly threw his way while you crawl backwards
away from your enemy.
The momentary distraction bought you enought time to gain some ground and stand
again on your feet. Your opponent charges after you again with a furious war
cry. You scoop up a wooden shield along with your broken scimitar from the pile
before turning to take the full force of the enranged ruin kobold leader.
You leap vertically towards him with all the strength you can muster and as the
kobold swings with what is surely all of his own, you reorient the shield to be
directly between the kobolds blade and your feet. The kobolds considerable
strength combined with your own blasts you upward. You leave the shield far
below you and allow your body a half rotation and your feet to make contact
with the upper half of the arena walls. One step, a jump and a full body
extention, throwing with all your might is all you need to whip one end of the
rope around the railing at the bottom of the goblin stands. You know you only
have a split second before the nearest goblin cuts the line and even less time
before the simple lash comes loose but a fraction of a second is all you need
yank the line and bring yourself within arms reach of the railing. A surprised
goblin spectator draws a dagger and makes a swipe at your hand as soon as you
do so, but that was why you took the risk of re-aquiring your broken blade. You
bring your opposite arm forward and block the swing just in time. 
The expression on the goblins face instantly changes from surprised and gleeful
to one of utmost terror as you pull yourself up, over the railing, out of the
arena and into the midst of the scattering goblin spectators. 
'''
        )

    def twenty_one_encounter1(self): # yikes a fight with a broken sword, weakened=True
        dprint(
            '''
One final glace backwards reveals the kobold who aided your escape lying on its
back staring emotionlessly at the distant ceiling. With you full attention on
the pandemonium before you, your next objective becomes apparent. The best
thing you've got to defend yourself is half of a crude old goblin scimitar. As
a few goblins approach you to detain you again, You know this is going to be a
tough fight. 
'''
        )
        self.player.weakened = True

    def twenty_one_victory1(self): # this..this is the long one, a little of everything, return
        self.player.weakened = False
        prompts = ('"And why on earth would I choose all them?!"',
                   '"Is that supposed to be a fair choice?!"',
                   '"I\'ll fight you!"',
                   '"I\'ll fight everyone else!"',
                   '"Neither!"')
        dprint(
            '''
You've managed to stay strong through the battle and now at victory, you slide
the best looking sword out from one of your fallen goblins hands. The fight
isn't over yet. Even though you see the stands mostly cleared out by now, you
know more powerful goblins are surely on their way.
You run to and up the stairs towards the nearest exit three at a time and enter
the hallway. The path before you is clear but that doesn't help, in fact it
would almost be better at this time to get a feel for directions based on the
flow of goblin traffic through these now deserted passages.
So, you wend your way blindly, only aware of up and down as the winding,
twisting, labyrinthine tunnels continue onward. Your best bet, you reason, is
upwards towards what might be the surface from here. So you naturally stick to
the right path unless one path very clearly heads farther upwards for longer
in which case you go that way. After a while you realize another thing you are
surprised to wish you had more of; dead ends. The tunnels rarely ever come to a
full stop continually criss-crossing and connecting to small or larger chamber
each with varying light levels, purposes and decor. Along your way you see
several goblins but each time you do they are always in the very act of ducking
out if sight or dissapearing in some other way. Its almost eery how adept they
appear to be at simply vanishing on the spot. That is, until you realize that
these goblins were likely born and raised in these tunnels and know them by
heart.
After nearly ten minutes of this, you get the sense they might just be watching
you and laughing as you go in odd loops through what they might see as simple
corridors. It was maddening imagining this going on forever, endless loops,
pits, schutes, slides, chambers, and rooms. 
You needed to stop. 
You needed a breather. Just some time to think and get your bearings right.
*skitter*
You jerk your head to look behind you and see nothing. They're definitely out
there, watching you. but now you needed to think and maybe exactly one goblin
to ask directions. You're pretty sure you haven't seen anything twice so far so
you're somewhat confident you haven't been going in circles, but you don't have
a clue if you've been making any meaningful progress either. 
*shuffle*
You pause for another unfruitful glance behind you. 
The passages have looked about the same the whole time with only little
variation in decor and chizel paterns. Maybe you just needed to abandon your
right path method and just go as straight as possible. But really, who knew how
far into this mountain the goblins mined. You may starve to death before you
find its end. 
*chatter*
. . .
Really what you needed was company. Anything that might know these halls better
than you did. And you knew they were nearby. 
You sit downm, cross-legged and close your eyes. Listening for the goblins
around you. 
*jitter* *chuckle* *tap tap tap* *shuffle*
Farther, farther, you needed to hear deeper into the endless caverns.
*chatter* *tromp* *tromp*
Through the halls you hear the sound of something heavier than a goblin, or
maybe, yes it sounded like a bunch of goblins heading towards you. 
Monents later, you realize that you don't even have to try very hard to hear
this new heavy sound. You open your eyes and imediately see the faint but
growing light of torches around two of the corners available to you.
You wanted company but not this many! 
You know that hiding here would be futile and so you make a brea for the third
exit. The only one without approaching kobolds. The the next fork you see the
light coming from all but one path yet again. 
You count it fortunate that this is also the case at the next two forks but by
the third you realize the odds of this happening this many times to be greater
than coincidental. The goblins were leading you somewhere. They were backing
you into corners knowing that you wouldn't be foolhardy enough to fight all of
them at once.
Bend after bend, fork after fork, chamber after chamber, this continues at
varying paces for a few minutes before finally, the tunnel opens into a huge
dark cavern. A cliff about twenty0 feet in prevents you from fleeing any
further and you watch as the hoard files in behind you. Their bright green eyes
shining in their torch light. After a few moments, about 500 goblins stand upon
this same cliff edge with you keeping about three paces back, just staring.
And then, one of the goblins at the edge hurls his torch into the abyss. The
torch is caught by a hither to unseen hand at the other side of what you
quickly deduce are mirroring cliff faces. The caught torch is lowered to a
trough along the ground and the entire cavern is imediately iluminated by fire.
In the light of the flames you see on the the other side of the cavern, a
carven throne and a huge armored goblin sitting thereon with an unmistakable
grin upon his face. 
"You've caused quite a ruckus, little lum!" says the king in perfect common.
"There have not been many who have escaped an arena of ours. You must be
powerful! I desire to see your full strength for myself but unfortunately,
you're belongings have already been melted down." At this moment the king turns
to one of the even larger goblins to either side of him and speaks some command
in gobbldeeguk. The goblin nods and sprints off at top speed while the kind
gets off his throne and speaks again, adressing you.
"This does not stay my desire, however," and as he nears the edge of the chasm,
he hurls a drawn blade across to you. It was a two edged, straight, shorsword
just like the one you carried before arriving here. Still crude and clearly
goblin made but it was still clean and sharp and the goblin crowd behind you
backs away another pace upon seeing it.
"This should do in the stead of your own blade... Now, I give you a choice,
fight all of my citezens with you right now, or, fight me!"
The goblins around you began to slowly shuffle backwards and some in the back
begin to panic as gates just like the portcullises in the arena materialize at
each of the exits.
'''
        )
        option = basic_player_prompt(prompts)
        if option == 1:
            dprint(
                '''
"Ah, of course, you wouldn't know! We goblins elect kings based on thier
strength and skill in battle over all else. It would not be much of a threat to
me if I fought all my subjects here right now. And I suppose I may have just
swayed you in your desicion in saying that so I'll make it easy for you and
choose option two in your stead."
Several things happen at once. The portcullised vanish, the goblins begin to
scatter, and the king, after winding up a bit, takes a running jump easily
thirty feet across the entire chasm, landing ontop of one of his subjects,
killing it.
He stands and pulls his hammer from his back and straightens up revealing that
he was about your height, huge for a goblin.
'''
            )
        elif option == 2:
            dprint(
                '''
The king pauses, briefly, grin even wider and chuckles before answering.
"Yes it is."
"Allow me to show you!"
The king takes a few steps back before drawing his hammer from his back and
leaping clear across the chasm right on top of one of his subjects which dies
instantly. 
'''
            )
        elif option == 3:
            dprint(
                '''
"I was hoping you'd say that!" 
The king takes a few steps back before drawing his hammer from his back and
leaping clear across the chasm right on top of one of his subjects which dies
instantly.
'''
            )
        elif option == 4:
            dprint(
                '''
"Hmm, interesting choice, still, You probably have a higher chance of surviving
with that choice."
The king sounds quite put out at your dicision but withdraws back to his throne
none the less.
After doing this he waves his hand dismissively and several hundred goblins
move in to attack all at once.
Not many are armed with more than little daggers but their sheer numbers grow
almost imediately too great to defend against. You manage to swing at a few but
its like throwing a hankerchief into a bucket of water.
'''
            )
            self.player.hp -= 2
            display_health(self.player)
            self.player.hp -= 1
            display_health(self.player)
            dprint(
                '''
More and more swarm your increasingly helpless form, the jeers and cackles of a
whole goblin civilization ringing in your ears
'''
            )
            for _ in range(5):
                if self.player.hp > 0:
                    self.player.hp -= random.randint(1, 2)
                    display_health(self.player)
            dprint(
                '''
Through tiny gaps in the swarm and the blood in your eyes, you see the sad face
of the gobblin king watching your distruction.
'''
            )
            for _ in range(12):
                if self.player.hp > 0:
                    self.player.hp -= random.randint(1, 3)
                    display_health(self.player)
            dprint(
                '''
Your sword falls somewhere into the crowd as blades and fangs dig into your
flesh. With the last bits of strength you posess, you bear your final apology
to your mother, your siblings, and the others who were counting on you to bring
justice to their enemies and salvation from further harm at their hands.
'''
            )
            for _ in range(9):
                if self.player.hp > 0:
                    self.player.hp -= random.randint(1, 2)
                    display_health(self.player)
            dprint(
                '''
As your mind drifts away and your vision begins to fade, so does the pain,
replaced only with regret and hope that someone greater and stronger than
yourself can finish what you started.
'''
            )
            for _ in range(15):
                if self.player.hp > 0:
                    self.player.hp -= random.randint(1, 4)
                    display_health(self.player)
            dprint(
                '''
Your life was over, you knew it and there was nothing you could do about it.
No clever trick or quick thinking could help you escape. Your final thought
before your mind vanished forever is of your life before the kobolds flipped it
upside-down. You were greatful at least that you were able to enjoy life even
if just for a little while.
'''
            )
            while self.player.hp > 0:
                self.player.hp -= 5
                display_health(self.player)
            return False
        else:
            dprint(
                '''
"Wrong answer!" Chuckled the king grinning wider than ever.
"ROBGOC!" he bellowed.
For the briefest moment you look up to see a huge iron something fall from the
ceiling dropped by the servant he ordered earlier. 
The next moment, you were dead.
'''
            )
            return False
    
    def twenty_one_encounter2(self): # no way just 4 lines!
        dprint(
            '''
"I trust you will give me a good fight?" said the king of the goblins as he
takes a step towards you and the remaining goblins clear the area. 
"I can't say you'll survive, but I may spare you if you can manage to do some
decent damage to me. I'll be able to keep you as a training slave!"
'''
        )

    def twenty_one_victory2(self): # YOU'LL NEVER CATCh me ali...
        dprint(
            '''
"Alright, fine, thats enough! You have proven yourself useful to me. I have
always been interested in the way you lum fight. That being one of the reasons
I do not command my people to come down among your people and destroy them...
PETOH, BOH, ki shagdash glim aiguka!"
The two large guards of the king were back, having seemingly been ordered to
help the king subdue you again.
They charge in quickly and you defend yourself to the best of your ability, but
not long after, you have your back against the edge of the chasm. Petoh, the
one clesest to you tries to thrust a torch into your face. You manage to knock
it out of his grip but loose your sword down the chasm as well. 
With one eye on your enemies, you see out of your pereipheral vision, the light
of the torch hit a fair sized lip less than sixty feet down before dropping out
of sight. 
You could survive 60 feet. If you had some level of cushioning...
In a split second decision, you duck down narrowly avoiding the king's hammer
and wrap both arms around the goblin Boh, before arching backwards sending both
you and he over the chasm's edge. 
Seconds later you hear a sickening crunch directly below you and you brace
for impact. . . 
'''
        )


    def ch_22(self): # following the trail pt 4, Spring 45th-47th, 3044, 6th age
        mon_list0 = self.config_monsters({'shinigami':1})
        mon_list1 = self.config_monsters({'large cave slime':3})
        mon_list2 = self.config_monsters({'bark golem':1})
        self.twenty_intro()
        player_lives = self.battle.story(mon_list=mon_list0, dialog=self.twenty_encounter0(), collective=False)
        if player_lives:
            self.twenty_victory0()
            player_lives = self.battle.story(mon_list=mon_list1, dialog=self.twenty_encounter1(), collective=True)
            if player_lives:
                self.twenty_victory1()
                player_lives = self.battle.story(mon_list=mon_list2, dialog=self.twenty_encounter2(), collective=False)
                if player_lives:
                    self.twenty_victory2()
                    self.story_reward()
                    self.story_prep(location='1-9', name='to the camp')
                    return True
                else: 
                    return False
            else:
                return False
        else:
            return False

    def twenty_two_intro(self): # recolection 1
        dprint(
            f'''
*slam*
Something broke, your sure of it. Everything hurts. The wind is knocked clean
out of you. But you're alive. 
Whats more, from this point you can see that the chasm begins to slope slightly
forward, its not a lot but it may be enough to get farther out of the king and
other goblin's reach. Your main priority right now is survival and the only way
that is assured is getting away from the goblins. 
As the king screams after you, and life and energy begins to reenter your body,
you drag the crushed form of Boh and slide over the edge hoping and praying
that the chasm would lead you somewhere with a soft landing and maybe from
there, an escape and not just a dead end and certain death.
You slide and drop deeper and deeper picking up speed you wish you had more
control over. The rough, sometines jagged stone tears at your prison rags. The
goblin you took with you has fallen far out of sight but before long, the chasm
begins to level off and thin. In the pitch blackness you begin sliding slower
and slower hitting foreign objects the subjects of likely centuries of
discarded goblin things and likely goblins themselves too. After another minute
of sliding, you are able to apply the breaks enough to be sure you won't take
any significant damage. A the same time the width of the chasm is reduced to
only a few feet wide and enclosing. 
Finally, applying most of your remaining strength, you manage to brace your
legs between what has now become the ceiling and the floor and you skid to a
stop. 
It's pitch black. Your eyes are not adjusting at all, but you really don't need
them to. You know what you would see if they did. Without further hessitation
you again begin sliding, much more controlled now, farther down the chasm.
Every so often, when you hit a particularly easy spot to traverse, you move
horrizontally closer to the unseen edge of the chasm. You have no idea how deep
you are into the depths of the earth but you know even after that cave what
seemes like years ago now, that this is the farthest down you've ever been. 
Minutes, hours, maybe even days pass going deeper and deeper under the
mountain, when, during one of your rare horrizontal movements, your hand meets
a wall. You reach around briefly to be sure that you had found the edge and
notice a general inward slope in the edge wall. 
By this point the floor and ceiling were less than two feet appart on average
and even tighter near the edge. While sticking to this side, its generous slope
allows you to almost walk downwards. 
Another long while passes of this when your forward foot hits nothing but thin
air. It takes a lot of effort not to resume your wild careening down the chasm
and stay steady on the admitedly less than solid ground. It takes you what
seems like thirty minutes to figure out where the ground went. When you do
you heart leaps. Feeling in the darkness you feel a clearly abnormal hole in the
wall where you had been sliding. The hole quickly turnes into a tunnel and that
tunnel quickly becomes more and more likely to be artificial. It was a much more
controlled slope that spirals slowly downward in loose loops. 
Eventually, the tunnel opened into a small, flat cavern and you saw a faint
light for the first time since the goblins' lights. The light was bright and
purple, a glow emenating from another off-shooting tunnel.
As you approach the light, you feel a strange energy radiating from the
entrance. Inside the tunnel the light becomes noticeably brighter and you hear
a soft hum, like a thousand birds flapping their wings but quiet and distant. 
You round the corner and see the source of the light. It was a large circular
pool of unknown depth filled with a thick, opaque, bright purple, radiant
liquid which churned and frothed unprompted in circular patterns around the
pool. At the very center of the pool was a massive inverted pyramid with five
sides which connected to the ceiling and decended to less than an inch above
the surface. The closer the pyramid grew to the pool's surface, the more it
radiated with the same bright purple hue as the stirring liquid and the more
thick vein-like structures of this same color and radiance seemed to grow and
twist around its sides.
The sight was turely mezmorizing and before you knew it you found yourself
crouching down at the edge of the pool admiring its contents. You realize this
liquid may be dangerous and so you edge away but you can help your curiosity.
You grab a convenient pebble, back to the exit incase the worst should happen
and toss it in. 
Nothing happens. Infact less than what you expected from a liquid happens. The
pebble simply vanishes out of sight without any evidence either audibly or
visually of disturbing the substance in any way. 
You cast your eyes around for a larger stone and unable to find any, you
briefly exit the chamber to find one from outside.
You return and cast in the larger stone. 
Again, nothing happens, the liquid is not disturbed in any way. Less even than
a gas. You don't even hear the stone hit the bottom. . . 
It coundn't just be an illusion, could it? you ask yourself, staring into its
swirling surface. 
You tear off a small peice of your goblin shoe and dangle it inches above the
surface. You release, and, just like the inorganic material, nothing happens.
There's a good chance its safe then, right? You reason. Surely your tests have
proven so. 
Should anything happen, you crouch low and far from the pool's edge and reach
just a pinky forward towards the liquid.
less than an inch away. You feel the distant hum, more inside you than around
you. You take two deep breaths and, as lightly and minimally as possible, tap
the surface.
'''
        )
        input()
        dprint(
            f'''
Everything goes dark. Tangibly thick smoke swirls around you. You jerk your arm
back, having still felt nothing. You feel an odd shifting, like gravity tilting
the wrong ways and then... The smoke, the cave, everything vanishes and reforms
with a powerful rushing sound.
But you're no longer where you were before. No longer crouching in some deep
cave. You find yourself somewhere equally dark but somewhere that feels much
more wide and open, outdoors maybe but theres no sun here nor stars or moon,
just a soft dry breeze and dark shapes in the distance like crumbling mountains
of obsidian. 
You try to stand but recieve no respose. You have no control over your body.
Your head turns on its own, your eyes blink on their own, you feel hair
slightly longer than your own cover your forehead, you feel sore in all the
wrong places. You feel clothing you did not have moments ago. 
You are experiencing someone elses reality.
The sounds of dust and silt sliding across stone in the breeze is interrupted
by a soft but clear grunt made by the stone to your left. Last you knew, stones
didn't grunt. Your heart rate spikes, finally something you feel would have
happened to your own body. Your head turns just the slightest degree in the
direction of the stone.
"H-Hello?" came your voice. It was quiet, high-pitched and tmid, but clear,
like a child, inocent and scared, but confident.
You see what you thought was a boulder visibly freeze confirming your suspicion
but a new sound meets your ears at your voice.
*eep*
It appeared, that both of the masses on either side of you were living
creatures.
'''
        , speed=.045)

    def twenty_two_encounter0(self): # guardian of the gate
        dprint(
            f'''
Suddenly, a thick cloud of smoke, a rushing sound, and the sensation of falling
all directions at once takes all of your senses far from the strange scene. The
next thing you know, you land on your backside after having leaped backwards
from the pool. Back to reality with the same old sores and wounds, clothes,
environment and plights that come with it. 
That was definitely the strangest thing you had ever experienced but you can't
dwell on it. Something else is in the room with you now, rising from the pool
taking the form of a tall ghostly human like figure with abnormally long limbs
and nails. You back to the exit as it makes its full ascent, and as it turns
its blank canvas of a face directly towards you, it screams a long rising,
peircing, bone rattling scream. A long drawn out shriek that fills you with
unearthly terror.
'''
        )

    def twenty_two_victory0(self): # hurry up already
        dprint(
            f'''
At the final strike, the aparition wails more high and terrible than ever
before but only for a short period of time. The ghost simply faces you, unholy
wrath written in its jerking twitching motions. It lunges once more before you
can even react and its misty form glides straight through your chest. 
Your entire body suddenly feels icy cold as if you has just fallen into a
frozen lake. Instantly overcome with a fit of shivers, you do your best to look
around you and see nothing. No sign of the ghost. You conclude only two
possible options: either the ghost has vanished or it now resides in your own
body. 
You sit there quivering from head to toe for the better part of an hour before
you decide that even if its just this freezing sensation, you have felt no more
damage.
You struggle to stand and upon doing so, you understandably find it very
difficult to focus feeling this way. Dispite this you have no idea what to do
about it, so, you grit your chattering teeth and do your best to ignore the
cold. You scan your surroundings, you must have traveled a fair distance from
the strange pool where the fight started and you had had that strange vision.
In the dark you can begin to make out a few minor details about the cave you
didn't recognize before. 
Feeling your way in the darkness, shivering all the while, you find your way
along the right hand wall of the cave tunnels. These ones are much less random
seeming than your past experience. They come to much sooner dead ends than
before allowing you to metally check off several tunnels over the hours of
searching and feeling.
'''
        )
    
    def twenty_two_encounter1(self): # they come in L size
        dprint(
            f'''
You find your way into one particular tunnel and a few steps in, your foot
sinks into a pot of mud which you instantly feel begin to tear away at the
flesh of your leg. Try as you might, you cannot remove it from the burning
sludge. As you struggle, surrounded in ice and fire, both eating away at your
body, mind and will, you plunge your blade into the puddle dangerously close
your your submerged and melting foot. Upon doing so, you feel the slime
physically slacken its grip on your flesh. In that instant you yank and most of
your leg pulls free. You stab again and the puddle both releases your foot and
bubbles up from the stony cave floor forming a large cave slime. At the same
moment a few others pop out of the walls and various other places to attack.
'''
        )

    def twenty_two_victory1(self): # Escape, Elysium
        dprint(
            f'''
Minutes after the final slime exploded and the acid drained away, you were
still gripping your burned leg shivering all the while. At last you again grit
your teeth and stand bearing the pain and you listen for the sounds in the
cave. You remember what you did in the goblin halls, straining your ears,
blocking out all other senses, focusing with all your might for signals your
ears pick up.
Your eyes fly open, somewhere out there you hear a low moaning sound that you
could only imagine being two things: the sound of strong air currents or
vengeful spirits. Despite that you had already encountered one of those things
and not the other. You make a hobbling, shivering break for the sound. 
A left, another left, a difficult vertical climb and a right. One bend and fork
after another, you hear the sound grow stronger and stronger before you finally
enter a large cavern and feel a breeze. The air is cold and it seems to blow in
a circular motion around this dark cavern. 
Just before you finish your circuit around the cavern you pass a certain fork
and are immediately thrown forward onto your hands and knees. An overpowering
air current blasts out from a perpendicular opening on the cavern wall.
You turn around and stagger forward doing you best not to be thrown backwards
again while trying not to fall forward as well. 
It takes you several minutes but you make it, crawling now, head first into the
wind tunnel.
What feels like hours later, the tunnel, the wind, the absolute complete
darkness, all that had by now become familiar to you in the deep, comes to an
end. This new cavern open before you swirls with wind similar to the last one 
but this time you can see the source. At the far end and about fourty or fifty
feet up the far wall, you see what is unmistakably daylight trickling in from
somewhere soon after. 
You drop you your bruised and cut knees, eyes forward, involuntarily and
tearfully thanking open air for a view of the outside world which you start
towards, beginning with a crawl and as meager strength begins to come back into
your battered, torn, strained and starved body, that crawl becomes a staggering
walk and then a weak jog by the time you reach the far wall. 
Even after regaining some of your strength back, the lack of food and water in
your metabolism causes you to take a long time to sieze enough fleeting energy
to attempt the arduous climb up the the light.
The greatest thing keeping you going through the pain and fatigue, was the near
guarantee that you would be out of these caves soon and you're quest to rescue
your siblings was not over. 
It was these thoughts that propelled you up and over the wall, into the tunnel
and through, all the way to the slim fissure leading to what seemed like a
bright and sunny spring day outside. 
It took a some work widening the crack and slithering through, but you managed
it. Instantly the persistant albeit diminishing sensation of cold gripping your
person ever since destroying that ghost at the edge of the supernatural pool,
leaves you filling your body with a warmth and a comfort that made all other
cares seem to fade away. You collapse flat on your back in the gravel. The sun
beating down upon you, the warm dry breeze in your hair, the greens and blues
of leaves a wide sky above you, you may as well have found yourself in the
blessed fields of Elysium. 
'''
        )
    
    def twenty_two_encounter2(self): # golem number 1: bark.
        dprint(
            f'''
Without setting up camp, or even getting up from where you lay, the sky slowly
begins to darken until night arrives and the expanse above you fills with those
familiar twinkling motes of light. 
Before you drift to sleep lying in the rocks, your mind drifts for a moment and
your mind's eye is filled with the strange experience you had had beside that
strange pool deep under the mountain.
Nothing like that had ever happened to you before, nor had you heard of
something like that happeneing to anyone, even to people who were aquainted
with magics and illusions and stuff of that nature. You had truly slipped into
someone elses consciousness. Someone who was clearly not in a comfortable
position. You empathized with them, whoever they were, wherever they were.
Something like morbid curiosity gave you fleeting desires to see what would
happen next but you also knew that whoever's life you were experiencing was or
at least seemed nigh more painful and dangerous than yours was currently.
You hoped the child was alright, and grew thankful again that at least you
could see stars and the cresent moon above you.
With those thoughts you drifted off to sleep. . .
'''
        )
        dprint(
            '''
*crash*
You wake suddenly and jump to your feet, imediately reminded that your legs are
sore and wounded, and colapse again to the gravel which had partially been
molded to your body while you slept. From the ground, you listen and scan your
surroundings for what could have made the sound.
Rather quickly, you hear and then see two masses moving about along the edge of
the cliff you slept under. One of them is smaller and looks to be some kind of
four legged mammal like a dog or a wolf but somehow different. The second looks
almost like a small giant, it moves about on two legs and stands upright like
that of a humanoid but it was as tall as some of the trees around it.
Then you realize what made the crashing sound. The two seemed to ge fighting
and the humanoid thing was attacking partially by picking up and throwing huge
boulders at its foe. One such boulder missed the target and ended up soaring
more than sixty feet colliding and shattering against the cliff wall about
twenty feet from where you sat spying. For risk of becoming an involuntary
target, you crouch walk closer to the fray for a better look at its
participants. 
Only about fourty or fifty feet away now, you can see what is clearly a
direwolf saddled and armored fighting. . . actually you're still not quite
certain up close what this thing is. It was tall, wide and humanoid like you
had seen before but it's ody was composed of strips of bark that seemed to
stick together and move on their own. 
You move still closer, keeping and quiet and indetectable as possible. The
growling of the direwold was clear in your ears and the strange bark creature
was making no sounds as it fought. You could see its face, blank with two deep
holes for eyes and a fixedly gaping pit for a mouth exposing no teeth nor
anything but more bark inside. 
The bark creature, landed a strong hit on the wolf which began to flee into
the woods. The attacker did not persue, instead, it paused for a moment before
turning slowly towards your hiding place and then barreling directly for you.
'''
        ,.0375)

    def twenty_two_victory2(self): # heheh... yeah... were back baby!
        dprint(
            f'''
The golem began to crumbe before your eyes leaving nothing more than a large
pile of inanimate bark scraps. You were greatful that, despite your weakness
you were able to fight as you normally would, doing so also made you acutely
aware of what you felt was likely a fractured rib the result of your escape
from the goblin king.
You couldn't wait any more, though, during the fight you realized that the
direwolf who was the pervious foe of the golem was tytpically used as a steed
for Kobolds. Furthermore, that particular direwolf was laden with a saddle of
sorts as well as wooden armor.
Without a moment's hessitation save it be a little grimace from your wounds
and soreness, you take off in the direction the direwolf had fled. The trees
pass by you in blurrs surprising even yourself by your speed. It would seem
that the memory and motivations of your main task had subconsciously reawakened.
The discomfort around your body seemed to melt away as you ran and a smile, for
the first time in what seemed like eons, grew upon your face.
You were back. Not only that, but you were close, and sure enough after about
five minutes, you see through the trees, smoke rising in the early blue glow
coming up over the horrizon.
'''
        )


    def ch_23(self): # spying out the kobold camp, Spring 47th-48th, 3044, 6th age
        mon_list = self.config_monsters({'small kobold':1})
        self.twenty_three_intro()
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.twenty_three_encounter0(), surprise=True)
        if player_lives:
            self.six_victory0()
            self.story_reward()
            self.story_prep(location='1-10', name='follow Luxkhanna')
            return True
        else:
            return False

    def twenty_three_intro(self): # infiltrating the stronghold
        dprint(
            f'''
Peering through the trees near the top of a hill, you survey the area below
you. About half an hour had passed since you left the crumbling pile of bark
behind. From there you had mad your way towards what you had since sonfirmed to
be the very kobold stronghold you had been looking for this entire journey thus
far. Beginning at the bottom of the hill upon which you are perched, structures
of stone and wood sprawl outward in a veritable city of kobolds before you all
enclosed in a sturdy, well kept wall or large boulders and tree sized wooden
pikes which remind you all to well of the wall you encountered before the
nepenth wood. 
You see little dots which you imagine to be kobold civilians and soldiers alike
trapsing about between the various structures. You don't see too many, likely
because of the early hour, but you know there will be a significant amount
more as the day progresses.
You wait and patrol, eventually, circling the entire stronghold for what
becomes the rest of the day before you decide, you had found your ideal
infiltration point and make your move.
The sun sets quickly, darkening the south country and ushering in your moment.
By this point in your adventure you are fully aware that the darkness will only
inhibit your own perception but you chose the night time simply because you
knew there would be fewer kobolds about at night. You dart from tree to tree
about five hundred feet to the right of the eastern entrance. There, you set a
candle's worth of fire amid some prepared kindling. As soon as you doo and you
confirm that the kindling is well lit, you book it north, orienting your
position closer to the front of the entrance. From there, you wait for the
flames to catch the attention of the guard upon the wall. The distraction takes
a bit but soon you see the outside patrol jogging towards the diversion. As
soon as they pass, you make your move, crouching low but moving quickly out of
the tree line and right up to the wall.
This part was crucial, this was one of the only two entrances in the stronghold
which was not equipped with a ground guard. You hope was that while the tower
guard's eyes were focused on the results of the patrol's findings, you would
be able to slip through the gate unnoticed. Three factors were the main
determiners of your success. 
1: The tower guard had to keep their gaze upon the fire. 
2: The patrol investigating the fire needed to investigate for sufficient time. 
3: The eastern gate needed to be unguarded from the inside. 
That last factor was the most risky, if there was a ground guard at that gate
that was simply stationed on the inside. You were out of luck and would just
have to run and hope you could find another way in. What made it worse was that
you had no real way of knowing beforehand. It really was just a fifty percent
chance once you made it to the gate. Furthermore, that was only if you made it
that far.
Sprinting along the wall, watching both your step and the workings of your
distraction, you make it to the gate and peer around the corner. Inside, the
gate passage way is empty of kobolds but a sharp corner prevented you from
seeing far enough around the other side to make sure there was no guard. 
You crouch down lower and creep ans silently and quickly as possible through
the gate house. As you approach the end, you keep your eyes towards the far
side so as to survey around that corner. You see a few merchant stalls and the
backs of some stoneworked buildings. You take this to be a good omen, seeing no
sign of what would obviously appear the be a guardhouse. This in mind you peer
carefully around the corner and you instantly pull back, heart pounding. 
Just inside, not ten feet away was a kobold sitting on a stool looking right at
the entrance. 
You were running out of time. 
You didn't have to worry about the tower watch spotting you here but as soon as
the patrol came back, you were in deep trouble.
After a few moments you realize that, somehow, the kobold you saw hadn't made
any noise. You had recieved no hale, heard no alert. And that much have meant
that even though it was looking right at you, it hadn't seen you. But, you
reason as you begin to hear marching kobolds approach from behind you, the only
real way that can reasonably be possible with the kobold's darkvision would be
if the kobold was asleep!
Without peering a second time you round the corner and see the kobold you had
seen before perfectly upright, but fast asleep. You count your fortune but
don't stop there. The kobold patrol had just entered the gatehouse, you could
hear at least five sets of kobold boots marching quickly across echoing
cobblestones.
There were no barrels or obstructions, you could use to hide yourself. A this
rate your hessitation had gotten you into yet another fifty-fifty chance with
now, even higher stakes. Your only option was to duck into the alleyway between
the first two small stone buildings behind the sleeping kobold and hope that
there was no kobold in ther as well or on the street beyond who would happen
to look your way.
'''
        )

    def twenty_three_encounter0(self): # assassin
        dprint(
            f'''
You make your move quick and quiet as you had been all this time. This time,
however, the kobold on the other side was awake with its back turned. Try as
you might to enter the alley as silently and you could, the kobold still turns
having heard your entrance.
You brain works at hyper speed, scanning the area for anthing that you could
do. The alley decended slightly ending in a short wall before exiting to the
road beyond. This structure blocked most of the street's view of the alley and
upon noticing this you knew what needed to be done, you couldn't afford any
further hessitations.
Time seemed to resume, and you saw the eyes of the kobold pop and air begin to
collect in their lungs, you knew you only had one chance. . .
'''
        )

    def twenty_three_victory0(self): # sneeeekiing, seen Luxkhanna
        dprint(
            f'''
Quick, and silent, you take out the danger and carry the body to the darkest
edge of the alley just as you hear the kobold patrol pass on the other side of
the building. You take several silent deep breaths through your tattered goblin
tunic and edge to the outside of the alley. 
Seeing the coast clear, you again begin to creep your way along the inside of
the stronghold wall, ducking into allies when passersy by approach. Soon you
detect an opening from within one such alley and you use it to slip like a
shadow across the street and into the greater interior. For here you are much
more able to traverse undetected as the buildings, alleys, obstructions and
convenient hiding places are much more common. 
After nearly an hour, stalking the city, you see what might look like a town
map right at the edge of an alley across the street. Your heart again began to
race knowing that that map would likely show where the stronghold dungeon was
located. You imagine that would be where they would be keeping the human
prisoners, including your brother and sister. Now, it was no longer the risks
and the danger increasing your heartrate, it was the thought that they were
most likely here with you somewhere in the kobold stronghold. They were so
close!
You hold your position there for another several minutes before you find an
opening. With the dark nightly street void of enemy eyes, you slip across right
inside the alley. After a few more moments of listening just in case, you head
to the alley entrance and take a look at the map.
It's a crude depiction of vague streets and less than accurate building
locations, but you do see five rather prominent land marks labeled in the
common tongue: The "you are here" marker labeled out side of a shop you had
passed two streets ago; "The North Gate" at the very far north of the
stronghold; "The Keep" located near the southern end of the stronghold but
still closer to the center; A large brown circular structure labeled "Anznag's
Crater" taking up a large portion of the western stronghold; and, lastly, a
slightly smaller structure labeled "War Dungeon."
The marker was located about half way between the north gate and the keep. The
inaccuracy of the "you are hear" marker showed that the map was off in places but
even accounting for likely error, you were only five to ten minutes east of the
keep now, which meant it was only a hop skip and a jump from there to the
dungeon.
You do your best to memorize the map and back again into the shadows. Edging
your way closer and closer to the goal you had been seeking since the attack of
greentown and the abduction of your little brother and sister.
You look to your left and see the dark mass of what could only be the keep.
Even from here it looked more like a dark stone palace than a keep, massive and
looming in the darkness complete with towers, battlments and tattered banners
the twisted heraldry of which you could not make out in tha darkness. 
Another few minutes later you are stalking your way one street behind the main
causway leading to the keep, when you see something through the alley that
imediately catches your eye. A prosession of distinguished looking ruin kobolds
surrounding and following what looked to be an open palankeen upon which
lounged the largest, strongest, most distinguished looking ruin kobold you had
ever seen before, far surpassing all the rest of the group.
Making up your mind you decide to follow from alley to alley along side the
prosession listening in on their conversation all the while. At your distance
and position you can't hear much but you do make out one name as they address
the royalty in the center.
Luxkhanna.
'''
        )


    def ch_24(self): # infiltrate, encounter with Illfang Spring 48th, 3044, 6th age
        mon_list = self.config_monsters({'owlbear':1,'kobold chief':1,'ruin kobold trooper':1,'ruin kobold':1,'kobold guard':1,'kobold soldier':1,'kobold slave':1,'small kobold':1})
        self.twenty_four_intro()
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.twenty_four_encounter0(), collective=True)
        if player_lives:
            self.twenty_four_victory0()
            self.story_reward(name='Start back to Greentown',location='1-9')
            return True
        else:
            return False

    def twenty_four_intro(self): # Looooooooooooooorrrrrrrrre! 
        dprint(
            f'''
You know this was a good move to follow the kobold leader you had heard so much
about. Now that you were on him, you could find out where he stays and you
might even have a chance to take him out before or after you rescue your
siblings depending on how things went from here.
You continue your persuit straining your ears for words the kobolds were
speaking. You were unsure who's voice was who's but you were somewhat sure at
this point that the voice of Luxkhanna was the mild tennor you could pick up
the most frequently among the rest. Occasionally you could make out a few words
in order. Thankfully, like most kobolds around here, they spoke common. 
". . . And what of the human bandits, great capper? Ever since we destroyed
th. . . "
Each time their voices would fade you would slip out of the alley and move on
to the next. Closer and closer each time to the keep. 
". . . nothing. What comes out of that mountain is of little concern in the
plans of the great. . ."
Another alley closer.
". . . have killed our war beast in that canyon, admittedly a great loss, but
they will still pose no threat to us as we ma. . ."
You were now only a few building's away from the front court yard of the keep.
". . . es capper?"
"We have arrived. No more questions. Leave."
"Of course, lord. . ."
The palankeen dropped to the street, Luxkhanna dismounted, the bearers knelt
astride the palankeen towards Luxkhanna, the other nobles bowed and they with
their capper departed, Luxkhanna, towards the keep entrance and the nobles,
back up the street, each in silence.
You again snuck out of the alley and traveled all the way to the edge of the
keep entrance. You watched as your target approached and entered. Neither he
nor anyone else around here seemed to care much about security as, not only
were there no pedestrians around, there were, as far as you could detect, no
guards around either. It must have been the dead of night that was giving you
such a break. All the same though, you took your time and made absolutely sure
there were no obvious eyes upon the keep exterior. You begin to scale the
wall using some convenient leverage and a roll of rope you found and clamber
into a window a short way above the roof line. Inside you quickly sneak to a
stairwell nearby and head down just in time to see the kobold leader slipping
into a chamber in the center which, for the brief moment you saw inside while
the door was open, looked like it might be a throne room of sorts.
You head back up the stairs and in the direction of that center room.
Fortunately behind a weapon stand full of spears, you see a gap in the wood and
stone large enough to peer inside. 
You see Luxkhanna approach the throne but he does not continue to it.
He stops about ten feet before, and bends one knee bowing his head in an act of
reverence and salutation to one greater than himself siting just out of sight
upon the throne.
"Hail, the great kobold boss, Lord Illfang!"
"Speak your business, Capper Luxkhanna," came the voice of the kobold boss, just
deeper than Luxkhanna's with a hiss to it and a timbre that made it sound as
though there was something perpetually lodged in the back of his throat.
"Yes, my lord," answered Luxkhanna, faithfully, "I have come to report the
findings concering my scouts' investigations, discuss your great plan and
lastly recieve your orders."
"Report away. I have been rather curious concerning your repeated failures in
that area."
"Of course my lord. My initial scouting party still has yet to return. They are
being presumed dead. The second group, did return having dicovered truths that
the group that preceeded tham was likely ambushed and captured by goblins-"
"GOBLINS!?" shouted Illfang, "As soon as were done with the humans, they're
next!"
"I agree Boss!"
"Shut up and continue!"
"Yes, the party also found that the war beast had infact been slain as we
suspected, likely by the bandits. They had found signs of a battle with bandits
within the canyon as well, many died, but they must have still bested the
beast."
"I suppose you think it was not wise, to attack the bandit stronghold and anger
them?"
"I doubt none of your strategies, but that sentiment is reflected in many of
the rancoo nobles here."
". . ."
You could not see Illfang but the air in the room seemed to radiate with
malice. 
"Is that all you have to report?"
"All except that further bandits are coming through the canyon and attacking and
wresting our supply trains."
"I can understand their thoughts that I was foolish in my plans to attack the
human barbarians. I know that like them, you also boubted my strategy to attack
the humans in their towns. Don't deny it! I can see it written in your faces as
you speak with me. The doubt and even trechery is crystal clear. But now and
soon you will understand the plan. I have seen our victory as clearly as you
see me before you. Great Gog, has spoken to me as he has to this point and told
me that the time is soon to come! Everything, we have worked for and prepared
for is coming together. The loss of the beast he gave to us, the foolish and
clumsy escape of your human prisoners, the bandits, the treachery, all of your
failures have been only minor setbacks. It only means that much less of your
forces will join us in the conquest soon to come!"
"Does that mean that we will be making our move soon...my lord?"
"You have come to me to discuss my great plan, and this I have done. What I
have said will be enough to you for now."
"Of course, my lord Illfang."
"Now. . . This time, I do not have orders for you concerning your failures. . .
No, this time I give orders based on what you have heard of my great plan. You
know that our attack is near at hand, I want you to gather your forces and make
your way to my stronghold in the north-east. Now because the beast is dead, you
have lost your opportunity for greater glory. We will be attacking from my
own fortress rather than yours. Dissembark no later than two days after I do. I
Will meet you there and give you and your forces further instructions. It will
also likely be there that I explain to you all the entire plan as it has been
given to me. Not only that, but if you do not fail me again, at least you may
have a chance to meet the great Gog for yourself and recieve instructions at
his hand even as I have."
"My lord-"
"Shut up. . . That is all, leave my presence and do not come back until you see
me at my fortress. I expect you and your forces no more than twenty days from
this night."
". . . "
Without another word, Luxkhanna stood, turned and strode out of the hall,
leaving Illfang in a room full of tension and leaving you reeling.
You had heard that it was not only the settled humans under thier threat but
the barbaric bandit tribes of humans in tha area as well. You had heard that,
the true boss and leader of the Kobolds was a kobold called Illfang a fact you
might have deduced if you knew that the kobold title of capper was below that
of boss in their heirarchy. Not only that, but there might even be a greater
mastermind leading Illfang along. 
You had also heard about the Kobold's great war beast in the canyon that they
thought had been slain by bandits, but the two things that you heard that shook
you the most, was that Luxkhanna's human captives had escaped. Meaning that you
had no more reason to be here. And secondly, the kobolds had not planned to
stop at their initial attacks. They were planning something much bigger, much
worse and it would be happening soon. 
In other words, not only did you have no more need to be in this stronghold any
longer, but you also needed now to hurry home as fast as possible, to warn your
home of the impending attack.
Without thinking you stand up and back right into the spear stand sending it
crashing down with a deafening clatter. Moments later, you hear the soft but
clear taunting voice of Illfang address you from within the throne room.
"More treacherous scum under the rule of Luxkhanna, I wish you luck outrunning
the guards heh heh heh!"
Almost instantly after Illfang stopped speaking, two kobold guards rounded the
corner at the end of the hall at top speed. One, weilding a short bow, fired at
you right as you dove out the window from which you entered.
The drop wasn't too long but definitely longer because of your awkward and
sudden dive, you tried your best to cushion the landing but you still nearly
broke, feet first, through the straw roof. Another arrow wizzes past you and
sticks into the roof. Just when you thought you had escaped the guards, defying
Illfang's expectations, you hear a high alarm bell ringing loud and long,
peircing the night air, loud enough to wake kobolds for hundreds of feet
around.
There was nothing else to do. You run.
Deciding that it would be better to avoid the kobolds themselves rather than
their detection you decide to stick to the rooftops. It didn't take long for
kobolds of all shapes and sizes to exit, bleary-eyed and curious, from their
several abodes and wonder at the ruckus that had awoken them. And it wasn't
long after that, that some began to spot you, a human, an intruder, gliding
atop their rooves, leaping from building to building across allyways. 
Arrows, stones and larger more dangerous projectiles began steadily to zip by
you, some coming dangerously close.
'''
        )

    def twenty_four_encounter0(self): # Ruuuuuuuuuuuuuuuuuuun!
        dprint(
            f'''
After only a minute of this, you determined it would be a slightly safer path
out of here traveling by the streets, and so, finding your next relatively low
rooftop, you slide right into a small crowd of bewildered kobolds who hadn't
seen you yet. In passing, you topple several of them and leave the others
completely lost for a while, long enough that, by the time they realized what
had just happened, you were able to round the corner onto the next street.
Right as you rounded the corner however, another kobold did the same about a
block away armed and looking directly at you.
"Kill, that human!" It bellowed to the nearest kobolds who all turn to you and
attack. One kobold chooses not to participate opting to sick its pet on you
instead.
'''
        )

    def twenty_four_victory0(self): # *snort* that's how you escaped?!
        dprint(
            f'''
Leaving the scene a bloody mess, you sprint farther northward as more and more
kobolds begin dashing into veiw behind you. As soon as they begin appearing
ahead of you as well, you duck into the nearest available alley to the east.
This pattern of escape works fairly well until you reach the northern wall and
have to find other, rather strategic, methods closer to the sealed north gate. 
You know if you try to take a kobold hostage, they wouldn't think twice about
killing the both of you so that was out. Hiding was hardly in the cards. . .
Or was it?
The street you just burst into contained a total of zero kobolds!
You slip into a building with exacly one sleeping kobold inside and wait until
the main force of pursuers pass by. At that moment, you re-emerge carefully and
quietly from the building. And slip again into the alleyway. 
Hiding behind some trash heaps and a barrel, you watch as three and then four
more small groups of kobold guards pass by. After a bit more time you peer
around the corner and begin to sneak again from house to house in the dark
careful to check your surroundings at all times and especially before making
any moves. Carefull also to remain obstructed from view at all times.
Just then, as you were again hiding behind some burlap bags of trash, you have
an idea. You grab the bags of trash, two in each hand, and carefully exit the
alley. Your new path takes you north skirting the edge of each building. It was
a little hard to see in the current light level but moments later you detect a
group of kobolds rounding a corner up ahead. 
As quick as a wink you duck down, make yourself as small as possible, and pull
the trashbags close. The searching kobolds come and go paying no heed to the
inconspicuous pile of trash outside the house. As soon as the coast is clear
again, you stand and continue carying the bags with you. Only a half second
later you find yourself burried between fourty pounds or more of kobold trash
waiting for the next unsuspecting kobolds to pass by.
It was a bit more slow but it seemed to work very well. Kobolds were just so
used to seeing piles of discarded garbage in their stronghold that no one ever
bothered to question one until you made it all the way to the north gate, guard
house between its back wall in the stronghold wall itself. It was here when
finally a passing kobold did a quick double take after he had passed you by
and even gone a few steps. You had been preparing for this though. By this
point you decided that if anyone actually managed to spot you, you were close
enough that you could make a break for the gate. 
Like a blast of dynamite, you explode out of your faithful, rather smelly,
disguise, the kobold approaching you falls backwards and shields itself as you
blaze past. You exit the space between the back guard house and are imediately
spotted by the gate guards who hold their pikes forward in a feeble attempt to
stop you. You were cornered but you knew what you had to do, you'd done it once
before rather recently actually. Instead of rushing at the guard, you make a
hard right and stride up the steep staircase to the top rampart where your
saving grace stands pointing a javelin at your chest. 
The guard makes a jab forward, you react by turning your torso to the left and
leaning backwards deftly avoiding the point. From there you reach with your
left hand for the spear shaft and the right hand for the kobold's throat.
With it now grappled and panicking, you rotate left and force your victim
against the wall and over.
You found it hard to believe later, but the thought that crossed your mind as
you fell was:
"Only thirty feet? Peice of cake!"
Sure enough, the grass and soft dirt combined with the cushioning of a kobold
beneath your feet as well as a well executed tuck and roll maneuver upon
landing made it seem like the fall was nothing, leaving only your feet a bit
sore.
Continuing flight from the stronghold, you glance backwards to see guards, a
hundred feet behind you now, struggling to reopen the gate to pursue after
you further. Imediately after remembering the urgency of the situation you
can't help but let out a chuckle.
'''
        )


    def ch_25(self): # back from whence you came, Spring 48th, 3044, 6th age
        mon_list1 = self.config_monsters({'kobold soldier':2, 'dire wolf':2})
        mon_list2 = self.config_monsters({'irrawrtzus':1})
        self.twenty_five_intro()
        player_lives = self.battle.story(mon_list=mon_list1, dialog=self.twenty_five_encounter0(), collective=True)
        if player_lives:
            self.twenty_five_victory0()
            player_lives = self.battle.story(mon_list=mon_list2, dialog=self.twenty_five_encounter1(), collective=False)
            if player_lives:
                self.twenty_five_victory1()
                self.story_reward()
                self.story_prep(location='1-7', name='Back through the canyon')
                return True
            else:
                return False
        else:
            return False

    def twenty_five_intro(self): # wow thats refreshing
        dprint(
            f'''
Soon after your escape, you remembered the urgency of the situation. Illfang
the lord of the kobolds was planning a large scale attack on the humans of the
region including the inhabitants of Greentown. It would happen as soon as a few
weeks from today and you absolutely had to get back home before then. You're
not sure how long it's been since you left, you had lost track of the days long
ago, not to mention you had no idea how long youu ere under the Amn mountains.
The weight of the task bore down on you once again just as it had when you left
to find Robin and Rosie. 
'''
        )

    def twenty_five_encounter0(self): # just like good old times huh
        dprint(
            f'''
You again glance behind you making sure you were correctin your assumption that
the kobolds could not possibly pursue you. What you saw imediately proved you
wrong. Dashing through the trees were two heavily armed kobold riders chansing
you down on their steeds. You had overlooked the fact that the kobolds had
mounts now. 
'''
        )

    def twenty_five_victory0(self): # the seed of dread
        dprint(
            f'''
There was no time to waste, you had to keep going as fast as possible. You were
aware now that you were under persuit and also increasingly more aware of how
quickly time seemed to move when you wanted it to stand still.
A growing seed of dread began to grow within you knowing that after all this
time you had failed to rescue your siblings, although, that was fine because
they had apparently somehow managed to escape for themselves. The dread really
came in knowing that there was a chance then, that they had also made it home
and were now, yet again in grave danger and you were the one with the
information that could save them.
'''
        )

    def twenty_five_encounter1(self): # Joy != circumstances
        dprint(
            f'''
You head for the obvious breach in the looming mountain before you, keeping in
mind both personal experience and what you had gleaned from the conversation
between Illfang and Luxkhanna about what was coming out of there.
As soon as you drew even remotely close to the canyon's mouth, those obstacles
began to manifest themselves. A barkling here, a windwasp there, a few wild
beasts who had managed to survive, and soon enough you were feeling as you
had going through this canyon the opposite direction, assalted at every turn,
slown down significantly by the need to sneak past enemies rather then fight to
conserve energy and resources. This was especially important now and the last
time you had eaten anything was also the last time you were inside this canyon,
several entire days ago. You'd never been so long without sustenance and you
were really feeling it. Your legs and hands were shaking you vision grew fuzzy
sometimes and all you wanted to do was lay down, maybe forever. 
But the dread was keeping you on your feet. 
These things made a terrible combination that made you clumsy and wreckless and
it became only a matter of time before you would be found again, attacked and
drained of what little strength you had left.
'''
        )

    def twenty_five_victory1(self): # Joy == Focus, wise words
        dprint(
            f'''
You could tell, even this early on, it was going to be a long trek back.
Everything about your circumstances seemed to combine together to hedge up your
way. It was difficult to block out the constant sharp pains in your upper chest
every time you took a breath. You're injuries reminded you of Suphia and her
useful, frankly life saving, healing spells. You were reminded of the sacrifice
she made and remembered something she had said to you as you were about to
enter Amn mountain foothills.
"Motivation doesn't ebb and flow with your circumstances. The core and source
of true motivation comes from your focus. With that in mind, its always best to
focus your life on things that really matter. And then, poor circumstances will
mean very little to you."
It was difficult to keep going physically, but you knew where you were going,
why and that if you stopped, a lot of people were likely yo die. Whith that
focus in the forefront of your mind, and the mouth of the canyon less than a
few feet before you, you grit your teeth and move in. . . 
'''
        )


    def ch_26(self): # rush back to warn the town, Spring 48th-49th, 3044, 6th age
        mon_list1 = self.config_monsters({'greedy badger':1,'letiche':1})
        mon_list2 = self.config_monsters({'treent':1})
        self.twenty_five_intro()
        player_lives = self.battle.story(mon_list=mon_list1, dialog=self.twenty_five_encounter0(), collective=True)
        if player_lives:
            self.twenty_five_victory0()
            player_lives = self.battle.story(mon_list=mon_list2, dialog=self.twenty_five_encounter1(), collective=False)
            if player_lives:
                self.twenty_five_victory1()
                self.story_reward()
                self.story_prep(location='1-7', name='Continue')
                return True
            else:
                return False
        else:
            return False

    def twenty_six_intro(self): # Same old canyon
        dprint(
            f'''
It was bad. It wasn't quite as bad as you remeber it being, but the variety and
fequency of monsters making use of the only pass through the Amn mountains, was
extremely difficult to handle, especially in your current state.
The Kosaur, the kobolds war beast as it was called, must have had it good here,
constantly able to feast upon unwitting beastly and monstrous travelers. You
didn't regret in the slightest you're victory over it but you couldn't help but
remember the times when that was all that was in this canyon.
'''
        )

    def twenty_six_encounter0(self): # a challenger approaches
        dprint(
            f'''
As the first evening approaches, you decide to turn in early due to the
increasing soreness in your chest (and really everywhere else).
You clamber up to a shelf atop which you saw a shallow pocket int he cliff side
which looks to be a perfect hiding spot. As you near the top, you draw your
weapon almost out of habbit before even seeing the edge yet.
As you emerge over the top, you see, a creature you recognize and a creature
you do not, clearly battling to the death for dominance over the cliff self. 
They bath turn to you as you appraoch, weapon drawn.
'''
        )

    def twenty_six_victory0(self): # new best friend?
        dprint(
            f'''
Just as you finish off the last monster, you look over and see a creature the
size and shape of a large gray dog with two back to back pairs of antlers
looking at the remains of the fight with comically wide eyes. As your eyes meet
it imediately takes several steps back and loweres its head, its eyes still on
the glow still fading from your blade. 
You raise your weapon and charge screaming a battle cry at the top of your
lungs, but before you get more than a half step forward, the creature had
already, turned tail and zipped out of sight. 
Chuckling at your little bluff, you settle in for the evening atop this ledge.
The night comes quickly and the clear skies and surprising lack of monster
visitors allow you to quickly drift off to the bast sleep you had had in a long
time. You finally woke as the warmth of the spting sunshine was beginning to
iluminate the canyon before you. You rise and strech but recoil as your injured
rib is agrovated. Fully awake now, you take the next exactly three seconds to
break camp and begin heading your way back down and through the canyon. 
At the bottom you quickly realize why you had such a restful night. Before you
about fifty feet farther down the canyon stands the same creature you had seen
the previous evening which you had supposedly scared off. 
It didn't see you, but you saw it slowly, steathily crawling after an awakened
shrub as it approached the cliff ledge upon which you were sleeping. About a
minute later, right as the awakened shrub began skittering up the side towards
the top, the dog creature leapt out of it's hiding spot and pounced. 
The fight was short. The shrub was quickly torn to peices by the jaws of its
foe. Upon seeing this, and realizing you had had a protector throughout the
night, you slowly emerge from your hiding spot and walk slowly, still
cautiously, towards the monster. Your eyes meet again. You bend your knees
slightly and hold forward your hand. The dog's eyes widen again and, like
yesterday it fled with surprising speed.
"No wait!" You call after it, but its already long gone.
'''
        )

    def twenty_six_encounter1(self): # obviously too good to be true
        dprint(
            f'''
Hours pass with little event, you suspect that for some reason your unexpected
protector is still ahead of you ravaging all obstacles in your path. You hadn't
seen bahaviour like that from monsterous creatures before and you spent your
time contemplating why it might have acted that way. It looked like it was
going to attack you before you scared it off and after that it seemed to want
to protect you. Maybe it was trying to kill the creature you ended up defeating
and this was merely its way of thanking you? Maybe the creature was trying to
fight other monsters until it found one that could take you on? Maybe it was
something else entirely but either way, you had to take advantage of this while
you could and maybe you could further befrend the monster if you found it
again.
Your thoughts were interrupted as your eyes are met with a wonderful sight, a
fruit tree laden with what appeared to be bright red cherries perfrectly ripe
for picking. The sight made your mouth water, you had been keeping back the
hunger pangs with terrible river water but the sight of real food brought it
all back like a bolt of lightning. Most plant food in the canyon had already
been picked off by all the other creatures that have come before you. It was
surprising to see such a large and full cherry tree still mostly untouched. As
you draw near, you do see a few broken branches and marks on the tree
indicating that the tree had been used before by at least some creatures and on
top of that you saw no carcases nearby confirming your hunch that this was
infact a cherry tree rather than something poisonous.
Near the tree now, you pluck off one of the low hanging fruit and bring it to
your eyes for one last closer examination. 
'''
        )
        if self.player.hp > 0:
            self.player.hp -= random.randint(1, 3)
            display_health(self.player)
        dprint(
            '''
The next thing you knew you were flat on you back in the gravel having been
struck very hard in the lower back.
'''
        )

    def twenty_six_victory1(self): # Food... finally. Next time bring a bow.
        dprint(
            f'''
It seemed rather inefficient to have to chop down a cherry tree just to harvest
some cherries but as you filled your mouth with the sweet red fruit, you didn't
care. The taste was more vibrant than anything you could remember. The
difference between silt and mud straight to the slightly underripe cherries,
bursting with sweet and sour, made your eyes water. With every bite, you felt
your strength returning, as though the fruit itself had some kind of magic.
With a belly no longer gnawing with hunger, your mind sharpened and you ralized
to yourself how obvoiusly too good to be true that perfectly good and unpicked
cherry tree really was. It was lucky, you thought, that it wasn't something
much worse keeping other canyon crawlers from this fruit.
The canyon ahead, once a daunting stretch of unforgiving terrain and swarms of
enemies of all kinds, no longer felt as insurmountable. The faint echoes of
distant creatures didn't faze you as much now. You bundled up a few cherries
for later, picked up your weapon, and felt a surge of confidence. It was time
to move forward, and nothing in this canyon was going to stand in your way.
'''
        )


    def ch_27(self): # rush back to warn the town pt 2, Spring 49th-62nd, 3044, 6th age
        mon_list0 = self.config_monsters({'windwasp':3, 'black worm':1})
        mon_list1 = self.config_monsters({'big nepenth':1,'nepenth':3,'little nepenth':1})
        mon_list2 = self.config_monsters({'ruin kobold trooper':1,'ruin kobold':4,'kobold soldier':6})
        self.twenty_intro()
        player_lives = self.battle.story(mon_list=mon_list0, dialog=self.twenty_encounter0(), collective=False)
        if player_lives:
            self.twenty_victory0()
            player_lives = self.battle.story(mon_list=mon_list1, dialog=self.twenty_encounter1(), collective=True)
            if player_lives:
                self.twenty_victory1()
                self.adjust_team('Hesh', add=True)
                self.adjust_team('Coef', add=True)
                self.adjust_team('Deg', add=True)
                self.adjust_team('Virabela', add=True)
                self.adjust_team('Polly', add=True)
                player_lives = self.battle.story(mon_list=mon_list2, dialog=self.twenty_encounter2(), collective=False)
                if player_lives:
                    self.twenty_victory2()
                    self.adjust_team('Hesh', add=False)
                    self.adjust_team('Coef', add=False)
                    self.adjust_team('Deg', add=False)
                    self.adjust_team('Virabela', add=False)
                    self.adjust_team('Polly', add=False)
                    self.story_reward()
                    self.story_prep(location='1-3', name='Return Home')
                    return True
                else: 
                    return False
            else:
                return False
        else:
            return False

    def twenty_seven_intro(self): # canyon montage, new sword!
        dprint(
            f'''
After a good night's sleep and your energy somewhat replenished, your pace
through the canyon quickens noticeably. You manage four more restful nights
over the course of the next week or so which each time seems to double your
speed. Furthermore, you manage to intercept the rare animal prey of a monster
on your third day giving you a lot of energy and nutrition for the journey.
Monsters were so much more viscious and violent than non-monstrous animals
that very few animals would actually be able to make it alive through the
canyon. The large mountain goat you had found had infact just been killed by a
dire wolf so you were able to slay the wolf and take the goat for yourself.
On the morning of the ninth day in the canyon, you are walking along the river
bank when you see something you wish you hadn't in the grass.
The half dissolved corpse of the antlered dog monster that had been defending
you. Based on its rate of decay and how much of it was gone, you suppose it had
been less than a few hours since it had been killed. This meant that you were
about to have a much harder time getting through the canyon. Up until this point
you had been fighting mostly monsters who were coming from behind you, and now
they were going to start coming at you from all sides like before. You were
really struggling back then but even so you were only making it a few miles a
day and you had no idea how much longer you had to go.
Sure enough, the rest of that day proves to be full of delays and fights. Right
as the sun begins to set though, you enter a part of the canyon you recognized,
it was the scene of you're fight with the Kosaur. The meant that the mouth of
the canyon was much less than a day's journey ahead of you.
After a few moments of thought, you decide to try to make up lost time and try
to reach the end before camping. Knowing full well, it was likely to take you
much longer than it had taken you before. 
The sky darkens, night arrives, and the hours and steps continue to march on
with no sign of an exit. You do see some more familiar landmarks though. At the
end of hour two, you see several human skeletons clad in barbarian armor. These
must have been the Kosaur's first challengers. Recognizing the scene you look
far above you and see the ledge from which you had spied out the Kosaur's lair.
You thought the air would be thick with the smell of death and decay but the
monsters and beasts roaming through here must have done a good job leaving the
humans with nothing but bones. One near the back you see still has a decent
looking sword that looks and feels a fair bit like your original sword you had
lost to the goblins. You take it off his skeletal hands.
'''
        )

    def twenty_seven_encounter0(self): # will this be difficult though???
        dprint(
            f'''
By hour six, the fatigue really starts to hit you and monsters that didn't seem
to pose buch of a threat to you before, appear more so as your limbs shake and
your eye lids flutter.
'''
        )

    def twenty_seven_victory0(self): # Approaching the Nepenth wood again
        dprint(
            f'''
That fight happened to be the last fight you had before you finally saw the
exit of the canyon ahead of you through the darkness. You had finally made
it and in good time too. Only ten days through the canyon when it had taken
you about that long just to get however far you got last time. If you include
the unknown time spent in the goblin halls and otherwise under the mountain,
your really had to pat yourself and your inexplicable monster guide on the back
for accomplishing such a feat.
Your elation and relief at your success, only urged you further onward. You
recall that not far from here is the monument of sorts you had set up for
Suphia. That Would be a good spot to finaly get some rest.
As soon as you are a good distance from the canyon mouth, it seems to you like
monsters had simply ceased their existence. As far as you could see, there was
no sign, even in the dead of night, of enemies in any shape or size. You never
thought you'd think this thought, but you were actually glad you had gotten
used to the concentration of monsters in the canyon environment because now,
as you continued completely unrestrained and unthreatened. It felt so freeing
and liberating you thought you could sing.
It would only be a matter of an hour or so more before you spotted it and you
had to again pat yourself on the back. the jagged rock formation surrounding
her burrial site looked like tall shrines around a temple. The spot was well
elevated as it stood near the top of the Amn foothills so it could be seen far
and wide. Despite your time, energy and resources, you had done a decent job
memorailizing her. Upon arriving you find a few wild animals camping near the
spot which flee at the sight of you, scampering out of sight.
Climbing to the highest point available to you about fifty feet behind Suphia's
grave, you stand upon a boulder and survey the land ahead of you.
You see the Nepenth Wood resting in a long thin valley before you. Just beyond,
you can barely make out a hard line where the wall must be. Beyond that you see
the rolling Amn foothills all the way up to the horrizon. As you look, you see
the first faint blue glow of morning fill the sky to your right and decide
to head back down and get as much rest as possible. 
By mid morning you would say you had at least gotten a few hours of sleep and
call it good enough to head out again. You pay your last respects to suphia and
begin your way speedily towards the Nepenth wood.
If there was one thing of benefit that came from the desaster that was your
last crossing of these woods, it was that you knew how to do it right.
1: Cross during the day; 2: Stay quiet; 3: Move quickly; and, 4: Avoid the Pod
Nepenth at any cost. Those rules of thumb in that order resulted in your best
chance getting through safely. You also chose to sacrifice a few hours of
daylight for sleep so that, incase a fight did break out, you had more energy
at your disposal.
'''
        )

    def twenty_seven_encounter1(self): # Attempted panic attack
        dprint(
            f'''
Before long you enter the woods, the morning sun shining distastfully through
the branches upon the terror that once occured here. Hours later you begin to
see them, they're bulbous bodies, their limp vines, the emotionless wide
mouthed faces. It all began to come back to you like a steady trickle of water.
As each step passes you begin to hear the rustling of the trees in the wind,
snapping of twigs and the small sounds of the woodland begin to press upon your
ears like being submerged under water. Your attempts to be still and silent
quickly become rapid jerking and twisting motions towards any sound you hear.
The confidence you had entering the woods was ebbing fast. Each breath came in
short and shallow. Your heart began to beat in your ears like drums in the
deep. Each step you take becomes slower than the last as if the nepenths
themselves were wrapping themselves around you. Their slumbering forms were
nearer and clearer to you than ever and as you lay you eyes on another
slumbering nepenth, the memory of that night floods unbidden into your mind's
eye. 
You could see it so clearly, blood soaked leaves, the stench of death, the
sound of screams and tearing flesh. You fall to your hands knees, each breath
coming in rapid shallow gulps. Despite you popping eyes, your vision narrows. A
dread and panic begins clawing its way up your throat.
Out of the corner of your eye you see dark shapes moving through the trees,
creeping closer. You become acutely aware of how loud each gasp for breath is.
For a heartbeat, you are certain they know. You are alone, defensless, barely
able to breathe. The thick air of the wood, presses in on you and each second
lenghthens.
*CRACK*
You callapse onto your back, desparate to detect the source of the sound, panicked
whimpers betraying your position.
Directly beind you stands a Nepenth, nearly twenty feet tall, vines quivering
hungrilly at its sides, a hollow, avid grin stretched across its gaping maw.
It loomed over you like the specter of death. You worst fear had been realized.
At the same moment, it draws in a long gurgling breath and you let out a
strangled scream, drawing your sword and scrambling backwards as fast as
possible. 
In you panic, you fail to notice a smaller nepenth behind you which strikes
your back as soon as you back within its range.
'''
        )
        if self.player.hp > 0:
            self.player.hp -= random.randint(1, 2)
            display_health(self.player)
        dprint(
            '''
At the moment of its strike, the pain of it, the very same pain you had felt
back then brought your mind to that same night but moments after Suphia had
died. You remember feeling that pain, the thorned lashings on you back, wash
away in a new emotion that once again begins to fill you now. 
Rage.
The shaking of you limbs stabilize but your breathing does not. You glance
behind you just in time to see the smaller nepenth winding up again. You
knuckles are white on the hilt of your crude sword and right as it brings
its barbbed coiling vine down, you pitch your blade upwards with more force and
speed than ever before, urged on by your fury and the adrenaline left over
from your still ebbing panic attack. Your counter sent half the nepenth's vine
spinning into the air, but your slow start to real defense had gotten you in a
bad position, you look around and see another few approaching nepenths. 
'''
        )

    def twenty_seven_victory1(self): # excuse to fight without a debuff
        dprint(
            f'''
It felt strange standing there with an odd mixtrue of terror and fury filling
every bit of your mind and body, but somehow the cold sweat and hot blood kept
you fighting strong and ralatively safe throughout the fight and the rest of
the day's journey through the nepenth wood. Just as night begins to fall you
spot the wooden barrier that separates your old world from the terrors beyond.
Fortunately, the consentration of nepenths drastically thins the closer you get
the the wall so by the time it really gets dark, the threat is minimal and you
manage to make it through without much more than a quick squabble with a little
nepenth waking from its slumber. 
Over the next few days you marvel at the change in difficulty going there
versus coming back. You had become noticeably more practiced at combat but
surely that wasn't all. With the presence of that same constant nagging dread
and feeling of urgency in the back of your mind, it felt like the world itself
recognized the dire nature of the situation and removed from your path the
obstacles that would have otherwise been there. 
Whatever it was, it was little more than a few days before you found youreself
passing by the old stone tower you had explored and soon after that, you found
yourself in the familiar landscape of the southern greentown wilds, complete
with low rolling hills wide plains and occasional patches of trees or little
ponds, the sight was briefly welcoming to the eyes before you remembered the
battle field they would become in, by now, little over a few week's time if you
didn't keep up the pace. You had made excellent time, well beyond what you
could have expected, but even if you could have traveled instantly somehow, you
would have called it too little time to work with to save your home from the
looming threat of destruction.
'''
        )

    def twenty_seven_encounter2(self): # PEOPLE!!!, attack pattern Antima
        dprint(
            f'''
One mid-morning, you spot a small group of something moving slowly in the
distance accross the green fields. As you draw nearer, you deduce that they are
somewhat humanoid by their bipedal gait and general behavior. It took you only
a few hundred feet more to discover that these were about to be the first
humans you had seen since that barbarian just before entering the Kosaur's
canyon. Even better, these looked like the kind of humans that wouldn't attack
you on sight. 
About a thousand feet away, one of their number appeared to have noticed you as
the rest of the group truns in your direction, considers you for a few moments
and apparently decides you to be friendly as one of them waves after you.
Shortly after returning the hail, you come within recognizable distance and
earshot at which time several member of the party gasp and comment at your
appearance remarking that you didn't look even remotely healthy or alright in
any sense of the word.
It was certainly true, you were still clad in the same old skins the goblins
had provided you, which by now had become worn to the point of falling appart
at the seams. Beyond that, you had eaten very little especially with respect to
how much you were doing each day. These factors coupled with the wounds and
bandages covering your body from head to food gave you the appearance of
someone who might just keel over at the slightest touch. 
You insist that you are well enough to carry on but do not turn down the
rations and medicine they offer you. They introduce themselves quickly but tell
you that they happen to be on a mission following a trupe of Kobolds nearby who
had just recently broken camp and were on the move again. 
You recognized only one of them as a neighbor from down the road. His name was
Deg. The rest of them were introduced as they and you began to move after their
quary. The one seemingly in charge of this operation was a man about the age of
your older brother Elond. His name was Coef and dispite being, besides
yourself, the youngest in the group, he seemed to radiate with authority and
strength. 
On his left was a woman who seemed to be taking up the mantle of second in
command. She introduced herself as Virabela. Behind COef and Virabela walked a
man called Hesh and a woman called Polly. Last in line were yourself and Deg.
The six of you strode quickly in this formation for nearly an hour by which
time you were getting impatient and you told the group at large that you
planned to get back to greentown as quickly as possible. Deg, who among the
group had been the most intrested in where you had come from, asked again to
which, just as you had before, responded by saying that the story wasn't
important and that he had some urgent information to give to the mayor and the
captain as soon as possible. Coef interrupted Deg's reply aknowledging your
request and telling the rest of the group to slow down and get down and hush
up. 
Less than a quarter mile away, the kobolds had stopped and two in their rear
were looking out while the rest began to set up a fire and some of their
provisions. It didn't looks like a full camp was being set but this would
surely be a major stop for the next while. As you watched, Coef spoke up. 
"We need to mount an attack but if they see us appraoching them they'll most
likely flee. Execute attack pattern Antima. We'll use that little clump of
trees as the critical point. {self.player.name.capitalize()}, just follow Deg and don't do anything
any of the rest of us don't do."
With that, the group began to army crawl backwards in to the taller grasses
nearby you followed suit wondering what was about to happen. 
Once you achieve the camoflauge of the grass, you follow the group as they sneak
father backwards for several minutes before Coef makes some strange hand signal
and you, with the rest make a sharp right turn, almost completely turning
around. After about a minute in this direction, Coef raises a chenched fist at
which the group stops. 
"Approach the critical point at one point five." says Coef after a few moments
of silence. 
The group begins trotting forward through the grass, still hunched low,
directly towards the clump of trees slightly to your left. as soon as you enter
the treeline, Coef hold up two fingers in a v shape follwed by a fist, an o, a
vertically extended hand and an "ok" sign in quick succession at which the
group again drops to an army crawl and continues forward. 
Another few minutes later, you see a few more rapid hand signs and the group,
followed as best as possible by yourself, stops stands and begins to walk
forward at about a fourty five degree angle to the right of your previous
trajectory. By this time you were very confused. How was this any kind of
attack strategy? Were you in stealth or not? 
You emerge from the treeline. Looking behind you and to your left, you see the
troup of kobolds, noticeably closer and still on the watch for intruders just
like yourselves, still not bothering to sneak in any way before you can get a
better look though, Deg lifts his arm and blocks your view giving you a look
that you took to mean something like. Don't make eye contact. 
With that, some little fragment of comprehension comes into your mind. The
kobolds were bound to see you and were very likely to come at you. Your not
certain how all you'd done led you to this and you thought it a bit unnecessary
but it might just work!
Sure enough out of the corner of your eye you see that the kobolds had
vannished. You also just barely noticed a subtle hand gesture at his side as he
swung his arm at his side. It was him repeatedly touching his thumb to his
other extended fingers as if to mime blabbing. 
At once the group burst into chatter. Coef and Virabela were chatting up front
about the wheather. Behind them, Hesh and Polly were discussing methods of
gardening and beside you, Deg spoke up too. 
"Sorry about that {self.player.name}. The enemy needs to think we don't know
about them any eye contact could blow that cover."
Midway though that sentence, Deg's voice as well as the voices of all others in
the group were momentarily reduced to just above a whisper before returning in
perfect syncrony to their usual volume. As Deg continued to speak, this
inexplicable fluctuation in conversation volume occured twice more. It was
right at the end of the third time that you noticed the piculiar way Coef was
waiving his hands. Right before their volume increased again, his hands you
turn upwards and flap a few times as if conducting a band, at which signal, the
volume would increase.
From then on began to watch Coef's hand movements more carefully. After another
minute, Coef's hand suddenly froze in the air stuck in an "ok" position. 
Less than a seccond passed before he flicked his hand and you imediately
detected the difference. 
"... and thats why the attack strategy works see? The enemy thinks were unarmed
and unawares and all and as soon as they get close my favorites are the ones
with the almonds though. Its just the perfect combination of soft and crunchy
in my opinion but I mean, my opinion isn't too far from fact..."
Teh sudden change of topic must have meant that the kobolds would likely be
within earshot soon and the converstion had to be something innocent, like in
Deg's case, a description of his favorite pastry.
But you were hardly paying attention, Coef's hands while he blabbed nonsesically
at Virabela, had now formed a three. Now as he put down his ring finger, a two.
At that moment, you faintly heard a very differnet sound behind you, Coef put
down his middle finger. The sound was growing closer.
Coef put down his index finger and the atmosphere was imediately changed from
whatever it was to a complete battlefield, beginning with three perfectly
syncronized sword skills and a spell of some kind which completely destroyed
the closest kobold.
You likewise draw your sword and prapare to fight. 
'''
        )
        self.player.hp = self.player.maxhp

    def twenty_seven_victory2(self): # today's date, news of captives
        dprint(
            f'''
It was strange, maybe it was the full heal and food you had recieved from
these people, or maybe it was simply the fact that they were people who were
actually friendly to you, but whatever it was, even while fighting, you felt
the a powerful feeling of comfort and relief enter your mind while you were
with them. Unfortunately, however, you had to part from them soon. You could
not wait for their mission to finish up and they told you they would be staying
out for another full day. Dispite yourself and the nagging urgency in the back
of your mind, when they stopped that evening to camp, you decided to stick
around.
The next morning dawned bright and warm, you were not sure how long you had
been away but by the feeling of the warm air this early in the morning, you
suspected that Summer was just around the corner. Just then as you were about
to leave, having packed up a few last provisions Coef insisted you take, you
realized thay these people would probably know the date and you ask. 
"Iss the morning of the 62nd of Spring, 3044," answered polly, "And I don' at
all blame yer for wan'in to know. Being through what you have. Fact, 'snot the
fers time I've herd that question recently. Not one week ago back home, a whole
bigol crowd of kids turned up from the south-west, all in about the state you
were in, covered in rags and injuries. Course I wasn't- oi, whashrong!"
You had stood up very quickly and suddenly. The contents of your, bag which had
been on your lap spilled onto the floor. A memory of a part of the conversation
between Illfang and his leutinent came rocketing into your mind.
"...Your foolish and clumsy escape of the human prisoners..."
The humans who were being help captive in the south had escaped! They might
have been the ones taken from Greentown.
"Did they say where they had come from?" you almost shout as Polly, the others
were paying attention now. 
"Well, I say... I wasn't on duty then so... spose it wasn't my business to
ask."
Without further elaboration, you leap down tot eh ground, scrambling to get
everything back into your bag. 
"What's up {self.player.name}?"
You make no answer, your mind was filled with only one thought cycling through
your head like lines you were trying to memorize.
Your siblings, Robin and Rosie, had somehow escaped kobold prison on their own, 
without outside help, and had somehow also made it home.
It wasn't certain, they had come in from the south-west rather than the true
south, and you hadn't heard anything more that would suggest they cam from the
same place you had. But still, a large group of kids all arriving at greentown
at once? It was far from impossible. All things considered it was highly likely
that your siblings were with them. The only reason in your mind that they would
not be would be if the group had escaped from another unknown kobold place
somewhere to the south-west, only a slight variation. 
The only other thing that caused some doubt in your mind was your unsurety that
had remained with you all along so far, that all stemmed from the night they
had been taken. You had started out following them directly south and just
assumed that they would stay their course, if they veered and went to any other
kobold stronghold rather than the one you had found. You were out of luck and
were it not for the information you now had, your journey would be all for
nothing.
You straightened up, bag fully packed, and found yourself face to face with
Hesh. 
"What's wrong!?" He said firmly.
"I think my siblings might be with them! And I haven't seen them since I left
to go look for them nearly half a season ago!"
You decide to stop here and forgo telling them about the horrible thought that
had been haunting the back of your mind for the entire adventure back home so
far, that they might have died.
"I think you might be out of luck," said Coef, "I didn't recognise anyone from
greentown in the group, they were probably the ones taken from Tolbantha or
Pompon."
You didn't care and you told them so backing out of the camp and apologizing
before saying goodbye and sprinting north at top speed, leaving them still
rather confused. Just within earshot, you hear Virabela call after you saying
farewell. 
You extend your arm with your back still turned and continued, full speed, to
greentown. . .
'''
        )


    def ch_28(self): # plan is to attack first, Spring 62nd, 3044, 6th age
        mon_list = self.config_monsters({'windwasp':6, 'cykloone':2, 'windworm':3})
        self.twenty_four_intro()
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.twenty_four_encounter0(), collective=True)
        if player_lives:
            self.twenty_four_victory0()
            self.story_reward(name='',location='1-0')
            return True
        else:
            return False

    def twenty_eight_intro(self): # getting close
        dprint(
            f'''
The sun was high in the sky behind you, your hair flew like a banner in the
wind, your eyes and mouth were dry. You could feel supernatural energy pulsing
through your system with your blood, keeping your lungs whole and your energy
conserved. It was the 62nd of Spring and you estimate you had left somewhere
between the 45th and the 50th meaning that even now, Luxkhanna and his forces
were nearing or even now at Illfang's fortress readying for battle, bent on the
total destruction of all the humans in this region. If nothing else, you had to
get that information to Mayor Swendil and Captain Gurenge. But there was
something else, something that had urged you onward your entire adventure to
this point. Robin and Rosie might be waiting there.
'''
        )

    def twenty_eight_encounter0(self): # does this fight really have to happen?
        dprint(
            f'''
You clear a low ridge and immediately see two things: Greentown in the
distance, and monsters.
'''
        )

    def twenty_eight_victory0(self): # the report
        dprint(
            f'''
The town in sight seemed to spur you on to greater speed. You found yourself at
great risk of falling over as you bolt, full tilt, down the last hill and
across the wide fields leading to the very different looking greentown.
The fair sized but rather thin and insubstantial fence surrounding the town
was now made of raised earth, a layer of stone bricks and topped finally with
tall, sturdy-looking wooden pickets all coming to about twenty feet tall, over
twice the height of the old fence. 
You quickly drew near to the town wall and as you did so, you felt a strange
feeling of nerves come over you and you slow briefly before heading towards the
south gate. 
"Who r you?" Hailed a voice a top a wooden tower just inside the gate,
"Strangers arent being accepted ri- Oh flaimin' firebirds, is that {self.player.name} back from
the dead!?"
"Yes thats me!" you call back.
"I KNEW IT, I knew...!" The man's voice, trailed off. He had dissapeared from
the top of the tower and was bounding down at top speed, voice muffled behind
the wall. 
Soon, he rounded the wall to the right of the open gate and beckoned you
inside. This was unnecessary, you were still carrying a light jogging speed and
by now were less than a dozen or so feet from the gate by the time he came
around. 
When he did so, you recognized the face of a neighbor from down your street.
"Mr. Tullets?"
"Yeremenber!" He responts, delighted, and you begin walking with him into town.
"Hey listen here, you've been presumed dead officialy, but last week a bunch of
Greentown kids the Kobolds kidnapped came back, an so we've suspended a few of
those presumtions because more'n half of 'em were on that list. Weh? Yer
siblings you say? What was their names again?"
That same energy you had felt the first time you heard about this came back to
you in full force and you asked about your family. Upon telling their names,
Mr. Tullets puts his hand on his chin and puts on a contemplative face for a
few seconds before, slowly, like the rising of the sun, his eyes widen and his
face breaks into a grin.
"You know what...? Robin, yeah, Robin was with em', in fact, yeah, how could I
have forgotten 'im! He was all in the front and takin charge an' the like!"
It was like a volcano of relief and energy had erupted inside you. You couldn't
help yourself from laughing, bouncing on the tips of your feet and saying
things like "YES!" and "REALLY!" and "WHERE" over and over again.
Mr. Tullets was laughing too now, "Heh heh, Hi'm not sure where he might be but
my best guess would be either back at home r the barracks- Ahh go on, I can
tell you wanna go..! Go, heheheh!"
Thanking Mr. Tullets and once again assuming a full sprint, you head for the
barracks. If he was there he could reunite with Robin and warn the Captain in
one trip. The barracks were alse a bit closer to the south gate than home was. 
'''
        )
        dprint(
            f'''
The town looked very different from the time you left. All sorts of new
structures had been erected and there were tents all over the place, lining the
streets, filling lawns, and even pitched on level roof tops. What was more, the
population of greentown seems to have doubled or even trippled since the last
time you were here. These people, understandably, turned and starred as you, a
strange boy clad in a filthy, tettered animal skin and covered head to foot in
cuts, scars, dirt and sweat sprints at top speed past them. The people and
change about the town was a bit dissorienting but you managed to find your way
to the barracks.
The front yard was full of tents but void of people except for a few soldiers
training on dummies near the cobbled stone exterior of the main building. You
move towards the main entrance and step inside to see, not Robin, nor even the
captain, but Tiffey talking gloomily to a man Rulid did not recognize.
As you enter, their conversation is cut and Tiffey, looks around to see who
had entered.
"Theres no way..." she says upon seeing you. She strolls around and toward you,
her mouth slightly agape, "But, you... you were..."
"Dead?" you finish for her.
"I suppose, you would like the see the captain." she said. 
She gave you a little smile, rested her hands on her knife hilts considering
you for a moment, and left down the hall with the man without another word.
Only a few seconds later, you hear hurried footsteps down the hall.
Captain Outh Gurenge, came shortly into view with a look of amazement on his
face. The look made you smile probably the shortest lived smile in the history
of mankind as the man that imediately followed the Captain was none other than
Electo the brother of Suphia. The moment your eyes meet, his expression shifts,
a flicker of hopeful expectation dimming as he registers the empty space beside
you. He doesn't ask, or demand any explanation; he simply stands, fists
clenched at his sides, and stares into your face as if searching for any sign
that this isn't real.
You open your mouth to speak, to offer some explanation that will never be
enough. But the words don't come. The only thing that makes it past your
constricted throat is a hoarse, "I'm s-s-rry..." feeble and quivering.
All you wanted to do was look away but you couldn't bring yourself to do it.
Electo's face was stoney, blank and expressionless, but his eyes were shining
with tears. At this point you couldn't help yourself. The memory of her death
filling your mind once more.
What seemed like days later, you feel people take seats on either side of you.
Tiffey and the captain had sat down beside you, the captain looking a little
awkward, but Tiffey looking at you consolingly, placed her arm over your
shaking shoulders. You raise your head. Electo had gone without another word.
With a sting you realize that you had gone out to reunite a family, and in the
process torn one appart.
'''
        )
        dprint(
            f'''
It was a long time before you were able to calm down and sit up. The excitement
and relief of mere minutes ago had vanished completely, but you could at least
think straight again, focus, speak and listen. The Captain took notice of this
as you began to tell him of your journey and so began to tell stories of his
own knowing that you would understand.
The Kobolds had raided Greentown, Pompon to the west and Tolbantha to the north
all in one night during a single coordinated attack. During the attack, the
Kobold's main goals seemed to be the following: 1, the wreak havoc; 2, to tear
down and destory town defenses including walls and towers; and 3, to capture
and abduct specifically children of each settlment. Because of the nature of
their attacks, the kobolds had had massive success in all three of those
objectives. Shortly following the attack, the remaining populations of Pompon
and Tolbantha gathered to Greentown to recover and prepare for the future. 
Shortly following that, a powerful force of soldiers and scouts went north-east
following the path many of the kobolds took upon their retreat from Tolbantha.
about ten days ago, they returned having discovered the location of a powerful
and hitherto unknown fortress in the northern desert badlands. The left quickly
so as to remain un-discovered but saw ominous signs that the kobolds were not
done and were possibly planning something else big in the near future. 
At this point, you found your voice again and unloaded everything that you had
discivered and surmised from the conversation you had heard from Illfang and
Luxkhanna.
The Entire Kobold population in the region was preparing to launch a full scale
assault on Greentown in the very near future. Illfang, the Kobold Lord was the
one behind these plans and he is determined to wipe out humanity in the entire
region.
At this point you still had a deep throbbing grief in your chest but the old
urgency and ferver you had had before was back as well.
The captain asked you what happened with you and the others the night of the
raid and you answered that you and the others were fighting your way through
the kobolds raiders after your siblings.
"Ahh, I thought you were going after a leader you had spotted or something.
Well, none the less, I'm still glad I sent people with you. You probably
wouldn't have made it very far after them on your own."
With another jold of sorrow, you think you would hafe prefered it but you do
not voice this and merely grit your teeth and nod.
The captian watches you for a moment before saying, "You know, {self.player.name}, I've
seen that look before...It belonged to my face... A long time ago, when I was a
younger man on the front lines. We were... reckless. Too young to know what we
were doing, what we could lose."
He pauses, his gaze drifting past you, as if seeing his past playing out before
him. "We were stationed in hostile territory with a friend, Rheyven. Closest
thing to a brother I ever had. He saved my life more than once out there and I
his. One night..." The Captain's voice hitches slightly, though he composes
himself. "One night, we were ambushed. I made it out. He didn't."
He lets the silence sit between you both, his eyes heavy. "And you know, for a
long time, I carried that like a curse. Blamed myself. There wasn't a day I
didn't replay it in my head, imagining how I might've done things differently."
He sighs, the weight of old sorrow clear on his face, "But there came a time
when I realized carrying the dead with me... wouldn't keep them alive, bring
them back or make them happy. It only drags me down."
The Captain places a firm hand on your shoulder, his grip grounding. "{self.player.name},
you did what you could. Suphia's choice to come, her bravery, it was her own.
And it's up to you to honor that. To live the life she wanted to see you live.
That's how you carry them forward; not by holding the weight, but by letting
their memory, their sacrifice, make you stronger."
"She's still out alive {self.player.name}. At the very least inside you. And if you only
remember her dead then she can no longer help you."
You remember her final act in life. To strengthen you and help you move
forward. It was she who had allowed you to make it through to Luxkhanna's
stronghold and you knew from that moment onward that the best way to honor that
would be to do everything in your power to live in such a way that would be a
blessing to the lives of others.
You felt a new strength emerge within you. You look the Captain in the eyes and
you both nod.
'''
        )
        dprint(
            f'''
With new found motivation within you and once again, that urgency coming back
into your mind. You ask the Captain what we could do about the impending
attack. 
"Well, under normal circumstances, I would wait for a bit more evidence that
such an attack is inevetable, but I'm reminded of the last time you returned
with word of an attack as we did nothing about it, I would hate to make that
mistake again."
Within only a few minutes, you change into some better clothes and find
yourself you are surrounded by the most powerful and influencial people in
greentown, gathered around the confrencing table in the barracks for an
emergency meeting to discuss the recent and alarming new evidence.
As the meeting progressed, Mayor Swendil, and his cabinet, raised some
scepticism about the credibility of the evidence recieved. The scepticism was
imediately shot down by the urgency of the matter. Guards members including
Officer Jerrimathyus posed plans that would best enable defense of the town. 
A visiting officer from the Kedren Main Patrol Force by the name of Officer
Mickle, then posed a possible preemptive counter strike which was quickly shot
down due tot he overwhelming defensive advantage the kobolds would have. The
captain of the Tolbantha Guard named Aluah then proposed an evacuation which
was strongly considered before being eventually rejected due to the
catastrophic consequenses of failure. Up until this point the meeting had
lasted for a few hours. The evening sun was just beginning to cast orange light
through the high windows of the meeting room, when the door the the meeting
room burst open and hit the wall with a bang. There in the doorway, sporting
a massive black eye, covered in bandages and having clearly sprinted all the
way here, gasping for breath, was Robin.
You nearly fall out of your chair in your haste and for a brief moment before
you reach him, you hessitate, considering his bandages. But the look Robin
gives you tell you it wouldn't matter. Completely ignoring the important eyes
upon you, you stand in embrace for nearly a full minute before you part eyes
stinging and feeling more pure joy than you had felt in months. You part and
both simultaneously look each other up and down before also saying in perfect
unison "What happened to you?"
You laugh and hug again before Robin apparently notices the bemused onlookers.
"Oh, so whats this?" he asks.
"You may join if you would like Robin," Said Captain Gurenge, "We're discussing
the new evidence your brother has just brought to light of a large scale attack
by the kobolds."
"What?!" said Robin.
They then filled Robin in on what has been proposed thus far. By the time they
get to the Counter attack idea and it's rejection, robin says, "Well, why not?"
Robin then enumerated details about the Kobold stronghold he had beed held in,
each part being confirmed by your first hand account as well.
The kobold stronghold there had weaknesses, openings and blind spots. Robin
proposed that a small elite force might be able to head to the Kobold
stronghold in the north-east and infiltrate during inactive hours. Following
this proposal, an officer from Pompon named Dykester added more to the plan
saying that the kobolds could be easilly fooled by simple distractions. This
was again confirmed by both you and your brother. He also noted that the
Kobolds would likely not be expecting an attack on the eve of their own.
A few expressed concerns but overall, it was decided that a separate defensive
strategy would be employed while the counterstrike mission was to be carried
out concurrently. 
Officer Dikester, and three others in the group, volunteered to be in the task
force including Officer Mickle from Kedren Main and the head guard to the
mayor, a woman called reywyn, then both you and Robin were asked to be in it as
well. Lastly, Captain Gurenge joined and said that he would recruit five others
of the town guard he knew would be useful on the team. This brought the total
number of members of this Advance Attack Force to twelve. 
Finally, all present members of the task force were invited to leave the
meeting to prepare. Except town guard captains which only applied to Captain
Gurenge who seemed a little put out.
You leave with Robin, a violent spring in your step but a deep forboding of the
mission to come. Despite this you and Robin talk and laugh and worry and wonder
and conspire all the way home where you mother. Thrilled to her core, sinks to
her knees out of relief before welcoming you back home. . . 
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

