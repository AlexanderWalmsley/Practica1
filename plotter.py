import cartopy
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
import pathlib as pth
# import cmocean
from numpy.core._multiarray_umath import ndarray
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from datetime import datetime
import json

plt.rcParams['figure.figsize'] = (12, 12)
configs = pth.Path("FIGURES_KING/configs").glob('*.json')
contour_name_list = ["contour", "contours", "contorno", "contornos"]
shading_name_list = ["shading", "sombreado", "colors", "colours", "coloring", "colouring"]
quiver_name_list = ["quivers", "vectors", "arrows", "flechas", "vectores"]
barb_name_list = ["barbs", "barbas"]


# Creates the base map to build upon
def plotMap(map_config):
    # Create a figure with an axes object on which we will plot. Pass the projection to that axes.
    fig, ax = plt.subplots(subplot_kw=dict(projection=projections[map_config["projection"]]))

    # Zoom in
    ax.set_extent(map_config["extent"])

    # Add map features
    ax.add_feature(cfeature.LAND, facecolor='0.9')  # Grayscale colors can be set using 0 (black) to 1 (white)
    ax.add_feature(cfeature.LAKES, alpha=0.9)  # Alpha sets transparency (0 is transparent, 1 is solid)
    ax.add_feature(cfeature.BORDERS, zorder=10)
    ax.coastlines(resolution=map_config["coastline_res"], color=map_config["coastline_color"],
                  linewidth=1, zorder=10)

    # We can use additional features from Natural Earth (http://www.naturalearthdata.com/features/)
    # states_provinces = cfeature.NaturalEarthFeature(
    #     category='cultural', name='admin_1_states_provinces_lines',
    #     scale='50m', facecolor='none')
    # ax.add_feature(states_provinces, edgecolor='gray', zorder=10)

    # Add lat/lon gridlines every 20° to the map
    gl = ax.gridlines(xlocs=np.arange(-180, 180, 10), ylocs=np.arange(-80, 90, 10), zorder=12, draw_labels=True)
    gl.top_labels = True
    gl.right_labels = False
    gl.bottom_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 18, 'color': 'gray'}
    gl.ylabel_style = {'size': 18, 'color': 'gray'}
    return fig, ax


# takes axes generated by plotMap(),  a dataset (ds), a dictionary, ideally from the .json file and a time value
# to plot colors onto the base map
def plot_shading(ax, ds, dictionary, t):
    # Plot the 500-hPa height contours on the map, in black, with line width 1, and plot it above everything else.

    lon = ds['longitude']
    lat = ds['latitude']
    if dictionary["level"] is not None:
        var = ds[dictionary["vars"][0]].sel(level=dictionary["level"]).isel(time=t).values
    else:
        var = ds[dictionary["vars"][0]].isel(time=t).values

    if "conversions" in dictionary:
        calculator = Calculator(var, dictionary)
        var = calculator.calculate()

    levels = np.arange(dictionary["levels"][0], dictionary["levels"][1], dictionary["levels"][2])
    smooth = ndimage.gaussian_filter(var, sigma=1, order=0) # add sigma to configs
    contour = ax.contourf(lon, lat, smooth, levels=levels, cmap=dictionary["colors"], zorder=3,
                          transform=ccrs.PlateCarree())

    cb = plt.colorbar(contour, shrink=0.8)
    cb.ax.set_ylabel('{}'.format(dictionary["name"]), fontsize=18)
    cb.ax.tick_params(labelsize=14)
    return


# takes axes generated by plotMap(),  a dataset (ds), a dictionary, ideally from the .json file and a time value
# to plot a contour onto the base map
def plot_contour(ax, ds, dictionary, t):
    # Plot the 500-hPa height contours on the map, in black, with line width 1, and plot it above everything else.

    lon = ds['longitude']
    lat = ds['latitude']
    if dictionary["level"] is not None:
        var = ds[dictionary["vars"][0]].sel(level=dictionary["level"]).isel(time=t).values
    else:
        var = ds[dictionary["vars"][0]].isel(time=t).values

    if "conversions" in dictionary:
        calculator = Calculator(var, dictionary)
        var = calculator.calculate()

    levels = np.arange(dictionary["levels"][0], dictionary["levels"][1], dictionary["levels"][2])
    smooth = ndimage.gaussian_filter(var, sigma=1, order=0)
    contour = ax.contour(lon, lat, smooth, levels=levels, linewidths=1.5, colors=dictionary['colors'],
                         zorder=11, transform=ccrs.PlateCarree())
    plt.clabel(contour, inline=True, fmt='%2i', fontsize=14)
    return


