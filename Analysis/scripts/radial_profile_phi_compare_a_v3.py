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
import ctypes

start_time = time.time()

a_dirs = {}
a_dirs["0"] = "run0031_KNL_l0_m0_a0_Al0_mu0.4_M1_correct_Ylm"
a_dirs["0.7"] = "run0028_KNL_l0_m0_a0.7_Al0_mu0.4_M1_correct_Ylm"
a_dirs["0.99"] = "run0029_KNL_l0_m0_a0.99_Al0_mu0.4_M1_correct_Ylm"

z_position = 0.0001	# z position of slice
number = 1550
dt = 0.25
t = number*dt

# choose a values to plot
a_list = ["0"] #, "0.7", "0.99"]

# set centre
center = [512.0, 512.0, 0]

# set up parameters
R_outer_horizon = 0.25	# R_outer = r_+ / 4 ~= 1 / 4 for an extremal Kerr BH
R_max = 100
N_bins = 128

#
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"

# define true radial solution function
M = 1
mu = 0.4
omega = 0.4
"""def true_radial_phi(r_BL, C1, C2):
	sol1 = ctypes.CDLL('~/GRChombo/Source/utils/KerrBH_Rfunc_lib.so').Rfunc(r_BL, True)
	sol1 = ctypes.CDLL('~/GRChombo/Source/utils/KerrBH_Rfunc_lib.so').Rfunc(r_BL, True)"""

#make_smoothed_profile(a_list[0], 20)
#sys.exit()

sphere_or_slice = True

R_min = 0.5

print("using sphere")
@derived_field(name = "weighting_field", units = "") # force_override=True)
def _weighting_field(field, data):
	return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* (data["spherical_radius"]**2)*(R_max - R_min))

def get_data(a_str, num):
	a = float(a_str)
	r_plus = 1 + math.sqrt(1 - a**2)
	R_min = r_plus/4
	data_sub_dir = a_dirs[a_str]
	dsi = yt.load(data_root_path + "/" + data_sub_dir + "/KerrSFp_{:06d}.3d.hdf5".format(num))
	print("loaded dataset number " + str(num) + " for " + data_sub_dir) 
	sphere = dsi.sphere(center, R_max) - dsi.sphere(center, R_min)
	rp = yt.create_profile(sphere, "spherical_radius", fields=["phi"], n_bins=N_bins, weight_field="weighting_field", extrema={"spherical_radius" : (R_min, R_max)})
	phi = rp["phi"].value
	print(phi)
	R = rp.x.value
	print("made profile")
	return (R, phi)
 
data_list = []
for i in range(0, len(a_list)):
	data_list.append(get_data(a_list[i], number))
	print("got profile for a=" + a_list[i], flush=True)

### plot phi profiles vs r_BS
colours = ['r-', 'b-', 'g-']

# make  plot 
for i in range(0, len(a_list)):
	a = a_list[i]
	R, phi = data_list[i]
	r_plus = 1 + math.sqrt(1 - float(a)**2)
	r_minus = 1 - math.sqrt(1 - float(a)**2)
	r = R*(1 + r_plus/(4*R))**2
	r_star = r + ((r_plus**2)*np.log(r - r_plus) - (r_minus**2)*np.log(r - r_minus))/(r_plus - r_minus)	
	plt.plot(r, phi, colours[i], label="a = " + a_list[i])
plt.ylabel("$\\phi$")
plt.legend(fontsize=8)
#plt.xlim(-10, 50)
#plt.ylim((-5, 35))
title = "$\phi$ radial profile, $l=m=0$, $M=1$, $\\omega=\\mu=0.4$, time={:.1f}".format(t) 
plt.title(title)
plt.xlabel("$r_*$")
plt.grid(axis="both")
plt.tight_layout()

save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/" 
save_name = "phi_profile_vs_r_star_compare_a_t={:.2f}.png".format(t)
save_path = save_root_path + save_name
plt.savefig(save_path, transparent=False)
plt.clf()
print("saved " + str(save_path))

