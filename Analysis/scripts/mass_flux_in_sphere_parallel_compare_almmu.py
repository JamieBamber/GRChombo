import yt 
import numpy as np
#from scipy.interpolate import interp1d
#from scipy.optimize import fsolve
import math
from yt import derived_field
from yt.units import cm
import time
import sys
from matplotlib import pyplot as plt
from os import makedirs

yt.enable_parallelism()

class data_dir:
	def __init__(self, num, l, m, a, mu, Al):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = mu
		self.Al = Al
		self.name = "run{:04d}_l{:d}_m{:d}_a{:s}_Al{:s}_mu{:s}_M1_correct_Ylm".format(num, l, m, a, Al, mu)

data_dirs = []		
def add_data_dir(num, l, m, a, mu, Al="0"):
	x = data_dir(num, l, m, a, mu, Al)
	data_dirs.append(x)

# choose datasets to compare
"""add_data_dir( 28, 0, 0, "0.7", "0.4")
add_data_dir( 54, 1, -1, "0.7", "0.4")
add_data_dir( 48, 2, 2, "0.7", "0.4")
add_data_dir( 42, 5, 1, "0.7", "0.4")
add_data_dir( 58, 5, 5, "0.7", "0.4")
add_data_dir( 55, 7, 1, "0.7", "0.4")
add_data_dir( 45, 10, 10, "0.7", "0.4")"""

#add_data_dir( 31, 0, 0, "0", "0.4")
add_data_dir(28, 0, 0, "0.7", "0.4")
#add_data_dir( 29, 0, 0, "0.99", "0.4")

# add_data_dir(68, 0, 0, "0.99", "1")

#add_data_dir( 46, 2, 2, "0", "0.4")

#add_data_dir( 32, 1, 1, "0", "0.4")
#add_data_dir( 39, 1, 1, "0.7", "0.4")
#add_data_dir( 37, 1, 1, "0.99", "0.4")

#add_data_dir( 46, 2, 2, "0", "0.4")
add_data_dir(48, 2, 2, "0.7", "0.4")
#add_data_dir( 47, 2, 2, "0.99", "0.4")

#add_data_dir( 50, 2, -2, "0.99", "0.4")
#add_data_dir( 49, 1, -1, "0.99", "0.4")

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"
M = 1
max_R = 450
dR = 0.1
phi0 = 0.1

output_dir = "data/flux_data"

half_box = True

change_in_E = True

data_Eulerian_rho = True
	
def calculate_mass_in_sphere(dd):
	data_sub_dir = dd.name
	a = dd.a	
	r_plus = M*(1 + math.sqrt(1 - a**2))
	min_radius = r_plus/4

	start_time = time.time()
	
	# load dataset time series
	dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_*.3d.hdf5"
	ds = yt.load(dataset_path) # this loads a dataset time series
	print("loaded data from ", dataset_path)
	print("time = ", time.time() - start_time)
	N = len(ds)
	
	# set centre
	center = [512.0, 512.0, 0]
	L = 512.0	

	data_storage = {}
	# iterate through datasets (forcing each to go to a different processor)
	for sto, dsi in ds.piter(storage=data_storage):
		time_0 = time.time()
		# store time
		current_time = dsi.current_time 
		output = [current_time]
		
		# make shell
		shell = dsi.sphere(center, max_R+0.5*dR) - dsi.sphere(center, max_R-0.5*dR)
			
		# calculate energy inside sphere
		meanJr = shell.mean("J_r", weight="cell_volume")
		if half_box:
			area = 2*np.pi*max_R**2
		flux = meanJr*area
		output.append(flux)
		
		# store output
		sto.result = output
		sto.result_id = str(dsi)
		dt = 2.5
		i = int(current_time/dt)
		print("done {:d} of {:d} in {:.1f} s".format(i+1, N, time.time()-time_0), flush=True)
	
	if yt.is_root():	
		# make data directory if it does not already exist
		makedirs(home_path + output_dir, exist_ok=True)
		# output to file
		dd.filename = "{:s}_mass_flux_at_R={:d}.csv".format(dd.name, max_R)
		output_path = home_path + output_dir + "/" + dd.filename 
		# output header to file
		f = open(output_path, "w+")
		f.write("# t	mass flux at R=" + str(max_R) + " #\n")
		# output data
		for key in sorted(data_storage.keys()):
			data = data_storage[key]
			f.write("{:.3f}	".format(data[0]))
			f.write("{:.2f}\n".format(data[1]))
		f.close()
		print("saved data to file " + str(output_path))
		
def load_data():
	# load data from csv files
	data = {}
	for dd in data_dirs:
		file_name = home_path + output_dir + "/" + "{:s}_mass_flux_at_R={:d}.csv".format(dd.name, max_R)
		data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		print("loaded data for " + dd.name)
	return data 	

def plot_graph():
	data = load_data()
	#colours = ['r-', 'b-', 'b-.', 'g--', 'c-', 'c--', 'y-', 'k--']
	colours = ['r-', 'b-', 'g-', 'r--', 'b--', 'g--']
	i = 0
	for dd in data_dirs:
		line_data = data[dd.num]
		t = line_data[:,0]
		flux = line_data[:,1]
		label_ = "l={:d} m={:d} a={:.2f}".format(dd.l, dd.m, dd.a)
		plt.plot(t[1:], flux, colours[i], label=label_)
		i = i + 1
	plt.xlabel("$t$")
	plt.ylabel("mass flux across R=" + str(max_R))
	plt.legend(loc='upper left', fontsize=8)
	plt.title("scalar field energy flux across R={:.0f}, $M=1$, $\\mu=1$".format(max_R))
	#plt.xlim((0, 450))
	#plt.ylim((0, 0.004))
	plt.tight_layout()
	save_path = home_path + "plots/KerrBH/mass_flux_across_R={:.0f}_compare_alm.png"
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()

for dd in data_dirs:
	calculate_mass_in_sphere(dd)

#plot_graph()
