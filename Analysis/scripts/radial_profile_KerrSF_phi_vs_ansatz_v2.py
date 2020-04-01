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
data_sub_dir = "run0063_KNL_l0_m0_a0_Al0_mu1_M1_new_rho_more_levels"
#data_sub_dir = "run0022_KNL_l0_m0_a0_Al0_mu1_M1_correct_Ylm"
number = 130
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

sphere_or_slice = False
# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
if sphere_or_slice:
	@derived_field(name = "weighting_field", units = "")
	def _weighting_field(field, data):
		return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* (data["cylindrical_radius"]**2)*(R_max - R_min))
	data = ds.sphere(center, R_max) - ds.sphere(center, R_min)
elif not sphere_or_slice:
	@derived_field(name = "weighting_field", units = "")
	def _weighting_field(field, data):
		return data["cell_volume"] # pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* (data["cylindrical_radius"])*(R_max - R_min)*cm)
	data = ds.r[:,:,z_position]
	data.set_field_parameter("center", center)

# make profile
rp = yt.create_profile(data, "spherical_radius", fields=["phi"], n_bins=N_bins, weight_field="weighting_field", extrema={"spherical_radius" : (R_min, R_max)})
print("made profile")
### plot profile

def k_func(z):
	result = ((1/z)**(0.35))*np.exp(-z/50) + 1/(50 + z)
	return result

def anzatz_phi(r_star, phi, gamma):
	result = np.zeros(r_star.size)
	Abest = np.max((phi/0.1 - 1)*np.power(r_BL/r_plus, gamma))
	print("Abest = ", Abest)
	for i in range(0, r_star.size):
		z = (r_BL[i]/r_plus)
		k = k_func(z)
		result[i] = 0.1*(1 + Abest/(z**gamma))*np.cos((k*(r_star[i] + C) + 0)*mu*r_plus)
	return result

def envelope(r_BL, phi, gamma):
	Abest = np.max((phi/0.1 - 1)*np.power(r_BL/r_plus, gamma))
	print("Abest = ", Abest)
	return 0.1*(1 + Abest*np.power(r_BL/r_plus, -gamma))

def envelope2(r_BL, r_star):
        return 0.1*(1 + A*r_plus/r_BL)/(1 + np.exp(-(r_star+2)/5))

# plot phi

save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/"
#R = data["spherical_radius"].value
#phi = data["phi"].value
R = rp.x.value
phi = rp["phi"].value
r_BL = R*(1 + r_plus/(4*R))**2
r_minus = M*(1 - np.sqrt(1 - a**2))
r_star = r_BL/r_plus + np.log(r_BL/r_plus - 1)

dt = 0.25
t = number*dt

# fit anzatz parameters

#popt, pconv = curve_fit(anzatz_phi, x, phi, p0=(0.1, 0))

def plot_wavelengths(type):
	osc_phi = phi/envelope(r_BL, phi, 1)
	local_extrema_indices = argrelextrema(np.abs(osc_phi), np.greater)[0]
	local_extrema = r_star[local_extrema_indices]
	r_BL_extrema = r_BL[local_extrema_indices]
	wl = 2*(local_extrema[1:] - local_extrema[:-1])
	pos = 0.5*(local_extrema[1:] + local_extrema[:-1])
	r_BL_pos =  0.5*(r_BL_extrema[1:] + r_BL_extrema[:-1]) 
	k = 2*np.pi/wl
	z = r_BL/r_plus
	if (type == "loglog"):
		plt.plot(np.log(r_BL_pos/r_plus), np.log(k), "r+", label="estimated k")
		## fit line to points ##
		ln_z = np.log(r_BL_pos/r_plus)
		ln_k = np.log(k)
		p = np.polyfit(ln_z[0:6], np.log(k)[0:6], deg=1)
		x = np.linspace(ln_z[0], ln_z[5], 16)
		plt.plot(x, p[0]*x + p[1], 'm--', label="{:.2f} + {:.2f}x".format(p[1], p[0])) 
		p2 = np.polyfit(ln_z[5:], np.log(k)[5:], deg=1)
		x = np.linspace(ln_z[5], ln_z[-1], 16)
		plt.plot(x, p2[0]*x + p2[1], 'c--', label="{:.2f} + {:.2f}x".format(p2[1], p2[0]))
		ln_r = np.log(r_BL/r_plus)
		ln_k_anzatz = (1-ln_r)*(2*ln_r + 0.6)/(2+ln_r)
		plt.plot(ln_r, ln_k_anzatz, "b--", label="anzatz")
		#plt.xlim((-10, 100))
		#plt.ylim((0, 2.1))
		plt.legend()
		plt.title("estimated k vs position")
		plt.xlabel("ln(position in $r_{BL}/r_+$)")
		plt.ylabel("ln(k)")
		save_name = "phi_profile_k_plot_ln_ln.png"
	elif (type == "log"):
		plt.plot(pos, np.log(k), "r+", label="estimated k")
		plt.plot(r_star, np.log(mu*r_plus*(r_plus/r_BL)), "b--", label="$\\mu r_+ (r_+/r_{BL})$")
		plt.plot(r_star, np.log(mu*r_plus*np.sqrt(r_plus/r_BL)), "m--", label="$\\mu r_+ (r_+/r_{BL})^{1/2}$")
		#k_anzatz = mu*r_plus*np.sqrt(r_plus/r_BL)*np.exp(-r_BL/(30*r_plus))
		plt.plot(r_star, np.log(mu*r_plus*np.sqrt(r_plus/r_BL)) - r_BL/(40*r_plus), "c--", label="$\\mu r_+ (r_+/r_{BL})^{1/2}$")
		plt.legend()
		plt.title("estimated k vs position")
		plt.xlabel("position in $r_*$")
		plt.xlim((-10, 100))
		plt.ylim((-5, 1))
		plt.ylabel("ln(k)")
		save_name = "phi_profile_k_plot_ln.png"
	print("saved " + save_root_path + save_name)
	plt.savefig(save_root_path + save_name, transparent=False)
	plt.clf()
	
def plot_graph():
	r_type = "r_star"
	x = r_star
	x_label = "$r_*$"
	plt.plot(x, phi, 'r+', label="simulation phi")
	#plt.plot(x, envelope(r_BL, phi, 1), 'b--', label="ansatz envelope (1 + a/r**(3/4))")
	#plt.plot(x, envelope2(r_BL, r_star), 'm--', label="ansatz envelope v2")
	#anzatz = anzatz_phi(r_star, phi, 1)
	#plt.plot(x, anzatz, 'g--', label="anzatz phi")
	plt.xlabel(x_label)
	plt.ylabel("$\\phi$")
	plt.grid(axis='both')
	#plt.ylim((-0.5, 0.5))
	plt.xlim((-10, 200))
	#plt.legend()
	title = data_sub_dir + " time = {:.1f}".format(t) 
	plt.title(title)
	plt.tight_layout()
	save_name = data_sub_dir + "_t={:.1f}_phi_profile_vs_anzatz".format(t) + r_type + ".png"
	print("saved " + save_root_path + save_name)
	plt.savefig(save_root_path + save_name, transparent=False)
	plt.clf()
	
#plot_wavelengths("loglog")
plot_graph()
