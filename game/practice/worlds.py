
from actions import *
from players import Fighter
from monsters import init_enemies, drops
from misc import Hospital, Marketplace, Gym, Quit
from story import *


skills = init_skills()
allies = init_allies()


class SaveLoad:
    def __init__(self, xp_thresholds) -> None:
        self.name = 'Save/Load'
        self.xp_thresholds = xp_thresholds
    
    def run(self, player=None, world=None, xp_thresholds=None):
        if os.path.exists('save_game.json') and player != None:
            dprint('1: Save\n2: Load\n3: Erase save\n4: Return\n')
            user = input().strip().lower()
            if user in ['','s','save','1','o','one','w','d','x','z','a','q','1: save']:
                return self.save(player=player)
            elif user in ['l','load','2','t','two','r','f','g','y','6','5','2: load']:
                try:
                    return self.load(player=player, xp_thresholds=xp_thresholds)
                except json.decoder.JSONDecodeError as err:
                    dprint('The file was currupted!')
                    print(f'{err}\n\n')
                    dprint(' . . . ',.085)
                    dprint('Returning . . .')
                    return True
            elif user in ['e','3','erase','es','erase save','three','t','del','3: erase save']:
                os.remove('save_game.json')
                return True
            else:
                return True
        elif player != None:
            self.save(player=player)
            return True
        else:
            return True
            
    def save(self, filename='save_game.json', player:Fighter=None):
        if os.path.exists(filename):
            os.remove(filename)
        player_data = {
            'name': player.name,
            'gender': player.gender,
            'hp': player.hp,
            'atk': player.atk,
            'xp': player.xp,
            'level': player.level,
            'accuracy': player.accuracy,
            'col': player.col,
            'progress': player.progress,
            'asleep': player.asleep,
            'poisoned': player.poisoned,
            'blessed': player.blessed,
            'confused': player.confused,
            'frightened': player.frightened,
            'enranged': player.enranged,
            'focussed': player.focussed,
            'defended': player.defended,
            'empowered': player.empowered,
            'weakened': player.weakened,
            'energized': player.energized,
            'auto_battle': player.auto_battle,
            'title': player.title,
            'acu': player.acu,
            'agi': player.agi,
            'mag': player.mag,
            'maxmag': player.maxmag,
            'skill_slots': player.skill_slots,
            'known_skills': [skill.name for skill in player.known_skills],
            'allies': [ally.designation for ally in player.allies],
            'inventory': {item.name: count for item, count in player.inventory.contents.items()},
            'location': player.location,
            # Add other necessary attributes
        }
    
        with open(filename, 'w') as save_file:
            json.dump(player_data, save_file, indent=4)
        print(f"Game saved to {filename}.")
        return True

    def load(self, filename='save_game.json', player:Fighter=None):
        try:
            with open(filename, 'r') as save_file:
                player_data = json.load(save_file)
                # Recreate player object based on saved data
                player = Fighter(
                    name=player_data['name'],
                    gender=player_data['gender'],
                    hp=player_data['hp'],
                    atk=player_data['atk'],
                    xp=0,
                    level=player_data['level'], 
                    accuracy=player_data['accuracy'],
                    col=player_data['col'],
                    progress=player_data['progress'],
                    asleep=player_data['asleep'],
                    poisoned=player_data['poisoned'],
                    blessed=player_data['blessed'],
                    confused=player_data['confused'],
                    frightened=player_data['frightened'], 
                    enranged=player_data['enranged'],
                    focussed=player_data['focussed'],
                    defended=player_data['defended'],
                    empowered=player_data['empowered'],
                    weakened=player_data['weakened'],
                    energized=player_data['energized'],
                    auto_battle=player_data['auto_battle'],
                    title=player_data['title'],
                    acu=player_data['acu'],
                    agi=player_data['agi'],
                    mag=player_data['mag'],
                    maxmag=player_data['maxmag'],
                    skill_slots=player_data['skill_slots'], 
                    known_skills=[0],
                    location=player_data['location']
                )
                player.known_skills.pop()
                for s in player_data['known_skills']:
                    player.add_skill_by_name(skills, s)
                for i, c in player_data['inventory'].items():
                    player.inventory.add_item_by_name(drops, i, count=c)
                for a_d in player_data['allies']:
                    player.add_ally_by_name(allies, a_d)
                player.gain_xp_quietly(player_data['xp'], self.xp_thresholds)

                print(f"Game loaded from {filename}.")
                return True
        except FileNotFoundError:
            print(f"No save file found at {filename}.")
            return True


