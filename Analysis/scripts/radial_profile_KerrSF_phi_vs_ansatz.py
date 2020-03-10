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


start_time = time.time()

# load dataset
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
#data_sub_dir = "run0031_KNL_l0_m0_a0_Al0_mu0.4_M1_correct_Ylm"
data_sub_dir = "run0022_KNL_l0_m0_a0_Al0_mu1_M1"
number = 1460
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
R_plus = 0.25*r_plus	# R_outer = r_+ / 4
R_min = R_plus*1.01
R_max = 500
N_bins = 256

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

sphere_or_slice = False

# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
if sphere_or_slice:
	@derived_field(name = "weighting_field", units = "")
	def _rho_E_eff(field, data):
		return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* (data["cylindrical_radius"]**2)*(R_max - R_min))
	data = ds.sphere(center, R_max)
elif not sphere_or_slice:
	@derived_field(name = "weighting_field", units = "")
	def _rho_E_eff(field, data):
		return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* (data["cylindrical_radius"])*(R_max - R_min)*cm)
	data = ds.r[:,:,z_position]
	data.set_field_parameter("center", center)

# make profile
rp = yt.create_profile(data, "spherical_radius", fields=["phi"], n_bins=N_bins, weight_field="weighting_field", extrema={"spherical_radius" : (R_min, R_max)})
print("made profile")

### plot profile

# np.exp(-0.1*(r_BL/r_plus))

A = 5.6
C = -1
B1 = 0.1
B2 = 0

def k_func(z):
	# z = (r_BL/r_plus)
	result = 1/(1+0.05*z) - 0.05/z**2
	return result

def anzatz_phi(r_star):
	result = np.zeros(r_star.size)
	for i in range(0, r_star.size):
		z = (r_BL[i]/r_plus)
		k = k_func(z)
		result[i] = 0.1*(1 + A/z)*np.cos((k*(r_star[i] + C) + 0)*mu*r_plus)
	return result

def envelope(r_BL):
	return 0.1*(1 + A*r_plus*(r_BL**(-3/4)))

def envelope2(r_BL, r_star):
        return 0.1*(1 + A*r_plus/r_BL)(1 + np.exp(-r_star/5))

# plot phi

save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/"
R = rp.x.value
phi = rp["phi"].value
r_BL = R*(1 + r_plus/(4*R))**2
r_minus = M*(1 - np.sqrt(1 - a**2))
r_star = r_BL/r_plus + np.log(r_BL/r_plus - 1)

dt = 0.25
t = number*dt


# fit anzatz parameters

#popt, pconv = curve_fit(anzatz_phi, x, phi, p0=(0.1, 0))

anzatz = anzatz_phi(r_star)
def plot_wavelengths():
	osc_phi = phi/envelope(r_BL)
	local_max_indices = argrelextrema(osc_phi, np.greater)[0]
	local_min_indices = argrelextrema(osc_phi, np.less)[0]
	local_max = r_star[local_max_indices]
	local_min = r_star[local_min_indices]
	r_BL_max = r_BL[local_max_indices]
	r_BL_min = r_BL[local_min_indices]
	r_BL_pos1 = 0.5*(r_BL_max[1:] + r_BL_min)
	r_BL_pos2 = 0.5*(r_BL_max[:-1] + r_BL_min)
	r_BL_pos = np.concatenate((r_BL_pos1, r_BL_pos2))
	print("local_max.size = ", local_max.size)
	print("local_min.size = ", local_min.size)
	print(local_max, local_min)
	wl1 = 2*(local_max[1:] - local_min)
	pos1 = 0.5*(local_max[1:] + local_min)
	wl2 = 2*(local_min - local_max[:-1])
	pos2 = 0.5*(local_min + local_max[:-1])
	wl = np.concatenate((wl1,wl2)) # = 2*pi/k
	print("wl = ", wl)
	pos = np.concatenate((pos1, pos2)) 
	print("pos = ", pos)
	indices = np.linspace(0, 6, 6)
	#
	# wl_anzatz = (r_BL-r_plus)/(2*math.pi*r_plus) + 0.05*((r_BL-r_plus)/(2*math.pi*r_plus))**2
	z = (r_BL-r_plus)/(2*math.pi*r_plus)
	z_pos = (r_BL_pos - r_plus)/(2*math.pi*r_plus)
	plt.plot(pos, 2*np.pi/wl, "r+", label="estimated k")
	k_anzatz = 2*np.pi*r_plus/(r_BL)
	plt.plot(r_star, k_anzatz, "b--", label="$r_s/r$")
	#plt.xlim((-10, 100))
	plt.ylim((0, 5))
	plt.legend()
	plt.title("est. k vs position")
	plt.xlabel("est position ($r_*$)")
	plt.ylabel("est k")
	save_name = "phi_profile_k_plot.png"
	print("saved " + save_root_path + save_name)
	plt.savefig(save_root_path + save_name, transparent=False)
	plt.clf()
	
def plot_graph():
	r_type = "r_star"
	if (r_type == "r_tilde"):
		r_tilde = np.log(r_BL/r_plus - 1)
		x = r_tilde
		x_label = "$\\tilde{r}$"
	elif (r_type == "r_sigma"):
		r_sigma = 0.5*np.log((r_BL/r_plus)*(r_BL/r_plus - 1))
		x = r_sigma
		x_label ="$r_{\\sigma}$"
	elif (r_type == "r_star"):
		x = r_star
		x_label = "$r_*$"
	plt.plot(x, phi, 'r-', label="simulation phi")
	plt.plot(x, envelope(r_BL), 'b--', label="ansatz envelope")
	plt.plot(x, envelope2(r_BL, r_star), 'm--', label="ansatz envelope v2")
	plt.plot(x, anzatz, 'g--', label="anzatz phi")
	plt.xlabel(x_label)
	plt.ylabel("$\\phi$")
	plt.grid(axis='both')
	#plt.ylim((-0.5, 0.5))
	plt.xlim((-10, 50))
	plt.legend()
	title = data_sub_dir + " time = {:.1f}".format(t) 
	plt.title(title)
	plt.tight_layout()
	save_name = data_sub_dir + "_t={:.1f}_phi_profile_vs_anzatz".format(t) + r_type + ".png"
	print("saved " + save_root_path + save_name)
	plt.savefig(save_root_path + save_name, transparent=False)
	plt.clf()
	
plot_wavelengths()
