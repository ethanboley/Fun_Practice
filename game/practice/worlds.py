
from actions import *
from players import Fighter, Mage, Pugilist
from monsters import init_enemies
from misc import Hospital, Marketplace, Gym, Quit
from story import *


class WorldOne:
    def __init__(self, name, xp_thresholds):
        self.name = name
        self.number = 1
        self.mon_list = init_enemies()
        self.world_monsters = [monster for monster in self.mon_list if 1 in monster.world]
        self.pc = self.create_character()
        self.xp_thresholds = xp_thresholds
        self.book_one = BookOne(self.pc, self.xp_thresholds) # doesn't work if prompt is always 'Begin story'
        self.world_options = self.update_world_options()
    
    def create_character(self):
        dprint('What is your name: ')
        pname = input()
        dprint(f'Is {pname} male or female?')
        ugender = input()
        if ugender in ['2','f','F','3','female','Female','FEMALE','fEMALE','Fe','iron','not male','girl','GIRL','Girl','g','G','ggs',f'{pname} is a female. ']:
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
        # self.pc = self.create_character()
        time.sleep(1)
        dprint('.   .   .')
        time.sleep(1)
        sys.stdout.flush()
        time.sleep(1)
        dprint(f'. . . {self.pc.name[-3:]} . . .')
        time.sleep(1)
        dprint(f'. . . {self.pc.name}!')
        time.sleep(.30)
        dprint(f'Come one wake up, {self.pc.name}!')
        dprint('You just collapsed all the sudden are you ok?')
        dprint('Look, were still on our way back to town. Its not safe here!')
        dprint('Lets get going...')

    def update_world_options(self):
        battle = Battle(self.pc,self.xp_thresholds)
        hospital = Hospital('greentown hospital', self.pc.level)
        market = Marketplace('greentown market', self.pc.level, self.xp_thresholds, self)
        gym = Gym(self.pc)
        quit_game = Quit()
        world_options = []

        if self.pc.progress == 0:
            world_options.append(self.book_one)
        if self.pc.progress > 0:
            world_options.append(self.book_one)
            world_options.append(battle)
            if self.pc.location == '1-1' or self.pc.location == '1-3':
                world_options.append(hospital)
                world_options.append(market)
            if self.pc.level > 2:
                world_options.append(gym)
                if self.pc.level > 2 and (self.pc.location == '1-1' or self.pc.location == '1-3'):

                    world_options.append(hospital) if hospital not in world_options else None
                    world_options.append(market) if hospital not in world_options else None
                    pass

        world_options.append(quit_game)
        return world_options

    def world_loop(self):
        while True:
            print()
            dprint(f'. . . {self.name} . . . ',.1)
            input(f'{self.pc.progress}/32 - {self.number}\n')

            self.world_options = self.update_world_options()

            action = get_list_option(self.world_options)

            playing = action.run(self.pc, self, self.xp_thresholds)

            if not playing:
                break

            # if action in ['','1','0','c','C','continue','Continue','CONTINUE','Story','story','STORY','begin','b','d','5','town','Continue to the town']:
            
            #     book_one = BookOne(self.pc,self.xp_thresholds)
            #     playing = book_one.play_story(self.pc.progress)
            #     if not playing:
            #         break
            
            # elif action in ['2','Absolutely!!!','fight','Fight','f','F','2: fight','FIGHT']:
            #     current_battle = Battle(self.pc, self.xp_thresholds)
            #     playing = current_battle.regular(self.world_monsters)
            #     self.reset_monsters()
            #     if not playing:
            #         break
    
            # elif action in ['3','Hospital','hospital','h','H','HELP I\'M DYING!!!','heal']:
            #     hospital = Hospital('Greentown', self.pc.level)
            #     playing = hospital.resolve(self.pc, self.xp_thresholds, self)
            #     if not playing:
            #         break
            
            # elif action in ['4','m','M','marketplace','market','Market','Store','store','shop','Shop','SHOPPING!!!','s','S']:
            #     marketplace = Marketplace('justastore', self.pc.level, self.xp_thresholds, self)
            #     playing = marketplace.resolve(self.pc)
            #     if not playing:
            #         break

            # elif action in ['5','6','g','G','gym','Gym','GYM','t','T','training','train','Training','Train','TRAINING']:
            #     gym = Gym(self.pc)
            #     gym.skill_learning()

            # else:
            #     # dprint('Invalid input. ')
            #     dprint('Keep playing? Y/N')
            #     user = input()
            #     if user in ['N','n','Quit','quit','q','Q','Exit','exit','No','no','False','false','f','0','stop',' ']:
            #         playing = False
            #         break
    
    def reset_monsters(self):
        self.mon_list = init_enemies()
        self.world_monsters = [mon for mon in self.mon_list if 1 in mon.world]

