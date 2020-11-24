import yt
import numpy as np
# from scipy.interpolate import interp1d
# from scipy.optimize import fsolve
from yt import derived_field
import time
# import sys
import matplotlib.pyplot as plt
import math
from yt.units import cm

start_time = time.time()

# load dataset
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
data_sub_dir = "run1_l0_m-1_a0.99_Al0"
number = "000664"
dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_" + number + ".3d.hdf5"
ds = yt.load(dataset_path) 
print("loaded data from ", dataset_path)
print("time = ", time.time() - start_time)

# set centre
center = [512.0, 512.0, 0]
L = max(ds.domain_width.v)

# set up parameters
z_position = 0.001	# s position of slice
r_outer_horizon = 0.25	# R_outer = r_+ / 4 ~= 1 / 4 for an extremal Kerr BH
r_min = r_outer_horizon
r_max = 100
N_bins = 64

### derived fields

# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
@derived_field(name = "weighting_field", units = "")
def _rho_E_eff(field, data):
        return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* data["cylindrical_radius"]*(r_max - r_min)*cm)

@derived_field(name = "rho_E_eff", units = "")
def _rho_E_eff(field, data):
	return data["rho"]*pow(data["chi"],-3)

@derived_field(name = "rho_J_eff", units = "")
def _rho_J_eff(field, data):
        return data["S_azimuth"]*pow(data["chi"],-3)

@derived_field(name = "rho_J_prime_eff", units = "")
def _rho_J_prime_eff(field, data):
        return data["S_azimuth_prime"]*pow(data["chi"],-3)

# make slice 
slice = ds.r[:,:,z_position]
slice.set_field_parameter("center", center)

# make profile
rp = yt.create_profile(slice, "cylindrical_radius", fields=["rho", "S_azimuth"], n_bins=128, weight_field="weighting_field", extrema={"cylindrical_radius" : (r_min, r_max)})

### plot profile
fig, ax1 = plt.subplots()

colours = ['r', 'b']

# plot density
ax1.plot(rp.x.value, rp["rho"].value, colours[0] + '-')
ax1.tick_params(axis='y', colors=colours[0])
ax1.set_xlabel("coordinate radius")
ax1.set_ylabel("$\\rho$", color=colours[0])
ax1.set_ylim((0, 0.02))

# plot angular momentum
ax2 = ax1.twinx()
ax2.plot(rp.x.value, rp["S_azimuth"].value/rp["rho"].value, colours[1] + '-')
ax2.tick_params(axis='y', colors=colours[1])
ax2.set_ylabel("$\\rho_J \\; / \\;\\rho$", color=colours[1])
ax2.set_ylim((-1.0, 0))

dt = 0.2
title = data_sub_dir + " time = {:.1f}".format(int(number)*0.2) 
plt.title(title)
fig.tight_layout()

save_name = "plots/" + data_sub_dir + "_" + number + "_test_profile.png"
plt.savefig(save_name, transparent=False)

