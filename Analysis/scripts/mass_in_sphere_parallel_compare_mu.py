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
	def __init__(self, num, l, m, a, mu):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = mu
		self.name = "run{:04d}_KNL_l{:d}_m{:d}_a{:s}_Al0_mu{:s}_M1_correct_Ylm_new_rho".format(num, l, m, a, mu)
	filename = ""
		
def add_data_dir(list, num, l, m, a, mu):
	x = data_dir(num, l, m, a, mu)
	list.append(x)

data_dirs = []
# choose datasets to compare
add_data_dir(data_dirs, 59, 1, 1, "0.7", "0.05")
add_data_dir(data_dirs, 39, 1, 1, "0.7", "0.4")
add_data_dir(data_dirs, 61, 1, 1, "0.7", "1")
add_data_dir(data_dirs, 60, 1, 1, "0.7", "2")

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"
M = 1
max_radius = 450

output_dir = "data/compare_mu_mass"

half_box = True

change_in_E = True
	
"""@derived_field(name = "rho_J_eff", units = "")
def _rho_J_eff(field, data):
       	return data["S_azimuth"]*pow(data["chi"],-3)"""

rho_v1_yes_no = False

def calculate_mass_in_sphere(dd):
	data_sub_dir = dd.name
	a = dd.a	
	r_plus = M*(1 + math.sqrt(1 - a**2))
	min_radius = r_plus/4

	start_time = time.time()
	
	# load dataset time series
	
	if rho_v1_yes_no:
		# derived fields
		@derived_field(name = "rho_E_eff", units = "")
		def _rho_E_eff(field, data):
			r_BL = (data["spherical_radius"]/cm)*(1 + r_plus*cm/(4*data["spherical_radius"]))**2
			Sigma2 = r_BL**2 + (data["z"]*a*M/(r_BL*cm))
			Delta = r_BL**2 + (a*M)**2 - 2*M*r_BL
			A = (r_BL**2 + (a*M)**2)**2 - ((a*M)**2)*Delta*(data["x"]**2 + data["y"]**2)/((cm**2)*r_BL)
			alpha = pow(Delta*Sigma2/A, 0.5)
			beta = 2*a*(M**2)*r_BL/A 
			return (data["rho"]*alpha + beta*data["S_azimuth"])*pow(data["chi"],-3)

	elif not rho_v1_yes_no:
		# derived fields
        	@derived_field(name = "rho_E_eff", units = "")
        	def _rho_E_eff(field, data):
                	return data["rho"]
		

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
		dd.filename = "l={:d}_m={:d}_a={:s}_mu={:s}_mass_in_r={:d}_true.csv".format(dd.l, dd.m, str(dd.a), dd.mu, max_radius)
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
	for dd in data_dirs:
		file_name = home_path + output_dir + "/" + "l={:d}_m={:d}_a={:s}_mu={:s}_mass_in_r={:d}_true.csv".format(dd.l, dd.m, str(dd.a), dd.mu, max_radius)
		data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		print("loaded data for " + dd.name)
	return data 	

def plot_graph():
	data = load_data()
	colours = ['r-', 'b-', 'g-', 'm-']
	i = 0
	for dd in data_dirs:
		line_data = data[dd.num]
		t = line_data[:,0]
		mass = line_data[:,1] #- line_data[0,1]
		label_ = "l={:d} m={:d} a={:s} mu={:s}".format(dd.l, dd.m, str(dd.a), dd.mu)
		if change_in_E:
			plt.plot(t[1:], (line_data[1:,1] - line_data[0,1])/(float(dd.mu)**2), colours[i], label=label_)
		else:
			plt.plot(t, mass, colours[i], label=label_)
		i = i + 1
	plt.xlabel("time")
	if change_in_E:
		plt.ylabel("$\\Delta E / \mu^2$ in $r < $" + str(max_radius))
	else:
		plt.ylabel("$E$ in $r < $" + str(max_radius))
	plt.legend(loc='upper left', fontsize=8)
	plt.title("scalar field energy inside a sphere vs time, $M=1$, different $\\mu$")
	plt.tight_layout()
	if change_in_E:
		save_path = home_path + "plots/delta_mass_in_sphere_compare_mu_radius_" + str(max_radius) + ".png"
	else:
		save_path = home_path + "plots/mass_in_sphere_compare_mu_radius_" + str(max_radius) + ".png"
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()

#for dd in data_dirs:
#	calculate_mass_in_sphere(dd)

plot_graph()