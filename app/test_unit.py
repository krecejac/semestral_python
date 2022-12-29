import pytest
import src.generator as gen
import utils.var as var

def test_assign_terrain():
    assert(gen.assignTerrain(0.12, 0.5, 0, "Terra") == var.Color.DEEP_OCEAN)
    assert(gen.assignTerrain(100, 0.5, 0, "Terra") == var.Color.SNOW)
    assert(gen.assignTerrain(0.75, 100, 0, "Terra") == var.Color.JUNGLE)
    assert(gen.assignTerrain(0.65, 0.5, 0, "Kashyyyk") == var.Color.OCEAN)
    assert(gen.assignTerrain(0.65, 0.5, 100, "Mustafar") == var.Color.MAGMA)
    #Dagobah low possibiility of beach but not impossible (around 30%)
    assert(gen.assignTerrain(0.68, 0.25, -0.3, "Dagobah") == var.Color.BEACH)
    assert(gen.assignTerrain(0.68, 0.3, -0.3, "Dagobah") == var.Color.SWAMP)
    #Hoth very low possibility of beach but not impossible (around 20% or less)
    assert(gen.assignTerrain(0.68, 0.5, -0.4, "Hoth") == var.Color.ICE)
    #Tatooine very low possibility of snow but not impossible (around 20% or less)
    assert(gen.assignTerrain(0.76, 0.5, 0.4, "Tatooine") == var.Color.MOUNTAIN)
    assert(gen.assignTerrain(0.76, 0.8, 0.4, "Tatooine") == var.Color.SNOW)
    assert(gen.assignTerrain(0.75, 0.6, -0.1, "Kashyyyk") == var.Color.DENSE_FOREST)

def test_perlinCustom():
    pass
