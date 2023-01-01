"""
Variables and utilities module
"""
import math
import os
import os.path
import random
import glob


class Utils:
    """
    The module of utilities and variables. Handles all important info for the program.
    """
    def __init__(self, info):
        """
        Takes values from the graphical interface(user) and saves it.
        Can be changed at any moment.
        """
        self.width = info['Width']
        self.height = info['Height']
        self.shape_im = (self.height, self.width)  # SHOULD ALWAYS BE A SQUARE!
        # checks whether the dimension are square or not.
        self.CheckDimensions()
        # Used for normalizing values to [0,1]
        self.min_val = -math.sqrt(2) / 2
        # Used for normalizing values to [0,1]
        self.max_val = abs(self.min_val)
        self.octaves = info['Octaves']
        self.threshold = 0  # used later in assigning terrain
        self.persistence = info['Persistence']  # IMPORTANT
        self.lacunarity = info['Lacunarity']
        self.plot3d = info['Print3d']
        self.custom = info['Custom']  # custom noise/pnoise lib
        self.saving = info['Save']  # save images
        self.mapping = info['Mapping']
        self.save_im = len([name for name in os.listdir('utils/images') if os.path.isfile(
            'utils/images/' + name)])  # Counts the number of files in subdir
        # Counts the number of files in subdir
        self.save_graph = len([name for name in os.listdir(
            'utils/graphs') if os.path.isfile('utils/graphs/' + name)])
        self.curr_mode = info['Mode']
        self.SetMode()  # sets up the island Mode.
        self.RefreshHtmlFile()
        #TERRA = 0
        #DAGOBAH = 1
        #TATOOINE = 2
        #HOTH = 3
        #KASHYYYK = 4
        #KAMINO = 5
        #MUSTAFAR = 6
        # makes new random permutation and random.random seed.
        self.MakePermutation()

    def SetMode(self):
        if self.curr_mode == "Terra":  # NORMAL
            self.threshold = 0
        elif self.curr_mode == "Dagobah":  # DAGOBAH
            self.threshold = -0.3
        elif self.curr_mode == "Tatooine":  # TATOOINE
            self.threshold = 0.4
        elif self.curr_mode == "Hoth":  # HOTH
            self.threshold = -0.4
        elif self.curr_mode == "Kashyyyk":  # KASHYYYK
            self.threshold = -0.1

    def MakePermutation(self):
        """
        Creates new random seed for moisture and elevation. Also makes permutation table
        for custom perlin noise. It randomly assigns values and shuffle the list accordingly.
        Is used later in noiseRandom function.
        """
        self.seed = random.randint(0, 100)
        self.seed_moisture = self.seed - 1 if self.seed != 0 else 1
        self.permutation = []
        for i in range(256):
            self.permutation.append(i)

        random.shuffle(self.permutation)
        for i in range(256):
            self.permutation.append(self.permutation[i])
        return self.permutation

    def RefreshHtmlFile(self):
        files = glob.glob('utils/mapping/*')
        for f in files:
            os.remove(f)

    def CheckDimensions(self):
        """
        A quick check. If we were to put a non square values. The euclidian function in the
        generation of the noise would warp the land. This is to ensure the island looks normal.
        """
        if self.width != self.height:
            self.width = self.height


class Color:
    """
    RGB colors for each biom.
    """
    DEEP_OCEAN = (94, 129, 172)
    OCEAN = (115, 146, 183)
    BEACH = (235, 203, 139)
    DESERT = (240, 200, 119)
    LAND = (143, 176, 115)
    FOREST = (82, 133, 48)
    DENSE_FOREST = (0, 100, 0)
    MOUNTAIN = (76, 86, 106)
    HIGH_MOUNTAIN = (121, 133, 159)
    SNOW = (255, 255, 255)
    SWAMP = (189, 183, 107)
    SAWANNA = (225, 179, 120)
    JUNGLE = (0, 100, 0)
    TUNDRA = (223, 244, 243)
    ICE = (202, 225, 255)
    LAVA = (207, 16, 32)
    MAGMA = (161, 36, 36)
    BARREN = (62, 67, 68)
