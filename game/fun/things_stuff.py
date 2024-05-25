# things_stuff.py

class WorldMap:
    def __init__(self, things):
        self.things = things
        self.atlas = {
            'world 1':{0:('1-0','Tutorial'),1:('1-1',''),2:('1-2',''),
                       3:('1-3',''),4:('1-4',''),5:('1-5',''),6:('1-6',''),
                       7:('1-7',''),8:('1-8',''),9:('1-9',''),10:('1-10',''),
                       11:('1-11',''),12:('1-12',''),13:('1-13',''),
                       14:('1-14',''),15:('1-15',''),16:('1-16',''),
                       17:('1-17',''),18:('1-18',''),19:('1-19',''),
                       20:('1-20',''),21:('1-21',''),22:('1-22',''),
                       23:('1-23',''),24:('1-24',''),25:('1-25',''),
                       26:('1-26',''),27:('1-27',''),28:('1-28',''),
                       29:('1-29',''),30:('1-30',''),31:('1-31',''),
                       32:('1-32','')},
            'world 2':{33:('2-0',''),34:('2-1',''),35:('2-2',''),36:('2-3',''),
                       37:('2-4',''),38:('2-5',''),39:('2-6',''),40:('2-7',''),
                       41:('2-8',''),42:('2-9',''),43:('2-10',''),
                       44:('2-11',''),45:('2-12',''),46:('2-13',''),
                       47:('2-14',''),48:('2-15',''),49:('2-16'),
                       50:('2-17',''),51:('2-18',''),52:('2-19',''),
                       53:('2-20',''),54:('2-21',''),55:('2-22',''),
                       56:('2-23',''),57:('2-24',''),58:('2-25',''),
                       59:('2-26',''),60:('2-27',''),61:('2-28',''),
                       62:('2-29',''),63:('2-30',''),64:('2-31',''),
                       65:('2-32','')},
        #     'world 3':{'3-0',''),'3-1',''),'3-2',''),'3-3',''),'3-4',''),'3-5',''),'3-6',''),'3-7',''),'3-8',''),
        #                '3-9',''),'3-10',''),'3-11',''),'3-12',''),'3-13',''),'3-14',''),'3-15',''),'3-16'
        #                '3-17',''),'3-18',''),'3-19',''),'3-20',''),'3-21',''),'3-22',''),'3-23',''),'3-24',''),
        #                '3-25',''),'3-26',''),'3-27',''),'3-28',''),'3-29',''),'3-30',''),'3-31',''),'3-32','')},
        #     'world 4':{'4-0',''),'4-1',''),'4-2',''),'4-3',''),'4-4',''),'4-5',''),'4-6',''),'4-7',''),'4-8',''),
        #                '4-9',''),'4-10',''),'4-11',''),'4-12',''),'4-13',''),'4-14',''),'4-15',''),'4-16'
        #                '4-17',''),'4-18',''),'4-19',''),'4-20',''),'4-21',''),'4-22',''),'4-23',''),'4-24',''),
        #                '4-25',''),'4-26',''),'4-27',''),'4-28',''),'4-29',''),'4-30',''),'4-31',''),'4-32','')},
        #     'world 5':{'5-0',''),'5-1',''),'5-2',''),'5-3',''),'5-4',''),'5-5',''),'5-6',''),'5-7',''),'5-8',''),
        #                '5-9',''),'5-10',''),'5-11',''),'5-12',''),'5-13',''),'5-14',''),'5-15',''),'5-16'
        #                '5-17',''),'5-18',''),'5-19',''),'5-20',''),'5-21',''),'5-22',''),'5-23',''),'5-24',''),
        #                '5-25',''),'5-26',''),'5-27',''),'5-28',''),'5-29',''),'5-30',''),'5-31',''),'5-32','')},
        #     'world 6':{'6-0',''),'6-1',''),'6-2',''),'6-3',''),'6-4',''),'6-5',''),'6-6',''),'6-7',''),'6-8',''),
        #                '6-9',''),'6-10',''),'6-11',''),'6-12',''),'6-13',''),'6-14',''),'6-15',''),'6-16'
        #                '6-17',''),'6-18',''),'6-19',''),'6-20',''),'6-21',''),'6-22',''),'6-23',''),'6-24',''),
        #                '6-25',''),'6-26',''),'6-27',''),'6-28',''),'6-29',''),'6-30',''),'6-31',''),'6-32','')},
        #     'world 7':{'7-0',''),'7-1',''),'7-2',''),'7-3',''),'7-4',''),'7-5',''),'7-6',''),'7-7',''),'7-8',''),
        #                '7-9',''),'7-10',''),'7-11',''),'7-12',''),'7-13',''),'7-14',''),'7-15',''),'7-16'
        #                '7-17',''),'7-18',''),'7-19',''),'7-20',''),'7-21',''),'7-22',''),'7-23',''),'7-24',''),
        #                '7-25',''),'7-26',''),'7-27',''),'7-28',''),'7-29',''),'7-30',''),'7-31',''),'7-32','')},
        #     'world 8':{'8-0',''),'8-1',''),'8-2',''),'8-3',''),'8-4',''),'8-5',''),'8-6',''),'8-7',''),'8-8',''),
        #                '8-9',''),'8-10',''),'8-11',''),'8-12',''),'8-13',''),'8-14',''),'8-15',''),'8-16'
        #                '8-17',''),'8-18',''),'8-19',''),'8-20',''),'8-21',''),'8-22',''),'8-23',''),'8-24',''),
        #                '8-25',''),'8-26',''),'8-27',''),'8-28',''),'8-29',''),'8-30',''),'8-31',''),'8-32','')},
        #     'world 9':{'9-0',''),'9-1',''),'9-2',''),'9-3',''),'9-4',''),'9-5',''),'9-6',''),'9-7',''),'9-8',''),
        #                '9-9',''),'9-10',''),'9-11',''),'9-12',''),'9-13',''),'9-14',''),'9-15',''),'9-16'
        #                '9-17',''),'9-18',''),'9-19',''),'9-20',''),'9-21',''),'9-22',''),'9-23',''),'9-24',''),
        #                '9-25',''),'9-26',''),'9-27',''),'9-28',''),'9-29',''),'9-30',''),'9-31',''),'9-32','')},
        #     'world 10':{'10-0',''),'10-1',''),'10-2',''),'10-3',''),'10-4',''),'10-5',''),'10-6',''),'10-7',''),'10-8',''),
        #                '10-9',''),'10-10',''),'10-11',''),'10-12',''),'10-13',''),'10-14',''),'10-15',''),'10-16'
        #                '10-17',''),'10-18',''),'10-19',''),'10-20',''),'10-21',''),'10-22',''),'10-23',''),'10-24',''),
        #                '10-25',''),'10-26',''),'10-27',''),'10-28',''),'10-29',''),'10-30',''),'10-31',''),'10-32','')},
        #     'world 11':{'11-0',''),'11-1',''),'11-2',''),'11-3',''),'11-4',''),'11-5',''),'11-6',''),'11-7',''),'11-8',''),
        #                '11-9',''),'11-10',''),'11-11',''),'11-12',''),'11-13',''),'11-14',''),'11-15',''),'11-16'
        #                '11-17',''),'11-18',''),'11-19',''),'11-20',''),'11-21',''),'11-22',''),'11-23',''),'11-24',''),
        #                '11-25',''),'11-26',''),'11-27',''),'11-28',''),'11-29',''),'11-30',''),'11-31',''),'11-32','')},
        #     'world 12':{'12-0',''),'12-1',''),'12-2',''),'12-3',''),'12-4',''),'12-5',''),'12-6',''),'12-7',''),'12-8',''),
        #                '12-9',''),'12-10',''),'12-11',''),'12-12',''),'12-13',''),'12-14',''),'12-15',''),'12-16'
        #                '12-17',''),'12-18',''),'12-19',''),'12-20',''),'12-21',''),'12-22',''),'12-23',''),'12-24',''),
        #                '12-25',''),'12-26',''),'12-27',''),'12-28',''),'12-29',''),'12-30',''),'12-31',''),'12-32','')},
        #     'world 13':{'13-0',''),'13-1',''),'13-2',''),'13-3',''),'13-4',''),'13-5',''),'13-6',''),'13-7',''),'13-8',''),
        #                '13-9',''),'13-10',''),'13-11',''),'13-12',''),'13-13',''),'13-14',''),'13-15',''),'13-16'
        #                '13-17',''),'13-18',''),'13-19',''),'13-20',''),'13-21',''),'13-22',''),'13-23',''),'13-24',''),
        #                '13-25',''),'13-26',''),'13-27',''),'13-28',''),'13-29',''),'13-30',''),'13-31',''),'13-32','')},
        #     'world 14':{'14-0',''),'14-1',''),'14-2',''),'14-3',''),'14-4',''),'14-5',''),'14-6',''),'14-7',''),'14-8',''),
        #                '14-9',''),'14-10',''),'14-11',''),'14-12',''),'14-13',''),'14-14',''),'14-15',''),'14-16'
        #                '14-17',''),'14-18',''),'14-19',''),'14-20',''),'14-21',''),'14-22',''),'14-23',''),'14-24',''),
        #                '14-25',''),'14-26',''),'14-27',''),'14-28',''),'14-29',''),'14-30',''),'14-31',''),'14-32','')},
        #     'world 15':{'15-0',''),'15-1',''),'15-2',''),'15-3',''),'15-4',''),'15-5',''),'15-6',''),'15-7',''),'15-8',''),
        #                '15-9',''),'15-10',''),'15-11',''),'15-12',''),'15-13',''),'15-14',''),'15-15',''),'15-16'
        #                '15-17',''),'15-18',''),'15-19',''),'15-20',''),'15-21',''),'15-22',''),'15-23',''),'15-24',''),
        #                '15-25',''),'15-26',''),'15-27',''),'15-28',''),'15-29',''),'15-30',''),'15-31',''),'15-32','')},
        #     'world 16':{'16-0',''),'16-1',''),'16-2',''),'16-3',''),'16-4',''),'16-5',''),'16-6',''),'16-7',''),'16-8',''),
        #                '16-9',''),'16-10',''),'16-11',''),'16-12',''),'16-13',''),'16-14',''),'16-15',''),'16-16'
        #                '16-17',''),'16-18',''),'16-19',''),'16-20',''),'16-21',''),'16-22',''),'16-23',''),'16-24',''),
        #                '16-25',''),'16-26',''),'16-27',''),'16-28',''),'16-29',''),'16-30',''),'16-31',''),'16-32','')},
        #     'world 17':{'17-0',''),'17-1',''),'17-2',''),'17-3',''),'17-4',''),'17-5',''),'17-6',''),'17-7',''),'17-8',''),
        #                '17-9',''),'17-10',''),'17-11',''),'17-12',''),'17-13',''),'17-14',''),'17-15',''),'17-16'
        #                '17-17',''),'17-18',''),'17-19',''),'17-20',''),'17-21',''),'17-22',''),'17-23',''),'17-24',''),
        #                '17-25',''),'17-26',''),'17-27',''),'17-28',''),'17-29',''),'17-30',''),'17-31',''),'17-32','')},
        #     'world 18':{'18-0',''),'18-1',''),'18-2',''),'18-3',''),'18-4',''),'18-5',''),'18-6',''),'18-7',''),'18-8',''),
        #                '18-9',''),'18-10',''),'18-11',''),'18-12',''),'18-13',''),'18-14',''),'18-15',''),'18-16'
        #                '18-17',''),'18-18',''),'18-19',''),'18-20',''),'18-21',''),'18-22',''),'18-23',''),'18-24',''),
        #                '18-25',''),'18-26',''),'18-27',''),'18-28',''),'18-29',''),'18-30',''),'18-31',''),'18-32','')},
        #     'world 19':{'19-0',''),'19-1',''),'19-2',''),'19-3',''),'19-4',''),'19-5',''),'19-6',''),'19-7',''),'19-8',''),
        #                '19-9',''),'19-10',''),'19-11',''),'19-12',''),'19-13',''),'19-14',''),'19-15',''),'19-16'
        #                '19-17',''),'19-18',''),'19-19',''),'19-20',''),'19-21',''),'19-22',''),'19-23',''),'19-24',''),
        #                '19-25',''),'19-26',''),'19-27',''),'19-28',''),'19-29',''),'19-30',''),'19-31',''),'19-32','')},
        #     'world 20':{'20-0',''),'20-1',''),'20-2',''),'20-3',''),'20-4',''),'20-5',''),'20-6',''),'20-7',''),'20-8',''),
        #                '20-9',''),'20-10',''),'20-11',''),'20-12',''),'20-13',''),'20-14',''),'20-15',''),'20-16'
        #                '20-17',''),'20-18',''),'20-19',''),'20-20',''),'20-21',''),'20-22',''),'20-23',''),'20-24',''),
        #                '20-25',''),'20-26',''),'20-27',''),'20-28',''),'20-29',''),'20-30',''),'20-31',''),'20-32','')},
        }


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


