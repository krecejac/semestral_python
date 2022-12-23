import math
class Utils:
    def __init__(self, info):
        self.width = info['Width']
        self.height = info['Height']
        self.shape_im = (self.height,self.width)
        self.min_val = -math.sqrt(2) / 2
        self.max_val = abs(self.min_val)
        self.octaves = info['Octaves']
        self.threshold = 0
        self.persistence = info['Persistence'] #IMPORTANT
        self.lacunarity = info['Lacunarity']

class Color:
    DEEP_OCEAN = (94, 129, 172)
    OCEAN = (115, 146, 183)
    BEACH = (235, 203, 139)
    DESERT = (240, 200, 119)
    LAND = (143, 176, 115)
    FOREST = (82, 133, 48)
    DENSE_FOREST = (0,100,0)
    MOUNTAIN = (76, 86, 106)
    HIGH_MOUNTAIN = (121, 133, 159)
    SNOW = (255,255,255)
    SWAMP = (189,183,107)
    SAWANNA = (225,179,120)
    JUNGLE = (0,100,0)
    TUNDRA = (223,244,243)
    ICE = 	(202,225,255)
    LAVA = (207, 16, 32)
    MAGMA = (161,36,36)
    BARREN = (62, 67, 68)
class Mode:
    #TERRA = 0
    #DAGOBAH = 1
    #TATOOINE = 2
    #HOTH = 3
    #KASHYYYK = 4
    #KAMINO = 5
    #MUSTAFAR = 6
    def __init__(self, utils:Utils, mode_curr):
        self.curr_mode = mode_curr.upper()
        if self.curr_mode == "TERRA": # NORMAL
            utils.threshold = 0
        elif self.curr_mode == "DAGOBAH": # DAGOBAH
            utils.threshold = -0.3
        elif self.curr_mode == "TATOOINE": # TATOOINE
            utils.threshold = 0.4
        elif self.curr_mode == "HOTH": # HOTH
            utils.threshold = -0.4
        elif self.curr_mode == "KASHYYYK": # KASHYYYK
            utils.threshold = -0.1