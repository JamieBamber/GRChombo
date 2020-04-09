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

z_position = 0.001	# z position of slice
number = 1550
dt = 0.25
t = number*dt

# choose a values to plot
a_list = ["0", "0.7", "0.99"]

# set centre
center = [512.0, 512.0, 0]

# set up parameters
R_max = 450
N_bins = 150

#
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"

# define true radial solution function
M = 1
mu = 0.4
omega = 0.4
def true_radial_phi(r_BL, C1, C2):
	sol1 = ctypes.CDLL('~/GRChombo/Source/utils/KerrBH_Rfunc_lib.so').Rfunc(r_BL, True)
	sol1 = ctypes.CDLL('~/GRChombo/Source/utils/KerrBH_Rfunc_lib.so').Rfunc(r_BL, True)
### 

sphere_or_slice = False
# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
if sphere_or_slice:
        @derived_field(name = "weighting_field", units = "")
        def _weighting_field(field, data):
                return data["cell_volume"].in_base("cgs") * N_bins / (2*math.pi* (data["spherical_radius"]**2)*cm)
elif not sphere_or_slice:
        @derived_field(name = "weighting_field", units = "")
        def _weighting_field(field, data):
                return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* (data["cylindrical_radius"])*cm)

def get_data(a_str, number):
	a = float(a_str)
	r_plus = 1 + math.sqrt(1 - float(a)**2)
	R_min = r_plus/4	
	data_sub_dir = a_dirs[a_str]
	dsi = yt.load(data_root_path + "/" + data_sub_dir + "/KerrSFp_{:06d}.3d.hdf5".format(number))
	print("loaded dataset number " + str(number) + " for " + data_sub_dir) 
	if sphere_or_slice:
		data = dsi.sphere(center, R_max) - dsi.sphere(center, R_min)
		rp = yt.create_profile(data, "spherical_radius", fields=["phi"], n_bins=N_bins, weight_field="weighting_field", extrema={"spherical_radius" : (R_min, R_max)})
	elif not sphere_or_slice:
		data = dsi.r[:,:,z_position]
		data.set_field_parameter("center", center)
		rp = yt.create_profile(data, "cylindrical_radius", fields=["phi"], n_bins=N_bins, weight_field="weighting_field", extrema={"cylindrical_radius" : (R_min, R_max)})
	phi = rp["phi"].value/(R_max - R_min)
	R = rp.x.value
	print("made profile")
	return (R, phi)
 
phi_list = []
R_list = []
for i in range(0, len(a_list)):
	R, phi = get_data(a_list[i], number)
	R_list.append(R)
	phi_list.append(phi)
	print("got profile for a=" + a_list[i], flush=True)

### plot phi profiles vs r_BS
colours = ['r-', 'b-', 'g-']

# make  plot 

for i in range(0, len(a_list)):
	a = a_list[i]
	r_plus = 1 + math.sqrt(1 - float(a)**2)
	r_minus = 1 - math.sqrt(1 - float(a)**2)
	R = R_list[i]
	r = R*(1 + r_plus/(4*R))**2
	r_star = r + ((r_plus**2)*np.log(r - r_plus) - (r_minus**2)*np.log(r - r_minus))/(r_plus - r_minus)	
	#plt.plot(r_star, phi_list[i], colours[i], markersize=2, label="a = " + a_list[i])
	#plt.plot(np.log(r - r_plus), phi_list[i], colours[i], markersize=2, label="a = " + a_list[i])
	plt.plot(r_star - r, phi_list[i], colours[i], markersize=2, label="a = " + a_list[i])
plt.ylabel("$\\phi$")
plt.legend(fontsize=8)
plt.xlim((-15, 12))
title = "field profile, $M\mu=M\omega=0.4$ $l=m=0$ time={:.1f}".format(t) 
plt.title(title)
#plt.xlabel("$r_*$")
#plt.xlabel("$\\ln(r_{BL} - r_+)$")
plt.xlabel("$r_* - r_{BL}$")
plt.grid(axis="both")
plt.tight_layout()

save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/" 
#save_name = "phi_profile_vs_r_star_compare_a_t={:.2f}.png".format(z_position, t)
#save_name = "phi_profile_vs_ln_r-r_plus_compare_a_t={:.2f}.png".format(t)
save_name = "phi_profile_vs_r_star-r_compare_a_t={:.2f}.png".format(t)
save_path = save_root_path + save_name
plt.savefig(save_path, transparent=False)
plt.clf()
print("saved " + str(save_path))
