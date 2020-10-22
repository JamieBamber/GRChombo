import yt
import numpy as np
from scipy.interpolate import interp1d
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
data_sub_dir = "run2.2_KNL_l0_m0_a0.99_Al0"
number = "000600"
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
r_max = 500
N_bins = 128
a = 0.99

### derived fields

# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
@derived_field(name = "weighting_field", units = "")
def _rho_E_eff(field, data):
        return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* (data["cylindrical_radius"])*(r_max - r_min)*cm)

"""@derived_field(name = "rho_E_eff", units = "")
def _rho_E_eff(field, data):
	return data["rho"]*pow(data["chi"],-3)

@derived_field(name = "rho_J_eff", units = "")
def _rho_J_eff(field, data):
        return data["S_azimuth"]*pow(data["chi"],-3)

@derived_field(name = "rho_J_prime_eff", units = "")
def _rho_J_prime_eff(field, data):
        return data["S_azimuth_prime"]*pow(data["chi"],-3)"""

# make sphere / slice 
# sphere = ds.sphere(center, r_max)
data = ds.r[:,:,z_position]
data.set_field_parameter("center", center)

# make profile
rp = yt.create_profile(data, "spherical_radius", fields=["phi"], n_bins=N_bins, weight_field="weighting_field", extrema={"spherical_radius" : (r_min, r_max)})

### plot profile

# plot phi
R = rp.x.value
phi = rp["phi"].value
r_plus = 1 + math.sqrt(1 - a**2)
r_BL = R*(1 + r_plus/(4*R))**2
r_star = r_BL + np.log(r_BL)
r_3_4 = r_BL**(3.0/4)
ln_r_BL = np.log(r_BL - 1)

interp_start = 5
interp_end = 40

f = interp1d(ln_r_BL[interp_start:interp_end], phi[interp_start:interp_end], kind='cubic')

x_interp = np.linspace(ln_r_BL[interp_start], ln_r_BL[interp_end-1], 100)
y_interp = f(x_interp)
x = np.concatenate((ln_r_BL[0:interp_start], x_interp, ln_r_BL[interp_end:]), axis=None)
y = np.concatenate((phi[0:interp_start], y_interp, phi[interp_end:]), axis=None)

plt.plot(x, y, 'r-')
plt.xlabel("$\\ln(r_{BL}-1)$")
plt.ylabel("$\\phi$")
plt.grid(axis='both')
#plt.ylim((-0.5, 0.5))

dt = 0.25
title = data_sub_dir + " time = {:.1f}".format(int(number)*dt) 
plt.title(title)
plt.tight_layout()

save_name = "plots/" + data_sub_dir + "_" + number + "_phi_profile_interp.png"
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
