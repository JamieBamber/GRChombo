import yt
import numpy as np
from yt import derived_field
import time
# import sys
import matplotlib.pyplot as plt
import math
from yt.units import cm

start_time = time.time()

# load dataset
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"

m_dirs = {}
m_dirs["0"] = "run2.2_KNL_l0_m0_a0.99_Al0"
m_dirs["2"] = "run3_KNL_l0_m2_a0.99_Al0_M1"
m_dirs["3"] = "run4_KNL_l0_m3_a0.99_Al0"

m_list = list(m_dirs.keys())

number = "001480"

# set centre
center = [512.0, 512.0, 0]
L = 512.0

# set up parameters
z_position = 0.001	# s position of slice
r_outer_horizon = 0.25	# R_outer = r_+ / 4 ~= 1 / 4 for an extremal Kerr BH
r_min = r_outer_horizon
r_max = 200
N_bins = 128
a = 0.99

### derived fields
@derived_field(name = "rho_E_eff", units = "")
def _rho_E_eff(field, data):
        return data["rho"]*pow(data["chi"],-3)

@derived_field(name = "rho_J_eff", units = "")
def _rho_J_eff(field, data):
        return data["S_azimuth"]*pow(data["chi"],-3)

"""@derived_field(name = "rho_J_prime_eff", units = "")
def _rho_J_prime_eff(field, data):
        return data["S_azimuth_prime"]*pow(data["chi"],-3)"""

# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
@derived_field(name = "weighting_field", units = "")
def _rho_E_eff(field, data):
	return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* (data["cylindrical_radius"])*(r_max - r_min)*cm)

rho_data = {}
for key in m_dirs.keys():
	dataset_path = data_root_path + "/" + m_dirs[key] + "/KerrSFp_" + number + ".3d.hdf5"
	ds = yt.load(dataset_path) 
	print("loaded data from ", dataset_path)
	print("time = ", time.time() - start_time)
	data = ds.r[:,:,z_position]
	data.set_field_parameter("center", center)

	# make profile
	rp = yt.create_profile(data, "spherical_radius", fields=["rho"], n_bins=N_bins, weight_field="weighting_field", extrema={"spherical_radius" : (r_min, r_max)})
	rho_data[key] = rp["rho"].value
	if key == "0":
		R = rp.x.value

### plot profile

# plot phi
R = rp.x.value
r_plus = 1 + math.sqrt(1 - a**2)
r_BL = R*(1 + r_plus/(4*R))**2
ln_r_BL = np.log(r_BL - 1)

colours = ["r", "b", "g", "m"]

for i in range(0, len(m_list)):
	plt.plot(r_BL, np.log(rho_data[m_list[i]]), colours[i] + '-', label="m = " + m_list[i])
#plt.xlabel("$\\ln(r_{BL}-1)$")
plt.xlabel("$r_{BL}$")
plt.ylabel("$\\ln(\\rho)$")
plt.legend()
plt.grid(axis='both')
plt.ylim(bottom=-6)
dt = 0.25
title = "l0_a0.99_Al0_M1, time = {:.1f}".format(int(number)*dt) 
plt.title(title)
plt.tight_layout()

save_root_path = "/home/dc-bamb1/GRChombo/Analysis/"
save_name = save_root_path + "plots/" + "l0_a0.99_Al0_M1" + "_t={:.1f}".format(int(number)*dt) + "_ln_rho_profile_compare_m.png"
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
