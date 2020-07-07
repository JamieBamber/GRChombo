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

#print("yt version = ",yt.__version__)

yt.enable_parallelism()

class data_dir:
	def __init__(self, num, l, m, a, mu, Al):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = mu
		self.Al = Al
		self.name = "run{:04d}_KNL_l{:d}_m{:d}_a{:s}_Al{:s}_mu{:s}_M1_KerrSchild".format(num, l, m, a, Al, mu)

data_dirs = []		
def add_data_dir(num, l, m, a, mu, Al="0"):
	x = data_dir(num, l, m, a, mu, Al)
	data_dirs.append(x)

# choose datasets to compare

"""add_data_dir(74, 0, 0, "0.7", "0.4")
add_data_dir(39, 1, 1, "0.7", "0.4")
add_data_dir(73, 4, 4, "0.7", "0.4")
add_data_dir(76, 5, 5, "0.7", "0.4")
add_data_dir(77, 2, 2, "0.7", "0.4")"""

#add_data_dir(74, 0, 0, "0.7", "0.4")
#add_data_dir(78, 1, -1, "0.7", "0.4")
#add_data_dir(75, 1, 1, "0.7", "0.4", "0.5")
#add_data_dir(39, 1, 1, "0.7", "0.4")

#add_data_dir(67, 0, 0, "0", "1")
#add_data_dir(79, 0, 0, "0.7", "1")
#add_data_dir(68, 0, 0, "0.99", "1")

#add_data_dir(101, 1, 1, "0.7", "0.4")
#add_data_dir(102, 2, 2, "0.7", "0.4")
#add_data_dir(103, 0, 0, "0.7", "0.4")
#add_data_dir(104, 1, -1, "0.7", "0.4")
#add_data_dir(105, 1, 1, "0.99", "0.4")
#add_data_dir(106, 0, 0, "0.99", "0.4")
#add_data_dir(107, 4, 4, "0.7", "0.4")
#add_data_dir(108, 8, 8, "0.7", "0.4")
add_data_dir(110, 1, 1, "0.7", "0.05")
add_data_dir(111, 1, 1, "0.7", "1")

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"
M = 1
max_r = 450
phi0 = 0.1

output_dir = "data/compare_almmu_mass"

half_box = True

change_in_E = True

start_num=0
end_num=30
	
def calculate_mass_in_sphere(dd):
	data_sub_dir = dd.name
	a = dd.a	
	r_plus = M*(1 + math.sqrt(1 - a**2))
	min_r = r_plus

	start_time = time.time()
	
	# load dataset time series
	
	# derived fields
	@derived_field(name = "r_KS", units = "")
	def _r_KS(field, data):
		R = data["spherical_radius"]/cm
		z = data["z"]/cm
		aM = M*a
		r_KS = np.sqrt((R**2 - aM**2)/2 + np.sqrt((R**2 - aM**2)/4 + (aM*z)**2))
		return r_KS
		
	dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_*.3d.hdf5"
	ds_all = yt.load(dataset_path) # this loads a dataset time series
	print("loaded data from ", dataset_path)
	print("time = ", time.time() - start_time)
	ds = ds_all[start_num:end_num]
	N = len(ds)

	ds0 = ds[0] # get the first dataset 
	
	# set centre
	center = [512.0, 512.0, 0]
	L = 512.0	
		
	data_storage = {}
	# iterate through datasets (forcing each to go to a different processor)
	for sto, dsi in ds.piter(storage=data_storage):
		current_time = dsi.current_time 
		dt = 2.5
		i = int(current_time/dt)
		#if (i % 2 == 0):
		time_0 = time.time()
		# store time
		output = [current_time]
		
		# make sphere (defined by r_KS)
		ad = dsi.all_data()
		sphere = ad.cut_region(["(obj['r_KS'] < {:.3f}) & (obj['r_KS'] > {:.3f})".format(max_r, min_r)])
		volume = sphere.sum("cell_volume")
		if half_box:
			volume = 2*volume
			
		# calculate energy inside sphere
		meanE = sphere.mean("rho", weight="cell_volume")
		E = volume*meanE
		output.append(E)
		
		# store output
		sto.result = output
		sto.result_id = str(dsi)
		print("done {:d} of {:d} in {:.1f} s".format(i+1, N, time.time()-time_0), flush=True)
		
	if yt.is_root():	
		# output to file
		dd.filename = "l={:d}_m={:d}_a={:s}_mu={:s}_mass_in_r={:d}_KerrSchild_conserved_rho.csv".format(dd.l, dd.m, str(dd.a), dd.mu, max_r)
		output_path = home_path + output_dir + "/" + dd.filename 
		# output header to file
		print("writing data")
		if (start_num==0):
			f = open(output_path, "w")
			f.write("# t	mass in r<=" + str(max_r) + " #\n")
		else:
			f = open(output_path, "a")
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
		file_name = home_path + output_dir + "/" + "l={:d}_m={:d}_a={:s}_mu={:s}_Al={:s}_mass_in_r={:d}_KerrSchild_conserved_rho.csv".format(dd.l, dd.m, str(dd.a), dd.mu, dd.Al, max_r)
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
		mu = float(dd.mu)
		mass = line_data[:,1] #- line_data[0,1]
		E0 = 0.5*(mu**2)*(4*np.pi/3)*(max_r**3)*phi0**2
		delta_mass = (mass[1:] - mass[0])/E0
		m = abs(dd.m)
		if (dd.m < 0):
			a = -dd.a
		else:
			a = dd.a
		label_ = "$a=${:2f}".format(dd.a)
		if change_in_E:
			plt.plot(t[1:], delta_mass, colours[i], label=label_)
		else:
			plt.plot(t, mass, colours[i], label=label_)
		i = i + 1
	plt.xlabel("$t$")
	if change_in_E:
		plt.ylabel("$\\Delta E / E_0$ in $r < $" + str(max_r))
	else:
		plt.ylabel("$E$ in $r < $" + str(max_r))
	plt.legend(loc='upper left', fontsize=8)
	plt.title("scalar field energy inside a sphere vs time, $M=1$, $\\mu=0.4$, $l=m=0$")
	#plt.xlim((0, 450))
	#plt.ylim((0, 0.004))
	plt.tight_layout()
	if change_in_E:
		save_path = home_path + "plots/delta_mass_in_sphere_compare_a_l=m=0_Kerr_Schild_radius_" + str(max_r) + ".png"
	else:
		save_path = home_path + "plots/mass_in_sphere_compare_mu_radius_" + str(max_r) + ".png"
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()

#for dd in data_dirs:
#	calculate_mass_in_sphere(dd)

plot_graph()