class WorldOne:
    def __init__(self, name, xp_thresholds):
        self.name = name
        self.number = 1
        self.mon_list = init_enemies()
        self.world_monsters = [monster for monster in self.mon_list if 1 in monster.world]
        self.xp_thresholds = xp_thresholds
        self.pc = self.create_character()
        self.book_one = BookOne(self.pc, self.xp_thresholds)
        self.world_options = self.update_world_options()
    
    def create_character(self):
        if os.path.exists('save_game.json'):
            dprint('You have a save file available. \nLoad? \n1: Y \n2: N')
            uload = input().strip().lower()
            if uload in ['0','1','','!',')','q','`','y','t','g','h','u','6','7','yes','l','load','?','1: y','1: yes','1:y','sure','s','i would like to load the file thank you','one','uno','e','w','3','load? 1: y']:
                pc = self.load('save_game.json')
                if pc == None:
                    pass
                else:
                    return pc
        dprint('What is your name: ')
        pname = input()
        dprint(f'Is {pname} male or female?')
        ugender = input().strip().lower()
        if ugender in ['2','f','3','female','fe','iron','not male','girl','g','ggs',f'{pname} is a female.','d','r','c','v','t','i','q','w','e','6','x','xx','fem','two','too','lady','l','wow, a lady knight!']:
            pgender = 'Female'
        else:
            pgender = 'Male'
        if pname == 'admin':
            pc = Fighter(pname, pgender, 5000, 600, 0, 100, .96, 10000)
            return pc
        if pname == 'debug':
            pc = Fighter(pname, pgender, 23, 4, 300, 3, .755, 30, 7)
            return pc
        else:
            pc = Fighter(pname, pgender, 10, 2, 0, 1, .69, 3)
            return pc

    def save(self, filename='save_game.json'):
        if os.path.exists(filename):
            os.remove(filename)
        player_data = {
            'name': self.pc.name,
            'gender': self.pc.gender,
            'hp': self.pc.hp,
            'atk': self.pc.atk,
            'xp': self.pc.xp,
            'level': self.pc.level,
            'accuracy': self.pc.accuracy,
            'col': self.pc.col,
            'progress': self.pc.progress,
            'asleep': self.pc.asleep,
            'poisoned': self.pc.poisoned,
            'blessed': self.pc.blessed,
            'confused': self.pc.confused,
            'frightened': self.pc.frightened, 
            'enranged': self.pc.enranged,
            'focussed': self.pc.focussed,
            'defended': self.pc.defended,
            'empowered': self.pc.empowered,
            'weakened': self.pc.weakened,
            'energized': self.pc.energized,
            'auto_battle': self.pc.auto_battle,
            'title': self.pc.title,
            'acu': self.pc.acu,
            'agi': self.pc.agi,
            'mag': self.pc.mag,
            'maxmag': self.pc.maxmag,
            'skill_slots': self.pc.skill_slots,
            'known_skills': [skill.name for skill in self.pc.known_skills],
            'allies': [ally.designation for ally in self.pc.allies],
            'inventory': {item.name: count for item, count in self.pc.inventory.contents.items()},
            'location': self.pc.location,
            # Add other necessary attributes
        }
    
        with open(filename, 'w') as save_file:
            json.dump(player_data, save_file, indent=4)
        print(f"Game saved to {filename}.")

    def load(self, filename):
        try:
            with open(filename, 'r') as save_file:
                try:
                    player_data = json.load(save_file)
                except json.decoder.JSONDecodeError as err:
                    dprint('The file was currupted!')
                    print(f'{err}\n\n')
                    dprint(' . . . ',.085)
                    dprint('Creating new character . . .')
                    return None
                # Recreate player object based on saved data
                player = Fighter(
                    name=player_data['name'],
                    gender=player_data['gender'],
                    hp=player_data['hp'],
                    atk=player_data['atk'],
                    xp=0,
                    level=player_data['level'], 
                    accuracy=player_data['accuracy'],
                    col=player_data['col'],
                    progress=player_data['progress'],
                    asleep=player_data['asleep'],
                    poisoned=player_data['poisoned'],
                    blessed=player_data['blessed'],
                    confused=player_data['confused'],
                    frightened=player_data['frightened'], 
                    enranged=player_data['enranged'],
                    focussed=player_data['focussed'],
                    defended=player_data['defended'],
                    empowered=player_data['empowered'],
                    weakened=player_data['weakened'],
                    energized=player_data['energized'],
                    auto_battle=player_data['auto_battle'],
                    title=player_data['title'],
                    acu=player_data['acu'],
                    agi=player_data['agi'],
                    mag=player_data['mag'], 
                    known_skills=[0],
                    maxmag=player_data['maxmag'],
                    skill_slots=player_data['skill_slots'],
                    location=player_data['location']
                )
                player.known_skills.pop()
                for s in player_data['known_skills']:
                    player.add_skill_by_name(skills, s)
                for i, c in player_data['inventory'].items():
                    player.inventory.add_item_by_name(drops, i, count=c)
                for a_d in player_data['allies']:
                    player.add_ally_by_name(allies, a_d)
                player.gain_xp_quietly(player_data['xp'], self.xp_thresholds)

                print(f"Game loaded from {filename}.")
                return player
        except FileNotFoundError:
            print(f"No save file found at {filename}.")
            return None

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
        save_load = SaveLoad(self.xp_thresholds)
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
        
        world_options.append(save_load)
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
    
    def reset_monsters(self):
        self.mon_list = init_enemies()
        self.world_monsters = [mon for mon in self.mon_list if 1 in mon.world]

