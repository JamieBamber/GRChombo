import yt
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve
from yt import derived_field
import time
import sys
from matplotlib import pyplot as plt

yt.enable_parallelism()

m_dirs = {}
m_dirs["-3"] = "run10_KNL_l0_m-3_a0.99_Al0_M1"
m_dirs["-2"] = "run7_KNL_l0_m-2_a0.99_Al0_M1"
m_dirs["-1"] = "run1_KNL_l0_m-1_a0.99_Al0_M1"
m_dirs["0"] = "run2.2_KNL_l0_m0_a0.99_Al0"
m_dirs["1"] = "run5_KNL_l0_m1_a0.99_Al0_M1"
m_dirs["2"] = "run3_KNL_l0_m2_a0.99_Al0_M1"
m_dirs["3"] = "run4_KNL_l0_m3_a0.99_Al0_M1"
m_dirs["10"] = "run9_KNL_l0_m10_a0.99_Al0_M1"

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"
max_radius = 200
min_radius = 

def calculate_mass_in_sphere(m):
	data_sub_dir = m_dirs[m]
	
	start_time = time.time()
	
	# load dataset time series
	
	dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_*.3d.hdf5"
	ds = yt.load(dataset_path) # this loads a dataset time series
	print("loaded data from ", dataset_path)
	print("time = ", time.time() - start_time)
	N = len(ds)
	
	ds0 = ds[0] # get the first dataset 
	
	# set centre
	center = [512.0, 512.0, 0]
	L = 512.0	
	
	half_box = True
	
	# derived fields
	@derived_field(name = "rho_E_eff", units = "")
	def _rho_E_eff(field, data):
		return data["rho"]*pow(data["chi"],-3)
	
	"""@derived_field(name = "rho_J_eff", units = "")
	def _rho_J_eff(field, data):
        	return data["S_azimuth"]*pow(data["chi"],-3)
	
	@derived_field(name = "rho_J_prime_eff", units = "")
	def _rho_J_prime_eff(field, data):
        	return data["S_azimuth_prime"]*pow(data["chi"],-3)"""
	
	data_storage = {}
	# iterate through datasets (forcing each to go to a different processor)
	for sto, dsi in ds.piter(storage=data_storage):
		time_0 = time.time()
		# store time
		current_time = dsi.current_time 
		output = [current_time]
		
		# make sphere
		sphere = dsi.sphere(center, radius)
		volume = sphere.sum("cell_volume")
		if half_box:
			volume = 2*volume
			
		# calculate energy inside sphere
		meanE = sphere.mean("rho_E_eff", weight="cell_volume")
		E = volume*meanE
		output.append(E)
		#
		
		"""# find angular momentum inside largest sphere
		sphere = dsi.sphere(center, r_list[-1])
		volume = sphere.sum("cell_volume")
		if half_box:
        		volume = 2*volume
		meanJ =	sphere.mean("rho_J_eff", weight="cell_volume")
		J = volume*meanJ
		output.append(J)"""
	
		# store output
		sto.result = output
		sto.result_id = str(dsi)
		dt = 1.25
		i = int(current_time/dt)
		print("done {:d} of {:d} in {:.1f} s".format(i+1, N, time.time()-time_0))
	
	if yt.is_root():	
		# output to file
		output_file = "data/mass_inside_r=" + str(radius) + "/" + data_sub_dir + "_mass_in_r=" + str(radius) + ".csv"
		output_path = home_path + output_file
		# output header to file
		f = open(output_path, "w+")
		f.write("# t	mass in r<=" + str(radius) + " #\n")
		# output data
		for key in sorted(data_storage.keys()):
			data = data_storage[key]
			f.write("{:.3f}	".format(data[0]))
			f.write("{:.2f}\n".format(data[1]))
		f.close()
		print("saved data to file " + str(output_file))
		
#for m in ["-2", "-1", "2", "3"]:
#	calculate_mass_in_sphere(m)


def load_data():
	# load data from csv files
	data = {}
	home_path="/home/dc-bamb1/GRChombo/Analysis/"
	for key in m_dirs.keys():
		file_name = home_path + "data/mass_inside_r=" + str(radius) + "/" + m_dirs[key] + "_mass_in_r=" + str(radius) + ".csv"
		try:
			data[key] = np.genfromtxt(file_name, skip_header=1)
			print("loaded data for m = " + key)
		except:
			pass
	print("loaded available data")
	return data 	

def fix_time_data(m):
	file_name = home_path + "data/mass_inside_r=" + str(radius) + "/" + m_dirs[m] + "_mass_in_r=" + str(radius) + ".csv"
	old_data = np.genfromtxt(file_name, skip_header=1)
	dt = 1.25
	N = old_data.shape[0]
	new_t_data = dt*np.linspace(0.0, N-1, N)
	# output header to file
	f = open(file_name, "w+")
	f.write("# t	mass in r<=" + str(radius) + " #\n")
	# output data
	for i in range(0, N):
		f.write("{:.3f}	".format(new_t_data[i]))
		f.write("{:.2f}\n".format(old_data[i,1]))
	f.close()
	print("remade " + file_name)		

def plot_graph():
	data = load_data()
	colours = ['c--', 'r--', 'b--', 'g-', 'b-', 'r-', 'c-', 'm-']
	i = 0
	for key in data.keys():
		line_data = data[key]
		x = line_data[:,0]
		y = line_data[:,1] #- line_data[0,1]
		label_ = "m = " + key
		plt.plot(x, y, colours[i], label=label_)
		i = i + 1
	plt.xlabel("time")
	plt.ylabel("$E$ in $r < $" + str(radius))
	plt.legend(loc='upper left')
	plt.tight_layout()
	save_path = home_path + "plots/mass_in_sphere_radius_" + str(radius) + ".png"
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()


#fix_time_data("-2")	
#calculate_mass_in_sphere("10")
plot_graph()
