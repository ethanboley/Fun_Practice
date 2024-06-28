
from random import random
from things_stuff import *
from actions import *


# --- useable items

class MagicGlass(Item):
    def __init__(self, name, level, sell_price, rarity, sold, can_use):
        super().__init__(name, level, sell_price, rarity, sold, can_use)

    def use(self, player=None, enemy=None, xp_thresholds=None):
        player.mag += (player.maxmag // 2)


class GlassOfTheWeave(Item):
    def __init__(self, name, level, sell_price, rarity, sold, can_use):
        super().__init__(name, level, sell_price, rarity, sold, can_use)

    def use(self, player=None, enemy=None, xp_thresholds=None):
        player.mag = player.maxmag


class LifePotion(Item):
    def __init__(self, name, level, sell_price, rarity, sold, can_use):
        super().__init__(name, level, sell_price, rarity, sold, can_use)
    
    def use(self, player=None, enemy=None, xp_thresholds=None):
        player.hp += 8 + (player.level * self.rarity) + self.level
        display_health(player)


class GigaLifePotion(Item):
    def __init__(self, name, level, sell_price, rarity, sold, can_use):
        super().__init__(name, level, sell_price, rarity, sold, can_use)
    
    def use(self, player=None, enemy=None, xp_thresholds=None):
        player.hp = player.maxhp
        display_health(player)


class GlassBottle(Item):
    def __init__(self, name, level, sell_price, rarity, sold, can_use):
        super().__init__(name, level, sell_price, rarity, sold, can_use)

    def use(self, player=None, enemy=None, xp_thresholds=None):
        pass


class KalesOBottle(Item):
    def __init__(self, name, level, sell_price, rarity, sold, can_use):
        super().__init__(name, level, sell_price, rarity, sold, can_use)

    def use(self, player=None, enemy=None, xp_thresholds=None):
        pass
        

class LittleDagger(Item):
    def __init__(self, name, level, sell_price, rarity, sold, can_use):
        super().__init__(name, level, sell_price, rarity, sold, can_use)

    def use(self, player=None, enemy=None, xp_thresholds=None):
        if random.random() < player.accuracy:
            enemy.hp -= 1
            dprint(f"{player.name} throws {self.name} at {enemy.name} dealing 1 damage!")
            if enemy.is_alive():
                dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
            else:
                dprint(f'{player.name} has defeated {enemy.name}!')
                player.gain_xp(enemy.xp, xp_thresholds)
                player.gain_col(enemy.col)
                enemy.drop(player)
        else:
            dprint(f"{player.name} misses with the dagger!")
        

class VenomGlass(Item):
    def __init__(self, name, level, sell_price, rarity, sold, can_use):
        super().__init__(name, level, sell_price, rarity, sold, can_use)

    def use(self, player=None, enemy=None, xp_thresholds=None):
        dprint(f'{player.name} chucks the small bottle at the {enemy.name}')
        dprint(f'it shatters on impact and the venom seeps into it\'s body')
        damage = 12 + player.level + (player.atk - 1)
        dprint(f'The venom deals {damage} damage! ')
        enemy.hp -= damage
        if enemy.is_alive():
            dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
        else:
            dprint(f'the poison killed {enemy.name}!')
            player.gain_xp(enemy.xp, xp_thresholds)
            player.gain_col(enemy.col)
            enemy.drop(player)
        

class NepenthFruit(Item):
    def __init__(self, name, level, sell_price, rarity, sold, can_use):
        super().__init__(name, level, sell_price, rarity, sold, can_use)

    def use(self, player=None, enemy=None, xp_thresholds=None):
        dprint(f'{player.name} eats a fruit during battle and')
        dprint('feels a short surge of power')
        player.hp += 6
        

class NawsothFruit(Item):
    def __init__(self, name, level, sell_price, rarity, sold, can_use):
        super().__init__(name, level, sell_price, rarity, sold, can_use)

    def use(self, player=None, enemy=None, xp_thresholds=None):
        dprint(f'{player.name} eats a fruit during battle')
        dprint('the fruit has healing properties!')
        player.hp += (player.maxhp // 4) - 1
        

class ReturnSoulStone(Item):
    def __init__(self, name, level, sell_price, rarity, sold, can_use):
        super().__init__(name, level, sell_price, rarity, sold, can_use)

    def use(self, player=None, enemy=None, xp_thresholds=None):
        pass # for use on a team mate self use will be atomatic
        

class OozeJelly(Item):
    def __init__(self, name, level, sell_price, rarity, sold, can_use):
        super().__init__(name, level, sell_price, rarity, sold, can_use)

    def use(self, player=None, enemy=None, xp_thresholds=None):
        pass # similar to the venom glass but does more damage and doesn't drop drops
        

class TrembleShortcake(Item):
    def __init__(self, name, level, sell_price, rarity, sold, can_use):
        super().__init__(name, level, sell_price, rarity, sold, can_use)

    def use(self, player=None, enemy=None, xp_thresholds=None):
        pass # adds temporary buff to speed and damage
        

class SuperAjaStone(Item):
    def __init__(self, name, level, sell_price, rarity, sold, can_use):
        super().__init__(name, level, sell_price, rarity, sold, can_use)

    def use(self, player=None, enemy=None, xp_thresholds=None):
        pass # high damaging attack

# --- #

def init_items():
    col_coin = Item('col coin', 1, 1, 0, False, False)
    grand_col = Item('grand col', 5, 10, 5, False, False)
    colossal_col = Item('colossal col', 8, 50, 8, False, False)
    magic_glass = MagicGlass('magic glass', 1, 4, 1, True, True)
    glass_of_the_weave = GlassOfTheWeave('glass of the weave', 20, 20, 4, True, True)
    life_potion = LifePotion('life potion', 1, 7, 2, True, True)
    vermilion_life_potion = LifePotion('vermilion life potion', 2, 10, 3, True, True)
    rose_life_potion = LifePotion('rose life potion', 3, 15, 4, True, True)
    magenta_life_potion = LifePotion('magenta life potion', 5, 21, 5, True, True)
    fuchsia_life_potion = LifePotion('fuchsia life potion', 8, 28, 6, True, True)
    purple_life_potion = LifePotion('purple life potion', 12, 40, 7, True, True)
    lavender_life_potion = LifePotion('lavender life potion', 18, 64, 8, True, True)
    azure_life_potion = LifePotion('azure life potion', 28, 100, 9, True, True)
    indigo_life_potion = LifePotion('indigo life potion', 42, 180, 10, False, True)
    blue_life_potion = LifePotion('blue life potion', 64, 240, 11, False, True)
    navy_life_potion = LifePotion('navy life potion', 96, 365, 12, False, True)
    deoxidized_blood_of_life_god = LifePotion('bottled deoxidized blood of the life potion deity', 120, 1000, 15, False, True)
    giga_life_potion = GigaLifePotion('giga life potion', 16, 20, 4, True, True)
    glass_bottle = GlassBottle('glass bottle', 1, 0, 1, True, True)
    kales_o_bottle = KalesOBottle('kales o bottle', 5, 11, 5, False, True)
    prostomium = Item('prostomium', 1, 1, 1, False, False)
    slime_jelly = Item('slime jelly', 1, 1, 0, False, False)
    mundane_scrap_metal = Item('mundane scrap metal', 1, 1, 0, False, False)
    little_dagger = LittleDagger('little dagger', 1, 1, 0, False, True)
    onix_stone = Item('onix stone', 4, 5, 3, True, False)
    monster_tooth = Item('monster tooth', 1, 2, 1, False, False)
    venom_glass = VenomGlass('venom glass', 2, 5, 2, False, True)
    carapas = Item('carapas', 1, 1, 0, False, False)
    slime_membrane = Item('slime membrane', 4, 11, 4, False, False)
    hide = Item('hide', 3, 1, 1, True, False)
    simple_fabric = Item('simple fabric', 2, 1, 0, True, False)
    living_wood = Item('living wood', 1, 2, 1, False, False) #
    aged_teak_log = Item('aged teak log', 2, 3, 2, False, False) #
    opal = Item('opal', 8, 10, 4, True, False)
    nepenth_fruit = NepenthFruit('nepenth fruit', 1, 2, 1, False, True)
    argiros_sheet = Item('agiros sheet', 9, 2, 1, True, False)
    nepenths_ovule = Item('nepenths ovule', 4, 8, 4, False, False)
    nawsoth_fruit = NawsothFruit('nawsoth fruit', 6, 5, 2, True, True) #
    emarald = Item('emerald', 11, 15, 4, True, False)
    acutite = Item('acutite', 2, 3, 2, False, False)
    crystalite = Item('crystalite', 3, 6, 3, False, False)
    return_soul_stone = ReturnSoulStone('return soul stone', 5, 5, 5, False, True)
    ruby = Item('ruby', 15, 25, 5, True, False)
    droplet_of_villi = Item('droplet of villi', 6, 14, 6, False, False) #
    lizard_hide = Item('lizard hide', 7, 4, 1, True, False)
    sapphire = Item('sapphire', 20, 35, 6, True, False)
    thicc_tendon = Item('thicc tendon', 1, 6, 1, False, False)
    noblewood = Item('noblewood', 2, 6, 2, False, False) #
    blue_blood_diamond = Item('blue blood diamond', 23, 50, 7, True, False)
    ooze_jelly = OozeJelly('ooze jelly', 1, 4, 1, False, True)
    living_stone = Item('living stone', 4, 15, 4, False, False)
    solidite = Item('solidite', 4, 12, 4, False, False)
    diamond = Item('diamond', 31, 85, 8, True, False)
    tremble_shortcake = TrembleShortcake('tremble shortcake', 7, 10, 7, True, True)
    hyper_slime_jelly = Item('hyper slime jelly', 2, 10, 2, False, False)
    super_aja_stone = SuperAjaStone('super aja stone', 9, 110, 9, False, True)

    items = [col_coin, 
             prostomium, slime_jelly, mundane_scrap_metal, little_dagger, onix_stone, 
             monster_tooth, glass_bottle, magic_glass, living_wood, simple_fabric,
             aged_teak_log, opal, nepenth_fruit, argiros_sheet, nepenths_ovule, 
             nawsoth_fruit, life_potion, vermilion_life_potion, emarald, hide, 
             rose_life_potion, magenta_life_potion, fuchsia_life_potion, 
             purple_life_potion, lavender_life_potion, azure_life_potion, 
             indigo_life_potion, blue_life_potion, navy_life_potion, 
             deoxidized_blood_of_life_god, acutite, grand_col, kales_o_bottle, 
             crystalite, return_soul_stone, ruby, droplet_of_villi, 
             lizard_hide, sapphire, thicc_tendon, 
             noblewood, blue_blood_diamond, ooze_jelly, living_stone,
             solidite, slime_membrane, carapas, diamond, tremble_shortcake, 
             venom_glass, hyper_slime_jelly, super_aja_stone, giga_life_potion, 
             glass_of_the_weave, colossal_col]

    return items


# --- spells

class SpellAttack(Spell):
    def __init__(self, name, type, level, cost, cooldown, damage, nature):
        super().__init__(name, type, level, cost, cooldown, damage, nature)
    
    def effect(self, enemy, caster, weak_damage=0, strong_damage=0):
        enemy.hp -= strong_damage
        self.set_downtime()
        dprint(f'{caster.name} casts {self.name}!') # TODO define spells
        dprint(f'The spell hits {enemy.name} for {strong_damage} damage!')
        if enemy.is_alive():
            dprint(f'{enemy.name} has {enemy.hp} hp remaining.')
        else:
            dprint(f'{self.name} blasted {enemy.name} to bits!')


class Healing(Spell):
    def __init__(self, name, type, level, cost, cooldown, damage, nature):
        super().__init__(name, type, level, cost, cooldown, damage, nature)
    
    def effect(self, enemy, caster, weak_damage=0, strong_damage=0): 
        dprint(f'A wave of healing energy surges through {caster.name}')
        targets = [caster]
        for ally in caster.allies:
            targets.append(ally)
        target = get_list_option(targets)
        target.hp += weak_damage
        if target.hp > target.maxhp:
            target.hp = (target.hp - target.maxhp) // 2 + target.hp
        dprint(f'{self.name} feels vitality returning.')
        display_health(target)

# --- #

def init_spells(): # name, type, level, cost, cooldown, damage, 
    magic_punch = SpellAttack('magic punch', 1, 1, 1, 1, 1, 0) 
    small_healing_word = Healing('small healing word', 1, 2, 1, 1, 1, 1) 
    magic_missile = SpellAttack('magic missile', 1, 2, 3, 1, 2, 0)
    acid_splash = SpellAttack('acid splash', 1, 2, 3, 2, 2, 0)
    fire_bolt = SpellAttack('fire bolt', 1, 3, 4, 3, 3, 0)
    thunder_wave = SpellAttack('thunder wave', 1, 3, 4, 4, 2, 0)
    vicious_mockery = SpellAttack('vicious mockery', 1, 4, 6, 4, 3, 0)
    magic_arrow = SpellAttack('magic arrow', 1, 4, 6, 5, 3, 0) 
    cure_wounds = Healing('cure wounds', 1, 5, 11, 5, 4, 1)
    bane = SpellAttack('bane', 1, 5, 8, 5, 4, 0)
    chromatic_orb = SpellAttack('chromatic orb', 1, 6, 9, 4, 5, 0)
    shocking_grasp = SpellAttack('shocking grasp', 1, 6, 8, 4, 5, 0)
    witch_bolt = SpellAttack('witch bolt', 1, 7, 10, 5, 9, 0)
    shatter = SpellAttack('shatter', 1, 7, 10, 4, 7, 0)
    emperor = SpellAttack('emperor', 1, 8, 9, 6, 5, 0)
    light_healing = Healing('light healing', 1, 8, 13, 5, 6, 1)
    emerald_splash = SpellAttack('emerald splash', 1, 9, 9, 5, 6, 0)
    fireball = SpellAttack('fireball', 1, 9, 11, 4, 11, 0)
    magicians_red = SpellAttack('magicians red', 1, 10, 10, 7, 7, 0)
    healing_word = Healing('healing word', 1, 10, 14, 4, 7, 1)
    fear = SpellAttack('fear', 1, 11, 12, 6, 7, 0)
    lightning = SpellAttack('lightning', 1, 12, 12, 6, 8, 0)
    dragon_pulse = SpellAttack('dragon pulse', 1, 13, 15, 4, 10, 0)
    dream_eater = SpellAttack('dream eater', 1, 14, 14, 7, 9, 0)
    electroball = SpellAttack('electroball', 1, 15, 18, 5, 10, 0)
    explosion = SpellAttack('explosion', 1, 16, 16, 6, 11, 0)
    gravity = SpellAttack('gravity', 1, 17, 20, 5, 9, 0)
    heal_pulse = Healing('heal pulse', 1, 18, 23, 6, 16, 1)
    hex = SpellAttack('hex', 1, 19, 20, 6, 11, 0)
    hurricane = SpellAttack('hurricane', 1, 20, 21, 7, 19, 0)
    recover = Healing('recover', 1, 21, 24, 7, 20, 1)
    remote_bomb = SpellAttack('remote bomb', 1, 22, 18, 10, 17, 0)
    nightmare = SpellAttack('nightmare', 1, 23, 24, 10, 16, 0)
    rock_tomb = SpellAttack('rock tomb', 1, 24, 26, 8, 23, 0)
    water_pulse = SpellAttack('water pulse', 1, 25, 27, 8, 25, 0)
    thunderlance = SpellAttack('thunderlance', 1, 26, 26, 9, 34, 0)
    electrosphere = SpellAttack('electrophere', 1, 27, 29, 7, 25, 0)
    vermin_bane = SpellAttack('vermin bane', 1, 28, 28, 11, 26, 0)
    heal = Healing('heal', 1, 29, 34, 8, 30, 1)

    stone_free = SpellAttack('stone free', 1, 30, 28, 11, 1, 0)
    gold_experience = Healing('gold experience', 1, 32, 33, 12, 1, 1)
    flamethrower = SpellAttack('flamethrower', 1, 34, 35, 8, 1, 0)
    incinerate = SpellAttack('incinerate', 1, 36, 37, 9, 1, 0)
    crazy_diamond = Healing('crazy diamond', 1, 38, 40, 13, 1, 1)
    stasis = SpellAttack('stasis', 1, 40, 31, 12, 1, 0)
    self_destruct = SpellAttack('self destruct', 1, 42, 43, 9, 1, 0)
    grand_fireball = SpellAttack('grand fireball', 1, 44, 41, 13, 1, 0)
    synthesis = Healing('synthesis', 1, 46, 48, 11, 1, 1)
    dragon_lightning = SpellAttack('dragon lightning', 1, 48, 45, 12, 1, 0)
    disintegrate = SpellAttack('disintegrate', 1, 50, 49, 11, 1, 1)
    chain_dragon_lightning = SpellAttack('chain dragon lightning', 1, 52, 51, 11, 1, 1)
    blasphemy = SpellAttack('blasphemy', 1, 54, 50, 12, 1, 1)
    heavy_recover = Healing('heavy recover', 1, 56, 60, 15, 1, 1)
    nuclear_blast = SpellAttack('nuclear blast', 1, 58, 56, 13, 1, 1)
    blessing_of_titania = Healing('blessing of titania', 1, 60, 59, 15, 1, 1)
    domain_expansion = SpellAttack('domain expansion', 1, 64, 60, 15, 1, 1)

    black_hole = SpellAttack('black hole', 1, 68, 63, 12, 1, 1)
    reality_slash = SpellAttack('reality slash', 1, 72, 65, 14, 1, 1)
    transfer_unit_durability = Healing('transfer unit durability', 1, 76, 79, 16, 1, 1)

    Slash_Kill = SpellAttack('/kill @e[type=enemy]', 1, 80, 71, 15, 1, 1) # top tier
    Power_Word_Heal = Healing('Power Word Heal', 1, 82, 88, 16, 1, 1) # top tier
    Delayed_Strike_Lightning_Bolt = SpellAttack('Delayed Strike Lightning Bolt', 1, 84, 80, 13, 1, 1) # top tier
    Release_Recolection = SpellAttack('Release Recolection', 1, 86, 76, 15, 1, 1) # top tier
    Kamehameha = SpellAttack('Kamehameha', 1, 88, 79, 15, 1, 1) # top tier
    Meteor_Swarm = SpellAttack('Meteor Swarm', 1, 90, 84, 13, 1, 1) # top tier
    True_Death = SpellAttack('True Death', 1, 92, 82, 16, 1, 1) # top tier
    Grasp_Heart = SpellAttack('Grasp Heart', 1, 94, 85, 15, 1, 1) # top tier
    Urbosas_Fury = SpellAttack('Urbosa\'s Fury', 1, 96, 92, 17, 1, 1) # top tier
    Hyper_Beam = SpellAttack('Hyper Beam', 1, 98, 93, 16, 1, 1) # top tier
    Star_Platinum = SpellAttack('Star Platinum', 1, 100, 87, 17, 1, 1) # top tier
    Miphas_Grace = Healing('Mipha\'s Grace', 1, 102, 94, 21, 1, 1) # top tier
    Fallen_Down = SpellAttack('Fallen Down', 1, 104, 94, 16, 1, 1) # top tier

    spells = [magic_punch, small_healing_word, magic_missile, acid_splash, 
              fire_bolt, thunder_wave, vicious_mockery, vicious_mockery, 
              magic_arrow, cure_wounds, bane, chromatic_orb, shocking_grasp, 
              witch_bolt, shatter, emperor, light_healing, emerald_splash, 
              magicians_red, fireball, healing_word, fear, lightning]
    
    return spells


