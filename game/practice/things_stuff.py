
# initialize_pygame()
from actions import *


class Skill():
    def __init__(self, name, type, level, cost, cooldown, damage):
        self.name = name
        self.type = type
        self.level = level
        self.cost = cost
        self.cooldown = cooldown
        self.downtime = cooldown
        self.damage = damage

    def tick(self):
        if self.downtime <= self.cooldown:
            self.downtime += 1

    def set_downtime(self):
        self.downtime -= self.cooldown

    def is_usable(self):
        if self.downtime >= self.cooldown:
            return True
        return False


class Spell(Skill):
    def __init__(self, name, type, level, cost, cooldown, damage, nature):
        super().__init__(name, type, level, cost, cooldown, damage)
        self.nature = nature


class Spall(Skill): # for pugilists (verb: to break into small peices)
    def __init__(self, name, type, level, cost, cooldown, damage):
        super().__init__(name, type, level, cost, cooldown, damage)


class Item():
    def __init__(self, name, level, sell_price, rarity, sold, can_use) -> None:
        self.name = name
        self.level = level
        self.sell_price = sell_price
        self.rarity = rarity
        self.sold = sold
        self.can_use = can_use


class Inventory():
    def __init__(self):
        self.contents = {} # {item:count}

    def add_item(self, item):
        if item in self.contents.keys():
            self.contents[item] += 1
        else:
            self.contents[item] = 1

    def remove_item(self, item):
        if item in self.contents.keys():
            if self.contents[item] == 1:
                self.contents.pop(item)
            else:
                self.contents[item] -= 1


