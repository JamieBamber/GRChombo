import yt
import numpy as np
from yt import derived_field
import time
# import sys
import matplotlib.pyplot as plt
import math
from scipy.optimize import minimize
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
R_min = R_plus*2
R_max = 50
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

# calculate some values
R = rp.x.value
phi = rp["phi"].value
r_BL = R*(1 + r_plus/(4*R))**2
r_minus = M*(1 - np.sqrt(1 - a**2))
r_star = r_BL/r_plus + np.log(r_BL/r_plus - 1)

dt = 0.25
t = number*dt

def envelope(r_BL, A):
	return 0.1*(1.05 + A*r_plus/r_BL)

# find the best fitting envelope
def loss_func(A, r_BL, true_y):
	envelope_y = envelope(r_BL, A)
	loss = np.sum(np.abs(envelope_y - true_y))
	constraint = np.sum(np.abs(np.greater(envelope_y, true_y)))
	print("constraint = ", constraint)
	return loss + 10000000*(r_BL.size)*constraint 

res = minimize(loss_func, 10, args=(r_BL, phi))
A_best = res.x[0]
print("best fit value of A is ", A_best)

save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/"
def plot_graph():
	x = r_star
	x_label = "$r_*$"
	plt.plot(x, phi, 'r-', label="simulation phi")
	plt.plot(x, envelope(r_BL, A_best), 'b--', label="best fit ansatz envelope, A={:.2f}".format(A_best))
	plt.xlabel(x_label)
	plt.ylabel("$\\phi$")
	plt.grid(axis='both')
	#plt.ylim((-0.5, 0.5))
	#plt.xlim((-10, 75))
	plt.legend()
	title = data_sub_dir + " time = {:.1f}".format(t) 
	plt.title(title)
	plt.tight_layout()
	save_name = data_sub_dir + "_t={:.1f}_phi_profile_with_envelope".format(t) + ".png"
	print("saved " + save_root_path + save_name)
	plt.savefig(save_root_path + save_name, transparent=False)
	plt.clf()
	
plot_graph()
