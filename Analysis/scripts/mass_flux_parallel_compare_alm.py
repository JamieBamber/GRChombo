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
add_data_dir(data_dirs, 22, 0, 0, "0")

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"
max_radius = 450
outer_thickness = 10 # box width = 8 
inner_thickness = 0.05 # min box width = 1/16 = 0.0625 
M = 1

output_dir = "data/compare_alm_flux"

half_box = True

Jr_or_Sr = True

def calculate_flux(dd):
	data_sub_dir = dd.name
	a = dd.a	
	r_plus = M*(1 + math.sqrt(1 - a**2))
	r_minus = M*(1 - math.sqrt(1 - a**2))
	min_radius = r_plus
	max_r = max_radius*(1 + 4*r_plus/max_radius)**2

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
		
	if Jr_or_Sr: 
		# derived fields
		@derived_field(name = "rho_Jr_eff", units = "")
		def _rho_Jr_eff(field, data):
			r_BL = (data["spherical_radius"]/cm)*(1 + r_plus*cm/(4*data["spherical_radius"]))**2
			Sigma2 = r_BL**2 + (data["z"]*a*M/(r_BL*cm))
			#Delta = r_BL**2 + (a*M)**2 - 2*M*r_BL
			# r^2*(r_BL - r_minus)/(Sigma^2*r)*S_r*det(gamma)		
			return ((data["spherical_radius"]**2/cm**2)*(r_BL - r_minus)/(Sigma2*r_BL))*data["S_r"]*pow(data["chi"],-3)
	
	elif not Jr_or_Sr:
		# derived fields
                @derived_field(name = "rho_Jr_eff", units = "")
                def _rho_Jr_eff(field, data):
                        return data["S_r"]*pow(data["chi"],-3)	

	"""@derived_field(name = "rho_J_eff", units = "")
	def _rho_J_eff(field, data):
        	return data["S_azimuth"]*pow(data["chi"],-3)"""
	
	data_storage = {}
	# iterate through datasets (forcing each to go to a different processor)
	for sto, dsi in ds.piter(storage=data_storage):
		time_0 = time.time()
		# store time
		current_time = dsi.current_time 
		output = [current_time]
		
		# make inner and outer shells
		outer_shell = dsi.sphere(center, max_radius+0.5*outer_thickness) - dsi.sphere(center, max_radius-0.5*outer_thickness)
		inner_shell = dsi.sphere(center, min_radius+inner_thickness) - dsi.sphere(center, min_radius)

		# calculate inner and outer flux
		Jr_outer = outer_shell.mean("rho_Jr_eff", weight="cell_volume")*4*math.pi*(max_radius**2)
		Jr_inner = inner_shell.mean("rho_Jr_eff", weight="cell_volume")*4*math.pi*((r_plus/4)**2)
		output.append(Jr_outer)
		output.append(Jr_inner)
		
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
		if Jr_or_Sr:
			dd.filename = "l={:d}_m={:d}_a={:s}_flux.csv".format(dd.l, dd.m, str(dd.a), max_radius)
		elif not Jr_or_Sr:
			dd.filename = "l={:d}_m={:d}_a={:s}_flux_old.csv".format(dd.l, dd.m, str(dd.a), max_radius)
		output_path = home_path + output_dir + "/" + dd.filename 
		# output header to file
		f = open(output_path, "w+")
		f.write("# t	flux r={:.0f}	flux r={:.2f} \n".format(max_radius, min_radius))
		# output data
		for key in sorted(data_storage.keys()):
			data = data_storage[key]
			f.write("{:.3f}	".format(data[0]))
			f.write("{:.3f}	".format(data[1]))
			f.write("{:.3f}\n".format(data[2]))
		f.close()
		print("saved data to file " + str(output_path))
		
def load_data():
	# load data from csv files
	data = {}
	for dd in data_dirs:
		file_name = home_path + output_dir + "/" + "l={:d}_m={:d}_a={:s}_flux.csv".format(dd.l, dd.m, str(dd.a), max_radius)
		data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		print("loaded data for " + dd.name)
	"""old_data = {}
	for dd in data_dirs:
                file_name = home_path + output_dir + "/" + "l={:d}_m={:d}_a={:s}_flux_old.csv".format(dd.l, dd.m, str(dd.a), max_radius)
                old_data[dd.num] = np.genfromtxt(file_name, skip_header=1)
                print("loaded data for " + dd.name)"""
	return data 	

def plot_graph():
	data = load_data()
	colours = ['r-', 'g-', 'b--', 'c--'] 

	i = 0
	for dd in data_dirs:
		a = dd.a
		r_plus = M*(1 + math.sqrt(1 - a**2))
		min_radius = r_plus
		line_data = data[dd.num]
		#old_line_data = old_data[dd.num]
		t = line_data[:,0]
		outer_flux = line_data[:,1] 
		inner_flux = line_data[:,2]
		#old_outer_flux = old_line_data[:,1] 
		#old_inner_flux = old_line_data[:,2]		 
		label_ = "l={:d} m={:d} a={:s}".format(dd.l, dd.m, str(dd.a))
		plt.plot(t[:], outer_flux[:], 'r-', label=label_+" Jr R={:.0f}".format(max_radius))
		plt.plot(t[:], inner_flux[:], 'b-', label=label_+" Jr R={:.2f}".format(min_radius))
		#plt.plot(t[:], old_outer_flux[:], 'b--', label=label_+" Sr R={:.2f}".format(max_radius))
		#plt.plot(t[:], old_inner_flux[:], 'c--', label=label_+" Sr R={:.2f}".format(min_radius))
		plt.plot(t[:], outer_flux[:]-inner_flux[:], 'g-', label=label_+" net growth rate")
		i = i + 1
	plt.xlabel("time")
	plt.ylabel("energy flux across the outer radius and horizon" + str(max_radius))
	plt.legend(loc='upper left', fontsize=8)
	plt.title("scalar field energy flux vs time, $M=1, \\mu=0.4$")
	plt.tight_layout()
	save_path = home_path + "plots/flux_compare_alm_radius_r=" + str(max_radius) + "_.png"
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()

"""Jr_or_Sr = True

for dd in data_dirs:
	calculate_flux(dd)

Jr_or_Sr = False

for dd in data_dirs:
        calculate_flux(dd)"""

plot_graph()
