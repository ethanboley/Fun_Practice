    

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
            if self.contents[item] <= 1:
                self.contents.pop(item)
            else:
                self.contents[item] -= 1


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


# # Define background music
# bgm_opening = pg.mixer.Sound('game\practice\music\mus_date.mp3')
# bgm_battle = pg.mixer.Sound('game\practice\music\mus_date_fight.mp3')
# bgm_hospital = pg.mixer.Sound('game\practice\music\mus_town.mp3')
# bgm_boss = pg.mixer.Sound('game\practice\music\Unlimited Power (loop).mp3')

