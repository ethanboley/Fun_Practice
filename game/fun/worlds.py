
from actions import *
from players import Fighter, Mage, Pugilist
from monsters import init_enemies
from misc import Hospital, Marketplace
from story import *


class WorldOne:
    def __init__(self, name):
        self.name = name
        self.number = 1
        self.mon_list = init_enemies()
        self.world_monsters = [monster for monster in self.mon_list if 1 in monster.world]
        self.story_prompt = 'begin story'
        self.world_options = [self.story_prompt] # fight, hospital, market
        self.pc = None
    
    def create_character(self):
        dprint('What is your name: ')
        pname = input()
        dprint(f'Is {pname} male or female?')
        ugender = input()
        if ugender in ['2','f','F','3','female','Female','FEMALE','fEMALE','Fe','iron','not male','girl','GIRL','Girl','g','G',f'{pname} is a female. ']:
            pgender = 'Female'
        else:
            pgender = 'Male'
        udomain = input('Choose your Domain \n1: Fighter \n2: Mage \n3: Pugilist\n')
        # dbugp = 7 # For debugging purposes. Adjust to test certain story points with varying accuracy (value matches stpry progress). 

        if udomain in ['','f','F','1','0','fighter','Fighter','FIGHTER','fight','Fight','FIGHT','1: Fighter','idk']:
            pc = Fighter(pname, pgender, 10, 2, 0, 1, .69, 3)
            return pc
        if udomain in ['2','m','M','mage','Mage','MAGE','w','magic','2: Mage ','yay, spells']:
            pc = Mage(pname, pgender, 10, 1, 0, 1, .59, 4)
            return pc
        if udomain in ['3','p','P','pugilist','Pugilist','PUGILIST','pug','3: Pugilist','punchy boy','Iskhan']:
            pc = Pugilist(pname, pgender, 10, 2, 0, 1, .65, 2)
            return pc
        if udomain == 'admin': 
            pc = Mage(pname, pgender, 5000, 600, 0, 100, .96, 10000)
            return pc
        if udomain == 'debug':
            # pc = Fighter(pname, pgender, 10 + (2 * dbugp), 1 + dbugp, 95 + round(1.16 ** dbugp) + (200 // dbugp + 1), dbugp // 2, .88, 3 * dbugp, dbugp)
            pc = Fighter(pname, pgender, 23, 4, 300, 3, .755, 30, 7) # adjust according to stats by level in experiments
            return pc
        else:
            pc = Fighter(pname, pgender, 6, 1, 0, 1, .4, 0)
            return pc
    
    def introdction(self):
        self.pc = self.create_character()
        time.sleep(1)
        dprint('.   .   .')
        time.sleep(1)
        sys.stdout.flush()
        time.sleep(1)
        dprint(f'. . . {self.pc.name[-2:]} . . .')
        time.sleep(1)
        dprint(f'. . . {self.pc.name}!')
        time.sleep(.30)
        dprint(f'Come one wake up, {self.pc.name}!')
        dprint('You just collapsed all the sudden are you ok?')
        dprint('Look, were still on our way back to town. Its not safe here!')
        dprint('Lets get going...')

    def update_world_options(self):
        if self.pc.progress == 1:
            self.story_prompt = 'Continue to the town?'
            self.world_options[0] = self.story_prompt
        if self.pc.progress > 1 and 'fight' not in self.world_options:
            self.world_options.append('fight')
            self.story_prompt = 'continue?'
            self.world_options[0] = self.story_prompt
        if self.pc.progress > 2 and 'hospital' not in self.world_options:
            self.world_options.append('hospital')
        if self.pc.progress > 5 and 'market' not in self.world_options:
            self.world_options.append('market')

    def world_loop(self, xp_thresholds):
        while True:
            print()
            dprint(f'{self.name} . . . ')
            input(f'{self.pc.progress}/32\n')

            self.update_world_options()

            for i in range(len(self.world_options)):
                dprint(f'{i + 1}: {self.world_options[i]}')
            action = input()

            if action in ['','1','0','c','C','continue','Continue','CONTINUE','Story','story','STORY','begin','b','d','5','town','Continue to the town']:
                book_one = BookOne(self.pc,xp_thresholds)
                playing = book_one.play_story(self.pc.progress)
                if not playing:
                    break
            
            elif action in ['2','Absolutely!!!','fight','Fight','f','F','2: fight','FIGHT']:
                current_battle = Battle(self.pc, xp_thresholds)
                playing = current_battle.regular(self.world_monsters)
                self.reset_monsters()
                if not playing:
                    break
    
            elif action in ['3','Hospital','hospital','h','H','HELP I\'M DYING!!!','heal']:
                hospital = Hospital('Greentown', self.pc.level)
                playing = hospital.resolve(self.pc, xp_thresholds, self)
                if not playing:
                    break
            
            elif action in ['4','5','m','M','marketplace','market','Market','Store','store','shop','Shop','SHOPPING!!!','s','S']:
                marketplace = Marketplace('justastore', self.pc.level, xp_thresholds, self)
                playing = marketplace.resolve(self.pc)
                if not playing:
                    break

            else:
                # dprint('Invalid input. ')
                dprint('Keep playing? Y/N')
                user = input()
                if user in ['N','n','Quit','quit','q','Q','Exit','exit','No','no','False','false','f','0','stop',' ']:
                    playing = False
                    break
    
    def reset_monsters(self):
        self.mon_list = init_enemies()
        self.world_monsters = [mon for mon in self.mon_list if 1 in mon.world]

