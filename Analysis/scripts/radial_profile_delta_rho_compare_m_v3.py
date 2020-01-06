import yt
from yt import derived_field
from yt.units import cm
import numpy as np
import time
import matplotlib.pyplot as plt
import math
from os import makedirs
import sys
from scipy.interpolate import interp1d

start_time = time.time()

m_dirs = {}
m_dirs["-3"] = "run10_KNL_l0_m-3_a0.99_Al0_M1"
m_dirs["-2"] = "run7_KNL_l0_m-2_a0.99_Al0_M1"
m_dirs["-1"] = "run1_KNL_l0_m-1_a0.99_Al0_M1"
m_dirs["0"] = "run2.2_KNL_l0_m0_a0.99_Al0"
m_dirs["1"] = "run5_KNL_l0_m1_a0.99_Al0_M1"
m_dirs["2"] = "run3_KNL_l0_m2_a0.99_Al0_M1"
m_dirs["3"] = "run4_KNL_l0_m3_a0.99_Al0_M1"
m_dirs["10"] = "run9_KNL_l0_m10_a0.99_Al0_M1"

z_position = 0.001	# z position of slice
number = 220
dt = 5*0.25
t = number*dt

# choose m values to plot
m_list = ["-2", "-1", "0", "1", "2", "3", "10"]
data_sub_dirs = []
for m in m_list:
	data_sub_dirs.append(m_dirs[m])

# root directory for saving 
# movie_name = "m=plus_minus_2_delta_rho_profile_v2_movie"
save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/" 

# set centre
center = [512.0, 512.0, 0]

# set up parameters
r_outer_horizon = 0.25	# R_outer = r_+ / 4 ~= 1 / 4 for an extremal Kerr BH
r_min = r_outer_horizon
r_max = 250
N_bins = 128
a = 0.99
r_plus = 1 + math.sqrt(1 - a**2)

### derived fields
# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
@derived_field(name = "weighting_field", units = "")
def _rho_E_eff(field, data):
        return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* data["cylindrical_radius"]*(r_max - r_min)*cm)

# load datasets
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"

def make_profile(ds):
	slice = ds.r[:,:,z_position]
	slice.set_field_parameter("center", center)
	rp = yt.create_profile(slice, "spherical_radius", fields=["rho"], n_bins=128, weight_field="weighting_field", extrema={"spherical_radius" : (r_min, r_max)})
	rho = rp["rho"].value
	R = rp.x.value
	print("made profile")
	return (R, rho)

def get_data(key, number):
	data_sub_dir = m_dirs[key]
	ds0 = yt.load(data_root_path + "/" + data_sub_dir + "/KerrSFp_{:06d}.3d.hdf5".format(0))
	print("loaded initial dataset for " + data_sub_dir) 
	dsi = yt.load(data_root_path + "/" + data_sub_dir + "/KerrSFp_{:06d}.3d.hdf5".format(5*number))
	print("loaded dataset number " + str(number) + "for " + data_sub_dir) 
	R, rho0 = make_profile(ds0)
	rho = make_profile(dsi)[1]
	delta_rho = rho - rho0
	return (R, delta_rho)
 
R, delta_rho1 = get_data(m_list[0], number)
print("got profile for m=" + m_list[0], flush=True)
delta_rho_list = [delta_rho1]
for i in range(1, len(m_list)):
	delta_rho = get_data(m_list[i], number)[1]
	delta_rho_list.append(delta_rho)
	print("got profile for m=" + m_list[i], flush=True)

### plot delta rho profiles vs r_BS
r_BL = R*(1 + r_plus/(4*R))**2
r = r_BL
ln_r = np.log(r)
r_star = np.log(r - 1)

colours = ['r--', 'b--', 'g-', 'b-', 'r-', 'c-', 'm-']

# make  plot 
for i in range(0, len(m_list)):
	plt.plot(r_star, r*delta_rho_list[i], colours[i], label="m = " + m_list[i])
plt.ylabel("${r_{BL}}\\Delta\\rho$")
#plt.ylabel("$\\Delta\\rho$")
plt.legend(fontsize=8)
#plt.ylim((-5, 35))
title = "density profile, $L=0$, $M=1$, $z$={:.3}, time={:.1f}".format(z_position, t) 
plt.title(title)
plt.xlabel("$\\ln(r_{BL} - 1)$")
plt.grid(axis="both")
plt.tight_layout()

save_name = "r_delta_rho_vs_ln_r-1_profile_compare_m_z={:.3f}_t={:.2f}.png".format(z_position, t)
save_path = save_root_path + save_name
plt.savefig(save_path, transparent=False)
plt.clf()
print("saved " + str(save_path))

