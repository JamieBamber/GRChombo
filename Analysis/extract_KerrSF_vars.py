import yt
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve
from yt import derived_field
import time

yt.enable_parallelism()

start_time = time.time()

# load dataset time series
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
data_sub_dir = "run1_l0_m1_a0.99_Al0"

# restart number
restart_number = 19

dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_*.3d.hdf5"
ds = yt.load(dataset_path) # this loads a dataset time series
print("loaded data from ", dataset_path)
print("time = ", time.time() - start_time)

ds0 = ds[0] # get the first dataset 
""" print(dir(ds0.fields))
print(dir(ds0.fields.chombo))
print(dir(ds0.fields.gas))
print(dir(ds0.fields.index)) """
# set centre
center = [512.0, 512.0, 0]
L = 0.5*max(ds0.domain_width.v)

# set up parameters
N_radii = 5
N = len(ds)
print("number of files = ", N)
r_list = np.linspace(10, 0.75*0.5*L, N_radii)

half_box = True

# output file
output_file = data_sub_dir + "_vars" + ".csv"

# derived fields
@derived_field(name = "rho_E_eff", units = "")
def _rho_E_eff(field, data):
	return data["rho"]*pow(data["chi"],-3)

@derived_field(name = "rho_J_eff", units = "")
def _rho_J_eff(field, data):
        return data["S_azimuth"]*pow(data["chi"],-3)

@derived_field(name = "rho_J_prime_eff", units = "")
def _rho_J_prime_eff(field, data):
        return data["S_azimuth_prime"]*pow(data["chi"],-3)

# set up output data containers
time_data = []
E_data = np.zeros((N, N_radii))
J_data = []

if restart_number == 0:
	# output header to file
	f = open(output_file, "w+")
	f.write("# time	E at ")
	for n in range(0, len(r_list)):
		f.write("{:.1f}	".format(r_list[n]))
	f.write("J\n")  
	f.write("#\n")
elif restart_number != 0:
	# reopen previous file
	f = open(output_file, "a")

# iterate through datasets
for i in range(restart_number, N): 
	dsi = ds[i]
	time_0 = time.time()
	# store time
	current_time = dsi.current_time 
	time_data.append(current_time)
	f.write("{:.1f}	".format(current_time))
	
	# iterate over sphere radii
	for n in range(0,len(r_list)):
		r = r_list[n]
		sphere = dsi.sphere(center, r)
		volume = sphere.sum("cell_volume")
		if half_box:
			volume = 2*volume
		
		# calculate energy inside sphere
		meanE = sphere.mean("rho_E_eff", weight="cell_volume")
		E = volume*meanE
		# store value
		E_data[i, n] = E
		print("E for radius {:f} is {:f}".format(r, E))
		f.write("{:f}	".format(E))
		#
	
	# find angular momentum inside largest sphere
	sphere = dsi.sphere(center, r_list[-1])
	volume = sphere.sum("cell_volume")
	if half_box:
        	volume = 2*volume
	
	meanJ =	sphere.mean("rho_J_eff", weight="cell_volume")
	J = volume*meanJ
	# store value
	J_data.append(J)
	print("J is {:f}".format(J))
	f.write("{:f}\n".format(J))
	
	print("done {:d} of {:d} in {:.1f} s".format(i+1, N, time.time()-time_0))
	print("current run time = ", time.time() - start_time)

f.close()
print("written output to ", output_file)

