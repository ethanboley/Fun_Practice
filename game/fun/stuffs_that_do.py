
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
        player.hp += 18 + player.level
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
             nawsoth_fruit, life_potion, emarald, hide, 
             acutite, grand_col, kales_o_bottle, crystalite, 
             return_soul_stone, ruby, droplet_of_villi, 
             lizard_hide, sapphire, thicc_tendon, 
             noblewood, blue_blood_diamond, ooze_jelly, living_stone,
             solidite, slime_membrane, carapas, 
             diamond, tremble_shortcake, venom_glass, 
             hyper_slime_jelly, super_aja_stone, giga_life_potion, 
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

class Escaping(Spell):
    def __init__(self, name, type, level, cost, cooldown, damage, nature):
        super().__init__(name, type, level, cost, cooldown, damage, nature)
    
    def effect(self, enemy, caster, weak_damage=0, strong_damage=0):
        caster.run()

# --- #

def init_spells():
    magic_punch = SpellAttack('magic punch', 1, 1, 1, 1, 1, 0)
    small_healing_word = Healing('small healing word', 1, 1, 1, 1, 1, 1)
    dissengage = Spell('dissengage', 1, 1, 1, 1, 0, 2)
    magic_missile = SpellAttack('magic missile', 1, 1, 2, 1, 2, 0)
    acid_splash = SpellAttack
    fire_bolt = SpellAttack
    expeditious_retreat = Spell
    thunder_wave = SpellAttack
    vicious_mockery = SpellAttack
    magic_arrow = SpellAttack
    cure_wounds = Healing
    bane = SpellAttack
    chromatic_orb = SpellAttack
    shocking_grasp = SpellAttack
    witch_bolt = SpellAttack
    shatter = SpellAttack
    emperor = Spell
    light_healing = Healing
    emerald_splash = SpellAttack
    misty_step = Spell
    magicians_red = SpellAttack
    fireball = SpellAttack
    fear = Spell
    lightning = SpellAttack
    hanged_man = Spell
    dragon_pulse = SpellAttack
    dream_eater = Spell
    electroball = SpellAttack
    explosion = SpellAttack
    gravity = Spell
    heal_pulse = Healing
    hex = SpellAttack
    hurricane = Spell
    nightmare = Spell
    remote_bomb = SpellAttack
    recover = Healing
    rock_tomb = Spell
    water_pulse = SpellAttack
    thunderlance = SpellAttack
    electrosphere = SpellAttack
    vermin_bane = SpellAttack
    heal = Healing
    generate_element = Spell

    crazy_diamond = Healing
    stone_free = Spell
    gold_experience = Healing
    flamethrower = SpellAttack
    incinerate = SpellAttack
    judgement = Spell
    stasis = Spell
    self_destruct = SpellAttack
    synthesis = Healing
    teleport = Spell
    revalis_gale = Spell
    invisibility = Spell
    heavy_recover = Healing
    grand_fireball = SpellAttack
    dragon_lightning = SpellAttack
    disintegrate = SpellAttack
    chain_dragon_lightning = SpellAttack
    blasphemy = SpellAttack
    bless_of_titania = Healing
    nuclear_blast = SpellAttack
    black_hole = SpellAttack
    reality_slash = SpellAttack
    transfer_unit_durability = Healing

    Power_Word_Kill = SpellAttack # top tier
    Delayed_Strike_Lightning_Bolt = SpellAttack # top tier
    Release_Recolection = Spell # top tier
    Meteor_Swarm = SpellAttack # top tier
    True_Death = SpellAttack # top tier
    Grasp_Heart = SpellAttack # top tier
    Greater_Teleportation = Spell # top tier
    Urbosas_Fury = SpellAttack # top tier
    Hyper_Beam = SpellAttack # top tier
    Star_Platinum = Spell # top tier
    Miphas_Grace = Healing # top tier
    Fallen_Down = SpellAttack # top tier