# ------------ useable items


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
        player.hp += (player.maxhp // 2)
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
        if random.random() < self.accuracy:
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
        



# ---------------------------------------------------------------------------------------------------------------------


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


def init_skills(): # 0 is sword skills, 1 is spells (stands), 2 is martial arts (sumo, hamon, sao ma skills)
    horizontal = Skill('horizontal', 0, 1, 1, 4, 2) # level - 1, * cost (-1 if 4+, -2 8+, ect), lower if 2 higher if 4+
    vertical = Skill('vertical', 0, 1, 1, 3, 1) # reduce slightly by cooldown
    slant = Skill('slant', 0, 1, 1, 2, 1)
    linear = Skill('linear', 0, 2, 1, 3, 2)
    single_shot = Skill('single shot', 0, 2, 1, 2, 1)
    parallel_sting = Skill('parallel sting', 0, 2, 2, 2, 2) # cost 2 = 8 # (level + (cost * 3))
    streak = Skill('streak', 0, 3, 1, 3, 2)
    uppercut = Skill('uppercut', 0, 3, 1, 4, 3)
    back_rush = Skill('back rush', 0, 4, 1, 5, 4)
    diagonal_sting = Skill('diagonal sting', 0, 4, 2, 2, 3)
    serration_wave = Skill('serration wave', 0, 5, 1, 2, 3)
    triangular = Skill('triangular', 0, 5, 3, 3, 8)
    avalanche = Skill('avalanche', 0, 6, 1, 6, 9)
    horizontal_arc = Skill('horizontal arc', 0, 6, 2, 4, 9)
    double_cleave = Skill('double cleave', 0, 7, 2, 5, 11)
    canine = Skill('canine', 0, 7, 3, 2, 8)
    fade_edge = Skill('fade edge', 0, 8, 1, 2, 4)
    vertical_arc = Skill('vertical arc', 0, 8, 2, 4, 11)
    savage_fulcrum = Skill('savage fulcrum', 0, 9, 3, 4, 13)
    sonic_leap = Skill('sonic leap', 0, 9, 1, 3, 10)
    fell_cresent = Skill('fell cresent', 0, 10, 1, 3, 11)
    quad_pain = Skill('quad pain', 0, 11, 4, 2, 14)
    rapid_bite = Skill('rapid bite', 0, 12, 2, 2, 13)
    flashing_peirce = Skill('flashing peirce', 0, 13, 1, 2, 13)
    cascade = Skill('cascade', 0, 14, 1, 3, 15)
    treble_scythe = Skill('treble scythe', 0, 15, 3, 3, 20)
    rage_spike = Skill('rage spike', 0, 16, 1, 3, 17)
    horizontal_square = Skill('horizontal square', 0, 17, 4, 4, 25)
    vertical_square = Skill('vertical square', 0, 18, 4, 4, 26)
    water_surface_slash = Skill('water surface slash', 0, 19, 1, 3, 20)
    snake_bite = Skill('snake bite', 0, 20, 2, 3, 23)
    folium = Skill('folium', 0, 21, 1, 2, 21)
    water_wheel = Skill('water wheel', 0, 22, 2, 3, 25)
    phantom_moon = Skill('phantom moon', 0, 23, 1, 3, 24)
    slashing_ray = Skill('slashing ray', 0, 24, 2, 3, 27)
    flowing_dance = Skill('flowing dance', 0, 25, 3, 3, 30)
    silent_ruin = Skill('silent ruin', 0, 26, 1, 2, 26)
    thunderclap_flash = Skill('thuderclap flash', 0, 27, 1, 3, 28)
    double_circular = Skill('double circular', 0, 28, 2, 4, 32)
    striking_tide = Skill('striking tide', 0, 29, 1, 3, 30)
    reaver = Skill('reaver', 0, 30, 1, 3, 31)
    slice_n_dice = Skill('slice n dice', 0, 31, 6, 3, 42)
    oblique = Skill('oblique', 0, 32, 1, 3, 33)
    blessed_rain = Skill('blessed rain', 0, 33, 5, 3, 42)
    embu = Skill('embu', 0, 34, 1, 3, 35)
    vorpal_strike = Skill('vorpal strike', 0, 35, 1, 3, 37)
    absolute_void = Skill('absolute void', 0, 36, 1, 3, 37)
    whirlpool = Skill('whirlpool', 0, 37, 4, 3, 44)
    ukifune = Skill('ukifune', 0, 38, 1, 3, 39)
    dancing_flash = Skill('dancing flash', 0, 39, 3, 2, 40)
    star_splash = Skill('star splash', 0, 40, 8, 2, 43)
    waterfall_basin = Skill('waterfall basin', 0, 42, 1, 3, 42)
    scarlet_fan = Skill('scarlet fan', 0, 44, 3, 3, 48) 
    deadly_sins = Skill('deadly sins', 0, 46, 7, 4, 59)
    constant_flux = Skill('constant flux', 0, 48, 2, 3, 51)
    clear_blue = Skill('clear blue', 0, 50, 3, 3, 55) 
    cataract = Skill('cataract', 0, 52, 2, 2, 52) 
    roar = Skill('roar', 0, 54, 2, 5, 58) 
    meteor_break = Skill('meteor break', 0, 56, 7, 4, 71) 
    dead_calm = Skill('dead calm', 0, 58, 12, 3, 83) 
    howling_octave = Skill('howling octave', 0, 60, 8, 3, 75) 
    raging_sun = Skill('raging sun', 0, 62, 6, 3, 74) 
    neutron = Skill('neutron', 0, 64, 5, 2, 66) 
    godspeed = Skill('godspeed', 0, 66, 3, 2, 67) 
    tsujikaze = Skill('tsujikaze', 0, 68, 9, 3, 84) 
    burning_bones = Skill('burning bones', 0, 70, 4, 3, 77) 
    volcanic_blazer = Skill('volcanic blazer', 0, 72, 8, 5, 95) 
    obscuring_clouds = Skill('burning bones', 0, 74, 10, 3, 93) 
    crucifixion = Skill('crucifixion', 0, 76, 6, 2, 78) 
    solar_heat_haze = Skill('solar heat haze', 0, 78, 9, 3, 96) 
    nova_ascension = Skill('nova ascension', 0, 80, 10, 4, 105) 
    beneficient_radiance = Skill('beneficient radiance', 0, 82, 4, 3, 89) 
    dragon_halo = Skill('dragon halo', 0, 84, 6, 3, 95) 
    Rengoku = Skill('Rengoku', 0, 86, 1, 3, 88) # (top tier)
    Meteor_Fall = Skill('Meteor Fall', 0, 88, 2, 4, 96) # (top tier)
    Hinokami_Kagura = Skill('Hinokami Kagura', 0, 90, 3, 3, 96) # (top tier)
    Lai = Skill('Lai', 0, 92, 1, 3, 96) # (top tier)
    Devine_Sword = Skill('Devine Sword', 0, 94, 1, 5, 101) # (top tier)
    Hiogi = Skill('Hiogi', 0, 96, 3, 3, 105) # (top tier)
    Zekku = Skill('Zekku', 0, 98, 1, 3, 102) # (top tier)
    Mothers_Rosario = Skill('Mothers Rosario', 0, 100, 11, 1, 111) # (top tier)
    The_Eclipse = Skill('The Eclipse', 0, 102, 27, 3, 164) # (top tier)
    Starburst_Stream = Skill('Starburst Stream', 0, 104, 16, 3, 150) # (top tier)


    skills = [horizontal, vertical, slant, linear, single_shot, parallel_sting, 
              streak, uppercut, back_rush, diagonal_sting, serration_wave, 
              triangular, avalanche, horizontal_arc, double_cleave, canine, 
              fade_edge, vertical_arc, savage_fulcrum, sonic_leap, fell_cresent, 
              quad_pain, rapid_bite, flashing_peirce, cascade, treble_scythe, 
              rage_spike, horizontal_square, vertical_square, 
              water_surface_slash, snake_bite, folium, water_wheel, phantom_moon, 
              slashing_ray, flowing_dance, silent_ruin, thunderclap_flash, 
              double_circular, striking_tide, reaver, slice_n_dice, oblique, 
              blessed_rain, embu, vorpal_strike, absolute_void, whirlpool, 
              ukifune, dancing_flash, star_splash, waterfall_basin, scarlet_fan, 
              deadly_sins, constant_flux, clear_blue, cataract, roar, 
              meteor_break, dead_calm, howling_octave, raging_sun, neutron, 
              godspeed, tsujikaze, burning_bones, volcanic_blazer, 
              obscuring_clouds, crucifixion, solar_heat_haze, nova_ascension, 
              beneficient_radiance, dragon_halo, Rengoku, Meteor_Fall, 
              Hinokami_Kagura, Lai, Devine_Sword, Hiogi, Zekku, Mothers_Rosario, 
              The_Eclipse, Starburst_Stream]

    return skills


def init_spells():
    magic_punch = Spell('magic punch', 1, 1, 1, 1, 1, 0)
    small_healing_word = Spell('small healing word', 1, 1, 1, 1, 1, 1)
    dissengage = Spell('dissengage', 1, 1, 1, 1, 0, 2)
    magic_missile = Spell('magic missile', 1, 1, 2, 1, 2, 0)
    acid_splash = Spell
    fire_bolt = Spell
    expeditious_retreat = Spell
    thunder_wave = Spell
    vicious_mockery = Spell
    magic_arrow = Spell
    cure_wounds = Spell
    bane = Spell
    chromatic_orb = Spell
    shocking_grasp = Spell
    witch_bolt = Spell
    shatter = Spell
    emperor = Spell
    light_healing = Spell
    emerald_splash = Spell
    misty_step = Spell
    magicians_red = Spell
    fireball = Spell
    fear = Spell
    lightning = Spell
    hanged_man = Spell
    dragon_pulse = Spell
    dream_eater = Spell
    electroball = Spell
    explosion = Spell
    gravity = Spell
    heal_pulse = Spell
    hex = Spell
    hurricane = Spell
    nightmare = Spell
    remote_bomb = Spell
    recover = Spell
    rock_tomb = Spell
    water_pulse = Spell
    thunderlance = Spell
    electrosphere = Spell
    vermin_bane = Spell
    heal = Spell
    generate_element = Spell

    crazy_diamond = Spell
    stone_free = Spell
    gold_experience = Spell
    flamethrower = Spell
    incinerate = Spell
    judgement = Spell
    stasis = Spell
    self_destruct = Spell
    synthesis = Spell
    teleport = Spell
    revalis_gale = Spell
    invisibility = Spell
    heavy_recover = Spell
    grand_fireball = Spell
    dragon_lightning = Spell
    disintegrate = Spell
    chain_dragon_lightning = Spell
    blasphemy = Spell
    bless_of_titania = Spell
    nuclear_blast = Spell
    black_hole = Spell
    reality_slash = Spell
    transfer_unit_durability = Spell

    Power_Word_Kill = Spell # top tier
    Release_Recolection = Spell # top tier
    Meteor_Swarm = Spell # top tier
    True_Death = Spell # top tier
    Grasp_Heart = Spell # top tier
    Greater_Teleportation = Spell # top tier
    Urbosas_Fury = Spell # top tier
    Hyper_Beam = Spell # top tier
    Star_Platinum = Spell # top tier
    Delayed_Strike_Lightning_Bolt = Spell # top tier
    Miphas_Grace = Spell # top tier
    Fallen_Down = Spell # top tier



# # Define background music
# bgm_opening = pg.mixer.Sound('game\practice\music\mus_date.mp3')
# bgm_battle = pg.mixer.Sound('game\practice\music\mus_date_fight.mp3')
# bgm_hospital = pg.mixer.Sound('game\practice\music\mus_town.mp3')
# bgm_boss = pg.mixer.Sound('game\practice\music\Unlimited Power (loop).mp3')

