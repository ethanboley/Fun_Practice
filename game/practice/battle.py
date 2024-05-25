
from actions import *
from monsters import init_enemies


class Battle:
    def __init__(self, active_player, xp_thresholds):
        self.active_player = active_player
        self.xp_thresholds = xp_thresholds
        self.type = 0
        self.active_monsters = []
        self.active_teamates = []
        self.name = 'battle'
        self.battle_options = ['attack', 'special', 'item', 'run']
        self.all_monsters = init_enemies()

    def regular(self, mon_list):
        # define the initial participants of this particular battle
        self.init_parti(mon_list)
        # set seconds to 1
        seconds = 1
        # set round num to 1
        round_num = 0
        # set player mag val
        if self.active_player.mag != self.active_player.maxmag:
            self.active_player.mag += 1 + self.active_player.level
            if self.active_player.mag >= self.active_player.maxmag:
                self.active_player.mag = self.active_player.maxmag
        # describe the encounter
        dprint(f'You encounter a {self.active_monsters[-1].name}!')
    
        # begin battle
        while self.active_player.is_alive() and len(self.active_monsters) != 0:
            # handle the rounds
            if seconds % 20 == 1:
                round_num += 1
                dprint(f'Round {round_num}, FIGHT! ')
            # handle the player's turn
            if self.active_player.title == 'Fighter':
                self.handle_fighter_turn(seconds)
            elif self.active_player.title == 'Mage':
                self.handle_mage_turn(seconds)
            elif self.active_player.title == 'Pugilist':
                self.handle_pugilist_turn(seconds)
            elif self.active_player.title == 'tamer':
                self.handle_tamer_turn(seconds)
            # go through the ally's turns
            self.handle_ally_turns(seconds)
            # handle the monster's turns
            self.handle_monster_turns(seconds)
            if not self.active_player.is_alive():
                return False # tell the game the player is dead
            # add monsters to the battle if it lasts too long
            self.handle_additional_monsters(seconds, mon_list)
            # increment seconds
            seconds += 1
        
        return True # tell the game the player is still alive

    def boss(self, mon_list):
        self.init_parti(mon_list)
    
    def story(self, mon_list:list, dialog=None):
        to_use_mons = []
        for mon in mon_list:
            to_use_mons.append(mon)
        self.active_monsters.append(to_use_mons.pop())
        seconds = 1
        round_num = 0
        if self.active_player.mag != self.active_player.maxmag:
            self.active_player.mag += 1 + self.active_player.level
            if self.active_player.mag >= self.active_player.maxmag:
                self.active_player.mag = self.active_player.maxmag
        dialog

        dprint(f'A {self.active_monsters[-1].name} moves in to attack!')

        # while self.active_player.is_alive():
        while True:
            # handle the rounds
            if seconds % 20 == 1:
                round_num += 1
                dprint(f'Round {round_num}, FIGHT! ')
                # for i in range(len(to_use_mons)):
                #     dprint(to_use_mons[i].name)
            # handle the player's turn
            if self.active_player.title == 'Fighter':
                self.handle_fighter_turn(seconds)
            elif self.active_player.title == 'Mage':
                self.handle_mage_turn(seconds)
            elif self.active_player.title == 'Pugilist':
                self.handle_pugilist_turn(seconds)
            elif self.active_player.title == 'tamer':
                self.handle_tamer_turn(seconds)
            if len(to_use_mons) == 0 and len(self.active_monsters) == 0:
                return True
            if len(self.active_monsters) == 0:
                self.active_monsters.append(to_use_mons.pop())
                dprint(f'A {self.active_monsters[-1].name} closes in!')
            # go through the ally's turns
            self.handle_ally_turns(seconds)
            # handle the monster's turns
            self.handle_monster_turns(seconds)
            if not self.active_player.is_alive():
                return False # tell the game the player is dead
            seconds += 1

    def handle_fighter_turn(self, seconds):
        if seconds % self.active_player.agi == 0:
            # prompt for battle option
            for i in range(4):
                print(f'{i + 1}: {self.battle_options[i]}')
            option = input()

            if option in ['','1','0','f','F','fight','Fight','FIGHT','attack','a','A','Y','y','yes']:
                # define target
                if len(self.active_monsters) == 1:
                    target = self.active_monsters[-1]
                else:
                    dprint('target which monster')
                    target = get_list_option(self.active_monsters)
                
                # adjust player skill cooldown ??? 
                for skill in self.active_player.known_skills:
                    if skill.downtime < skill.cooldown:
                        skill.downtime += 1

                # attack
                self.active_player.attack(target, self.xp_thresholds)
                # update active monsters
                if not target.is_alive():
                    self.active_monsters.remove(target)

            elif option in ['2','Skill','skill','s','S','spell','Spell','SKILL','SPELL']:
                # define the target
                if len(self.active_monsters) == 1:
                    target = self.active_monsters[-1]
                else:
                    dprint('target which monster')
                    target = get_list_option(self.active_monsters)
                # special attack
                self.active_player.special_attack(target, self.xp_thresholds)
                # update active monsters
                if not target.is_alive():
                    self.active_monsters.remove(target)
            
            elif option in ['3', 'item', 'Item', 'i', 'I', 'bag', 'Bag', 'b', 'B']:
                # define the target
                if len(self.active_monsters) == 1:
                    target = self.active_monsters[-1]
                else:
                    dprint('target which monster')
                    target = get_list_option(self.active_monsters)
                # use item
                self.active_player.use_item(target, self.xp_thresholds)
                # update active monsters
                if not target.is_alive():
                    self.active_monsters.remove(target)
            
            else:
                escape = 0
                for i in range(len(self.active_monsters)):
                    if self.active_player.run():
                        escape += 1
                if len(self.active_monsters) == 1 and escape == 1:
                    dprint(f'{self.active_player.name} escaped!')
                    self.active_monsters.clear()
                elif len(self.active_monsters) == 2:
                    if escape == 1:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 2:
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                elif len(self.active_monsters) == 3:
                    if escape == 2:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 3:
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                elif len(self.active_monsters) == 4:
                    if escape == 2:
                        dprint(f'{self.active_player.name} barely escaped with their life!')
                        self.active_monsters.clear()
                    elif escape == 3:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 4: 
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                elif len(self.active_monsters) > 4:
                    if escape >= 6:
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                    elif escape == 5:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 4:
                        dprint(f'{self.active_player.name} barely escaped with their life!')
                        self.active_monsters.clear()
                    elif escape == 3:
                        dprint('Wow... miracles really do happen!')
                        self.active_monsters.clear()
                else:
                    dprint(f'{self.active_player.name} failed their escape attempt.')

    def handle_mage_turn(self, seconds):
        if seconds % self.active_player.agi == 0:
            # prompt for battle option
            for i in range(4):
                print(f'{i + 1}: {self.battle_options[i]}')    
            option = input()

            if option in ['','1','0','f','F','fight','Fight','FIGHT','attack','a','A','Y','y','yes']:
                # define target
                if len(self.active_monsters) == 1:
                    target = self.active_monsters[-1]
                else:
                    dprint('target which monster')
                    target = get_list_option(self.active_monsters)
                
                # adjust mage spell cooldown ??? 
                for spell in self.active_player.known_spells:
                    if spell.downtime < spell.cooldown:
                        spell.downtime += 1

                # attack
                self.active_player.attack(target, self.xp_thresholds)
                # update active monsters
                if not target.is_alive():
                    self.active_monsters.remove(target)

            elif option in ['2','Skill','skill','s','S','spell','Spell','SKILL','SPELL']:
                # define the target
                if len(self.active_monsters) == 1:
                    target = self.active_monsters[-1]
                else:
                    dprint('target which monster')
                    target = get_list_option(self.active_monsters)
                # special attack
                self.active_player.special_attack(target, self.xp_thresholds)
                # update active monsters
                if not target.is_alive():
                    self.active_monsters.remove(target)
            
            elif option in ['3', 'item', 'Item', 'i', 'I', 'bag', 'Bag', 'b', 'B']:
                # define the target
                if len(self.active_monsters) == 1:
                    target = self.active_monsters[-1]
                else:
                    dprint('target which monster')
                    target = get_list_option(self.active_monsters)
                # use item
                self.active_player.use_item(target, self.xp_thresholds)
                # update active monsters
                if not target.is_alive():
                    self.active_monsters.remove(target)
            
            else:
                escape = 0
                for i in range(len(self.active_monsters)):
                    if self.active_player.run():
                        escape += 1
                if len(self.active_monsters) == 1 and escape == 1:
                    dprint(f'{self.active_player.name} escaped!')
                    self.active_monsters.clear()
                elif len(self.active_monsters) == 2:
                    if escape == 1:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 2:
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                elif len(self.active_monsters) == 3:
                    if escape == 2:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 3:
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                elif len(self.active_monsters) == 4:
                    if escape == 2:
                        dprint(f'{self.active_player.name} barely escaped with their life!')
                        self.active_monsters.clear()
                    elif escape == 3:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 4: 
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                elif len(self.active_monsters) > 4:
                    if escape >= 6:
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                    elif escape == 5:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 4:
                        dprint(f'{self.active_player.name} barely escaped with their life!')
                        self.active_monsters.clear()
                    elif escape == 3:
                        dprint('Wow... miracles really do happen!')
                        self.active_monsters.clear()
                else:
                    dprint(f'{self.active_player.name} failed their escape attempt.')

    def handle_pugilist_turn(self, seconds):
        if seconds % self.active_player.agi == 0:
            # prompt for battle option
            for i in range(4):
                print(f'{i + 1}: {self.battle_options[i]}')    
            option = input()

            if option in ['','1','0','f','F','fight','Fight','FIGHT','attack','a','A','Y','y','yes']:
                # define target
                if len(self.active_monsters) == 1:
                    target = self.active_monsters[-1]
                else:
                    dprint('target which monster')
                    target = get_list_option(self.active_monsters)
                
                # adjust pugilist spall cooldown ??? 
                for spall in self.active_player.known_spalls:
                    if spall.downtime < spall.cooldown:
                        spall.downtime += 1

                # attack
                self.active_player.attack(target, self.xp_thresholds)
                # update active monsters
                if not target.is_alive():
                    self.active_monsters.remove(target)

            elif option in ['2','Skill','skill','s','S','spall','Spall','SKILL','SPALL','spell']:
                # define the target
                if len(self.active_monsters) == 1:
                    target = self.active_monsters[-1]
                else:
                    dprint('target which monster')
                    target = get_list_option(self.active_monsters)
                # special attack
                self.active_player.special_attack(target, self.xp_thresholds)
                # update active monsters
                if not target.is_alive():
                    self.active_monsters.remove(target)
            
            elif option in ['3', 'item', 'Item', 'i', 'I', 'bag', 'Bag', 'b', 'B']:
                # define the target
                if len(self.active_monsters) == 1:
                    target = self.active_monsters[-1]
                else:
                    dprint('target which monster')
                    target = get_list_option(self.active_monsters)
                # use item
                self.active_player.use_item(target, self.xp_thresholds)
                # update active monsters
                if not target.is_alive():
                    self.active_monsters.remove(target)
            
            else:
                escape = 0
                for i in range(len(self.active_monsters)):
                    if self.active_player.run():
                        escape += 1
                if len(self.active_monsters) == 1 and escape == 1:
                    dprint(f'{self.active_player.name} escaped!')
                    self.active_monsters.clear()
                elif len(self.active_monsters) == 2:
                    if escape == 1:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 2:
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                elif len(self.active_monsters) == 3:
                    if escape == 2:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 3:
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                elif len(self.active_monsters) == 4:
                    if escape == 2:
                        dprint(f'{self.active_player.name} barely escaped with their life!')
                        self.active_monsters.clear()
                    elif escape == 3:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 4: 
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                elif len(self.active_monsters) > 4:
                    if escape >= 6:
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                    elif escape == 5:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 4:
                        dprint(f'{self.active_player.name} barely escaped with their life!')
                        self.active_monsters.clear()
                    elif escape == 3:
                        dprint('Wow... miracles really do happen!')
                        self.active_monsters.clear()
                else:
                    dprint(f'{self.active_player.name} failed their escape attempt.')

    def handle_tamer_turn(self, seconds):
        if seconds % self.active_player.agi == 0:
            # prompt for battle option
            for i in range(4):
                print(f'{i + 1}: {self.battle_options[i]}')    
            option = input()

            if option in ['','1','0','f','F','fight','Fight','FIGHT','attack','a','A','Y','y','yes']:
                # define target
                if len(self.active_monsters) == 1:
                    target = self.active_monsters[-1]
                else:
                    dprint('target which monster')
                    target = get_list_option(self.active_monsters)
                
                # adjust player skill cooldown ??? 
                for skill in self.active_player.known_skills:
                    if skill.downtime < skill.cooldown:
                        skill.downtime += 1

                # attack
                self.active_player.attack(target, self.xp_thresholds)
                # update active monsters
                if not target.is_alive():
                    self.active_monsters.remove(target)

            elif option in ['2','Skill','skill','s','S','spell','Spell','SKILL','SPELL']:
                # define the target
                if len(self.active_monsters) == 1:
                    target = self.active_monsters[-1]
                else:
                    dprint('target which monster')
                    target = get_list_option(self.active_monsters)
                # special attack
                self.active_player.special_attack(target, self.xp_thresholds)
                # update active monsters
                if not target.is_alive():
                    self.active_monsters.remove(target)
            
            elif option in ['3', 'item', 'Item', 'i', 'I', 'bag', 'Bag', 'b', 'B']:
                # define the target
                if len(self.active_monsters) == 1:
                    target = self.active_monsters[-1]
                else:
                    dprint('target which monster')
                    target = get_list_option(self.active_monsters)
                # use item
                self.active_player.use_item(target, self.xp_thresholds)
                # update active monsters
                if not target.is_alive():
                    self.active_monsters.remove(target)
            
            else:
                escape = 0
                for i in range(len(self.active_monsters)):
                    if self.active_player.run():
                        escape += 1
                if len(self.active_monsters) == 1 and escape == 1:
                    dprint(f'{self.active_player.name} escaped!')
                    self.active_monsters.clear()
                elif len(self.active_monsters) == 2:
                    if escape == 1:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 2:
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                elif len(self.active_monsters) == 3:
                    if escape == 2:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 3:
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                elif len(self.active_monsters) == 4:
                    if escape == 2:
                        dprint(f'{self.active_player.name} barely escaped with their life!')
                        self.active_monsters.clear()
                    elif escape == 3:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 4: 
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                elif len(self.active_monsters) > 4:
                    if escape >= 6:
                        dprint(f'{self.active_player.name} escaped!')
                        self.active_monsters.clear()
                    elif escape == 5:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                        self.active_monsters.clear()
                    elif escape == 4:
                        dprint(f'{self.active_player.name} barely escaped with their life!')
                        self.active_monsters.clear()
                    elif escape == 3:
                        dprint('Wow... miracles really do happen!')
                        self.active_monsters.clear()
                else:
                    dprint(f'{self.active_player.name} failed their escape attempt.')
    
    def handle_ally_turns(self, seconds):
        for ally in self.active_teamates:
            if seconds % ally.agi == 0:
                target = ally.take_turn()
                if not target.is_alive:
                    self.active_monsters.remove(target)

    def handle_monster_turns(self, seconds):
        for monster in self.active_monsters:
            if seconds % monster.agi == 0:
                monster.attack(self.active_player)

    def handle_additional_monsters(self, seconds, mon_list):
        if seconds % 120 == 0:
            self.active_monsters.append(choose_monster(self.active_player, mon_list))
            dprint('The sound of battle and the smell of blood atracts')
            dprint(f'a {self.active_monsters[-1].name} which joins the fight!')

    def init_parti(self, mon_list):
        for ally in self.active_player.allies:
            self.active_teamates.append(ally)
        self.active_monsters.append(choose_monster(self.active_player,mon_list))

