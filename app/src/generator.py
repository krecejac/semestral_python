import numpy as np
from noise import pnoise2
from PIL import Image
import matplotlib.pyplot as plt
import math
import plotly
import plotly.graph_objects as go
import utils.var as var

class Vector2:
    """
    My implementation of vector values. Has the coordinates, x and y.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def dot(self, other):
        return self.x*other.x + self.y*other.y

def getConstantVector(v):
    #v is the value of the permutation table
	h = v & 3
	if(h == 0):
		return Vector2(1.0, 1.0)
	elif(h == 1):
		return Vector2(-1.0, 1.0)
	elif(h == 2):
		return Vector2(-1.0, -1.0)
	else:
		return Vector2(1.0, -1.0)

def fade(t):
    #ease function for the curve, also 
    #as the called fade function.
	return ((6*t - 15)*t + 10)*t*t*t

def lerp(t, a1, a2):
    #linear interpolation
	return a1 + t*(a2-a1)

def noiseRandom(x, y, permutation):
    # Determine grid cell coordinates
	X = math.floor(x) & 255
	Y = math.floor(y) & 255
    # Detemine interpolation weights
	xf = x-math.floor(x)
	yf = y-math.floor(y)

    #hash coordinates of the 4 corners of grid
	valueTopRight = permutation[permutation[X+1]+Y+1]
	valueTopLeft = permutation[permutation[X]+Y+1]
	valueBottomRight = permutation[permutation[X+1]+Y]
	valueBottomLeft = permutation[permutation[X]+Y]
	
	topRight = Vector2(xf-1.0, yf-1.0)
	topLeft = Vector2(xf, yf-1.0)
	bottomRight = Vector2(xf-1.0, yf)
	bottomLeft = Vector2(xf, yf)
	
    #calculating dot products
	dotTopRight = topRight.dot(getConstantVector(valueTopRight))
	dotTopLeft = topLeft.dot(getConstantVector(valueTopLeft))
	dotBottomRight = bottomRight.dot(getConstantVector(valueBottomRight))
	dotBottomLeft = bottomLeft.dot(getConstantVector(valueBottomLeft))
	
	u = fade(xf)
	v = fade(yf)
    #linear interpolation
	return lerp(u,
		lerp(v, dotBottomLeft, dotTopLeft),
		lerp(v, dotBottomRight, dotTopRight)
	)

def saveImage( image, utils ):
    filename = utils.curr_mode.lower() + str(utils.save_im) + ".png"
    utils.save_im += 1
    image.save(f"utils/images/{filename}", 'PNG')

def saveGraph(utils):
    filename = "utils/graphs/" + "graph" + str(utils.save_graph) + ".png"
    plt.savefig(filename)

def makeInteractiveGraph(elevation):
    """
    Takes elevation map and uses plotly library to and shows it in html.
    """
    terrain_cmap = plt.cm.get_cmap('terrain')
    terrain = matplotlib_to_plotly(terrain_cmap, 255)
    plotly.offline.init_notebook_mode(connected=True)
    fig2 = go.Figure(data=[go.Surface(colorscale=terrain,z=elevation)])
    fig2.update_layout(title='Perlin Noise 3D Terrain')
    html = plotly.offline.plot(fig2, filename='utils/mapping/3d-terrain-plotly.html',include_plotlyjs='cdn')
    from IPython.core.display import HTML
    HTML(html)

def matplotlib_to_plotly(cmap, pl_entries):
    """
    Takes cmap of terrain and transforms it to the plotly color map.
    """
    h = 1.0/(pl_entries-1)
    pl_colorscale = []
    for k in range(pl_entries):
        C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
        pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])
    return pl_colorscale

def show3Dgraph( elevation:np.array, moisture:np.array, utils:var.Utils ):
    """
    If the 3D plot option is switched on, we plot both graphs on a figure or and save it.
    """
    if elevation.shape != utils.shape_im or moisture.shape != utils.shape_im:
        raise ValueError("The generated noise is not in default width or height")
    fig = plt.figure()
    x = np.arange(len(elevation[0])) #Both surfaces have same x,y axis, they are the same lenght
    y = np.arange(len(elevation))    #Both surfaces have same x,y axis, they are the same lenght
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

def Dagobah(m):
    #Favorizes high moisture biomes like Forest, Jungle, Land.
    if m < 0.3: return var.Color.LAND
    if m < 0.4: return var.Color.FOREST
    if m < 0.7: return var.Color.JUNGLE
    else: return var.Color.TUNDRA

def Hoth(m):
    #Favorizes high moisture/elevation biomes like Tundra, Snow
    if m < 0.3: return var.Color.LAND
    if m < 0.5: return var.Color.TUNDRA
    else: return var.Color.SNOW

def Tatooine(m):
    #Favorizes low moisture biomes like Desert, Sawanna
    if m < 0.4: return var.Color.DESERT
    if m < 0.6: return var.Color.SAWANNA
    else: return var.Color.LAND

def Kashyyyk(m):
    #Favorizes higher moisture biomes. But not much as Dagobah.
    if m < 0.1: return var.Color.LAND
    if m < 0.5: return var.Color.FOREST
    if m < 0.8: return var.Color.DENSE_FOREST
    else: return var.Color.SWAMP

def Kamino(e):
    #Favorizes water. Special mode.
    if e <= 0.5: return var.Color.DEEP_OCEAN
    if e <= 0.74: return var.Color.OCEAN
    if e <= 0.755: return var.Color.BEACH
    else: return var.Color.HIGH_MOUNTAIN

def Mustafar(e):
    #Special bonus mode. Uses lava as ocean and magma as low elevation values.
    if e <= 0.6: return var.Color.LAVA
    if e <= 0.65: return var.Color.MAGMA
    if e <= 0.74: return var.Color.BARREN
    else: return var.Color.HIGH_MOUNTAIN

def assignTerrain(e, m, threshold, mode):
    """
    Main function used for determinign each biome. Elevation and moisture.
    If there is set special mode, the condition changes the result fitting for the right biom.
    In edge cases, there is the threshold method used for determining simular biomes like Hoth or Dagobah.
    The modes are: Terra, Dagobah, Tatooine, Hoth, Kashyyyk, Kamino, Mustafar
    """
    if mode == "Kamino": return Kamino(e)     #Special modes of Kamino and Mustafar
    if mode == "Mustafar": return Mustafar(e) #Special modes of Kamino and Mustafar
    #Takes care of low elevation first
    if e <= 0.6: return var.Color.DEEP_OCEAN
    if e <= 0.65: return var.Color.OCEAN
    if e <= 0.68:
        if m < 0.6+threshold: return var.Color.BEACH #it's not impossible for Hoth to have beach
        elif mode == "Hoth": return var.Color.ICE
        else: return var.Color.SWAMP

    #Next is deciding if we are in mountains. Simular for each mode. Tatooine doesnt have much snow.
    if e > 0.75:
        if m-threshold < 0.3: return var.Color.MOUNTAIN #it's not impossible for Tatooine to have snow
        if m < 0.5: return var.Color.HIGH_MOUNTAIN
        else: return var.Color.SNOW

    #The rest is vastly different.
    if e <= 0.75:
        if mode == "Dagobah": return Dagobah(m)
        if mode == "Tatooine": return Tatooine(m)
        if mode == "Hoth": return Hoth(m)
        if mode == "Kashyyyk": return Kashyyyk(m)
        # normal mode of Terra
        if m < 0.3: return var.Color.DESERT
        if m < 0.4: return var.Color.SAWANNA
        if m < 0.5: return var.Color.LAND
        if m < 0.6: return var.Color.FOREST
        else: return var.Color.JUNGLE

def makeImage(elevation:np.array, moisture:np.array, utils:var.Utils):
    """
    From the elevation and moisture noises we assign correct Terrain (also depending on the mode)
    and fill the rgb numpy array with tuples of colors. After that we show the image or and
    save it.
    """
    if elevation.shape != utils.shape_im or moisture.shape != utils.shape_im:
        raise ValueError("The generated noise is not in default width or height")
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

def perlinCustom(nx, ny, utils:var.Utils ):
    """
    The custom implementation of perlin noise. Inspired by the perlin noise reference
    implementation by none other than the Ken Perlin.
    https://cs.nyu.edu/~perlin/noise/
    """
    amplitude = 1
    frequency = 1
    max_value = 0
    e = 0
    if utils.octaves > 3:
        octaves = 3
    else: octaves = utils.octaves
    #fractal brownian motion uses octaves.
    for octave in range(octaves):
        e += (noiseRandom(nx * frequency, ny * frequency, utils.permutation) * amplitude)
        max_value += amplitude
        amplitude *= utils.persistence
        frequency *= 2
    e /= max_value
    return e

def perlinLib( nx, ny, utils:var.Utils ):
    return pnoise2(nx, ny, octaves=utils.octaves, persistence=utils.persistence, 
    lacunarity=utils.lacunarity, base=utils.seed)

def createPixel(ny, utils:var.Utils, row) -> np.array:
    """
    This function chooses whether we use the pnoise library or use my custom implementation.
    """
    if utils.custom:
        return np.array([perlinCustom(nx, ny, utils) for nx in row])
        #return perlinCustom(nx, ny, utils)
    else:
        return np.array([perlinLib(nx, ny, utils) for nx in row])
        #return perlinLib(nx, ny, utils)

def createElevation(y, utils:var.Utils) -> np.array:
    """
    Function for calculating elevation. Takes x,y coordinates in the matrix and the
    current noise mode (pnoise library, custom).
    It also shapes the noise to circular shape with
    euclidian reshaping function 
    """
    ny = 2*y/utils.height - 1
    row = np.array([ (2*x/utils.width - 1) for x in range(utils.width)])
    d = np.array([((min( 1, (np.power(nx,2) + np.power(ny,2)) / np.sqrt(2) ) + 0.4)) for nx in row ])
    row_e = createPixel(ny,utils,row)
    row_e = (row_e + ( np.negative(d) + 1)) / 2
    row_e = ( row_e - utils.min_val )/(utils.max_val-utils.min_val)
    return row_e

def createMoisture(y, utils:var.Utils) -> np.array:
    """
    Function for calculating moisture. Takes x,y coordinates in the matrix and the
    current noise mode (pnoise library, custom).
    """
    ny = 2*y/utils.height - 1
    row = np.array([ (2*x/utils.width - 1) for x in range(utils.width)])
    row_m = createPixel(ny,utils,row)
    row_m = ( row_m - utils.min_val )/(utils.max_val-utils.min_val)
    return row_m

def createNoise(choice):
    """
    Main function for creating perlin noise. Takes a dictionary from user input
    for the utilities object. The result is 2d numpy array of computed
    elevation and moisture noises.
    """
    utils = var.Utils(choice) #the dictionary from input
    elevation = np.array([
        (createElevation(y, utils)) for y in range(utils.height)
        ])
    moisture = np.array([
        (createMoisture(y, utils)) for y in range(utils.height)
        ])
    makeImage(elevation, moisture, utils)
    if utils.plot3d: #if the 3d Plot option is selected, the variable is set to 1
        show3Dgraph(elevation, moisture, utils)
    if utils.mapping:
        makeInteractiveGraph(elevation)
