import yt
import numpy as np
from yt import derived_field
from yt.units import cm
from scipy.special import sph_harm
import time
import sys
import matplotlib.pyplot as plt
import math

start_time = time.time()

### derived fields
"""@derived_field(name = "rho_E_eff", units = "")
def _rho_E_eff(field, data):
        return data["rho"]*pow(data["chi"],-3)

@derived_field(name = "rho_J_eff", units = "")
def _rho_J_eff(field, data):
        return data["S_azimuth"]*pow(data["chi"],-3)

@derived_field(name = "rho_J_prime_eff", units = "")
def _rho_J_prime_eff(field, data):
        return data["S_azimuth_prime"]*pow(data["chi"],-3)"""

# set centre
L = 1024.0
center = [L/2, L/2, 0]

# set up parameters
r_outer_horizon = 0.25	# R_outer = r_+ / 4 ~= 1 / 4 for an extremal Kerr BH
r_min = r_outer_horizon
r_max = 500
N_bins = 128
a = 0.99
l = 1
m = 1

# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
@derived_field(name = "weighting_field", units = "")
def _weighting_field(field, data):
	return data["rho"] * data["cell_volume"].in_base("cgs") * N_bins / (2*math.pi* (data["spherical_radius"]**2)*(r_max - r_min)*cm)

# load dataset
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
data_sub_dir = "run0035_KNL_l1_m1_a0_Al0_mu1_M0.4_correct_Ylm"
number = 1535
dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_{:06d}.3d.hdf5".format(number)
ds = yt.load(dataset_path) 
print("loaded data from ", dataset_path)
print("time = ", time.time() - start_time)

# make smoothed interpolated grid
level = 0
data = ds.sphere(center, r_max)
data.set_field_parameter("normal", [0, 0, 1])
data.set_field_parameter("center", center)
R_data = np.array(data["index", "spherical_radius"])
print(R_data.shape)
Y_lm_data = sph_harm(m, l, 0, np.array(data["index", "spherical_theta"]))
print("got Ylm data")
weight_data = np.array(data["weighting_field"])*Y_lm_data  
print("got weight field")
hist, bin_edges = np.histogram(R_data, bins=N_bins, range=(r_min, r_max), weights=weight_data)
print("made histogram")
#rp = yt.create_profile(data, "spherical_radius", fields=["rho"], n_bins=N_bins, weight_field="weighting_field", extrema={"spherical_radius" : (r_min, r_max)})
#print("made profile")

### plot profile

# plot phi
R = 0.5*(bin_edges[0:-1] + bin_edges[1:])
rho = hist
r_plus = 1 + math.sqrt(1 - a**2)
r = R*(1 + r_plus/(4*R))**2

plt.plot(np.log10(r - r_plus), rho, 'r-')
plt.xlabel("$\\log_{10}(r_{BL}-r_+)$")
plt.ylabel("$\\rho_{l=%d, m=%d$" % (l, m))
plt.grid(axis='both')
#plt.ylim((-0.5, 0.5))

dt = 0.25
title = data_sub_dir + " time = {:.1f}".format(int(number)*dt) 
plt.title(title)
plt.tight_layout()
save_name = "plots/" + data_sub_dir + "_" + number + "Ylm_rho_profile.png"
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
