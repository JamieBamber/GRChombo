import yt
import numpy as np
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
add_data_dir(76, 5, 5, "0.7", "0.4")
add_data_dir(77, 2, 2, "0.7", "0.4")"""

#add_data_dir(74, 0, 0, "0.7", "0.4")
#add_data_dir(78, 1, -1, "0.7", "0.4")
#add_data_dir(75, 1, 1, "0.7", "0.4", "0.5")
#add_data_dir(39, 1, 1, "0.7", "0.4")
add_data_dir(71, 1, 1, "0.99", "0.4")
add_data_dir(72, 1, -1, "0.99", "0.4")
add_data_dir(77, 2, 2, "0.7", "0.4")
add_data_dir(73, 4, 4, "0.7", "0.4")

#add_data_dir(67, 0, 0, "0", "1")
#add_data_dir(79, 0, 0, "0.7", "1")
#add_data_dir(68, 0, 0, "0.99", "1")

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"
M = 1
dR = 0.01
phi0 = 0.1

output_dir = "data/compare_almmu_flux"

half_box = True

change_in_E = True

def calculate_mass_flux_in_sphere(dd):
	data_sub_dir = dd.name
	a = dd.a	
	r_plus = M*(1 + math.sqrt(1 - a**2))
	min_R = np.sqrt(2*M*r_plus)

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
		current_time = dsi.current_time 
		dt = 2.5
		i = int(current_time/dt)
		#if (i % 2 == 0):
		time_0 = time.time()
		# store time
		output = [current_time]
		
		# make sphere (defined by r_KS)
		shell = dsi.sphere(center, min_R+dR) - dsi.sphere(center, min_R)		
			
		# calculate radial (in terms of cartesian radius R) momentum and angular momentum flux in shell
		meanJ_R = shell.mean("J_r", weight="cell_volume")
		meanJ_azimuth_R = shell.mean("J_azimuth_r", weight="cell_volume")
		J_R = meanJ_R*2*np.pi*(min_R**2)
		J_azimuth_R = meanJ_azimuth_R*2*np.pi*(min_R**2)
		output.append(J_R)
		output.append(J_azimuth_R)
		
		# store output
		sto.result = output
		sto.result_id = str(dsi)
		print("done {:d} of {:d} in {:.1f} s".format(i+1, N, time.time()-time_0), flush=True)
		
	if yt.is_root():	
		# output to file
		dd.filename = "l={:d}_m={:d}_a={:s}_mu={:s}_Al={:s}_mass_ang_mom_flux_in_KerrSchild_cartesian_R.csv".format(dd.l, dd.m, str(dd.a), dd.mu, dd.Al)
		output_path = home_path + output_dir + "/" + dd.filename 
		# output header to file
		print("writing data")
		f = open(output_path, "w")
		f.write("# t	J_R	J_azimuth_R #\n")
		# output data
		for key in sorted(data_storage.keys()):
			data = data_storage[key]
			f.write("{:.3f}	".format(data[0]))
			f.write("{:.4f}	".format(data[1]))
			f.write("{:.4f}\n".format(data[2]))
		f.close()
		print("saved data to file " + str(output_path))
		
def load_data():
	# load data from csv files
	data = {}
	for dd in data_dirs:
		file_name = home_path + output_dir + "/" + "l={:d}_m={:d}_a={:s}_mu={:s}_Al={:s}_mass_ang_mom_flux_KerrSchild_cartesian_R.csv".format(dd.l, dd.m, str(dd.a), dd.mu, dd.Al)
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
		mass_flux = line_data[:,1]
		ang_mom_flux = line_data[:,2]
		F0 = (mu**2)*phi0
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

for dd in data_dirs:
	calculate_mass_flux_in_sphere(dd)

#plot_graph()

