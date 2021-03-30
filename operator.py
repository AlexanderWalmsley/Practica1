from netCDF4 import Dataset
import numpy as np
import xarray as xr
import pathlib as pth
import json

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

input_settings = {
    "new_var_id": "wspeed",
    "new_var_name": "Wind speed",
    "units": "m s**-1",
    "file": "ERA-5_MAY2019/wind_era5_may2019 - Copy.nc",
    "vars": ['u', 'v'],
    "levels": [200, 200],
    "operation": "sub",

}

input_dataset = xr.open_dataset(input_settings["file"])


# operations = {
#   "sub": subtract(vars_arr),
#  "magnitude": magnitude(vars_arr),
# "sum": sum(vars_arr)
# }

class Operator:
    def __init__(self, settings):
        self.settings = settings
        self.dataset = xr.open_dataset(input_settings["file"])
        # self.new_var_array = np.empty([len(self.dataset[self.settings["vars"][0]])])
        self.file = Dataset(settings["file"], 'r+',)
        self.var = self.file.createVariable(settings["new_var_id"], 'd', ('time', 'latitude', 'longitude'), zlib=False)

    def multiply_by_constant(self, constant):
        for i in range(0, len(self.dataset["time"])):
            if self.settings["levels"] is not None:
                var0 = self.dataset[self.settings["vars"][0]].sel(level=self.settings["levels"][0]).isel(time=i).values
            else:
                var0 = self.dataset[self.settings["vars"][0]].isel(time=i).values
            self.var[i, :, :] = var0 * constant

        return

    def add(self):
        for i in range(0, len(self.dataset["time"])):
            if self.settings["levels"] is not None:
                var0 = self.dataset[self.settings["vars"][0]].sel(level=self.settings["levels"][0]).isel(time=i).values
                var1 = self.dataset[self.settings["vars"][1]].sel(level=self.settings["levels"][1]).isel(time=i).values

            else:
                var0 = self.dataset[self.settings["vars"][0]].isel(time=i).values
                var1 = self.dataset[self.settings["vars"][1]].isel(time=i).values
            self.var[i, :, :] = (var0 + var1)

        return

    def subtract(self):
        for i in range(0, len(self.dataset["time"])):
            if self.settings["levels"] is not None:
                var0 = self.dataset[self.settings["vars"][0]].sel(level=self.settings["levels"][0]).isel(time=i).values
                var1 = self.dataset[self.settings["vars"][1]].sel(level=self.settings["levels"][1]).isel(time=i).values

            else:
                var0 = self.dataset[self.settings["vars"][0]].isel(time=i).values
                var1 = self.dataset[self.settings["vars"][1]].isel(time=i).values
            self.var[i, :, :] = (var0 - var1)
        return

    def multiply(self):
        for i in range(0, len(self.dataset["time"])):
            if self.settings["levels"] is not None:
                var0 = self.dataset[self.settings["vars"][0]].sel(level=self.settings["levels"][0]).isel(time=i).values
                var1 = self.dataset[self.settings["vars"][1]].sel(level=self.settings["levels"][1]).isel(time=i).values

            else:
                var0 = self.dataset[self.settings["vars"][0]].isel(time=i).values
                var1 = self.dataset[self.settings["vars"][1]].isel(time=i).values
            self.var[i, :, :] = (var0 * var1)

        return

    def divide(self):
        for i in range(0, len(self.dataset["time"])):
            if self.settings["levels"] is not None:
                var0 = self.dataset[self.settings["vars"][0]].sel(level=self.settings["levels"][0]).isel(time=i).values
                var1 = self.dataset[self.settings["vars"][1]].sel(level=self.settings["levels"][1]).isel(time=i).values

            else:
                var0 = self.dataset[self.settings["vars"][0]].isel(time=i).values
                var1 = self.dataset[self.settings["vars"][1]].isel(time=i).values
            self.var[i, :, :] = (var0 / var1)

        return

    def magnitude(self):

        for i in range(0,32):
            if self.settings["levels"] is not None:
                var0 = self.dataset[self.settings["vars"][0]].sel(level=self.settings["levels"][0]).isel(time=i).values
                var1 = self.dataset[self.settings["vars"][1]].sel(level=self.settings["levels"][1]).isel(time=i).values

            else:
                var0 = self.dataset[self.settings["vars"][0]].isel(time=i).values
                var1 = self.dataset[self.settings["vars"][1]].isel(time=i).values
            self.var[i, :, :] = np.sqrt(var0 ** 2 + var1 ** 2)

        return



op = Operator(input_settings)
op.magnitude()



