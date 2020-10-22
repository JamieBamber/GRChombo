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

class data_dir:
	def __init__(self, run_number, l, m, a, mu, number):
		self.run_number = run_number
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = float(mu)
		self.number = number
		self.name = "run{:04d}_KNL_l{:d}_m{:d}_a{:s}_Al0_mu{:s}_M1_correct_Ylm_new_rho".format(run_number, l, m, a, mu)

data_dirs = []
def add_data_dir(run_number, l, m, a, mu, number):
        x = data_dir(run_number, l, m, a, mu, number)
        data_dirs.append(x)

# choose datasets to compare
add_data_dir(59, 1, 1, "0.7", "0.05", 380)
add_data_dir(39, 1, 1, "0.7", "0.4", 380)
add_data_dir(61, 1, 1, "0.7", "1", 760)
add_data_dir(60, 1, 1, "0.7", "2", 1520)

# load dataset time series
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF/"

# set centre
center = [512.0, 512.0, 0]

# set up parameters
z_position = 0.001	# s position of slice
R_max = 300
N_bins = 512
M = 1
colours = ['r-', 'b-', 'g-', 'm-']
log_x = True

# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
@derived_field(name = "weighting_field", units = "")
def _weighting_field(field, data):
        return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi*data["cylindrical_radius"]*cm)

def make_profile(ds, R_min):
	slice = ds.r[:,:,z_position]
	slice.set_field_parameter("center", center)
	rp = yt.create_profile(slice, "spherical_radius", fields=["J_r", "rho"], n_bins=N_bins, weight_field="weighting_field", extrema={"spherical_radius" : (R_min, R_max)})
	Jr = rp["J_r"].value
	rho = rp["rho"].value
	R = rp.x.value
	print("made profile")
	return (R, Jr, rho)
	
time = 0
min_r = R_max
max_r = 0

for i in range(0,len(data_dirs)):
	dd = data_dirs[i]
	dataset_path = data_root_path + dd.name + "/KerrSFp_{:06d}.3d.hdf5".format(dd.number)
	ds = yt.load(dataset_path)
	print("loaded data from ", dataset_path)
	r_plus = M*(1 + np.sqrt(1 - (dd.a)**2))
	R_plus = r_plus/4
	R, Jr, rho = make_profile(ds, R_plus)
	# plot graph
	time = ds.current_time
	r = R*(1 + r_plus/(4*R))**2
	min_r = min(min_r, r[0])
	max_r = max(max_r, r[-1])
	if log_x:
		x = np.log10(r/M)
	else:
		x = r/M
	plt.plot(x, -Jr/rho, colours[i], label="a={:.2f}, l={:d}, m={:d}, $\\mu$={:.2f}".format(dd.a, dd.l, dd.m, dd.mu))
title = "Radial momentum per unit mass, $M=1$, time = {:.1f}".format(time) 
plt.ylabel("radial momentum per unit mass $J_r \;/\; \\rho$")
if log_x:
	x0 = np.linspace(np.log10(min_r/M), np.log10(max_r/M), 100)
	plt.plot(x0, np.zeros(len(x0)), c="0.75", linestyle="dashed")
	plt.xlabel("$\\log_{10}(r_{BL}/M)$")
else:
	plt.xlabel("$r_{BL}/M$")
plt.ylim((-0.5, 0.5))
plt.title(title)
plt.tight_layout()
plt.legend(fontsize=10)
save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/" 
save_name = save_root_path + "Jr_profile_compare_mu_t={:.1f}.png".format(time)
plt.savefig(save_name, transparent=False)
plt.clf()
print("saved " + str(save_name))
	
	
