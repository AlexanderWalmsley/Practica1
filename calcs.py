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

windshear_settings = [{
    "new_var_id": "ushear",
    "new_var_name": "U Windshear",
    "units": "m s**-1",
    "file1": "ERA-5_MAY2019/wind_era5_may2019.nc",
    "var1": 'u',
    "file2": "ERA-5_MAY2019/swind_era5_may2019.nc",
    "var2": 'u10',
    "levels": [850, None],
    "operation": "sub",
    "output_file": "ERA-5_MAY2019/wind_era5_may2019.nc"
},
    {
        "new_var_id": "vshear",
        "new_var_name": "V Wind Shear",
        "units": "m s**-1",
        "file1": "ERA-5_MAY2019/wind_era5_may2019.nc",
        "var1": 'v',
        "file2": "ERA-5_MAY2019/swind_era5_may2019.nc",
        "var2": 'v10',
        "levels": [850, None],
        "operation": "sub",
        "output_file": "ERA-5_MAY2019/wind_era5_may2019.nc"

    }]
thck_settings = [{
    "new_var_id": "thck",
    "new_var_name": "THCK",
    "units": "m s**-1",
    "file1": "ERA-5_MAY2019/hgt2_era5_may2019.nc",
    "var1": 'z',
    "file2": "ERA-5_MAY2019/hgt2_era5_may2019.nc",
    "var2": 'z',
    "levels": [1000, 700],
    "operation": "sub",
    "output_file": "ERA-5_MAY2019/hgt2_era5_may2019.nc"
}]


# operations = {
#   "sub": subtract(vars_arr),
#  "magnitude": magnitude(vars_arr),
# "sum": sum(vars_arr)
# }

class Operator:
    def __init__(self, settings):
        self.settings = settings
        self.dataset1 = xr.open_dataset(settings["file1"])
        if self.settings["file1"] == self.settings["file2"]:
            self.dataset2 = self.dataset1
        else:
            self.dataset2 = xr.open_dataset(settings["file2"])

        # self.new_var_array = np.empty([len(self.dataset[self.settings["vars"][0]])])
        self.file = Dataset(settings["output_file"], 'r+', )

        if settings["new_var_id"] in self.file.variables:
            self.var = self.file[settings["new_var_id"]]
        else:
            self.var = self.file.createVariable(settings["new_var_id"], 'd', ('time', 'latitude', 'longitude'),
                                                zlib=False)
        self.ops = {"sub": self.subtract(),
                    "add": self.add(),
                    "divide": self.divide(),
                    "multiply": self.multiply(),
                    "magnitude": self.magnitude()}

    def add(self):
        for i in range(0, len(self.dataset1["time"])):
            if self.settings["levels"][0] is not None:
                var0 = self.dataset1[self.settings["var1"]].sel(level=self.settings["levels"][0]).isel(time=i).values
            else:
                var0 = self.dataset1[self.settings["var1"]].isel(time=i).values
            if self.settings["levels"][1] is not None:
                var1 = self.dataset2[self.settings["var2"]].sel(level=self.settings["levels"][1]).isel(time=i).values
            else:
                var1 = self.dataset2[self.settings["var2"]].isel(time=i).values
            self.var[i, :, :] = (var0 + var1)

        return

    def subtract(self):
        for i in range(0, len(self.dataset1["time"])):
            if self.settings["levels"][0] is not None:
                var0 = self.dataset1[self.settings["var1"]].sel(level=self.settings["levels"][0]).isel(time=i).values
            else:
                var0 = self.dataset1[self.settings["var1"]].isel(time=i).values
            if self.settings["levels"][1] is not None:
                var1 = self.dataset2[self.settings["var2"]].sel(level=self.settings["levels"][1]).isel(time=i).values
            else:
                var1 = self.dataset2[self.settings["var2"]].isel(time=i).values
            self.var[i, :, :] = (var0 - var1)
        return

    def multiply(self):
        for i in range(0, len(self.dataset1["time"])):
            if self.settings["levels"][0] is not None:
                var0 = self.dataset1[self.settings["var1"]].sel(level=self.settings["levels"][0]).isel(time=i).values
            else:
                var0 = self.dataset1[self.settings["var1"]].isel(time=i).values
            if self.settings["levels"][1] is not None:
                var1 = self.dataset2[self.settings["var2"]].sel(level=self.settings["levels"][1]).isel(time=i).values
            else:
                var1 = self.dataset2[self.settings["var2"]].isel(time=i).values
            self.var[i, :, :] = (var0 * var1)

        return

    def divide(self):
        for i in range(0, len(self.dataset1["time"])):
            if self.settings["levels"][0] is not None:
                var0 = self.dataset1[self.settings["var1"]].sel(level=self.settings["levels"][0]).isel(time=i).values
            else:
                var0 = self.dataset1[self.settings["var1"]].isel(time=i).values
            if self.settings["levels"][1] is not None:
                var1 = self.dataset2[self.settings["var2"]].sel(level=self.settings["levels"][1]).isel(time=i).values
            else:
                var1 = self.dataset2[self.settings["var2"]].isel(time=i).values
            self.var[i, :, :] = (var0 / var1)

        return

    def magnitude(self):

        for i in range(0, len(self.dataset1["time"])):
            if self.settings["levels"][0] is not None:
                var0 = self.dataset1[self.settings["var1"]].sel(level=self.settings["levels"][0]).isel(time=i).values
            else:
                var0 = self.dataset1[self.settings["var1"]].isel(time=i).values
            if self.settings["levels"][1] is not None:
                var1 = self.dataset2[self.settings["var2"]].sel(level=self.settings["levels"][1]).isel(time=i).values
            else:
                var1 = self.dataset2[self.settings["var2"]].isel(time=i).values
            self.var[i, :, :] = np.sqrt(var0 ** 2 + var1 ** 2)

        return

    def check(self):
        print(self.file.variables)
        return


for j in range(0, len(windshear_settings)):
    op = Operator(windshear_settings[j])
    op.ops[windshear_settings[j]["operation"]]
    op.check()
