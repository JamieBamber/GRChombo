import yt
import numpy as np
#from scipy.interpolate import interp1d
#from scipy.optimize import fsolve
import math
from yt import derived_field
import time
import sys
from matplotlib import pyplot as plt
from os import makedirs

yt.enable_parallelism()

"""run0007=(0.2 10 0.02 0.5 0 0 0)
run0008=(0.2 10 0.025 0.5 0 0 0)
run0009=(0.2 10 0.015 0.5 0 0 0)
run0010=(0.2 10 0.01 0.5 0 0 0)
run0011=(0.2 10 0.03 0.5 0 0 0)
#
run0012=(0.2 10 0.02 0.5 1 1 0)
run0015=(0.48847892320123 12.21358 1 0.0625 0 0 0)"""

class data_dir:
        def __init__(self, num, M, d, mu, dt_mult):
                self.num = num
                self.M = M
                self.d = d
                self.mu = float(mu)
                self.dt_mult = dt_mult
                self.name = "run{:04d}_M{:s}_d{:s}_mu{:s}_dt_mult{:s}".format(num, M, d, mu, dt_mult)

data_dirs = []
def add_data_dir(num, M, d, mu, dt_mult):
        x = data_dir(num, M, d, mu, dt_mult)
        data_dirs.append(x)

# choose datasets to compare

#add_data_dir(4, "0.1", "10", "0.1", "0.25")
#add_data_dir(3, "0.1", "10", "0.02", "0.25")
#add_data_dir(2, "0.1", "10", "0.005", "0.25")
#add_data_dir(1, "0.1", "10", "0.014142136", "0.25")

add_data_dir(7, "0.2", "10", "0.02", "0.5")
add_data_dir(8, "0.2", "10", "0.025", "0.5")
add_data_dir(9, "0.2", "10", "0.015", "0.5")
add_data_dir(10, "0.2", "10", "0.01", "0.5")
add_data_dir(11, "0.2", "10", "0.03", "0.5")
#add_data_dir(12, "0.2", "10", "0.02", "0.5", 1, 1, 0)
#run0015=(0.48847892320123 12.21358 1 0.0625 0 0 0)

# set up parameters
data_root_path = "/cosma6/data/dp174/dc-bamb1/GRChombo_data/NewtonianBinaryBHScalar/"
home_path="/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/"

max_radius = 4

output_dir = "data/Newtonian_Binary_BH_data"

change_in_E = True

def calculate_mass_in_sphere(dd):
	data_sub_dir = dd.name

	start_time = time.time()
	
	# load dataset time series
	
	dataset_path = data_root_path + data_sub_dir + "/Newton_plt*.3d.hdf5"
	ds = yt.load(dataset_path) # this loads a dataset time series
	print("loaded data from ", dataset_path)
	print("time = ", time.time() - start_time)
	N = len(ds)
	
	ds0 = ds[0] # get the first dataset 
	
	# set centre
	L = 256.0	
	center = [L/2, L/2, 0]
	rho0 = 0.5*(dd.mu**2)
	
	data_storage = {}
	# iterate through datasets (forcing each to go to a different processor)
	for sto, dsi in ds.piter(storage=data_storage):
		time_0 = time.time()
		# store time
		current_time = dsi.current_time 
		output = [current_time]
		
		# make sphere
		sphere = dsi.sphere(center, max_radius)
			
		# calculate energy inside sphere
		meanE = sphere.mean("rho", weight="cell_volume")
		output.append(meanE)
		
		# calculate angular momentum inside sphere
		meanJ = sphere.mean("rhoJ", weight="cell_volume")
		output.append(meanJ/rho0)

		# store output
		sto.result = output
		sto.result_id = str(dsi)
		dt = 2.0 * float(dd.dt_mult)
		i = int(current_time/dt)
		print("done {:d} of {:d} in {:.1f} s".format(i+1, N, time.time()-time_0), flush=True)
	
	if yt.is_root():	
		# make data directory if it does not already exist
		makedirs(home_path + output_dir, exist_ok=True)
		# output to file
		dd.filename = "{:s}_mean_rho_rhoJ_in_r={:d}.csv".format(dd.name, max_radius)
		output_path = home_path + output_dir + "/" + dd.filename 
		# output header to file
		f = open(output_path, "w+")
		f.write("# t	mean rho	mean rhoJ	in " + str(max_radius) + " #\n")
		# output data
		for key in sorted(data_storage.keys()):
			data = data_storage[key]
			f.write("{:.3f}	".format(data[0]))
			f.write("{:.8f}	".format(data[1]))
			f.write("{:.8f}\n".format(data[2]))
		f.close()
		print("saved data to file " + str(output_path))
		
def load_data():
	# load data from csv files
	data = {}
	for dd in data_dirs:
		file_name = home_path + output_dir + "/" + "{:s}_mean_rho_rhoJ_in_r={:d}.csv".format(dd.name, max_radius)
		data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		print("loaded data for " + dd.name)
	return data 	

def plot_graph():
	data = load_data()
	colours = ['r-', 'b-', 'g-', 'm-', 'c-', 'k-'] 
	i = 0
	for dd in data_dirs:
		line_data = data[dd.num]
		t = line_data[:,0]
		rho = line_data[:,1] #- line_data[0,1]
		rhoJ = line_data[:,2] #- line_data[0,1]
		label_ = "$\\mu=${:d}".format(dd.mu)
		if change_in_E:
			plt.plot(t[1:], rho[1:] - rho[0], colours[i], label=label_)
		else:
			plt.plot(t, mass, colours[i], label=label_)
		i = i + 1
	plt.xlabel("time")
	if change_in_E:
		plt.ylabel("$\\Delta \\rho$ mean in $r < $" + str(max_radius))
	else:
		plt.ylabel("$E$ in $r < $" + str(max_radius))
	plt.legend(loc='upper left', fontsize=8)
	plt.title("scalar field energy inside a sphere vs time, $M=0.2,d=10$")
	plt.tight_layout()
	if change_in_E:
		save_path = home_path + "plots/Newtonian_binary_delta_mean_rho_in_sphere_radius_" + str(max_radius) + ".pdf"
	else:
		save_path = home_path + "plots/Newtonian_binary_mean_rho_in_sphere_radius_" + str(max_radius) + ".pdf"
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()

for dd in data_dirs[1:]:
	calculate_mass_in_sphere(dd)

#plot_graph()
