
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

        Args:
            monsters_to_include:
                A dictionary containing keys of type str which is the name of 
                the monster and values of type int which is the count of that 
                monster to include in the chapters monsters.

        Returns:
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
        battles = { # Basically the arguments for battle.battle(), mon_list, dialog, collective and surprise followed by optional boss_dialog
            0:(self.config_monsters({'monster':2}), getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')), False, False, ['']),
            1:(self.config_monsters({'monster':2}), getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')), True, False, ['']),
            2:(self.config_monsters({'boss':1}), getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')), True, False, [getattr(self, f'boss_{ch_num}_0')(), getattr(self, f'boss_{ch_num}_1')]), 
            3:(self.config_monsters({'monster':1}), getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')), False, False, ['']),
            4:(self.config_monsters({'monster':3}), getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')), False, True, ['']),
            5:(self.config_monsters({'person':1}), getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')), True, False, [''])}
        return self.chapter_loop(ch_num, part, parts, battles)

    # battles can count by 1 starting at 0 and work because the ACTUALL part is floordivided by 2 to find the correct battle args
    '''


    def ch0(self): # spring, 69th, 3044, 6th age.
        ch_num, part, parts = (0, 0, 2)
        battles = { # part (battle number):(mon_list, dialog, collective=False, surprise=False, boss_dialog=[''])
            0:(self.config_monsters({'Elond':1}),
               getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')),
               False, False)}
        return self.chapter_loop(ch_num, part, parts, battles)

    def passage_0_0(self): # The Ideal intro really
        dprint(
            f'''
It had been a freezing day, and as the evening approached,
the biting winds and snow carried on relentlessly. Ideal
didn't much care, he had warm enough padding underneath his
armor and his pounding heart was keeping him well warm
enough to carry on. 
For the past full day, he had been following a shady
character in the downtown Sanleay District. About 5 minutes
ago, his target had met with another hooded figure who
appeared to be his boss. They had soon after vacated their
meeting place at a brisk walk. Ideal, in pursuit, found
quickly that his quarry was likely trying to shake him off
as their route could not possibly have been more convoluted,
winding their way back and fourth through allys and side
streets with purpose. 
To keep from being personally spotted, he was following them
using a handy spell which allowed him to see through the
eyes of his bat, Turvy, which had been fluttering after
these shady figures. Although, that WAS the case. . . Up
until about a second or 2 ago.
Ideal blinked. Turvy had been less that 20 feet from them in
clear sight when they had inexplicably vanished into thin
air.
'''
        , story=True)
        dprint(f'Nah!', dialog=(.05, .1, '\n'))
        dprint(
            f'''
Ideal, croaked his frustration outloud. He had spent the
better part of his day tailing this figure, and now, right
when it mattered, he lost him; and maybe even his boss.
He rounded the corner, conjuring a small flame to see better
through the snowfall and increasing darkness. Turvy lighted
on his shoulder and crawled into his breast pocket quivering
slightly.
'''
        , story=True)
        dprint('"Apologies T," ', dialog=(.05, .2, ''))
        dprint(               'Ideal mumbled, ', dialog=(.05, .06, ''))
        dprint(                              '"I know iss cold, ', dialog=(.05, .08, ''))
        dprint(                                              '''you take it
easy now."''', dialog=(.05, .1, '\n'))
        dprint(
            f'''
He stalked farther into the vacant side street eyes peeled
for anything that he could have missed. He was sure he had
his eye on them when they had dissapeared, or Turvy's eye
rather. So it was likely a result of some kind of magic. 
Magic of that sort was mostly illegal outside schools,
religious sites, official law enforcement or military
garrisons or other sanctioned areas. 
He began shuffling low, scanning the walls and what little
ground he could sweep snow off of. After only about 5
minutes he found what he was looking for: a rune of some
kind carved faintly into the lowest brick layer about 10
feet before the fork at the end of the cobbled street and
about 20 past the point where the shady folk's tracks ended.
He wouldn't have seen it were it not for the snow.
It was emitting a faint and diminishing warmth which had
melted a little snow around it.
'''
        , story=True)
        dprint(
            f'''
A few minutes of clearing away snow and further investigation
later, he found another symbol, clearly not a rune this
time, of a severed hand resting atop a locked chest. He had
seen this symbol many times before in his line of work. It
was the emblem of a dangerous underground group within the
city and beyond called the Cult of the Hand.
'''
        , story=True)
        dprint(
            f'''
This was more than a religion it was the city's largest
criminal organization and infamous for their secrecy and
hatred for the people in power throughout all Mainenkedren,
maybe even the world. Ideal would die for his king, and
would spare no strength seeking out those who might do him
harm.
'''
        , story=True)
        dprint(
            f'''
For now though, and he hated this to be once again the case,
he had lost them. One day he would find them, settle the
score and bring safety once again to his beloved realm. 
'''
        , story=True)
        dprint(
            f'''
He could not have known, but another opportunity would be
coming soon. The cost would indeed be great, greater than
he ever could have anticipated. But help would also be
provided, help in what would now be rather unbelievable as
a few hundred miles to the south, in a tiny human village
called Greentown, this helper a {self.player.grammer['what_young']} by the name of
{self.player.name}, a normal, everyday 16 year old with no grand
aspirations or desires for anything that would upend the
comfort and simplicity of {self.player.grammer['altposs']} life there. Only by
somewhat extreme circumstances early that next year would
that all change.
'''
        )
        dprint(
            f'''
It was the 70th of spring. A day of many goodbyes, new
beginnings, and anticipation for life ahead. You could
hardly sleep last knight so you were awake at the crack of
dawn fully packed and waiting outside the north gate for
your father Rulid and oldest living brother Elond as well
as the captain of the guard in Greentown and a few others.
Just over 48 hours ago, you had met with these and other
members of "Rulid's Busses", a caravan train led by your
father for the last decade. For this reason you only saw
your father once every several months, but it was a steady
and decent source of income that kept your family stable
and happy during that time. The meeting 2 days ago had
discussed your departure once again from the comforts of
your home to venture to the capital of the world, the great
city of Kedren Main where you could potentially spend the
rest of your life, that night you had discussed the matter
with both of your parents who both agreed that dispite your
still being over 3 seasons under age, you were close enough
to adulthood that going to seek a future in the capital
would be a wise choice while you had the chance of free
passage via the caravan.
'''
        , story=True)
        dprint(
            f'''
Your mother Annabell was a little more against the idea of
your leaving home but agreed in the end knowing that your
life would be far better in the city surrounded by people
and a thriving economy, so long as you wrote her a letter
back home as frequently as would be reasonable and came
back with the caravan to visit whenever you could. At the
time you were excited but now you were something of a
nervous wreck. 
'''
        , story=True)
        dprint(
            f'''
You couldn't sleep and often found yourself bouncing your
leg or otherwise figiting wrestlessly anticipating the
journey ahead.
'''
        , story=True)
        dprint(f'"Hey {self.player.grammer["sibshort"]}," ', dialog=(.05, .1, ''))
        dprint(
         '''called the mild energetic voice of your older
brother, ''', dialog=(.05, .05, ''))
        dprint(
        '"you ready?!"', dialog=(.05, .12, '\n'))
        dprint(
            f'''
You turned and saw Elond, walking purposefully towards you
drawing 2 wooden swords and tossing one to you. 
'''
        , story=True)
        dprint(
            f'''
For a few moments after you caught the training weapon you
stood bewildered and a little alarmed before you remembered
that the night before, your brother had challenged you to a
duel the next morning. 
'''
        , story=True)
        dprint(
            f'''
He had wanted to see for himself this peculiar new younger
{self.player.grammer['sibling']} of his and {self.player.grammer['altposs']} new found aptitude. 
'''
        , story=True)
        dprint(
            f'''
The expression on your face changes to a grin as you realize
that Elond was dead serious. 
'''
        )

    def prefight_0_1(self): # bro fight!!!
        dprint(
            f'''
You ready yourself, assuming a practiced defensive stance.
Both hands on the hilt, blunted blade straight forward,
feet appart and the left slightly farther than the right.
'''
        , story=True)
        dprint(
            f'''
Elond grinned wider, a combination of intrest and ammusement
in his eyes. At the same moment you both leap into attack. 
'''
        , story=True)

    def passage_0_2(self): # Rulid memory, mean elf chick
        dprint(
            f'''
You both collapse to the dirt, gasping for breath. A strange
sense of nostalgia intermingled itself with the usual
exhastion, adrenaline and soreness after the fight. 
'''
        , story=True)
        dprint(
            f'''
Contemplating on this strange new post fight emotion, you
thought back on your childhood, playing with your siblings.
One particular event stood out from the rest. On the day in
question you were on an exciting adventure led by your
fearless oldest brother Rulid, he was nearly 12 at the time
and everyone saw him as the proud protector and one that
would always be there to save the day. Everything you could
ever remember about Rulid was like this. You couldn't
remember much, all things considered, you were only 5 when
he had vanished without a trace and was presumed dead. 
'''
        , story=True)
        dprint(
            f'''
Regardless, this was one of those times when Rulid seemed
to take the lead, taking you and Elond, (Robin had only
been 1 or 2 at the time) outside town to play adventure.
'''
        )
        dprint(
            f'''
You remember taking up little branches as your trusty
weapons and engaging in combat with trees and bushes as
children would, imaginations running wild. 
'''
        )
        dprint(
            f'''
That day stood out particularly clearly because it didn't
end up being just imagination. Having fun, you remember
siding with 9 year old Elond in an argument with Rulid
about whether to stay out or head back home. Rulid, ever
the responsible one, had agreed with mother to return home
before the evening.
'''
        , story=True)
        dprint(
            f'''
The argument escalated and Rulid ended up settling the
dispute with a three way duel. You and Elond verses Rulid.
It was a short spar. Rulid won desicively, almost
efforlessly, but the ruckuss had alerted a pair of slimes
lurking under the soil nearby. 
'''
        , story=True)
        dprint(
            f'''
The battle that ensued left Elond with a bad burn on his
leg and Rulid with a broken pinky finger. Slimes weren't
much a problem to grown fighters, but to 3 as good as
unarmed children with no formal training or experience,
it was a different story. Were it not for Rulid carrying
the fight, you could have all died.
'''
        , story=True)
        dprint(
            f'''
The chance to spar with your older brother must have cast
your mind back to the past, recalling that event.
'''
        , story=True)
        dprint(
f'''"Well this is an ammusing scene, "'''
        , dialog=(.05, .1, ''))
        dprint(
                                  '''called a dry female
voice from over your shoulder. '''
        , dialog=(.045, .07, ''))
        dprint(
                            '''As you sat up with Elond to
look, you saw a woman you had met the previous day while
packing. She had come from the caravan stationed outside
town to check on things and had seemed a tad short with you
and Elond even a little bit with your mother. She was also
not human. Maybe an elf, you couldn't tell for sure.'''
        , dialog=(.05, .07, '\n'))
        dprint(
            '''"Pearl!" '''
        , dialog=(.035, .09, ''))
        dprint(
                     '''Elond said getting up quickly, '''
        , dialog=(.05, .07, '\n'))
        dprint(
            '''
"Good morn-"
"Enough lolligaging" dropped Pearl, "We should have been on the road by this time
yesterday."
You both looked on as the elf turned on her heels and walked back the way she came
and out of view. 
"She's usually pretty nice actually." Said Elond as you both got to your feet.
"Just get to know her a bit and she turns into a great traveling companion, you'll
see!"
The two of you walked back towards Greentown to help haul boxes as requested, and
as you did you couldn't help feeling a sense of displeasure and forboding as you
walked. Despite Elond's assurances, you couldn't help remembering how the dwarf
had acted the day before. Maybe humanity was just naturally nicer than others.
Only time would tell. And this new journey would give you a LOT of time. 
 '''
        )


    def ch1(self): # spring, 72nd, 3044, 6th age.
        ch_num, part, parts = (1, 0, 6)
        self.adjust_team(to_modify={'Kizt':True, '':True, '':True, '':True, '':True, '':True})
        battles = { # part:(mon_list, dialog, collective=False, surprise=False, boss_dialog=[''])
            0:(self.config_monsters({'bullbous bow':3}), getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')), True, False),
            1:(self.config_monsters({'letiche':1, 'irrawrtzus':1}), getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')), True, False),
            2:(self.config_monsters({'black worm':1}), getattr(self, f'prefight_{ch_num}_{part}', default=dprint(end='')), False, False)}
        return self.chapter_loop(ch_num, part, parts, battles)

    def passage_1_0(self): # what's happened the last 2 days
        dprint(
            f'''
"So,[.08][s:.02] how old are you[s] again?"[w][n]
It was a younger person who had been talking your ear off for the last hours,[.07] trying
to figure out seemingly anything and everything about you,[.08] while[s:.06] somehow[s] telling
you everything about themselves,[w][s:.04] whether or not you wanted to hear it.[w][s] Well,[.5] maybe
he was young.[w] You wern't really sure if [s:.1]40[s][.2] was considered young for a halfling
but you honestly were trying your hardest not to care.[n][w]
It was day [s:.07]3 [s]of the journey to the capital.[w] A journey that had already proven
fairly trying in multiple different ways.[w] Your father's caravan train was large,[.3]
boasting a few dozen covered wagons,[.2] several passenger carriages,[.2][s:.07] and 30 extra ponies
and other steeds[s][.5] some of which you had never even seen[.05] before. Some of the smaller
folks,[.2] like this talkative halfling you were with,[.2] rode actual[s:.07] dogs.[w][s] Mastiffs as
steeds was strange and unusual for you but it wasn't the only thing that was somewhat
outlandish in your mind.[n][w]
Your father's caravan hired a wide variety of people for help in shipping.[w] So far
you had met dwarves,[.2] elves,[.2] halflings,[.2] gnomes,[.2] firbolgs[.2] and 1 fae,[.4] but that wasn't
all.[w] Day 1 of the journey,[.1] you had nearly committed murder when,[.3] rounding the corner
of a wagon,[.2] you saw[.08] to your great astonishment and horror,[1][s:.08] a kobold,[s][.09] just like
the ones you had spent the entire spring fighting.[w] Upon drawing your sword[.1] and
preparing to risk your life to defend your father's goods,[.1] you were tackled from
behind by a fellow human.[w] The commotion that ensued[.06] resulted in a very awkward
public talking to by several bystanders[.08] which only ended[.06] when your father,[.1] the
caravan head,[.1] came in person to your rescue.[w] To appease the masses tho,[.2] he had
also followed through with his own caravan bylaws[.1] and placed you in the roller[.2]
which was basically just a wagon used as a[.08] formal [s:.065]"timeout"[s] for [s:.065]"discontented crew
members."[s][n][w]
Since that day[.1] you had learned that Rulid's Busses also employed [s:.065]goblins[s] and [s:.075]orks[s]
as well as 1 [s:.085]goliath[s],[.3] all of which[.06] you had been raised hearing about as the
monsterous [s:.065]"bad guys"[s] of all your children stories.[w] Here,[.1] they had been employed
by your [s:.065]own father[s] to help Rulid's Busses thrive.[n][w]
Over the next days,[.1] you had met these strange folks and had been met in kind[.07] with gruff,[.1]
secretive,[.1] rude,[.1] dismissive[.1] and outright [s:.065]violent[s] personalities.[w] The Orks in
particular you had found[.08] loved the idea of spilling blood.[w] Because of your behavior
on the first day,[.1] you had only participated in your job on the caravan guard once[.1]
and during that time[.1] you were working along side 2 Orks which clearly gloried in
causing pain to the enemies you had overcome.[w] They wielded big brutish clubs which
invariably sprayed blood and bile with each contact[.07] all over everyone else in the
party.[w] And to make it worse,[.2] the the orks sometimes continued to [s:.06]beat their foe
long after it was defeated.[w][s] It didn't matter what Elond[.1] or your father[.08] said about
them[.08][s:.065] they were savages at heart.[n][w]
Today[.1] you were out on your second shift on guard duty.[w] It was a nice day generally
with little activity.[w] The last 3 hours you has spent talking with this halfling
who was also part of the caravan guard.[w] You wern't sure how though.[w] This person
was nearly half your size,[.2] which was saying something.[p]
'''
        , story=True, wrap=True)

    def prefight_1_1(self): # hunting cows
        dprint(
            f'''
The entire conversation[.1] you had been grilled about yourself[.1] and your background[.1]
all the while trying to do your job right[.1] and keep your eyes and ears open for
threats on this side of the caravan.[w] Right when you felt like you had had enough[.2]
a heard of monsters came to your rescue.[w]
'''
        , story=True, wrap=True)

    def passage_1_2(self): # not a fan of hunting party members
        dprint(
            f'''
Once again,[.1] after the first fight of the day,[.1] the Ork by the name of [s:.065]Kizt[s] on your
hunting party spent a full [s:.07]60 seconds[s] after the last beast was dead,[.1] beating its
corpse[.1] and laughing maniacally.[w] And then it[.07] just walked away,[.1] eyes closed[.08] with a
expression of [s:.055]deep satisfaction[s] on his face.[n][w]
This halfling character had also shown his colors.[w] He had hidden in the grass the
whole time[.1] and had never contributed to the fight at all.[w] Well,[.3] you probably should
have expected as much.[w] The only 2 on the team today that you really respected[.1] were
2 humans who you[.1][s:.065] honestly[s] had not spoken to very much[.1] but who had always been cordial when
you have[.1] and who faught efficiently on the battle field.[w] Team players,[.35] that was
a good description of them,[.25] not like many of the others.[n][w]
Regardless,[.3] with only a few members of the guard you could stand currently,[.2] you
would be trying your [s:.065]very best[s] to keep your distance from everyone[.08] until you were
needed again.[n][w]
'''
        , story=True, wrap=True)

    def prefight_1_3(self): # new things to fight
        dprint(
            f'''
Well,[.08] the appearance of monsters came to your rescue before,[.1] but now it was their
appearance that brought you out of the comfort of relative solitude.[n][w]
The only thing that boosted your spirits was the fact that[.07] due mostly to the changing
climate,[.1] you were being frequently intruduced to new[.06] and exciting kinds of foes.[n][w]
'''
        , story=True, wrap=True)

    def passage_1_4(self): # sneaking
        dprint(
            f'''
The day had ended with no further battles.[w] The sky was darkening[.1] and it was your
first turn this journey to take a watch for the night.[w] Your watch was not for several
hours but[.2] you tossed and turned unable to fall asleep.[w] You had been having frustrating
dreams of late[.15] involving kobolds once again attacking[.08] and taking your family members away.[n][w]
It was these dreams that kept you going strong on your search for your siblings,[.1]
but now that the threat was supposedly averted,[.2] they were only a hindrance and
now they were being made worse with the inclusion of kobolds,[.08] goblins,[.1] orks[.15] and
other monsterous beings [s:.065]teaming up against you.[s][n][w]
It wasn't very frustrating that they were keeping you awake,[.1] it was frustrating being reminded
that your father and brother[.06] were so convinced that these [s:.075]ACTUAL [s:.08]MONSTERS[w][s] were [s:.07]ok[s]
to keep around![w] You had spent nearly your [s:.065]entire spring[s] fighting off the [s:.065]same kobolds
and goblins[s] you were now being [s:.06]forced to work with.[s][n][w]
You had actually brought these concerns to your father[.07] who brought up the somehwhat
predictable point[.09] that he's been hiring[.08] and working with them for
the better part of 2 decades now with [s:.08]little [s:.065]issue.[s][w] Well,[.1] that might be true,[.1] but
your father hadn't been seeing them in a fight much[.25] as he would've always been
up front[.08] leading.[n][w]
Just as you were thinking this,[.1] the perfect opportunity presented itself.[w] You heard
the lowered voice of what was clearly the kobold on the guard position [s:.06]across from
yours[s][.06] whom you had been eyeing all day.[w] It was speaking in kobold or some other [s:.065]clicky
gutteral[s] language nearby.[n][w]
Carefully you rolled to your stomach and rose slowly and siletly to your feet.[w] This was your
chance to expose the monsters for the savage liers and cheats that they were[.1] and
always had been.[n][w]
It didn't take long to find them,[.5] 2 kobolds speaking in hushed voices on the side
of a wagon.[w] It was no use trying to determine what they were scheming[.07] due to the
language[.2] but the extra layer of secrecy did not paint a good picture.[n][w]
You supposed there would be no point in listening for long to this nonsense,[.1] so
at the first sign of suspicious action you jumped out to catch them.[w] The one you
had heard first,[.09] had reached under the wagon cover for something.[w] It was your father's
livelihood in there[.1] and you would not have it taken by such creatures.[n][w]
At your sudden appearance the kobolds both jumped[.1] and the one in the front drew
his dagger.[w] The other instantly dashed over the grass burm you were camping
against.[n][w]
[s:.06]"What are you doing,[.1] what did you take!?"[s][n][w]
At this,[.1] the kobold with the weapon drawn[.065] smirked and lowered his dagger[.07] calling
something in kobold over his shoulder[.06] to his vanished compatriot[w] [s:.065]who came running
soon after trailing[.15] [s:.07]a black worm.[s][p]
'''
        , story=True, wrap=True)

    def prefight_1_5(self): # watch broken probably caused by nonhumans
        dprint(
            f'''
The worm was larger than any of you and moved about as fast.[w] Its circular maw,[.1]
covered in teeth,[.1] gaped wide after you.[w] Both of the kobolds bolted[.1] leaving
you to face the monster alone.[n][w]
'''
        , story=True, wrap=True)

    def passage_1_6(self): # Anticipation and forboding
        dprint(
            f'''
After the battle,[.065] and the comotion that started it,[.125] you were left alone surrounded
by tired and iritated eyes.[w] None of them[.55] grateful for the threat you had diverted
from the misteriously missing kobolds.[w] You didn't care for that though,[.1] you were
[s:.075]seething[s][.12] that it had come to this.[w] Soon after,[.12] your real watch began[.1] but you didn't
actually do much watching for monsters,[.1] just for those [s:.06]long tails and mischivious
snouts of [s:.065]the monsters among [s:.07]friends.[n][w]
'''
        , story=True, wrap=True)


    def ch_2(self): # spring, 75th, 3044, 6th age.
        pass

    def passage_2_0(self): # family bonding walking with Elond and Rulid
        dprint()

    def prefight_2_1(self): # morning battle
        dprint()

    def passage_2_2(self): # sneaking overhearing angering
        dprint()

    def prefight_2_3(self): # battle with a comrade
        dprint()

    def passage_2_4(self): # break it up
        dprint()


    def ch_3(self): # spring, 77th, 3044, 6th age.
        pass

    def passage_3_0(self): # Elond on life in Kedren Main and the races (hinting at bros racism)
        dprint()

    def prefight_3_1(self): # twister from another world
        dprint()

    def passage_3_2(self): # orks to the rescue, recollection 2
        dprint()


    def ch_4(self): # spring, 81st, 3044, 6th age.
        pass

    def passage_4_0(self): # travel montage, arrival at farthe outpost, that evening
        dprint()

    def prefight_4_1(self): # the pit
        dprint()

    def passage_4_2(self): # oop time to go
        dprint()

    def prefight_4_3(self): # poor inocent thug
        dprint()

    def passage_4_4(self): # investigations, sidequesting
        dprint()


    def ch_5(self): # spring, 82nd, 3044, 6th age.
        pass

    def passage_5_0(self): # Fam reminisces about little Rulid, his birth, head out
        dprint()

    def prefight_5_1(self): # early travel battle
        dprint()

    def passage_5_2(self): # more Rulid and anticipations
        dprint()


    def ch_6(self): # spring, 84th, 3044, 6th age.
        pass

    def passage_6_0(self): # bit greener landscape
        dprint()

    def prefight_6_1(self): # guard duty
        dprint()

    def passage_6_2(self): # smoke suddenly rising close up ahead
        dprint()

    def prefight_6_3(self): # a fight on the way to investigate
        dprint()

    def passage_6_4(self): # minotaur army massacre scene, where, who
        dprint()


    def ch_7(self): # spring, 84th, 3044, 6th age.
        pass

    def passage_7_0(self): # following the trail, theorizing, fearing
        dprint()

    def prefight_7_1(self): # mountain-side minotaur fight, minotaur panic
        dprint()

    def passage_7_2(self): # volcano? or worse.
        dprint()


    def ch_8(self): # spring, 85th, 3044, 6th age.
        pass

    def passage_8_0(self): # wake in a wagon, what happened, none of our business
        dprint()

    def prefight_8_1(self): # coastal battle
        dprint()

    def passage_8_2(self): # Elond ont he crazy life of the city and little Rulid, memories
        dprint()


    def ch_9(self): # spring, 87th, 3044, 6th age.
        pass

    def passage_9_0(self): # Maybe theyre not all so bad
        dprint()

    def prefight_9_1(self): # Guard duty
        dprint()

    def passage_9_2(self): # there she is! Moving closer.
        dprint()

    def prefight_9_3(self): # Guard duty
        dprint()

    def passage_9_4(self): # at the walls, the bustle of diamond bay, Check Inn
        dprint()


    def ch_10(self): # spring, 88th, 3044, 6th age.
        pass

    def passage_10_0(self): # early morning commute, the report
        dprint()

    def prefight_10_1(self): # The day we met
        dprint()

    def passage_10_2(self): # Who is this person? Until found
        dprint()


    def ch_11(self): # spring, 89th, 3044, 6th age.
        pass

    def passage_11_0(self): # Considering the offer involves testing out/
        dprint()

    def prefight_11_1(self): # a cool new training atomaton
        dprint()

    def passage_11_2(self): # maybe not the worse idea ever, in fact..!
        dprint()


    def ch_12(self): # spring, 89th, 3044, 6th age. 
        pass

    def passage_12_0(self): # Offer accepted! Oreintation, you're here too!?
        dprint()

    def prefight_12_1(self): # Obliteratory test of strength fight
        dprint()

    def passage_12_2(self): # good timing! next final seelection will be summer 1
        dprint()


    def ch13(self): # spring, 92nd, 3044, 6th age.
        pass

    def passage_13_0(self): # intro to the Kedren Main Guard Initiation, Ideal
        dprint()

    def prefight_13_1(self): # night falls, test begins, first monsters
        dprint()

    def passage_13_2(self): # Hiding, fighting, dangerously arrogant moves
        dprint()

    def prefight_13_3(self): # The golems
        dprint()

    def passage_13_4(self): # goals, plans, Toby
        dprint()


    def ch14(self): # summer, 1st, 3044, 6th age.
        pass

    def passage_14_0(self): # Panic, the calming effect of others
        dprint()

    def prefight_14_1(self): # 3 way fight, traineesvGolemsvMonsters
        dprint()

    def passage_14_2(self): # short break to run
        dprint()

    def prefight_14_3(self): # sprint fight
        dprint()

    def passage_14_4(self): # talking, scheming, emergency
        dprint()

    def prefight_14_5(self): # the dreaded Cast Iron Golem
        dprint()
    
    def boss_14_0(self): # grinding and screeching on both sides
        dprint()

    def passage_14_6(self): # It's over, sunrise, leaving the forest, shocked facilitators
        dprint()


    def ch_15(self): # Summer 4th, 3044, 6th age.
        pass

    def passage_15_0(self): # Oorientation, training training
        dprint()

    def prefight_15_1(self): # Frist day, first spar
        dprint()

    def passage_15_2(self): # Wendy
        dprint()


    def ch_16(self): # Summer 17th, 3044, 6th age.
        pass

    def passage_16_0(self): # Rulid's busses leave, life, the update
        dprint()

    def prefight_16_1(self): # an example training fight
        dprint()

    def passage_16_2(self): # climbing the ladder, new friends in arms
        dprint()


    def ch17(self): # Summer 21st, 3044, 6th age.
        pass

    def passage_17_0(self): # The fest of all, poicing duty
        dprint()

    def prefight_17_1(self): # Spy some sketchoheads, ambush
        dprint()

    def passage_17_2(self): # Pursuit, dodging magics
        dprint()

    def prefight_17_3(self): # Theo's betrayal of The Hand
        dprint()

    def passage_17_4(self): # The firework bomb, firefighter duty
        dprint()


    def ch1(self): # summer, 22nd, 3044, 6th age.
        pass

    def passage_18_0(self): # Theo's Intel, what do
        dprint()

    def prefight_18_1(self): 
        dprint()

    def passage_18_2(self):
        dprint()

    def prefight_18_3(self):
        dprint()

    def passage_18_4(self):
        dprint()

    def prefight_18_5(self):
        dprint()

    def passage_18_6(self):
        dprint()


    def ch19(self): # spring, 72nd, 3044, 6th age.
        pass

    def passage_19_0(self):
        dprint()

    def prefight_19_1(self):
        dprint()

    def passage_19_2(self):
        dprint()

    def prefight_19_3(self):
        dprint()

    def passage_19_4(self):
        dprint()

    def prefight_19_5(self):
        dprint()

    def passage_19_6(self):
        dprint()


    def ch_20(self):
        pass

    def passage_20_0(self):
        dprint()

    def prefight_20_1(self):
        dprint()

    def passage_20_2(self):
        dprint()


    def ch_21(self):
        pass

    def passage_21_0(self):
        dprint()

    def prefight_21_1(self):
        dprint()

    def passage_21_2(self):
        dprint()


    def ch_22(self):
        pass

    def passage_22_0(self):
        dprint()

    def prefight_22_1(self):
        dprint()

    def passage_22_2(self):
        dprint()


    def ch_23(self):
        pass

    def passage_23_0(self):
        dprint()

    def prefight_23_1(self):
        dprint()

    def passage_23_2(self):
        dprint()


    def ch_24(self):
        pass

    def passage_24_0(self):
        dprint()

    def prefight_24_1(self):
        dprint()

    def passage_24_2(self):
        dprint()


    def ch25(self): # spring, 72nd, 3044, 6th age.
        pass

    def passage_25_0(self):
        dprint()

    def prefight_25_1(self):
        dprint()

    def passage_25_2(self):
        dprint()

    def prefight_25_3(self):
        dprint()

    def passage_25_4(self):
        dprint()
