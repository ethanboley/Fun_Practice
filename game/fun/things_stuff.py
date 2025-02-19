# things_stuff.py


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
    def __init__(self, name, level, sell_price, rarity, power=0, potency=0, sold=False, can_use=False, is_ingredient=False, craftable=False) -> None:
        self.name = name
        self.level = level
        self.sell_price = sell_price
        self.rarity = rarity
        self.power = power
        self.potency = potency
        self.sold = sold
        self.can_use = can_use
        self.is_ingredient = is_ingredient
        self.craftable = craftable


class Inventory():
    def __init__(self):
        self.contents = {} # {item:count}

    def get_count(self, item):
        for i, c in self.contents.items():
            if item == i:
                return c

    def add_item(self, item):
        existing_item = next((key for key in self.contents if key.name == item.name), None)

        if existing_item:
            if self.contents[existing_item] >= 10:
                print('Your pockets are full')
            else:
                self.contents[existing_item] += 1
        else:
            self.contents[item] = 1

    def remove_item(self, item):
        if item in self.contents.keys():
            if self.contents[item] <= 1:
                self.contents.pop(item)
            else:
                self.contents[item] -= 1
    
    def add_item_by_name(self, items, i_name, count=1):
        for i in items:
            if i.name == i_name:
                while count != 0:
                    self.add_item(i)
                    count -= 1
    
    def display_contents(self):
        for i, item in enumerate(list(self.contents.keys()), start=1):
            name = item.name
            count = self.contents[item]
            value = item.sell_price * self.contents[item]
            print(f'{i}: Item {name}; Quantity: {count}; Total Value: {value} col.')
    
    def has(self, item_name:str | None = None):
        for item in self.contents:
            if item.name == item_name:
                return True
        return False


# 0 is sword skills, 1 is spells (stands), 2 is martial arts (sumo, hamon, sao ma skills)

