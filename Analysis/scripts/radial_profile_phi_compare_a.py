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

a_dirs = {}
a_dirs["0"] = "run22_KNL_l0_m0_a0_Al0_M1"
a_dirs["0.7"] = "run24_KNL_l0_m0_a0.7_Al0_M1"
a_dirs["0.99"] = "run2.2_KNL_l0_m0_a0.99_Al0"

z_position = 0.001	# z position of slice
number = 141
dt = 5*0.25
t = number*dt

# choose a values to plot
a_list = ["0", "0.7", "0.99"]

# set centre
center = [512.0, 512.0, 0]

# set up parameters
R_outer_horizon = 0.25	# R_outer = r_+ / 4 ~= 1 / 4 for an extremal Kerr BH
R_min = 0.25
R_max = 250
N_bins = 128

#
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"

### 
# try making smoothed interpolated radial profile using scipy interpolaters
def make_smoothed_profile(key, number):
	# load dataset 
	data_sub_dir = a_dirs[key]
	dsi = yt.load(data_root_path + "/" + data_sub_dir + "/KerrSFp_{:06d}.3d.hdf5".format(5*number))
	print("loaded dataset number " + str(number) + " for " + data_sub_dir) 
	# make slice 	
	slice = dsi.r[:,:,z_position]
	slice.set_field_parameter("center", center)
	# get 1D data
	cyl_r = slice['index', 'cylindrical_radius']
	print("cyl_r.shape", cylindrical_radius.shape)
	phi = slice['chombo', 'phi']	
	print("phi.shape", phi.shape)
	phi_fit = interp1d(cyl_r, phi

make_smoothed_profile(a_list[0], 20)
sys.exit()

### derived fields
# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
@derived_field(name = "weighting_field", units = "")
def _weighting_field(field, data):
        return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* data["cylindrical_radius"]*(R_max - R_min)*cm)

def get_data(key, number):
	data_sub_dir = a_dirs[key]
	dsi = yt.load(data_root_path + "/" + data_sub_dir + "/KerrSFp_{:06d}.3d.hdf5".format(5*number))
	print("loaded dataset number " + str(number) + " for " + data_sub_dir) 
	slice = dsi.r[:,:,z_position]
	slice.set_field_parameter("center", center)
	rp = yt.create_profile(slice, "cylindrical_radius", fields=["phi"], n_bins=128, weight_field="weighting_field", extrema={"cylindrical_radius" : (R_min, R_max)})
	phi = rp["phi"].value
	R = rp.x.value
	print("made profile")
	return (R, phi)
 
R, phi1 = get_data(a_list[0], number)
print("got profile for m=" + a_list[0], flush=True)
phi_list = [phi1]
for i in range(1, len(a_list)):
	phi = get_data(a_list[i], number)[1]
	phi_list.append(phi)
	print("got profile for m=" + a_list[i], flush=True)

### plot phi profiles vs r_BS
colours = ['r-', 'b-', 'g-']

# make  plot 
for i in range(0, len(a_list)):
	a = a_list[i]
	r_plus = 1 + math.sqrt(1 - float(a)**2)
	r_minus = 1 - math.sqrt(1 - float(a)**2)
	r = R*(1 + r_plus/(4*R))**2
	ln_r = np.log(r - r_plus)
	r_star = r + ((r_plus**2)*np.log(r - r_plus) - (r_minus**2)*np.log(r - r_minus))/(r_plus - r_minus)	
	plt.plot(ln_r, phi_list[i], colours[i], label="a = " + a_list[i])
plt.ylabel("$\\phi")
plt.legend(fontsize=8)
#plt.ylim((-5, 35))
title = "field profile, $L=0$, $M=1$, $m=0$, $M\\omega=M\\mu=1$ $z$={:.3}, time={:.1f}".format(z_position, t) 
plt.title(title)
plt.xlabel("$\\ln(r_{BL} - r_+)$")
plt.grid(axis="both")
plt.tight_layout()

save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/" 
save_name = "phi_profile_vs_ln_r-r_plus_compare_a_z={:.3f}_t={:.2f}.png".format(z_position, t)
save_path = save_root_path + save_name
plt.savefig(save_path, transparent=False)
plt.clf()
print("saved " + str(save_path))

