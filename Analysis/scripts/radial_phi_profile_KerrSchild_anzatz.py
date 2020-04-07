import yt
import numpy as np
from yt import derived_field
import time
# import sys
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
from scipy.signal import argrelextrema
from yt.units import cm
from sys import exit as sysexit

start_time = time.time()

# load dataset
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
#data_sub_dir = "run0031_KNL_l0_m0_a0_Al0_mu0.4_M1_correct_Ylm"
#data_sub_dir = "run0063_KNL_l0_m0_a0_Al0_mu1_M1_new_rho_more_levels"
data_sub_dir = "run0022_KNL_l0_m0_a0_Al0_mu1_M1_KerrSchild"
number = 885
dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_{:06d}.3d.hdf5".format(number)
ds = yt.load(dataset_path) 
print("loaded data from ", dataset_path)
print("time = ", time.time() - start_time)

# set centre
center = [512.0, 512.0, 0]

# set up parameters
a = 0
M = 1
mu = 1
r_plus = M*(1 + np.sqrt(1 - a**2))
z_position = 0.001	# s position of slice
R_plus = r_plus	# R_outer = r_+ / 4
R_min = R_plus
R_max = 400
N_bins = 512

sphere_or_slice = False
# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
if sphere_or_slice:
	@derived_field(name = "weighting_field", units = "")
	def _weighting_field(field, data):
		return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* (data["spherical_radius"]**2)*(R_max - R_min))
	data = ds.sphere(center, R_max) - ds.sphere(center, R_min)
elif not sphere_or_slice:
	@derived_field(name = "weighting_field", units = "")
	def _weighting_field(field, data):
		return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* (data["cylindrical_radius"])*(R_max - R_min)*cm)
	data = ds.r[:,:,z_position]
	data.set_field_parameter("center", center)

# make profile
rp = yt.create_profile(data, "spherical_radius", fields=["phi"], n_bins=N_bins, weight_field="weighting_field", extrema={"spherical_radius" : (R_min, R_max)})
print("made profile")
### plot profile

def k_func(z):
	result = ((1/z)**(0.35))*(50/(50 + z))
	return result

C = -1

def anzatz_phi(r_star, phi, gamma):
	result = np.zeros(r_star.size)
	Abest = np.max((phi/0.1 - 1)*np.power(r/r_plus, gamma))
	print("Abest = ", Abest)
	for i in range(0, r_star.size):
		z = (r[i]/r_plus)
		k = k_func(z)
		result[i] = 0.1*(1 + Abest/(z**gamma))*np.cos((k*(r_star[i] + C) + 0)*mu*r_plus)
	return result

def envelope(r, phi, gamma):
	Abest = np.max((phi/0.1 - 1)*np.power(r/r_plus, gamma))
	print("Abest = ", Abest)
	return 0.1*(1 + Abest*np.power(r/r_plus, -gamma))

save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/"
#R = data["spherical_radius"].value
#phi = data["phi"].value
R = rp.x.value
phi = rp["phi"].value
r = R
r_minus = M*(1 - np.sqrt(1 - a**2))
r_star = r/r_plus + np.log(r/r_plus - 1)

dt = 0.25
t = number*dt

def plot_graph():
	x = r
	x_label = "$r_{KS}$"
	plt.plot(x, phi, 'r-', label="simulation phi")
	plt.plot(x, envelope(r, phi, 1), 'b--', label="ansatz envelope (1 + a/r)")
	#anzatz = anzatz_phi(r_star, phi, 1)
	#plt.plot(x, anzatz, 'g--', label="anzatz phi")
	plt.xlabel(x_label)
	plt.ylabel("$\\phi$")
	plt.grid(axis='both')
	#plt.ylim((-0.5, 0.5))
	#plt.xlim((-10, 200))
	plt.legend()
	title = data_sub_dir + " time = {:.1f}".format(t) 
	plt.title(title)
	plt.tight_layout()
	save_name = data_sub_dir + "_t={:.1f}_phi_profile_r".format(t) + ".png"
	print("saved " + save_root_path + save_name)
	plt.savefig(save_root_path + save_name, transparent=False)
	plt.clf()
	
#plot_wavelengths("loglog")
plot_graph()
