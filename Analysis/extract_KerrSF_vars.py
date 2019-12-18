import yt
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve
from yt import derived_field
import time
import sys

start_time = time.time()

# load dataset time series
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
data_sub_dir = "run1_l0_m1_a0.99_Al0"

dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_000000.3d.hdf5"
ds = yt.load(dataset_path) # this loads a dataset time series
print("loaded data from ", dataset_path)
print("time = ", time.time() - start_time)

print(ds.field_list)
print(ds.derived_field_list)
