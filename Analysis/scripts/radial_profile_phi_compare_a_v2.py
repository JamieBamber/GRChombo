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

# set centre
center = [512.0, 512.0, 0]

axis = "y"
z_position = 0.001	# z position of slice
y_position = center[1]
number = 141
dt = 5*0.25
t = number*dt

# choose a values to plot
a_list = ["0", "0.7", "0.99"]

# set up parameters
R_outer_horizon = 0.25	# R_outer = r_+ / 4 ~= 1 / 4 for an extremal Kerr BH
#R_min = 0.25
R_max = 250
N_bins = 128
#
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"

### 
# try making smoothed interpolated radial profile using scipy interpolaters
def get_raw_data(key, number):
	# load dataset 
	data_sub_dir = a_dirs[key]
	dsi = yt.load(data_root_path + "/" + data_sub_dir + "/KerrSFp_{:06d}.3d.hdf5".format(5*number))
	print("loaded dataset number " + str(number) + " for " + data_sub_dir) 
	# make circular slice	
	height = 0.1
	a = float(key)
	R_min = 0.25*(1 + math.sqrt(1 - a*a))
	if axis == "z":
		region = dsi.r[:,:,z_position]
		region.set_field_parameter("normal", [0, 0, 1])
	elif axis == "y":
		region = dsi.r[:,y_position,:]
		region.set_field_parameter("normal", [0, 1, 0])
	region.set_field_parameter("center", center)
	# get 1D data
	cyl_R = np.array(region['index', 'cylindrical_radius'])
	phi = np.array(region['chombo', 'phi'])	
	# manipulate data to get a sorted array of single R values
	inds1 = cyl_R.argsort()
	cyl_R_sorted = cyl_R[inds1]
	phi_sorted = phi[inds1]
	cyl_R_unique, inds2 = np.unique(cyl_R_sorted, return_index=True)
	phi_unique = np.zeros(cyl_R_unique.shape)
	for i in range(0, cyl_R_unique.size-1):
		phi_unique[i] = np.mean(phi_sorted[inds2[i]:inds2[i+1]])
	phi_unique[-1] = np.mean(phi_sorted[inds2[-1]:])
	#print("cyl_R.shape", cyl_R_unique.shape)
	#print("phi.shape", phi_unique.shape)
	#print(cyl_R_unique[0:200])
	#print(phi_unique[0:200])
	# trim to fit
	inds3 = np.where((cyl_R_unique > R_min) & (cyl_R_unique <= R_max))
	R = cyl_R_unique[inds3]
	phi = phi_unique[inds3]
	return (R, phi)

### plot phi profiles vs r_BS
colours = ['r-', 'b-', 'g-']

# make  plot 
for i in range(0, len(a_list)):
	a_str = a_list[i]
	a = float(a_str)
	R, phi = get_raw_data(a_str, number)
	r_plus = 1 + math.sqrt(1 - a**2)
	r_minus = 1 - math.sqrt(1 - a**2)
	r = R*(1 + r_plus/(4*R))**2
	sigma = np.sqrt((r - r_plus)*(r - r_minus))
	print("r0 = {:.4f}, r+ = {:.4f}".format(r[0], r_plus), flush=True)
	#r_star = r + ((r_plus**2)*np.log(r - r_plus) - (r_minus**2)*np.log(r - r_minus))/(r_plus - r_minus)	
	# fit curve to data
	#phi_fit = interp1d(ln_r_1, phi, kind="quadratic")
	#print("fitted curve to data")
	#x = np.linspace(ln_r_1[1], ln_r_1[-1], 250)
	#y = phi_fit(x)
	x = np.log10(sigma)
	y = phi
	plt.plot(x, y, colours[i], markersize="2", label="a = " + a_str)
plt.xlabel("$log_{10}(\\sigma)$")
plt.ylabel("$\\phi$")
plt.legend(fontsize=8)
#plt.xlim((1, 5))
if axis == "z":
	position = z_position
elif axis == "y":
	position = y_position
title = "field profile, $L=0$, $M=1$, $m=0$, $M\\omega=M\\mu=1$ {:s}={:.3}, time={:.1f}".format(axis, position, t) 
plt.title(title)
plt.grid(axis="both")
plt.tight_layout()

save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/" 
save_name = "phi_profile_vs_sigma_compare_a_{:s}={:.3f}_t={:.2f}.png".format(axis, position, t)
save_path = save_root_path + save_name
plt.savefig(save_path, transparent=False)
plt.clf()
print("saved " + str(save_path))

