
from actions import *
from monsters import init_doctors
from stuffs_that_do import init_items
from players import Fighter
from things_stuff import init_skills

items = init_items()

class Hospital:
    def __init__(self, name, quality):
        self.name = name
        self.quality = quality
    
    def run(self, player=None, world=None, xp_thresholds=None):
        return self.resolve(player,xp_thresholds, world)

    def welcome(self):
        options = ['healing', 'superheal', 'information', 'nothing']
        dprint(f'Welcome to {self.name}!')
        dprint(f'This hospital is a level {self.quality} facility. ')
        dprint('What seems to be the problem today! ')
        for i in range(len(options)):
            print(f'{i + 1}: {options[i]}')
        return input()

    def resolve(self, player, xp_thresholds, world):
        choice_task = self.welcome()

        if choice_task in ['healing','Healing','1','0','','h','H','reg']:
            self.heal(player, xp_thresholds)
            return True
        
        elif choice_task in ['superheal','Superheal','super heal','S','s','2','BIGBOI']:
            return self.superheal(player)

        elif choice_task in ['information','info','Information','Info','3','i','I']:
            self.give_info(player, xp_thresholds, world)
            return True
        
        else:
            return True

    def heal(self, player, xp_thresholds):
        cost = 1 + self.quality + (player.level // 3)
        dprint(f'Welcome to the {self.name} healing center! Good luck {player.name}! ')
        if player.col < cost:
            dprint(f'Oops, not enough money! You have {player.col} col, this service costs {cost} col.')
        elif player.level >= 85:
            dprint('Actually you\'re far to intimidating for our doctors, good bye!') 
        else:
            player.col -= cost
            round = 1
            healed = False
            while not healed:
                doctors = init_doctors()
                doc = choose_monster(player, doctors)
                dprint(f'your doctor will be {doc.name}')
                dprint(f'This is check number {round}.')
                while doc.is_alive():
                    doc.attack(player)
                    if player.hp >= player.maxhp:
                        player.hp = player.maxhp
                        dprint(f'{player.name} looks as good as new.')
                        healed = True
                        break
                    else:
                        display_health(player)
                        print()

                    player.hattack(doc)
                    if not doc.is_alive():
                        dprint(f'{doc.name} is going home for the day. ')
                        player.gain_xp(doc.xp, xp_thresholds)
                        break

                if round == 8 - player.level // 10:
                    dprint('It\'s closing time for the hospital.')
                    dprint(f'Rulid has {player.col} col')
                    break
                round += 1

    def superheal(self, player):
        cost = 5 + (self.quality // 2)
        dprint(f'Welcome to the {self.name} super healing booth.')
        dprint('here we don\'t use such foolish things like doctors and science.')
        dprint('we use the much more reasonable approach of,')
        dprint('lobbing potions at you until they work!')

        if player.col < cost:
            dprint(f'Not enough money, You have {player.col} col, this service costs {cost} col. ')
            return True
        else:
            player.col -= cost
            while True:
                dprint(f'How about this one! ')
                if random.random() > .8:
                    dprint('The potion worked!')
                    player.hp = player.maxhp
                    display_health(player)
                    dprint('Thanks for coming!')
                    return True
                elif random.random() > .55:
                    dprint('The potion worked ok.')
                    player.hp = player.maxhp - 5
                    display_health(player)
                    return True
                elif random.random() > .35:
                    dprint('Nope, \'nother dud!')
                else:
                    player.hp -= 1
                    dprint(f'The potioneer attacks {player.name} with a potion bottle for 1 damage!')
                    if player.is_alive():
                        display_health(player)
                    else:
                        dprint('You have died!')
                        return False

    def give_info(self, player, xp_thresholds:dict, world):
        next_thresh = xp_thresholds[player.level]
        low_atk = damage_calculator(atk=player.atk, level=player.level)
        atk = damage_calculator(atk=player.atk, level=player.level, crit=True)
        lowest = damage_calculator(atk=player.atk, level=player.level, f=player.weapon.force, crit=False, special=True)
        high_sptk = damage_calculator(atk=player.atk, level=player.level, power=player.known_skills[0].damage, f=player.weapon.force, crit=True, special=True)
        print()
        dprint(f'{player.name} is in world {world.number}: {world.name}')
        dprint(f'in the {self.name}.')
        dprint(f'{player.name} has the following stats:')
        print(f'Level: {player.level}')
        print(f'Experience Points: {player.xp}/{next_thresh}')
        print(f'Hit Points: {player.hp}/{player.maxhp}')
        print(f'Attack power: {low_atk}-{atk}')
        print(f'Skill attack power: {lowest}-{high_sptk}')
        print(f'Accuracy: {round((player.accuracy + player.acu) / 10, 2)}%')
        print(f'Speed: {1000 - player.agi}')
        print(f'Magic: {player.mag}/{player.maxmag}')
        print(f'Col: {player.col}')
        print('Skills:')
        for skill in player.known_skills:
            print(f'{skill.name.capitalize()} --> cost: {skill.cost}, cooldown: {skill.cooldown - skill.downtime}/{skill.cooldown}, power: {skill.damage}')
        print('Inventory:')
        player.inventory.display_contents()
        if player.level >= 6:
            print('Allies: ')
            for ally in player.allies:
                print(ally.name)
        print(f'Story progress: {player.progress}')


class Marketplace():
    def __init__(self, name, level, xp_thresholds, world):
        self.name = name
        self.level = level
        self.inventory = {}
        self.prices = {}
        self.salable = [item for item in items if item.sold]
        self.xp_thresholds = xp_thresholds
        self.world = world
    
    def run(self, player=None, world=None, xp_thresholds=None):
        return self.resolve(player)

    def stock_inventory(self):
        for item in self.salable:
            if item.level <= self.level:
                self.inventory[item] = self.level
    
    def welcome(self):
        options = ['sell','buy','information','black market']
        dprint('Welcome, young adventurer, to our humble marketplace')
        dprint(f'We are classified by our local government as a class {self.level}')
        dprint('market! Feel free to browse our wares or sell what you like!')
        dprint('What will be your business today?')
        self.stock_inventory()
        for i in range(len(options)):
            print(f'{i + 1}: {options[i]}')
        return input()
    
    def resolve(self, player):
        choice_task = self.welcome()

        if choice_task in ['','sell','Sell','SELL','1','S','s','0','buy from me!']:
            self.buy(player)
            dprint('Would you like to stay in the market?')
            user = input('1: Yes\n2: No\n')
        
            if user in ['','y','Y','1','0','Yes','YES','yes','sure']:
                return self.resolve(player)
            else:
                return True

        elif choice_task in ['2','Buy','buy','B','b','what have you got?']:
            self.sell(player)
            dprint('Would you like to stay in the market?')
            user = input('\n1: Yes \n2: No\n')
        
            if user in ['','y','Y','1','0','Yes','YES','yes','sure']:
                return self.resolve(player)
            else:
                return True

        elif choice_task in ['information','info','Information','Info','3','i','I']:
            self.give_info(player, self.xp_thresholds, self.world)
            dprint('Would you like to stay in the market?')
            user = input('\n1: Yes \n2: No\n')
        
            if user in ['','y','Y','1','0','Yes','YES','yes','sure']:
                return self.resolve(player)
            else:
                return True
        
        elif choice_task in ['Black Market', 'black market', 'm', 'M', '4', 'black', 'Black', 'market', 'b market', 'black m', 'bm', 'm', '...', 'you know what.']:
            survived = self.black_market(player)
            if survived:
                dprint('Would you like to stay in the market?')
                user = input('\n1: Yes \n2: No\n')

                if user in ['','y','Y','1','0','Yes','YES','yes','sure']:
                    return self.resolve(player)
                else: 
                    return True
            else:
                return False
        else:
            return True


    def buy(self, player): # in other words its the market place that's doing the buying
        dprint(f'Thank you, we\'d love to buy from you!')
        if len(player.inventory.contents) == 0:
            dprint('Actually, you don\'t have any items!')
            dprint('Good buy and fare well!')
        else:
            while True:
                dprint(f'Alrighty there, what have you got to sell?')
                if len(player.inventory.contents) == 0:
                    dprint('Oop, well, you don\'t actually have any more items!')
                    break
                dprint(f'You have {player.col} col!')
                to_sell = get_dict_option(player.inventory.contents)

                dprint(f'Let\'s see, this {to_sell.name} is worth {to_sell.sell_price} col.')
                dprint('Would you like to sell it?')
                choice = input('1: Yes \n2: No \n')
                if choice in ['', 'y', 'Y', 'yes', 'Yes', 'YES', '0', '1', 'of course!']:
                    player.inventory.remove_item(to_sell)
                    player.col += to_sell.sell_price
                    dprint(f'{player.name} has {player.col} col!')
                    dprint('would you like to sell more?')
                    choice = input('1: Yes \n2: No \n')
                    if choice not in ['', 'y', 'Y', 'yes', 'Yes', 'YES', '0', '1', 'of course!']:
                        break
                else:
                    print('not sellin\' huh, maybe something else?')


    def sell(self, player): # also here the player is buying from the market place get_dict
        dprint(f'Welcome! What would you like to buy?')
        if player.col == 0:
            dprint('Actually, you don\'t have any money!')
            dprint('Good buy and fare well!')
        else: 
            while True:
                dprint(f'Can I interest you in some exotic curios?')
                choice = input('1: Yes \n2: No \n')
                if choice in ['', 'y', 'Y', 'yes', 'Yes', 'YES', '0', '1', 'of course!']:
                    if player.col == 0:
                        dprint('Oop, well, you don\'t actually have any more money!')
                        break
                    dprint(f'You have {player.col} col!')
                    to_buy = get_dict_option(self.inventory)

                    if to_buy.sell_price > player.col:
                        dprint('That too expensive for you.')
                    else:
                        dprint(f'Ah, I see our {to_buy.name} interests you') 
                        dprint(f'it costs only {to_buy.sell_price} col.')
                        dprint('Would you like to buy it?')
                        choice = input('1: Yes \n2: No \n')
                        if choice in ['', 'y', 'Y', 'yes', 'Yes', 'YES', '0', '1', 'of course!']:
                            player.inventory.add_item(to_buy)
                            player.col -= to_buy.sell_price
                            self.update_inventory(to_buy)
                            dprint(f'You have {player.col} col!')
                        dprint('would you like to buy more?')
                        choice = input('1: Yes \n2: No \n')
                        if choice not in ['', 'y', 'Y', 'yes', 'Yes', 'YES', '0', '1', 'of course!']:
                            print('done browsin\' huh, good buy then?')
                            break
                else:
                    dprint('No huh? Strange...')
                    break

    def give_info(self, player, xp_thresholds, world):
        next_thresh = xp_thresholds[player.level]
        low_atk = damage_calculator(atk=player.atk, level=player.level)
        atk = damage_calculator(atk=player.atk, level=player.level, crit=True)
        lowest = damage_calculator(atk=player.atk, level=player.level, f=player.weapon.force, crit=False, special=True)
        high_sptk = damage_calculator(atk=player.atk, level=player.level, power=player.known_skills[0].damage, f=player.weapon.force, crit=True, special=True)
        print()
        dprint(f'{player.name} is in world {world.number}: {world.name}')
        dprint(f'in the {self.name} central marketplace.')
        dprint(f'{player.name} has the following stats:')
        print(f'Level: {player.level}')
        print(f'Experience Points: {player.xp}/{next_thresh}')
        print(f'Hit Points: {player.hp}/{player.maxhp}')
        print(f'Attack power: {low_atk}-{atk}')
        print(f'Skill attack power: {lowest}-{high_sptk}')
        print(f'Accuracy: {round((player.accuracy + player.acu) / 10, 2)}%')
        print(f'Speed: {1000 - player.agi}')
        print(f'Magic: {player.mag}/{player.maxmag}')
        print(f'Col: {player.col}')
        print('Skills:')
        for skill in player.known_skills:
            print(f'{skill.name.capitalize()} --> cost: {skill.cost}, cooldown: {skill.cooldown - skill.downtime}/{skill.cooldown}, power: {skill.damage}')
        print('Inventory:')
        player.inventory.display_contents()
        if player.level >= 6:
            print('Allies: ')
            for ally in player.allies:
                print(ally.name)
        print(f'Story progress: {player.progress}')

    def black_market(self, player):
        return True

    def update_inventory(self, item):
        if self.inventory[item] == 1:
            self.inventory.pop(item)
        else:
            self.inventory[item] -= 1


class Gym():
    def __init__(self, player):
        self.name = 'Training'
        self.level = player.level
        self.player = player
        self.skills = init_skills()
        self.learnables = [skill for skill in self.skills if skill.level <= self.level and skill.type == 0]
    
    def run(self, player=None, world=None, xp_thresholds=None):
        return self.skill_learning(player)

    def skill_learning(self, player:Fighter):
        dprint('Welcome to the skill gym, here you can learn new skills or')
        dprint('change the ones you know!')
        self.level = player.level

        while True:
            if  len(player.known_skills) < player.skill_slots:
                dprint('You appear to have an available skill slot.')
                dprint('would you like to learn or replace a skill?')
                lorp = ['learn','replace','nevermind'] # lorp: Learn or Replace
                for i in range(len(lorp)):
                    print(f'{i + 1}: {lorp[i]}')
                ans = input()
            
                if ans in ['0','1','l','L','Learn','learn','LEARN']: # if learn new
                    player.add_skill(self.learnables)
                if ans in ['2','r','R','replace','Replace','repl','Repl','REPLACE','REPL']: # if replace known
                    player.remove_skill()
                    player.add_skill(self.learnables)
                elif ans in ['3','n','N','NO','no','No','nope','Nope','NOPE','4','absolutely not!']:
                    dprint('Ok, you have a wonderful day!')
                    break
                else:
                    continue

            else:
                dprint('You don\'t seem content with your current skill set.')
                dprint('would you like to replace a skill you know?')
                print('1: replace a skill\n2: Nevermind\n')

                ans = input().lower().strip()
                if ans in ['1','0','r','replace','repl','e','','d','f','t','4','5']: # if replace known
                    player.remove_skill()
                    player.add_skill(self.learnables)
                elif ans in ['2','n','N','NO','no','No','nope','Nope','NOPE','3','absolutely not!']:
                    dprint('Alrighty then, have a magnifacent day!')
                    break
                else:
                    continue
        return True


class Alchemy:
    def __init__(self):
        self.name = 'Alchemy'

    def run(self, player=None, world=None, xp_thresholds=None):
        return self.create_potion(player, xp_thresholds)
    
    def create_potion(self, player:Fighter, xp_thresholds:dict):
        if not player.inventory.has('glass bottle'):
            dprint('You don\'t appear to have any available containers to')
            dprint('successfully do alchemy right now.')
            dprint('To proceed, you need the item called: glass bottle.')
            return True
        if random.getrandbits(1):
            dprint('Time to do some science!')
        else:
            dprint('Time to do some magic!')
        ability = ceil(player.level / 2) + 1
        dprint(f'You can use up to {ability} alchemical ingredients.')
        ingredients = [item for item in player.inventory.contents.keys() if item.is_ingredient]
        compound = []
        potential = 0
        for i in range(ability):
            dprint(f'Select items to mix ({ability - i} items left):')
            ingredient = get_list_option(ingredients)
            if ingredient is None:
                dprint('Oooo, actually you don\'t have anything to cook with!')
                return True
            player.inventory.remove_item(ingredient)
            ingredients.remove(ingredient)
            compound.append(ingredient)
            dprint(f'Current compound:')
            for i in compound:
                print(i.name)
            potential += ingredient.potency
            dprint(f'Compound potential: {potential}')
            dprint('Would you like to add more?\n1: Yes\n2: No\n')
            if input().lower().strip() in [' ', 'no', 'n', '2']:
                break
        
        dprint('Select something to produce with this compound:')
        product = get_list_option([item for item in items if item.craftable and (item.sell_price - 1) <= potential])
        bottle = [bottle for bottle in items if bottle.name == 'glass bottle']
        player.inventory.remove_item(bottle[0])
        player.inventory.add_item(product)
        dprint(f'You successfully produced 1 {product.name}!')
        player.gain_xp(product.rarity, xp_thresholds)
        return True


class Quit:
    def __init__(self) -> None:
        self.name = 'quit'
    
    def run(self, player=None, world=None, xp_thresholds=None):
        print('keep playing? \n1: No \n2: Yes')
        sure = input()
        if sure.strip() in ['2','3','y','Y','yes','Yes','YES','sure','definitely','p','P','2: Y','yep!']:
            return True
        return False
