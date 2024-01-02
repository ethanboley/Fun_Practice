
from actions import *
from monsters import init_doctors
from things_stuff import init_items

items = init_items()

class Hospital:
    def __init__(self, name, quality):
        self.name = name
        self.quality = quality

    def welcome(self):
        options = ['healing', 'superheal', 'information', 'nothing']
        dprint(f'Welcome to {self.name} hospital! ')
        dprint(f'This hospital is a level {self.quality} facility. ')
        dprint('What seems to be the problem today! ')
        for i in range(len(options)):
            print(f'{i + 1}: {options[i]}')
        return input()

    def resolve(self, player, choice_task, xp_thresholds):
        if choice_task in ['healing','Healing','1','0','','h','H','reg']:
            self.heal(player, xp_thresholds)
            return True
        
        elif choice_task in ['superheal','Superheal','super heal','S','s','2','BIGBOI']:
            return self.superheal(player)

        elif choice_task in ['information','info','Information','Info','3','i','I']:
            self.give_info(player)
            return True
        
        else:
            return True

    def heal(self, player, xp_thresholds):
        dprint(f'Welcome to the {self.name} healing center! Good luck {player.name}! ')
        if player.col < 2:
            dprint('Oops, sorry unfortunately you don\'t have enough money, ')
            dprint('and here at this facility we don\'t speak BROKE!')
        else:
            player.col -= 2
            done = False
            while not done:
                doctors = init_doctors()
                doc = choose_monster(player, doctors)
                dprint(f'your doctor will be {doc.name}')
                round = 1
                while player.hp != player.maxhp and doc.is_alive():
                    dprint(f'This is check number {round}.')
                    doc.attack(player)
                    if player.hp >= player.maxhp:
                        player.hp = player.maxhp
                        dprint(f'{player.name} looks as good as new.')
                        done = True
                        break
                    else:
                        dprint(f'{player.name} has {player.hp} hp.') # keep going.
                        display_health(player)

                    player.hattack(doc)
                    if not doc.is_alive():
                        dprint(f'{doc.name} is going home for the day. ')
                        player.gain_xp(doc.xp, xp_thresholds)
                        break

                    if round == 10:
                        dprint('It\'s closing time for the hospital.')
                        break
                    round += 1

    def superheal(self, player):
        dprint(f'Welcome to the {self.name} super healing booth.')
        dprint('here we don\'t use such foolish things like doctors and science.')
        dprint('we use the much more reasonable approach of,')
        dprint('lobbing potions at you until they work!')
        if player.col < 2:
            dprint('Bro, you couldn\'t even afford care from those foolish, ')
            dprint('bookish, brainy, doctors with all their logic and reason! ')
            return True
        elif player.col < (5 + self.quality):
            dprint('Well as much as we\'d love to chuck our snake oil at you,')
            dprint('you simply lack the funds for such care!')
            return True
        else:
            player.col -= (5 + self.quality)
            while True:
                dprint(f'How about this one! ')
                player.hp -= 1
                if not player.is_alive():
                    dprint('You died by a potion bottle!')
                    return False
                dprint(f'{player.name}: {player.hp} hp')
                if random.randint(1, 10) - (1 + self.quality * 2) <= 0:
                    dprint(f'The potion worked!')
                    player.hp = player.maxhp
                    dprint('Thanks for coming!')
                    return True
                else:
                    dprint('Nope, \'nother dud! ')

    def give_info(self, player):
        pass # TODO


class Marketplace():
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.inventory = {}
        self.prices = {}
        self.salable = [item for item in items if item.sold]

    def stock_inventory(self):
        for item in self.salable:
            if item.level <= self.level:
                self.inventory[item] = self.level # starting at 1 for now change later to increase according to levels
    
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
    
    def resolve(self, player, choice_task):
        options = ['sell','buy','information','black market']
        if choice_task in ['','sell','Sell','SELL','1','S','s','0','buy from me!']:
            self.buy(player)
            dprint('Would you like to stay in the market? ')
            user = input('1: Yes\n2: No\n')
            if user in ['','y','Y','1','0','Yes','YES','yes','sure']:
                for i in range(len(options)):
                    print(f'{i + 1}: {options[i]}')
                user = input()
                self.resolve(player, user)

        elif choice_task in ['2','Buy','buy','B','b','what have you got?']:
            self.sell(player)
            dprint('Would you like to stay in the market? ')
            user = input()
            if user in ['','y','Y','1','0','Yes','YES','yes','sure']:
                for i in range(len(options)):
                    print(f'{i + 1}: {options[i]}')
                user = input()
                self.resolve(player, user)

        elif choice_task in ['information','info','Information','Info','3','i','I']:
            self.give_info(player)
            dprint('Would you like to stay in the market? ')
            user = input()
            if user in ['','y','Y','1','0','Yes','YES','yes','sure']:
                for i in range(len(options)):
                    print(f'{i + 1}: {options[i]}')
                user = input()
                self.resolve(player, user)
        
        elif choice_task in ['Black Market', 'black market', 'm', 'M', '4', 'black', 'Black', 'market', 'b market', 'black m', 'bm', 'm', '...', 'you know what.']:
            self.black_market(player)
            dprint('Would you like to stay in the market? ')
            user = input()
            if user in ['','y','Y','1','0','Yes','YES','yes','sure']:
                for i in range(len(options)):
                    print(f'{i + 1}: {options[i]}')
                user = input()
                self.resolve(player, user)


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
                to_sell_int = check_user_input('d',dict=player.inventory.contents) - 1
                # print(f'to_sell_int {to_sell_int}') # debug
                iteration = 0
                # print(f'iteration {iteration}') # debug
                # print(f'player.inventory.contents {player.inventory.contents}') # debug
                for key in player.inventory.contents:
                    # print(f'key {key}') # debug
                    if to_sell_int == iteration:
                        to_sell = key
                        # print(f'key {key}') # debug
                        break
                    iteration += 1
                    # print(f'iteration {iteration}') # debug
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


    def sell(self, player): # also here the player is buying from the market place
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
                    to_buy_int = check_user_input('d',dict=self.inventory) - 1
                    iteration = 0
                    for key in self.inventory:
                        if to_buy_int == iteration:
                            to_buy = key
                        iteration += 1
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

    def give_info(self, player):
        pass

    def black_market(self, player):
        pass

    def update_inventory(self, item):
        if self.inventory[item] == 0:
            self.inventory.pop(item)
        else:
            self.inventory[item] -= 1

    # def check_user_input(self, dictionary):
    #     user_in = '' # set the while loop start case
    #     while not str(user_in).isdigit(): # check if the user input can be converted into a number. 
    #         i = 0 # set the index for the display loop
    #         for key in dictionary: # print out the available values. <--+vvv
    #             print(f'{i + 1}: item, {key.name}; count, {dictionary[key]}') # mind this will only work if the key of the dict has a .name property
    #             i += 1 # increment the index
    #         print('Enter the number') # prompt the user
    #         user_in = input() # take in user input to be checked by the while condition. 
    #     user_int = int(user_in) # set second loop start case
    #     while user_int not in [x + 1 for x in range(len(dictionary))]: # once the user inputs a number, check if it's a good number
    #         user_int = self.check_user_input(dictionary) # if it isn't, restart by recursively calling the function. 
    #     else: # otherwise it is a good input
    #         iteration = 1 # set index for loop
    #         for key in dictionary: # loop through the keys in the dictionary again
    #             if iteration == user_int: # check if the good user input is equal to the loop number which identifies the correct key 
    #                 return key # return the user selected key
    #             else: # if not
    #                 iteration += 1 # increment


