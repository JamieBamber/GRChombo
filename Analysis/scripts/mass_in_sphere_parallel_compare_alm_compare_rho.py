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
	def __init__(self, num, l, m, a):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.name = "run{:04d}_KNL_l{:d}_m{:d}_a{:s}_Al0_mu0.4_M1_correct_Ylm".format(num, l, m, a)
	filename = ""
		

def add_data_dir(list, num, l, m, a):
	x = data_dir(num, l, m, a)
	list.append(x)

data_dirs = []
# choose datasets to compare
"""add_data_dir(data_dirs, 31, 0, 0, "0")
add_data_dir(data_dirs, 28, 0, 0, "0.7")
add_data_dir(data_dirs, 29, 0, 0, "0.99")
add_data_dir(data_dirs, 32, 1, 1, "0")"""
add_data_dir(data_dirs, 37, 1, 1, "0.99")
"""add_data_dir(data_dirs, 49, 1, -1, "0.99")
add_data_dir(data_dirs, 42, 5, 1, "0.7")
add_data_dir(data_dirs, 40, 10, 1, "0.7")
add_data_dir(data_dirs, 47, 2, 2, "0.99")
add_data_dir(data_dirs, 46, 2, 2, "0")
add_data_dir(data_dirs, 50, 2, -2, "0.99")
#add_data_dir(data_dirs, 55, 7, 1, "0.7")
#add_data_dir(data_dirs, 56, 2 1, "0.7")"""

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"
max_radius = 450
M = 1

output_dir = "data/compare_alm_mass"

half_box = True

change_in_E = True
true_rho = True
	
"""@derived_field(name = "rho_J_eff", units = "")
def _rho_J_eff(field, data):
       	return data["S_azimuth"]*pow(data["chi"],-3)"""

def calculate_mass_in_sphere(dd):
	data_sub_dir = dd.name
	a = dd.a	
	r_plus = M*(1 + math.sqrt(1 - a**2))
	min_radius = r_plus

	start_time = time.time()
	
	# load dataset time series
	
	if true_rho:
		# derived fields
		@derived_field(name = "rho_E_eff", units = "")
		def _rho_E_eff(field, data):
			r_BL = (data["spherical_radius"]/cm)*(1 + r_plus*cm/(4*data["spherical_radius"]))**2
			Sigma2 = r_BL**2 + (data["z"]*a*M/(r_BL*cm))
			Delta = r_BL**2 + (a*M)**2 - 2*M*r_BL
			A = (r_BL**2 + (a*M)**2)**2 - ((a*M)**2)*Delta*(data["x"]**2 + data["y"]**2)/((cm**2)*r_BL)
			alpha = pow(Delta*Sigma2/A, 0.5)
			beta = 2*a*(M**2)*r_BL/A 
			return (data["rho"]*alpha - beta*data["S_azimuth"])*pow(data["chi"],-3)

	elif not true_rho:
		# derived fields
        	@derived_field(name = "rho_E_eff", units = "")
        	def _rho_E_eff(field, data):
                	return data["rho"]**pow(data["chi"],-3)
		

	dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_*.3d.hdf5"
	ds = yt.load(dataset_path) # this loads a dataset time series
	print("loaded data from ", dataset_path)
	print("time = ", time.time() - start_time)
	N = len(ds)
	
	ds0 = ds[0] # get the first dataset 
	
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
		
		# make sphere
		sphere = dsi.sphere(center, max_radius) - dsi.sphere(center, min_radius)
		volume = sphere.sum("cell_volume")
		if half_box:
			volume = 2*volume
			
		# calculate energy inside sphere
		meanE = sphere.mean("rho_E_eff", weight="cell_volume")
		E = volume*meanE
		output.append(E)
		
		# store output
		sto.result = output
		sto.result_id = str(dsi)
		dt = 1.25
		i = int(current_time/dt)
		print("done {:d} of {:d} in {:.1f} s".format(i+1, N, time.time()-time_0), flush=True)
	
	if yt.is_root():	
		# make data directory if it does not already exist
		makedirs(home_path + output_dir, exist_ok=True)
		# output to file
		if true_rho:
			dd.filename = "l={:d}_m={:d}_a={:s}_mass_in_r={:d}_true.csv".format(dd.l, dd.m, str(dd.a), max_radius)
		output_path = home_path + output_dir + "/" + dd.filename 
		# output header to file
		f = open(output_path, "w+")
		f.write("# t	mass in r<=" + str(max_radius) + " #\n")
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
	old_data = {}
	for dd in data_dirs:
		file_name = home_path + output_dir + "/" + "l={:d}_m={:d}_a={:s}_mass_in_r={:d}_true.csv".format(dd.l, dd.m, str(dd.a), max_radius)
		data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		print("loaded data for " + dd.name)
	for dd in data_dirs:
                file_name = home_path + output_dir + "/" + "l={:d}_m={:d}_a={:s}_mass_in_r={:d}.csv".format(dd.l, dd.m, str(dd.a), max_radius)
                old_data[dd.num] = np.genfromtxt(file_name, skip_header=1)
                print("loaded data for " + dd.name)
	return (old_data, data) 	

def plot_graph():
	old_data, data = load_data()
	colours = ['r--', 'r-.', 'r-', 'b--', 'b-', 'c-', 'm-', 'k-', 'g-', 'g--', 'y-'] 
	i = 0
	for dd in data_dirs:
		old_line_data = old_data[dd.num]
		line_data = data[dd.num]
		t = line_data[:,0]
		mass = line_data[:,1] #- line_data[0,1]
		label_ = "l={:d} m={:d} a={:s}".format(dd.l, dd.m, str(dd.a))
		if change_in_E:
			plt.plot(t[1:], old_line_data[1:,1] - old_line_data[0,1], 'r-', label=label_+" old $\\rho$")
			plt.plot(t[1:], line_data[1:,1] - line_data[0,1], 'b-', label=label_+" new $\\rho$")
		else:
			plt.plot(t, mass, colours[i], label=label_)
		i = i + 1
	plt.xlabel("time")
	if change_in_E:
		plt.ylabel("$\\Delta E$ in $r < $" + str(max_radius))
	else:
		plt.ylabel("$E$ in $r < $" + str(max_radius))
	plt.legend(loc='upper left', fontsize=8)
	plt.title("scalar field energy inside a sphere vs time, $M=1, \\mu=0.4$")
	plt.tight_layout()
	if change_in_E:
		save_path = home_path + "plots/delta_mass_in_sphere_compare_alm_radius_" + str(max_radius) + "_compare_rho.png"
	else:
		save_path = home_path + "plots/mass_in_sphere_compare_alm_radius_" + str(max_radius) + ".png"
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()

#for dd in data_dirs:
#	calculate_mass_in_sphere(dd)

plot_graph()
