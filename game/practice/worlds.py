
from actions import *
from players import Fighter, Mage, Pugilist
from monsters import init_enemies
from misc import Hospital, Marketplace


class WorldOne:
    def __init__(self, name):
        self.name = name
        self.number = 1
        self.mon_list = init_enemies()
        self.world_monsters = [monster for monster in self.mon_list if 1 in monster.world]
        self.world_options = ['fight', 'hospital', 'market']
    
    def create_character(self):
        dprint('What is your name: ')
        pname = input()
        udomain = input('Choose your Domain \n1: Fighter \n2: Mage \n3: Pugilist\n')
        if udomain in ['','f','F','1','0','fighter','Fighter','FIGHTER','fight','Fight','FIGHT','1: Fighter ','idk']:
            pc = Fighter(pname, 20, 4, 0, 1, .7, 2)
            return pc
        if udomain in ['2','m','M','mage','Mage','MAGE','w','magic','2: Mage ','yay, spells']:
            pc = Mage(pname, 20, 3, 0, 1, .6, 2)
            return pc
        if udomain in ['3','p','P','pugilist','Pugilist','PUGILIST','pug','punchy boy','Iskhan']:
            pc = Pugilist(pname, 20, 3, 0, 1, .66, 2)

    def world_loop(self, pc, xp_thresholds):
        while True:
            print()
            dprint(f'{self.name} . . . ')
            input()

            for i in range(len(self.world_options)):
                dprint(f'{i + 1}: {self.world_options[i]}')
            action = input()
            
            if action in ['1', '0','','Absolutely!!!','fight','Fight','f','F','1: fight']:
                current_battle = Battle(pc, xp_thresholds)
                playing = current_battle.regular(self.world_monsters)
                self.reset_monsters()
                if not playing:
                    break
    
            elif action in ['2','Hospital','hospital','h','H','HELP I\'M DYING!!!','heal']:
            
                hospital = Hospital('Greentown', pc.level)
                option = hospital.welcome()
                playing = hospital.resolve(pc, option, xp_thresholds, self)
                if not playing:
                    break
            
            elif action in ['3','m','M','marketplace','market','Market','Store','store','shop','Shop','SHOPPING!!!','s','S']:
                marketplace = Marketplace('justastore', pc.level)
                option = marketplace.welcome()
                marketplace.resolve(pc, option)

            else:
                dprint('Invalid input. ')
                dprint('Keep playing? Y/N')
                user = input()
                if user in ['N','n','Quit','quit','q','Q','Exit','exit','No','no','False','false','f','0','stop']:
                    playing = False
    
    def reset_monsters(self):
        self.mon_list = init_enemies()
        self.world_monsters = [mon for mon in self.mon_list if 1 in mon.world]

