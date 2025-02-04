
from actions import *
from monsters import init_enemies


class Battle:
    def __init__(self, player, xp_thresholds):
        self.active_player = player
        self.xp_thresholds = xp_thresholds
        self.type = 0
        self.active_monsters = []
        self.active_teamates = [self.active_player]
        self.name = 'battle'
        self.battle_options = ['attack', 'special', 'item', 'run', 'auto/controlled']
        self.all_monsters = init_enemies()
    
    def run(self, player=None, world=None, xp_thresholds=None):
        return self.regular([monster for monster in self.all_monsters if monster.name in player.monsters_seen])

    def regular(self, mon_list):
        # define the initial participants of this particular battle
        boss_dialog = None
        if not self.init_parti(mon_list, True, True, False, mon_list):
            return True
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
            if seconds % 1000 == 1:
                round_num += 1
                dprint(f'Round {round_num}, FIGHT! ')
            # handle the player's turn
            ran = self.handle_fighter_turn(seconds, boss_dialog)
            if ran:
                self.active_monsters.clear()
            # go through the ally's turns
            self.handle_ally_turns(seconds, boss_dialog)
            # handle the monster's turns
            self.handle_monster_turns(seconds)
            if not self.active_player.is_alive():
                self.active_teamates.clear()
                return False # tell the game the player is dead
            # add monsters to the battle if it lasts too long
            self.handle_additional_monsters(seconds, mon_list)
            # increment seconds
            seconds += 1
        
        self.active_teamates.clear()
        return True # tell the game the player is still alive

    # def boss(self, mon_list:list, dialog=None, collective=True, surprise=False, boss_dialog=['']):
    #     for mon in mon_list:
    #         self.active_monsters.append(mon)
        
    #     self.active_teamates.append(self.active_player)
    #     for ally in self.active_player.allies:
    #         if ally not in self.active_teamates:
    #             self.active_teamates.append(ally)

    #     seconds = 1
    #     round_num = 0
    #     if self.active_player.mag != self.active_player.maxmag:
    #         self.active_player.mag += 1 + self.active_player.level
    #         if self.active_player.mag > self.active_player.maxmag:
    #             self.active_player.mag = self.active_player.maxmag
        
    #     dialog
    #     input('Ready?')

    #     if len(self.active_monsters) > 1:
    #         dprint(f'The {self.active_monsters[-1].name} {self.active_monsters[-1].title} and its minions attack!')
    #     else:
    #         dprint(f'The {self.active_monsters[-1].name} {self.active_monsters[-1].title} attacks!')

    #     while True:
    #         # handle the rounds
    #         if seconds % 1000 == 1:
    #             round_num += 1
    #             dprint(f'Round {round_num}, FIGHT! ')

    #         # handle the player's turn
    #         self.handle_fighter_turn(seconds, boss_dialog=boss_dialog)
    #         # go through the ally's turns
    #         self.handle_ally_turns(seconds)

    #         if len(self.active_monsters) == 0:
    #             self.active_teamates.clear()
    #             return True
            
    #         if len(self.active_monsters) == 0:
    #             self.active_teamates.clear()
    #             return True

    #         # handle the boss's and minions' turns
    #         self.handle_monster_turns(seconds)
    #         if not self.active_player.is_alive():
    #             self.active_teamates.clear()
    #             return False # tell the game the player is dead
    #         self.handle_boss_turns(seconds)
    #         if not self.active_player.is_alive():
    #             self.active_teamates.clear()
    #             return False # tell the game the player is dead
            
    #         seconds += 1

    # def story(self, mon_list:list, dialog=None, collective=False, surprise=False, boss_dialog=None):
    #     to_use_mons = []
    #     for mon in mon_list:
    #         to_use_mons.append(mon)

    #     if collective:
    #         for _ in range(len(to_use_mons)):
    #             self.active_monsters.append(to_use_mons.pop())
    #     else:
    #         self.active_monsters.append(to_use_mons.pop())
        
    #     self.active_teamates.append(self.active_player)
    #     for ally in self.active_player.allies:
    #         if ally not in self.active_teamates:
    #             self.active_teamates.append(ally)

    #     seconds = 1
    #     round_num = 0
    #     if self.active_player.mag != self.active_player.maxmag:
    #         self.active_player.mag += 1 + self.active_player.level
    #         if self.active_player.mag > self.active_player.maxmag:
    #             self.active_player.mag = self.active_player.maxmag

    #     dialog

    #     if collective:
    #         dprint('Enemies move in to attack!')
    #     else:
    #         dprint(f'A {self.active_monsters[-1].name} moves in to attack!')

    #     while True:
    #         # handle the rounds
    #         if seconds % 1000 == 1:
    #             round_num += 1
    #             dprint(f'Round {round_num}, FIGHT!')

    #         if surprise:
    #             dprint('Surprise attack!')
    #             ran = self.handle_fighter_turn(self.active_player.agi)
    #             if ran:
    #                 to_use_mons.clear()
    #             surprise = False

    #         # handle the player's turn
    #         ran = self.handle_fighter_turn(seconds)
    #         if ran:
    #             to_use_mons.clear()
    #         # go through the ally's turns
    #         self.handle_ally_turns(seconds)

    #         if len(to_use_mons) == 0 and len(self.active_monsters) == 0:
    #             self.active_teamates.clear()
    #             return True
    #         if len(self.active_monsters) == 0:
    #             self.active_monsters.append(to_use_mons.pop())
    #             dprint(f'A {self.active_monsters[-1].name} closes in!')
            
    #         # handle the monster's turns
    #         self.handle_monster_turns(seconds)
    #         if not self.active_player.is_alive():
    #             self.active_teamates.clear()
    #             return False # tell the game the player is dead
            
    #         seconds += 1

    def battle(self, mon_list: list, dialog=None, collective=False, surprise=False, boss_dialog=None):
        # Initialize monsters
        to_use_mons = mon_list.copy()  # Create a copy of the monster list
        is_boss = False
        for mon in mon_list:
            if hasattr(mon, 'phases'):
                is_boss = True

        self.init_parti(mon_list, False, collective, is_boss, to_use_mons)

        # Adjust player's magic stat
        if self.active_player.mag != self.active_player.maxmag:
            self.active_player.mag += 1 + self.active_player.level
            if self.active_player.mag > self.active_player.maxmag:
                self.active_player.mag = self.active_player.maxmag

        # Display dialog
        if dialog:
            dialog()

        # Display battle start message
        if is_boss:
            if len(self.active_monsters) > 1:
                for mon in self.active_monsters:
                    if hasattr(mon, 'title'):
                        dprint(f'The {mon.name} {mon.title} and its minions attack!')
            else:
                dprint(f'The {self.active_monsters[-1].name} {self.active_monsters[-1].title} attacks!')
        else:
            if collective:
                dprint('Enemies move in to attack!')
            else:
                dprint(f'A {self.active_monsters[-1].name} moves in to attack!')

        # Battle loop
        seconds = 1
        round_num = 0
        while True:
            # Handle rounds
            if seconds % 1000 == 1:
                round_num += 1
                dprint(f'Round {round_num}, FIGHT!')

            # Handle surprise attacks (story battles only)
            if surprise and not is_boss:
                dprint('Surprise round!')
                ran = self.handle_fighter_turn(self.active_player.agi)
                if ran:
                    to_use_mons.clear()
                    self.active_monsters.clear()
                surprise = False

            # Handle player's turn
            ran = self.handle_fighter_turn(seconds, boss_dialog=boss_dialog if is_boss else None)
            if ran and not is_boss:
                to_use_mons.clear()
                self.active_monsters.clear()

            # Handle ally turns
            self.handle_ally_turns(seconds, boss_dialog)

            # Check win condition
            if len(to_use_mons) == 0 and len(self.active_monsters) == 0:
                self.active_teamates.clear()
                return True

            # Add new monsters for story battles
            if not is_boss and len(self.active_monsters) == 0 and to_use_mons:
                self.active_monsters.append(to_use_mons.pop())
                dprint(f'A {self.active_monsters[-1].name} closes in!')

            # Handle monster turns
            self.handle_monster_turns(seconds)
            if not self.active_player.is_alive():
                self.active_teamates.clear()
                return False

            # Handle boss turns (boss battles only)
            if is_boss:
                self.handle_boss_turns(seconds)
                if not self.active_player.is_alive():
                    self.active_teamates.clear()
                    return False

            seconds += 1

    def handle_fighter_turn(self, seconds, boss_dialog=['']):
        if seconds % self.active_player.agi == 0:
            # prompt for battle option
            for i in range(len(self.battle_options)):
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
                if target.has_phases:
                    if target.hp <= 0:
                        if target.next_phase(self.active_player, boss_dialog, self.xp_thresholds):
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
                if target.has_phases:
                    if target.hp <= 0:
                        if target.next_phase(self.active_player, boss_dialog, self.xp_thresholds):
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
                if target.has_phases:
                    if target.hp <= 0:
                        if target.next_phase(self.active_player, boss_dialog, self.xp_thresholds):
                            self.active_monsters.remove(target)
            
            elif option in ['4','run','Run','RUN','rUN','r','R','4: run','four','nigero','flee']:
                escape = sum(1 for _ in self.active_monsters if self.active_player.run())
                monster_count = len(self.active_monsters)
                match (monster_count, escape):
                    case (m, e) if e == m:
                        dprint(f'{self.active_player.name} escaped!')
                    case (m, e) if e == m - 1:
                        dprint(f'{self.active_player.name} made a narrow escape!')
                    case (m, e) if m >= 4 and e == m - 2:
                        dprint(f'{self.active_player.name} barely escaped with their life!')
                    case (m, e) if m >= 4 and e == m - 3:
                        dprint('Wow... miracles really do happen, don\'t they!')
                    case _:
                        dprint(f'{self.active_player.name} failed their escape attempt.')
                        return False
                if escape > 0:
                    self.active_monsters.clear()
                return True

            else:
                self.active_player.auto_battle = not self.active_player.auto_battle

    def handle_ally_turns(self, seconds, boss_dialog):
        for ally in self.active_player.allies:
            if seconds % ally.agi == 0 and len(self.active_monsters):
                target = ally.choose_target(self.active_monsters)
                ally.take_turn(target, self.active_player)
                if target.has_phases:
                    if target.hp <= 0:
                        if target.next_phase(self.active_player, boss_dialog, self.xp_thresholds):
                            self.active_monsters.remove(target)
                if not target.is_alive():
                    if target in self.active_monsters:
                        self.active_monsters.remove(target)
                    self.active_player.gain_xp(ceil(target.xp / (len(self.active_teamates))), self.xp_thresholds)

    def handle_monster_turns(self, seconds):
        for monster in self.active_monsters:
            if seconds % monster.agi == 0:
                target = monster.choose_target(self.active_teamates)
                if target is None:
                    break
                monster.attack(target)
                if not target.is_alive():
                    if target in self.active_teamates:
                        self.active_teamates.remove(target)
                    try:
                        self.active_player.allies.remove(target)
                    except ValueError as value_error:
                        self.active_player.allies.append(target) # do nothing agi
                        self.active_player.allies.remove(target)
    
    def handle_boss_turns(self, seconds):
        for monster in self.active_monsters:
            if monster.has_phases:
                if seconds % monster.agi == 0:
                    target = monster.choose_target(self.active_teamates)
                    monster.fight(target)
                    if not target.is_alive():
                        if target in self.active_teamates:
                            self.active_teamates.remove(target)
                        try:
                            self.active_player.allies.remove(target)
                        except ValueError as value_error:
                            self.active_player.allies.append(target) # do nothing
                            self.active_player.allies.remove(target)

    def handle_additional_monsters(self, seconds, mon_list):
        if seconds % 6000 == 0:
            self.active_monsters.append(choose_monster(self.active_player,mon_list))
            dprint('The sound of battle and the smell of blood atracts')
            dprint(f'a {self.active_monsters[-1].name} which joins the fight!')

    def init_parti(self, mon_list, rand, collective, is_boss, to_use_mons):
        if not mon_list:
            dprint('You have no idea how to fight!')
            return False
        
        self.active_teamates.append(self.active_player)
        for ally in self.active_player.allies:
            if ally not in self.active_teamates:
                self.active_teamates.append(ally)
        if rand:
            self.active_monsters.append(choose_monster(self.active_player, mon_list))
        else:
            if is_boss or collective:
                # Add all monsters at once for boss battles or collective story battles
                self.active_monsters.extend(to_use_mons)
                to_use_mons.clear()
            else:
                # Add one monster at a time for regular story battles
                self.active_monsters.append(to_use_mons.pop())

        # remove any duplicates that may have possibly occured at any point ever
        # (I'm so freaking done with this issue)
        unique_teamates = set()
        for ally in self.active_teamates:
            unique_teamates.add(ally)
        final_team = list(unique_teamates)

        self.active_teamates = final_team
        self.active_player.allies.clear()
        for ally in self.active_teamates:
            self.active_player.allies.append(ally)
        self.active_player.allies.remove(self.active_player)
        return True