def init_skills(): 
    horizontal = Skill('horizontal', 0, 1, 1, 4, 2) # level - 1, * cost (-1 if 4+, -2 8+, ect), lower if 2 higher if 4+
    vertical = Skill('vertical', 0, 1, 1, 3, 1) # reduce slightly by cooldown
    slant = Skill('slant', 0, 1, 1, 2, 1)
    linear = Skill('linear', 0, 2, 1, 4, 2) # +1
    single_shot = Skill('single shot', 0, 2, 1, 3, 1)
    parallel_sting = Skill('parallel sting', 0, 2, 2, 3, 2) # cost 2 = 8 # (level + (cost * 3))
    streak = Skill('streak', 0, 3, 1, 4, 2)
    uppercut = Skill('uppercut', 0, 3, 1, 5, 3)
    back_rush = Skill('back rush', 0, 4, 1, 7, 4) # +2
    diagonal_sting = Skill('diagonal sting', 0, 4, 2, 4, 3)
    serration_wave = Skill('serration wave', 0, 5, 1, 4, 3)
    triangular = Skill('triangular', 0, 5, 3, 5, 8)
    avalanche = Skill('avalanche', 0, 6, 1, 8, 9)
    horizontal_arc = Skill('horizontal arc', 0, 6, 2, 6, 9)
    double_cleave = Skill('double cleave', 0, 7, 2, 8, 11) # +3
    canine = Skill('canine', 0, 7, 3, 5, 8)
    fade_edge = Skill('fade edge', 0, 8, 1, 5, 4)
    vertical_arc = Skill('vertical arc', 0, 8, 2, 7, 11)
    savage_fulcrum = Skill('savage fulcrum', 0, 9, 3, 8, 13) # cooldown increase
    sonic_leap = Skill('sonic leap', 0, 9, 1, 7, 10)
    fell_cresent = Skill('fell cresent', 0, 10, 1, 7, 11)
    quad_pain = Skill('quad pain', 0, 11, 4, 6, 14)
    rapid_bite = Skill('rapid bite', 0, 12, 2, 7, 13) # +4
    flashing_peirce = Skill('flashing peirce', 0, 13, 1, 7, 13)
    cascade = Skill('cascade', 0, 14, 1, 8, 15)
    treble_scythe = Skill('treble scythe', 0, 15, 3, 8, 20)
    rage_spike = Skill('rage spike', 0, 16, 1, 8, 17)
    horizontal_square = Skill('horizontal square', 0, 17, 4, 8, 25)
    vertical_square = Skill('vertical square', 0, 18, 4, 9, 26)
    water_surface_slash = Skill('water surface slash', 0, 19, 1, 9, 20) # cooldown increase
    snake_bite = Skill('snake bite', 0, 20, 2, 9, 23)
    folium = Skill('folium', 0, 21, 1, 8, 21)
    water_wheel = Skill('water wheel', 0, 22, 2, 10, 25) # +5
    phantom_moon = Skill('phantom moon', 0, 23, 1, 10, 24)
    slashing_ray = Skill('slashing ray', 0, 24, 2, 10, 27)
    flowing_dance = Skill('flowing dance', 0, 25, 3, 10, 30)
    silent_ruin = Skill('silent ruin', 0, 26, 1, 9, 26)
    thunderclap_flash = Skill('thuderclap flash', 0, 27, 1, 10, 28)
    double_circular = Skill('double circular', 0, 28, 2, 11, 32)
    striking_tide = Skill('striking tide', 0, 29, 1, 10, 30)
    reaver = Skill('reaver', 0, 30, 1, 10, 31)
    slice_n_dice = Skill('slice n dice', 0, 31, 6, 10, 42)
    oblique = Skill('oblique', 0, 32, 1, 10, 33)
    blessed_rain = Skill('blessed rain', 0, 33, 5, 10, 42)
    embu = Skill('embu', 0, 34, 1, 10, 35)
    vorpal_strike = Skill('vorpal strike', 0, 35, 1, 10, 37)
    absolute_void = Skill('absolute void', 0, 36, 1, 10, 37)
    whirlpool = Skill('whirlpool', 0, 37, 4, 10, 44)
    ukifune = Skill('ukifune', 0, 38, 1, 10, 39)
    dancing_flash = Skill('dancing flash', 0, 39, 3, 9, 40)
    star_splash = Skill('star splash', 0, 40, 8, 10, 43) # +6
    waterfall_basin = Skill('waterfall basin', 0, 42, 1, 11, 42)
    scarlet_fan = Skill('scarlet fan', 0, 44, 3, 11, 48) 
    deadly_sins = Skill('deadly sins', 0, 46, 7, 12, 59)
    constant_flux = Skill('constant flux', 0, 48, 2, 11, 51)
    clear_blue = Skill('clear blue', 0, 50, 3, 11, 55) 
    cataract = Skill('cataract', 0, 52, 2, 10, 52) 
    roar = Skill('roar', 0, 54, 2, 13, 58) 
    meteor_break = Skill('meteor break', 0, 56, 7, 12, 71) 
    dead_calm = Skill('dead calm', 0, 58, 12, 12, 83) # cooldown increase
    howling_octave = Skill('howling octave', 0, 60, 8, 12, 75) 
    raging_sun = Skill('raging sun', 0, 62, 6, 12, 74) 
    neutron = Skill('neutron', 0, 64, 5, 11, 66) 
    godspeed = Skill('godspeed', 0, 66, 3, 11, 67) 
    tsujikaze = Skill('tsujikaze', 0, 68, 9, 12, 84) 
    burning_bones = Skill('burning bones', 0, 70, 4, 12, 77) 
    volcanic_blazer = Skill('volcanic blazer', 0, 72, 8, 14, 95) 
    obscuring_clouds = Skill('burning bones', 0, 74, 10, 13, 93) # +7
    crucifixion = Skill('crucifixion', 0, 76, 6, 12, 78) 
    solar_heat_haze = Skill('solar heat haze', 0, 78, 9, 13, 96) 
    nova_ascension = Skill('nova ascension', 0, 80, 10, 14, 105)
    beneficient_radiance = Skill('beneficient radiance', 0, 82, 4, 13, 89) 
    dragon_halo = Skill('dragon halo', 0, 84, 6, 13, 95) 
    Rengoku = Skill('Rengoku', 0, 86, 1, 14, 88) # (top tier) # cooldown increase
    Meteor_Fall = Skill('Meteor Fall', 0, 88, 2, 15, 96) # (top tier)
    Hinokami_Kagura = Skill('Hinokami Kagura', 0, 90, 3, 14, 96) # (top tier)
    Lai = Skill('Lai', 0, 92, 1, 14, 96) # (top tier)
    Devine_Sword = Skill('Devine Sword', 0, 94, 1, 16, 101) # (top tier)
    Hiogi = Skill('Hiogi', 0, 96, 3, 14, 105) # (top tier)
    Zekku = Skill('Zekku', 0, 98, 1, 14, 102) # (top tier)
    Mothers_Rosario = Skill('Mothers Rosario', 0, 100, 11, 11, 111) # (top tier)
    The_Eclipse = Skill('The Eclipse', 0, 102, 27, 14, 164) # (top tier)
    Starburst_Stream = Skill('Starburst Stream', 0, 104, 16, 14, 150) # (top tier)


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

def init_spalls():
    punch = Spall('punch', 2, 1, 1, 1, 1)
    # flurry_of_blows = Spall()

    spalls = [punch]

    return spalls

# # Define background music
# bgm_opening = pg.mixer.Sound('game\practice\music\mus_date.mp3')
# bgm_battle = pg.mixer.Sound('game\practice\music\mus_date_fight.mp3')
# bgm_hospital = pg.mixer.Sound('game\practice\music\mus_town.mp3')
# bgm_boss = pg.mixer.Sound('game\practice\music\Unlimited Power (loop).mp3')

