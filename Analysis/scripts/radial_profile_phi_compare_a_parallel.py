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

yt.enable_parallelism()

start_time = time.time()

""" # load inputs
input1 = sys.argv[1]
if len(sys.argv) < 3:
        input2 = 0
else:
     	input2 = sys.argv[2] """

class data_dir:
	def __init__(self, num, l, m, a, mu):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = float(mu)
		self.name = "run{:04d}_KNL_l{:d}_m{:d}_a{:s}_Al0_mu{:s}_M1_correct_Ylm".format(num, l, m, a, mu)
	# filename = "" don't need to initialise attributes in python 

data_dirs = []
def add_data_dir(num, l, m, a, mu):
        x = data_dir(num, l, m, a, mu)
        data_dirs.append(x)

# choose datasets to compare
add_data_dir(2, 0, 0, "0.99", "1")
add_data_dir(22, 0, 0, "0", "1")

name = "l0_m0_mu1_compare_a_r_star"

# load dataset time series
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"

data_set_lengths = []
datasets = []

for dd in data_dirs:
	dataset_path = data_root_path + "/" + dd.name + "/KerrSFp_*.3d.hdf5"
	ds = yt.load(dataset_path)
	datasets.append(ds)
	data_set_lengths.append(len(ds)) 
	print("loaded data from ", dataset_path)
	print("time = ", time.time() - start_time)

min_length = np.min(data_set_lengths)
min_index = np.argmin(data_set_lengths)

# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
@derived_field(name = "weighting_field", units = "")
def _weighting_field(field, data):
        return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi*data["cylindrical_radius"]*cm)

# set centre
center = [512.0, 512.0, 0]
L = max(ds[0].domain_width.v)

# set up parameters
z_position = 0.001	# s position of slice
R_max = 75
N_bins = 128
M = 1
dt = 0.25
plot_interval = 5

# root directory for saving 
save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/" 
frames_dir = name + "_phi_profile_movie"
try:
	makedirs(save_root_path + frames_dir)
except:
	pass

# iterate through datasets (forcing each to go to a different processor)
i = 0
colours = ['r-', 'b-', 'g-', 'c-']

# dataset with the smallest number of timeslices
ds0 = datasets[min_index]

def plot_profile(dsi, index):
	dd = data_dirs[index]
	a = dd.a
	slice = dsi.r[:,:,z_position]
	slice.set_field_parameter("center", center)
	r_plus = M*(1 + np.sqrt(1 - a**2))
	R_min = r_plus/4
	# make profile
	rp = yt.create_profile(slice, "spherical_radius", fields=["phi"], n_bins=N_bins, weight_field="weighting_field", extrema={"spherical_radius" : (R_min, R_max)})
	### plot phi profile vs ln(r_BS - 1)
	R = rp.x.value
	r_BL = R*(1 + r_plus/(4*R))**2
	if (a==0):
		r_star = r_BL + r_plus*np.log(r_BL - r_plus)
	else:
		r_minus = M*(1 - np.sqrt(1 - a**2))
		r_star = r_BL + ((r_plus**2)*np.log(r_BL - r_plus) - (r_minus**2)*np.log(r_BL - r_minus))/(r_plus - r_minus)		
	phi = rp["phi"].value
	plt.plot(r_star, phi, colours[index], label="l={:d} m={:d} a={:.2f}".format(dd.l,dd.m,dd.a))
	
for dsi in ds0.piter():
	current_time = dsi.current_time
	number = int(current_time/(plot_interval*dt))
	print("plotting number {:d} of {:d}".format(number, min_length))
	
	# plot first dataset
	plot_profile(dsi, min_index)
	
	# plot remaining datasets
	for i in range(0,len(data_dirs)):
		if (i != min_index):
			dsi1 = yt.load(data_root_path + "/" + data_dirs[i].name + "/KerrSFp_{:06d}.3d.hdf5".format(number*plot_interval))
			plot_profile(dsi1, i)			
		else:
			pass
	plt.xlabel("$r_*$")
	plt.ylabel("$\\phi$")
	plt.grid(axis='y')
	plt.legend()
	plt.xlim((-15, 80))
	plt.ylim((-1, 1))
	
	title = "Scalar field evolution, $M\\mu=1$, time = {:.1f}".format(current_time) 
	
	plt.title(title)
	plt.tight_layout()
	
	save_name = save_root_path + frames_dir + "/frame_{:06d}.png".format(number)
	plt.savefig(save_name, transparent=False)
	plt.clf()
	print("saved " + str(save_name))
	
	
