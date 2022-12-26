import random
import numpy as np
from noise import pnoise2
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import utils.var as var

def Dagobah(m):
    if m < 0.3: return var.Color.LAND
    if m < 0.4: return var.Color.FOREST
    if m < 0.7: return var.Color.JUNGLE
    else: return var.Color.TUNDRA

def Hoth(m):
    if m < 0.3: return var.Color.LAND
    if m < 0.5: return var.Color.TUNDRA
    else: return var.Color.SNOW

def Tatooine(m):
    if m < 0.4: return var.Color.DESERT
    if m < 0.6: return var.Color.SAWANNA
    else: return var.Color.LAND

def Kashyyyk(m):
    if m < 0.1: return var.Color.LAND
    if m < 0.5: return var.Color.FOREST
    if m < 0.8: return var.Color.DENSE_FOREST
    else: return var.Color.SWAMP

def Kamino(e):
    if e <= 0.5: return var.Color.DEEP_OCEAN
    if e <= 0.74: return var.Color.OCEAN
    if e <= 0.755: return var.Color.BEACH
    else: return var.Color.HIGH_MOUNTAIN

def Mustafar(e):
    if e <= 0.6: return var.Color.LAVA
    if e <= 0.65: return var.Color.MAGMA
    if e <= 0.74: return var.Color.BARREN
    else: return var.Color.HIGH_MOUNTAIN

def color(e, m, threshold, mode):
    if mode == "Kamino": return Kamino(e)
    if mode == "Mustafar": return Mustafar(e)
    if e <= 0.6: return var.Color.DEEP_OCEAN
    if e <= 0.65: return var.Color.OCEAN
    if e <= 0.68:
        if m < 0.6+threshold: return var.Color.BEACH
        elif mode == "Hoth": return var.Color.ICE
        else: return var.Color.SWAMP

    if e > 0.75:
        if m-threshold < 0.3: return var.Color.MOUNTAIN
        if m < 0.5: return var.Color.HIGH_MOUNTAIN
        else: return var.Color.SNOW

    if e <= 0.75:
        if mode == "Dagobah": return Dagobah(m)
        if mode == "Tatooine": return Tatooine(m)
        if mode == "Hoth": return Hoth(m)
        if mode == "Kashyyyk": return Kashyyyk(m)
        if m < 0.3: return var.Color.DESERT
        if m < 0.4: return var.Color.SAWANNA
        if m < 0.5: return var.Color.LAND
        if m < 0.6: return var.Color.FOREST
        else: return var.Color.JUNGLE

def saveImage( image, utils ):
    filename = utils.curr_mode.lower() + str(utils.save_im) + ".png"
    utils.save_im += 1
    image.save(f"utils/images/{filename}", 'PNG')

def saveGraph(utils):
    filename = "utils/graphs/" + "graph" + str(utils.save_graph) + ".png"
    plt.savefig(filename)

def show_map( image_array, utils ):
    image = Image.fromarray(image_array)
    image.show()
    if( utils.saving ):
        saveImage(image, utils)

def show_graph( map ):
    plt.imshow(map)
    plt.show()

def show_3Dgraph( map:np.array, utils ):
    xx, yy = np.mgrid[0:map.shape[0], 0:map.shape[1]]
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111,projection='3d')
    ax.plot_surface(xx, yy, map,rstride=1, cstride=1, cmap='viridis',
            linewidth=0)
    if( utils.saving ):
        saveGraph(utils)
    plt.show()

def noise_create(choice):
    utils = var.Utils(choice)
    im = np.zeros(shape=(utils.shape_im[0], utils.shape_im[1],3), dtype=np.uint8)
    elevation = np.zeros(shape=(utils.shape_im[0], utils.shape_im[1]))
    seed = random.randint(0,100)
    seed_moisture = seed-1 if seed != 0 else 1
    for y in range(utils.height):
        for x in range(utils.width):
            nx = 2*x/utils.width - 1; ny = 2*y/utils.height - 1
            e = pnoise2(nx, ny, octaves=utils.octaves, persistence=utils.persistence, lacunarity=utils.lacunarity, base=seed)
            m = pnoise2(nx, ny, octaves=utils.octaves, persistence=utils.persistence, lacunarity=utils.lacunarity, base=seed_moisture)
            d = min( 1, (np.power(nx,2) + np.power(ny,2)) / math.sqrt(2) ) + 0.4
            e = (e + (1-d)) / 2
            e = ( e - utils.min_val)/(utils.max_val-utils.min_val)
            m = ( m - utils.min_val)/(utils.max_val-utils.min_val)
            elevation[y][x] = e
            colour = color(e, m, utils.threshold, utils.curr_mode)
            im[y][x] = colour
    show_map(im, utils)
    if( utils.plot3d ):
        show_3Dgraph(elevation, utils)