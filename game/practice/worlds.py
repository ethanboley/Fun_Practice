
# from actions import *
from players import Fighter
# from monsters import init_enemies, drops
from misc import Hospital, Marketplace, Gym, Alchemy, Quit
from story.book_1 import *
from story.book_2 import *
import pickle


skills = init_skills()
allies = init_allies()


class SaveLoad:
    def __init__(self, xp_thresholds) -> None:
        self.name = 'Save/Load'
        self.xp_thresholds = xp_thresholds
    
    def run(self, player=None, world=None, xp_thresholds=None):
        if os.path.exists('save_file.pkl') and player != None:
            dprint('1: Save\n2: Load\n3: Erase save\n4: Return\n')
            user = input().strip().lower()
            if user in ['','s','save','1','o','one','w','d','x','z','a','q','1: save']:
                return self.save(player=player)
            elif user in ['l','load','2','t','two','r','f','g','y','6','5','2: load']:
                try:
                    return self.load()
                except EOFError as err:
                    dprint('The file was currupted!')
                    print(f'{err}\n\n')
                    dprint(' . . . ',.085)
                    dprint('Returning . . .')
                    return True
                except pickle.UnpicklingError as err:
                    dprint('The file was currupted!')
                    print(f'{err}\n\n')
                    dprint(' . . . ',.085)
                    dprint('Returning . . .')
                    return True
            elif user in ['e','3','erase','es','erase save','three','t','del','3: erase save']:
                os.remove('save_file.pkl')
                return True
            else:
                return True
        elif player != None:
            self.save(player=player)
            return True
        else:
            return True
            
    def save(self, filename='save_file.pkl', player:Fighter=None):
        with open(filename, 'wb') as file:
            pickle.dump(player, file)
        return True

    def load(self, filename='save_file.pkl'):
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            print(f'No save file found at {filename}.')
            return None


class WorldOne:
    def __init__(self, name, xp_thresholds):
        self.name = name
        self.number = 1
        self.mon_list = init_enemies()
        self.world_monsters = [monster for monster in self.mon_list if 1 in monster.world]
        self.xp_thresholds = xp_thresholds
        self.pc = self.create_character()
        self.book_one = BookOne(self.pc, self.xp_thresholds)
        self.book_two = BookTwo(self.pc, self.xp_thresholds)
        self.world_options = self.update_world_options()

    def create_character(self):
        if os.path.exists('save_file.pkl'):
            dprint('You have a save file available. \nLoad? \n1: Y \n2: N')
            uload = input().strip().lower()
            if uload in ['0','1','','!',')','q','`','y','t','g','h','u','6','7','yes','l','load','?','1: y','1: yes','1:y','sure','s','i would like to load the file thank you','one','uno','e','w','3','load? 1: y']:
                pc = self.load('save_file.pkl')
                if pc != None:
                    return pc                    
        dprint('What is your name: ')
        pname = input()
        dprint(f'Is {pname} male or female?')
        ugender = input().strip().lower()
        if ugender in ['2','f','3','female','fe','iron','not male','girl','g','ggs',f'{pname} is a female.','d','r','c','v','t','i','q','w','e','6','x','xx','fem','two','too','lady','l','wow, a lady knight!','h']:
            pgender = 'Female'
        else:
            pgender = 'Male'
        if pname == '' and pgender == 'Female':
            pname = 'Reyna'
        elif pname == '' and pgender == 'Male':
            pname = 'Rowan'
        if pname == 'admin':
            print(f'hello {pname}, enter the book number you would like to skip to:')
            try:
                book = int(input().lower().strip())
            except ValueError:
                book = 1
            print(f'What would you actually like your name to be:')
            pname = input().strip()
            if book == 1:
                pc = Fighter(pname, pgender, 10, 2, 0, 1, 690, 3)
            if book == 2:
                print('In preparation, you need to be leveled properly as follows:')
                pc = Fighter(pname, pgender, 10, 2, 0, 1, 710, 100, progress=33)
                pc.gain_xp_quietly(3000, self.xp_thresholds)
            if book == 3:
                print('In preparation, you need to be leveled properly as follows:')
                pc = Fighter(pname, pgender, 10, 2, 0, 1, 720, 100, progress=67)
                pc.gain_xp_quietly(15000, self.xp_thresholds)
            else:
                pc = Fighter(pname, pgender, 10000, 5000, 0, 1, 999, 100000)
            return pc
        if pname == 'debug':
            pc = Fighter(pname, pgender, 23, 4, 300, 3, 755, 30, 7)
            return pc
        else:
            pc = Fighter(pname, pgender, 10, 2, 0, 1, 690, 3)
            return pc

    def save(self, filename='save_file.pkl'):
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, 'wb') as save_file:
            pickle.dump(self.pc, save_file)
        print(f'Game saved to {filename}.')

    def load(self, filename):
        try:
            with open('save_file.pkl', 'rb') as save_file:
                try:
                    player_data = pickle.load(save_file)
                except EOFError as err:
                    dprint('The file was currupted!')
                    print(f'{err}\n\n')
                    dprint(' . . . ',.085)
                    dprint('Creating new character . . .')
                    return None
                except pickle.UnpicklingError as err:
                    dprint('The file was currupted!')
                    print(f'{err}\n\n')
                    dprint(' . . . ',.085)
                    dprint('Creating new character . . .')
                    return None

                print(f'Game loaded from {filename}.')
                return player_data
        except FileNotFoundError:
            print(f'No save file found at {filename}.')
            return None

    def introdction(self):
        if self.pc.xp <= 0:
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
            self.pc.xp += 1

    def update_world_options(self):
        battle = Battle(self.pc,self.xp_thresholds)
        hospital = Hospital('greentown hospital', self.pc.level)
        market = Marketplace('greentown market', self.pc.level, self.xp_thresholds, self)
        gym = Gym(self.pc)
        save_load = SaveLoad(self.xp_thresholds)
        quit_game = Quit()
        alchemy = Alchemy()
        world_options = []

        if self.pc.progress == 0:
            world_options.append(self.book_one)
        if self.pc.progress > 0:
            world_options.append(self.book_one)
            world_options.append(battle)
            if self.pc.location in ['1-1','1-3']:
                world_options.append(hospital)
                world_options.append(market)
            if self.pc.level > 2:
                world_options.append(gym)
                if self.pc.level > 2 and (self.pc.location in ['1-1','1-3']):
                    world_options.append(hospital) if hospital not in world_options else None
                    world_options.append(market) if hospital not in world_options else None
                    pass
        if self.pc.progress >= 33:
            world_options.remove(self.book_one)
            world_options.insert(0, self.book_two)
        
        world_options.append(alchemy)
        world_options.append(save_load)
        world_options.append(quit_game)
        return world_options

    def world_loop(self):
        while True:
            print()
            dprint(f'<<------- {self.name} ------->>',.085)
            input(f'{self.pc.progress}/32 - {self.number}\n')

            self.world_options = self.update_world_options()

            action = get_list_option(self.world_options)

            playing = action.run(self.pc, self, self.xp_thresholds)

            if hasattr(playing, 'title'):
                self.pc = playing
                playing = self.pc.is_alive()
            if playing is None:
                playing == True
            if not playing:
                break
            self.pc.fix_team()
    
    def reset_monsters(self):
        self.mon_list = init_enemies()
        self.world_monsters = [mon for mon in self.mon_list if 1 in mon.world]