# 0 is sword skills, 1 is spells (stands), 2 is martial arts (sumo, hamon, sao ma skills)

def init_skills(): 
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
    savage_fulcrum = Skill('savage fulcrum', 0, 9, 3, 5, 13) # cooldown increase
    sonic_leap = Skill('sonic leap', 0, 9, 1, 4, 10)
    fell_cresent = Skill('fell cresent', 0, 10, 1, 4, 11)
    quad_pain = Skill('quad pain', 0, 11, 4, 3, 14)
    rapid_bite = Skill('rapid bite', 0, 12, 2, 3, 13)
    flashing_peirce = Skill('flashing peirce', 0, 13, 1, 3, 13)
    cascade = Skill('cascade', 0, 14, 1, 4, 15)
    treble_scythe = Skill('treble scythe', 0, 15, 3, 4, 20)
    rage_spike = Skill('rage spike', 0, 16, 1, 4, 17)
    horizontal_square = Skill('horizontal square', 0, 17, 4, 4, 25)
    vertical_square = Skill('vertical square', 0, 18, 4, 5, 26)
    water_surface_slash = Skill('water surface slash', 0, 19, 1, 5, 20) # cooldown increase
    snake_bite = Skill('snake bite', 0, 20, 2, 5, 23)
    folium = Skill('folium', 0, 21, 1, 4, 21)
    water_wheel = Skill('water wheel', 0, 22, 2, 5, 25)
    phantom_moon = Skill('phantom moon', 0, 23, 1, 5, 24)
    slashing_ray = Skill('slashing ray', 0, 24, 2, 5, 27)
    flowing_dance = Skill('flowing dance', 0, 25, 3, 5, 30)
    silent_ruin = Skill('silent ruin', 0, 26, 1, 4, 26)
    thunderclap_flash = Skill('thuderclap flash', 0, 27, 1, 5, 28)
    double_circular = Skill('double circular', 0, 28, 2, 6, 32)
    striking_tide = Skill('striking tide', 0, 29, 1, 5, 30)
    reaver = Skill('reaver', 0, 30, 1, 5, 31)
    slice_n_dice = Skill('slice n dice', 0, 31, 6, 5, 42)
    oblique = Skill('oblique', 0, 32, 1, 5, 33)
    blessed_rain = Skill('blessed rain', 0, 33, 5, 5, 42)
    embu = Skill('embu', 0, 34, 1, 5, 35)
    vorpal_strike = Skill('vorpal strike', 0, 35, 1, 5, 37)
    absolute_void = Skill('absolute void', 0, 36, 1, 5, 37)
    whirlpool = Skill('whirlpool', 0, 37, 4, 5, 44)
    ukifune = Skill('ukifune', 0, 38, 1, 5, 39)
    dancing_flash = Skill('dancing flash', 0, 39, 3, 4, 40)
    star_splash = Skill('star splash', 0, 40, 8, 4, 43)
    waterfall_basin = Skill('waterfall basin', 0, 42, 1, 5, 42)
    scarlet_fan = Skill('scarlet fan', 0, 44, 3, 5, 48) 
    deadly_sins = Skill('deadly sins', 0, 46, 7, 6, 59)
    constant_flux = Skill('constant flux', 0, 48, 2, 5, 51)
    clear_blue = Skill('clear blue', 0, 50, 3, 5, 55) 
    cataract = Skill('cataract', 0, 52, 2, 4, 52) 
    roar = Skill('roar', 0, 54, 2, 7, 58) 
    meteor_break = Skill('meteor break', 0, 56, 7, 6, 71) 
    dead_calm = Skill('dead calm', 0, 58, 12, 6, 83) # cooldown increase
    howling_octave = Skill('howling octave', 0, 60, 8, 6, 75) 
    raging_sun = Skill('raging sun', 0, 62, 6, 6, 74) 
    neutron = Skill('neutron', 0, 64, 5, 5, 66) 
    godspeed = Skill('godspeed', 0, 66, 3, 5, 67) 
    tsujikaze = Skill('tsujikaze', 0, 68, 9, 6, 84) 
    burning_bones = Skill('burning bones', 0, 70, 4, 6, 77) 
    volcanic_blazer = Skill('volcanic blazer', 0, 72, 8, 8, 95) 
    obscuring_clouds = Skill('burning bones', 0, 74, 10, 6, 93) 
    crucifixion = Skill('crucifixion', 0, 76, 6, 5, 78) 
    solar_heat_haze = Skill('solar heat haze', 0, 78, 9, 6, 96) 
    nova_ascension = Skill('nova ascension', 0, 80, 10, 7, 105)
    beneficient_radiance = Skill('beneficient radiance', 0, 82, 4, 6, 89) 
    dragon_halo = Skill('dragon halo', 0, 84, 6, 6, 95) 
    Rengoku = Skill('Rengoku', 0, 86, 1, 7, 88) # (top tier) # cooldown increase
    Meteor_Fall = Skill('Meteor Fall', 0, 88, 2, 8, 96) # (top tier)
    Hinokami_Kagura = Skill('Hinokami Kagura', 0, 90, 3, 7, 96) # (top tier)
    Lai = Skill('Lai', 0, 92, 1, 7, 96) # (top tier)
    Devine_Sword = Skill('Devine Sword', 0, 94, 1, 9, 101) # (top tier)
    Hiogi = Skill('Hiogi', 0, 96, 3, 7, 105) # (top tier)
    Zekku = Skill('Zekku', 0, 98, 1, 7, 102) # (top tier)
    Mothers_Rosario = Skill('Mothers Rosario', 0, 100, 11, 5, 111) # (top tier)
    The_Eclipse = Skill('The Eclipse', 0, 102, 27, 7, 164) # (top tier)
    Starburst_Stream = Skill('Starburst Stream', 0, 104, 16, 7, 150) # (top tier)


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

    spalls = [punch]

    return spalls

# # Define background music
# bgm_opening = pg.mixer.Sound('game\practice\music\mus_date.mp3')
# bgm_battle = pg.mixer.Sound('game\practice\music\mus_date_fight.mp3')
# bgm_hospital = pg.mixer.Sound('game\practice\music\mus_town.mp3')
# bgm_boss = pg.mixer.Sound('game\practice\music\Unlimited Power (loop).mp3')

