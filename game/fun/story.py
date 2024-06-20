
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


    def adjust_team(self, to_modify='', add_or_remove='add'):
        """
        Modifies the player's team by adding or removing allies based on their name.
        Also removes duplicate allies with the same name.

        Args:
            to_modify (str, optional): Name of the ally to add or remove. Defaults to ''.
            add_or_remove (str, optional): 'add' to add an ally, 'remove' to remove. Defaults to 'add'.
        """

        ally_names = set()
        for ally in self.player.allies: # empty the allies list completely
            ally_names.add(ally.name) # but before that record the unique names of all that were in it
            self.player.allies.remove(ally) # allies list should be empty now

        for ally in self.all_allies: # iterate through all allies in existence
            if ally.name == to_modify: # find the ally matching the desired ally

                if add_or_remove == 'add': # if the ally is to be added

                    ally_names.add(ally.name)

                else:
                    try:
                        ally_names.remove(ally.name)
                    except KeyError as key_error:
                        ally_names.add(ally.name)
                        ally_names.remove(ally.name)
            
        for ally in self.all_allies: # iterate through all allies in existence
            if ally.name in ally_names: # find only the names that are to be in the new team
                self.player.allies.append(ally) # add all those guys




    def ch_0(self):
        mon_list = self.config_monsters({'brown worm':1,'slime':1})
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.zero_encounter(),collective=True)
        if player_lives:
            self.zero_victory()
            self.story_reward()
            self.adjust_team('Robin', 'add')
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
        self.adjust_team('Robin', 'add')
        self.one_intro()
        player_lives = self.battle.story(mon_list=mon_list1, dialog=self.one_encounter0(), collective=True)
        if player_lives:
            self.one_victory0()
            player_lives = self.battle.story(mon_list=mon_list2, dialog=self.one_encounter1())
            if player_lives:
                self.one_victory1()
                self.story_reward()
                self.adjust_team('Robin', 'remove')
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
        dprint('cornered. They begin to turn and prepare to fight!')

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
        self.adjust_team('Robin', 'add')
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
                    self.adjust_team('Robin','remove')
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
        dprint('*pant* "Well, that was ... strange! I\'ve never even seen let')
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
        mon_list1 = self.config_monsters({'slime':2,'awakened shrub':1,'barkling':1})
        mon_list2 = self.config_monsters({'small kobold': 3})
        self.adjust_team('Robin', 'add')
        self.three_intro()
        player_lives = self.battle.story(mon_list=mon_list1, dialog=self.three_encounter0(), collective=True)
        if player_lives:
            self.three_victory0()
            player_lives = self.battle.story(mon_list=mon_list2, dialog=self.three_encounter1(), collective=True)
            if player_lives:
                self.three_victory1()
                self.story_reward()
                self.adjust_team('Robin', 'remove')
                return True
            else:
                return False
        else:
            return False
        
    def three_intro(self):
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

    def three_encounter0(self):
        dprint('Rather sooner than you expected, you come across a few monsters')
        dprint('upon which to practice but dispite the surprise, you\'re both')
        dprint('ready to go!')

    def three_victory0(self):
        dprint('Upon achieving victory in what turned out to be a more dificult')
        dprint('fight than expected, you about face and make your way back')
        dprint('towards home.')

    def three_encounter1(self):
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

    def three_victory1(self):
        dprint('more than a little tired, you both hurry home in the mid')
        dprint('afternoon sun to report what has now become a seriously')
        dprint('worrying problem.')
        dprint('With little issue, you make it back and head, not home, but to')
        dprint('the town garrison to report the two kobold attacks. . .', .04)


    def ch_4(self):
        mon_list = self.config_monsters({'little nepenth':1})
        self.four_intro()
        self.adjust_team('Robin', 'remove')
        player_lives = self.battle.story(mon_list=mon_list, dialog=self.four_encounter0())
        if player_lives:
            self.four_victory0()
            self.story_reward()
            self.adjust_team('Robin', 'remove')
            return True
        else:
            return False

    def four_intro(self):
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

    def four_encounter0(self):
        dprint('You and Robin stay after and speak with the captain who tells')
        dprint('you that he is willing to bring someone your age on if you can')
        dprint('prove yourself in a fight. A few minutes later, Robin is')
        dprint('sitting in the stands watching you armed and ready to fight')
        dprint('whatever the captain brings through that portcullis ahead.')
        dprint('"These suckers can be found in the deeper forests to the far')
        dprint('south of there, we usually use them to test new recruits so')
        dprint('good luck to ya!"')

    def four_victory0(self):
        dprint('.  .  .',.25)
        dprint('Having passed the captain\'s test and standing over the')
        dprint('dissolving form of the Nepenth, you hear a short cheer from the')
        dprint('anxiously spectating Robin as wells as an impressed slow clap')
        dprint('from the captain who welcomes you to the ranks with open arms.')


    def ch_5(self):
        mon_list0 = self.config_monsters({'dire wolf':4, 'small kobold':3, 'kobold slave':2, 'kobold guard':2})
        mon_list1 = self.config_monsters({'dire wolf':1, 'kobold slave':2, 'small kobold':2, 'kobold soldier':1})
        mon_list2 = self.config_monsters({'dire wolf':3, 'small kobold':2, 'kobold guard':1})
        self.adjust_team('Henry','add')
        self.adjust_team('Liliyah','add')
        self.adjust_team('Tiffey','add')
        self.adjust_team('Kajlo Sohler','add')
        self.adjust_team('Officer Jerrimathyus','add')
        self.adjust_team('Robin', 'remove')
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
                    self.adjust_team('Robin', 'remove')
                    return True
                else: 
                    return False
            else:
                return False
        else:
            return False

    def five_intro(self):
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

    def five_encounter0(self):
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

    def five_victory0(self):
        dprint(
            '''
Blood was spilt on both sides in this battle that was never
supposed to happen, but you can't go home yet, this was
the reason you came out here in the first place. Most of you are
still able to keep fighting and the monsters are on the run. You
all need rest but you need answers more. 
'''
        )

    def five_encounter1(self):
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

    def five_victory1(self):
        dprint(
            '''
Finally, after 2 brutal battles you have 2 captives bound and ready
for interrogation. It's rough but you can distinguish a little of
the thick accented Common tongue amongst snarls and cries of your
captives. 
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
    
    def five_encounter2(self):
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
    
    def five_victory2(self):
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
        pass # another mission

    def ch_7(self):
        pass # the cave

    def ch_8(self):
        pass # red herring of some kind

    def ch_9(self):
        pass # returning home

    def ch_10(self):
        pass # wake in flames robin abducted single fight giving chase

    def ch_11(self):
        pass # the hunt begins

    def ch_12(self):
        pass # alone in the woods

    def ch_13(self):
        pass # alone in the woods pt 2

    def ch_14(self):
        pass # alone in the woods pt 3 found a clue

    def ch_15(self):
        pass # following the trail

    def ch_16(self):
        pass # following the trail pt 2

    def ch_17(self):
        pass # surrounded by nepenths (pre boss)

    def ch_18(self):
        pass # scounting the kosaur's lair

    def ch_19(self):
        pass # Kosaur boss fight

    def ch_20(self):
        pass # kosaur boss recovery

    def ch_21(self):
        pass # following the trail pt 3

    def ch_22(self):
        pass # following the trail pt 4

    def ch_23(self):
        pass # found the kobold camp and spot Robin

    def ch_24(self):
        pass # infiltrate, encounter with Illfang

    def ch_25(self):
        pass # the kobold plans

    def ch_26(self):
        pass # rush back to warn the town

    def ch_27(self):
        pass # rush back to warn the town pt 2

    def ch_28(self):
        pass # plan is to attack first

    def ch_29(self):
        pass # heading out

    def ch_30(self):
        pass # the boss' lair

    def ch_31(self):
        pass # the boss' lair pt 2

    def ch_32(self):
        pass # Illfang boss fight

