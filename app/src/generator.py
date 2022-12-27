import numpy as np
from noise import pnoise2
from PIL import Image
import matplotlib.pyplot as plt
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

def assignTerrain(e, m, threshold, mode):
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
class Vector2:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def dot(self, other):
		return self.x*other.x + self.y*other.y

def GetConstantVector(v):
	h = v & 3
	if(h == 0):
		return Vector2(1.0, 1.0)
	elif(h == 1):
		return Vector2(-1.0, 1.0)
	elif(h == 2):
		return Vector2(-1.0, -1.0)
	else:
		return Vector2(1.0, -1.0)

def Fade(t):
	return ((6*t - 15)*t + 10)*t*t*t

def Lerp(t, a1, a2):
	return a1 + t*(a2-a1)

def noiseRandom(x, y, permutation):
	X = math.floor(x) & 255
	Y = math.floor(y) & 255

	xf = x-math.floor(x)
	yf = y-math.floor(y)

	topRight = Vector2(xf-1.0, yf-1.0)
	topLeft = Vector2(xf, yf-1.0)
	bottomRight = Vector2(xf-1.0, yf)
	bottomLeft = Vector2(xf, yf)
	
	valueTopRight = permutation[permutation[X+1]+Y+1]
	valueTopLeft = permutation[permutation[X]+Y+1]
	valueBottomRight = permutation[permutation[X+1]+Y]
	valueBottomLeft = permutation[permutation[X]+Y]
	
	dotTopRight = topRight.dot(GetConstantVector(valueTopRight))
	dotTopLeft = topLeft.dot(GetConstantVector(valueTopLeft))
	dotBottomRight = bottomRight.dot(GetConstantVector(valueBottomRight))
	dotBottomLeft = bottomLeft.dot(GetConstantVector(valueBottomLeft))
	
	u = Fade(xf)
	v = Fade(yf)
	
	return Lerp(u,
		Lerp(v, dotBottomLeft, dotTopLeft),
		Lerp(v, dotBottomRight, dotTopRight)
	)

def saveImage( image, utils ):
    filename = utils.curr_mode.lower() + str(utils.save_im) + ".png"
    utils.save_im += 1
    image.save(f"utils/images/{filename}", 'PNG')

def saveGraph(utils):
    filename = "utils/graphs/" + "graph" + str(utils.save_graph) + ".png"
    plt.savefig(filename)

def showGraph( map ):
    plt.imshow(map)
    plt.show()

def show3Dgraph( elevation:np.array, utils, moisture:np.array ):
    fig = plt.figure()
    x = np.arange(len(elevation[0]))
    y = np.arange(len(elevation))
    (x ,y) = np.meshgrid(x,y)

    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(x,y,elevation, cmap='terrain')
    ax1.set_zlim([0, 1.2])
    ax1.set_title("Elevation map")

    ax2 = fig.add_subplot(122, projection='3d')
    surf2 = ax2.plot_surface(x,y,moisture, cmap='Blues')
    fig.colorbar(surf2, shrink=0.5, aspect=10)
    ax2.set_title("Moisture map")

    plt.show()
    if utils.saving:
        saveGraph(utils)


def makeImage(elevation, moisture, utils):
    rgb = [
        assignTerrain(elevation[y][x], moisture[y][x], utils.threshold, utils.curr_mode)
        for y in range(utils.height)
        for x in range(utils.width) 
    ]
    image = Image.new("RGB", utils.shape_im)
    image.putdata(rgb)
    image.show()
    if utils.saving:
        saveImage(image, utils)

def createPixel(nx, ny, utils):
    if utils.custom:
        return PerlinCustom(nx, ny, utils)
    else:
        return PerlinLib(nx, ny, utils)

def PerlinLib( nx, ny, utils ):
    return pnoise2(nx, ny, octaves=utils.octaves, persistence=utils.persistence, 
    lacunarity=utils.lacunarity, base=utils.seed)

def PerlinCustom( nx, ny, utils):
    amplitude = 1
    frequency = 1
    max_value = 0
    e = 0
    if utils.octaves > 3:
        octaves = 3
    else: octaves = utils.octaves
    for octave in range(octaves):
        e += (noiseRandom(nx * frequency, ny * frequency, utils.permutation) * amplitude)
        max_value += amplitude
        amplitude *= utils.persistence
        frequency *= 2
    e /= max_value
    return e

def createElevation(x, y, utils):
    nx = 2*x/utils.width - 1; ny = 2*y/utils.height - 1
    e = createPixel(nx, ny, utils)
    d = min( 1, (np.power(nx,2) + np.power(ny,2)) / np.sqrt(2) ) + 0.4
    e = (e + (1-d)) / 2
    e = ( e - utils.min_val)/(utils.max_val-utils.min_val )
    return e

def createMoisture(x, y, utils):
    nx = 2*x/utils.width - 1; ny = 2*y/utils.height - 1
    m = createPixel(nx, ny, utils)
    m = ( m - utils.min_val)/(utils.max_val-utils.min_val )
    return m

def noiseCreate(choice):
    utils = var.Utils(choice)
    elevation = np.zeros(shape=(utils.shape_im[0], utils.shape_im[1]), dtype=np.uint8)
    moisture = np.zeros(shape=(utils.shape_im[0], utils.shape_im[1]), dtype=np.uint8)
    elevation = np.array([
        [createElevation(x,y,utils) for x in range(utils.width)] for y in range(utils.height) 
        ])
    moisture = np.array([
        [createMoisture(x,y,utils) for x in range(utils.width)] for y in range(utils.height)
        ])
    makeImage(elevation, moisture, utils)
    if utils.plot3d:
        show3Dgraph(elevation, utils, moisture)