# takes axes generated by plotMap(),  a dataset (ds), a dictionary, ideally from the .json file and a time value
# to plot colors onto the base map
def plot_vectors(ax, ds, dictionary, t):
    if dictionary["level"] is not None:
        var1 = ds[dictionary["vars"][0]].sel(level=dictionary["level"]).isel(time=t).values
        var2 = ds[dictionary["vars"][1]].sel(level=dictionary["level"]).isel(time=t).values
    else:
        var1 = ds[dictionary["vars"][0]].isel(time=t).values
        var2 = ds[dictionary["vars"][1]].isel(time=t).values
    if "conversions" in dictionary:
        calculator1 = Calculator(var1, dictionary)
        calculator2 = Calculator(var2, dictionary)
        var1 = calculator1.calculate()
        var2 = calculator2.calculate()
    lon = ds['longitude']
    lat = ds['latitude']
    nral = dictionary["density"] # lower is denser
    ax.quiver(lon[::nral], lat[::nral], var1[::nral, ::nral], var2[::nral, ::nral],
              pivot='middle', zorder=12, transform=ccrs.PlateCarree())

    return


def plot_barbs(ax, ds, dictionary, t):
    if dictionary["level"] is not None:
        var1 = ds[dictionary["vars"][0]].sel(level=dictionary["level"]).isel(time=t).values
        var2 = ds[dictionary["vars"][1]].sel(level=dictionary["level"]).isel(time=t).values
    else:
        var1 = ds[dictionary["vars"][0]].isel(time=t).values
        var2 = ds[dictionary["vars"][1]].isel(time=t).values
    if "conversions" in dictionary:
        calculator1 = Calculator(var1, dictionary)
        calculator2 = Calculator(var2, dictionary)
        var1 = calculator1.calculate()
        var2 = calculator2.calculate()

    lon = ds['longitude']
    lat = ds['latitude']
    nral = dictionary["density"]
    ax.barbs(lon[::nral], lat[::nral], var1[::nral, ::nral], var2[::nral, ::nral],
             pivot='middle', zorder=12, length=dictionary["length"], transform=ccrs.PlateCarree())

    return


def plot_scatter(ax, ds, dictionary):
    ax.scatter(ds[dictionary["position"][0]], ds[dictionary["position"][1]], transform=ccrs.PlateCarree(),
               edgecolors=ds[dictionary['colors']])
    return


class Calculator:

    def __init__(self, a, settings):
        self.calcs = settings["conversions"]
        self.a = a

    def add(self, b):
        self.a += b
        return

    def subract(self, b):
        self.a -= b
        return

    def multiply(self, b):
        self.a = self.a * b
        return

    def divide(self, b):
        self.a = self.a / b
        return

    def calculate(self):
        if self.calcs is not None:
            for ii in range(len((self.calcs))):
                if self.calcs[ii][0] == "add":
                    self.add(self.calcs[ii][1])
                elif self.calcs[ii][0] == "subtract":
                    self.subract(self.calcs[ii][1])
                elif self.calcs[ii][0] == "multiply":
                    self.multiply(self.calcs[ii][1])
                elif self.calcs[ii][0] == "divide":
                    self.divide(self.calcs[ii][1])
            return self.a


# main loop
for path in configs:
    config = open(path)
    config = json.load(config)
    map_settings = config["map_settings"]
    data = config["data"]
    ds2 = xr.open_dataset(data[0]['file'])
    projections = dict(Mercator=ccrs.Mercator(central_longitude=map_settings["central longitude"]),
                       Orthographic=ccrs.Orthographic(central_longitude=map_settings["central longitude"],
                                                      central_latitude=map_settings["central latitude"]),
                       PlateCarree=ccrs.PlateCarree())
    #
    for k in range(0, len(ds2["time"])):

        tt = k
        title = ''
        filename = ''
        # Get a new background map figure
        fig, ax = plotMap(map_settings)

        # loop through list of data dictionaries in json file
        for i in range(len(data)):

            # plot data in appropriate style
            if data[i]["plot?"] is True:

                dataset = xr.open_dataset(data[i]["file"])

                filename += '{}'.format(data[i]["id"]) + '_'

                if data[i]["type"] in shading_name_list:
                    print("shading")
                    plot_shading(ax, dataset, data[i], tt)

                elif data[i]["type"] in contour_name_list:
                    print("drawing contours")
                    plot_contour(ax, dataset, data[i], tt)
                    title += '{}'.format(data[i]["name"]) + ' (' + '{}'.format(data[i]["type"]) + '), '

                elif data[i]["type"] in barb_name_list:
                    print("drawing barbs")
                    plot_barbs(ax, dataset, data[i], tt)
                    title += '{}'.format(data[i]["name"]) + ' (' + '{}'.format(data[i]["type"]) + '), '

                elif data[i]["type"] in quiver_name_list:
                    print("drawing vectors")
                    plot_vectors(ax, dataset, data[i], tt, )
                    title += '{}'.format(data[i]["name"]) + ' (' + '{}'.format(data[i]["type"]) + '), '

        # Save and close the figure

        vtime = datetime.strptime(str(ds2.time.data[tt].astype('datetime64[ms]')), '%Y-%m-%dT%H:%M:%S.%f')
        plt.title('{}'.format(vtime), loc='right')
        plt.title('{}'.format(title[:-2]), loc='left')
        pth.Path('FIGURES_KING/' + filename[:-1] + '/').mkdir(exist_ok=True)
        plt.savefig('FIGURES_KING/' + '{}'.format(filename[:-1]) + '/' + '{}'.format(k) + '.png',
                    dpi=map_settings["dpi"])
        plt.close(fig)
        print("finished")