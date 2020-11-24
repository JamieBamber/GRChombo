import yt
import numpy as np
from yt import derived_field
import time
# import sys
import matplotlib.pyplot as plt
import math
from yt.units import cm
from scipy.optimize import curve_fit

""" #
For mu = 1 in code units

mu = 0.5 for r_s = 1. This puts it in Hui et al.'s regime III for the equivalent 
Schwarzchild BH

this has approx solutions 

A:	phi ~ r^{-3/4} \cos( 2\sqrt{2r} - const) ? < r 
B: 	phi ~ cos(const + ln(r-1))		 2 < r < ?

"""

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

sphere_or_slice = False

# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
if sphere_or_slice:
	@derived_field(name = "weighting_field", units = "")
	def _weighting_field(field, data):
		 return data["cell_volume"].in_base("cgs") * N_bins / (2*math.pi* (data["spherical_radius"]**2)*(r_max - r_min)*cm)
	data = ds.sphere(center, r_max)
elif not sphere_or_slice:
	@derived_field(name = "weighting_field", units = "")
	def _weighting_field(field, data):
       		return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* (data["cylindrical_radius"])*(r_max - r_min)*cm)
	data = ds.r[:,:,z_position]
	data.set_field_parameter("center", center)

# make profile
rp = yt.create_profile(data, "spherical_radius", fields=["phi"], n_bins=N_bins, weight_field="weighting_field", extrema={"spherical_radius" : (r_min, r_max)})
print("made profile", flush=True)

### plot profile

# calculate ln_r_BL
R = rp.x.value
phi = rp["phi"].value
r_plus = 1 + math.sqrt(1 - a**2)
r_BL = R*(1 + r_plus/(4*R))**2
ln_r_BL = np.log(r_BL - 1)
print("calculated r_BL", flush=True)

# Hui functions
def Hui_A(r, a1, a2):
	func = a1*(r**(-3.0/4))*np.cos(2*np.sqrt(2*r) + a2)
	return func

def Hui_B(x, a1, a2):
	func = a1*np.cos(a2 + x)
	return func

# fit the Hui_A function to the curve
"""x_min = -0.4
x_max = 4
bin_min = np.argmin(np.abs(ln_r_BL - x_min))
bin_max = np.argmin(np.abs(ln_r_BL - x_max))
print("found bin_min, bin_max for fitting as {:d}, {:d}".format(bin_min, bin_max))
x_fit = r_BL[bin_min:bin_max]
y_fit = phi[bin_min:bin_max]
popt, pconv = curve_fit(Hui_A, x_fit, y_fit, p0=[0.18, 9.0/4])  
A_consts = popt
print("fitted Hui regime III curve") """

# plot graph
#equation = "{:.2f}$r_{BL}^{-3/4}*\\cos(2*\\sqrt{2*r_{BL}} + ${:.2f})".format(A_consts[0], A_consts[1])
plt.plot(ln_r_BL, phi, 'r+', label="simulation")
# plt.plot(ln_r_BL[bin_min:bin_max], Hui_A(x_fit, A_consts[0], A_consts[1]), 'k-', linewidth=1, label="Hui III A {:.2f}$r^{-3/4}\\cos(2\sqrt{2r} + ${:.2f})".format(A_consts[0], A_consts[1]))
A_consts = [1, -1]
plt.plot(ln_r_BL, Hui_A(r_BL, A_consts[0], A_consts[1]), 'k-', linewidth=1, label="Hui III A {:.2f}$r^{{-3/4}}\\cos(2\\sqrt{{2r}} + ${:.2f})".format(A_consts[0], A_consts[1]))
plt.xlabel("$\\ln(r_{BL}-1)$")
plt.ylabel("$\\phi$")
plt.grid(axis='both')
#plt.ylim((-0.5, 0.5))

dt = 0.25
title = data_sub_dir + " time = {:.1f}".format(int(number)*dt) 
plt.title(title)
plt.tight_layout()

save_name = "plots/" + data_sub_dir + "_" + number + "_phi_profile_Hui_test.png"
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
