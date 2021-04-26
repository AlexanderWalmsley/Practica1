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

configs = pth.Path("configs/data").glob('*.json')





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
        self.ops = {"subtract": self.subtract(),
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


for path in configs:
    config = open(path)
    config = json.load(config)
    operations = config["operations"]

    for j in range(0, len(operations)):
        op = Operator(operations[j])
        op.ops[operations[j]["operation"]]
        op.check()
