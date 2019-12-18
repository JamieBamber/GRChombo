import yt
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve
from yt import derived_field
import time
import sys

yt.enable_parallelism()

start_time = time.time()

# load inputs
input1 = sys.argv[1]
if len(sys.argv) < 3:
	input2 = 0
else:
	input2 = sys.argv[2]

# load dataset time series
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
data_sub_dir = str(input1)

# restart number
restart_number = int(input2)

dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_*.3d.hdf5"
ds = yt.load(dataset_path) # this loads a dataset time series
print("loaded data from ", dataset_path)
print("time = ", time.time() - start_time)

ds0 = ds[0] # get the first dataset 

# set centre
center = [512.0, 512.0, 0]
L = 0.5*max(ds0.domain_width.v)

# set up parameters
N_radii = 5
N = len(ds)
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

data_storage = {}
# iterate through datasets (forcing each to go to a different processor)
for sto, dsi in ds.piter(storage=data_storage):
	time_0 = time.time()
	dsi = ds[i]
	# store time
	current_time = dsi.current_time 
	output = [current_time]
	
	# iterate over sphere radii
	for n in range(0,N_radii):
		r = r_list[n]
		sphere = dsi.sphere(center, r)
		volume = sphere.sum("cell_volume")
		if half_box:
			volume = 2*volume
		
		# calculate energy inside sphere
		meanE = sphere.mean("rho_E_eff", weight="cell_volume")
		E = volume*meanE
		output.append(E)
		#
	
	# find angular momentum inside largest sphere
	sphere = dsi.sphere(center, r_list[-1])
	volume = sphere.sum("cell_volume")
	if half_box:
        	volume = 2*volume
	meanJ =	sphere.mean("rho_J_eff", weight="cell_volume")
	J = volume*meanJ
	output.append(J)

	# store output
	sto.result = output
	sto.result_id = str(dsi)
	print("done {:d} of {:d} in {:.1f} s".format(i+1, N, time.time()-time_0))

if yt.is_root():	
	# output to file
	home_path="/home/dc-bamb1/GRChombo/Analysis"	
	output_file = home_path + "/" + data_sub_dir + "_vars" + ".csv"
	if restart_number == 0:
		# output header to file
		f = open(output_file, "w+")
		f.write("# time	E at ")
		for n in range(0, len(r_list)):
			f.write("{:.1f}	".format(r_list[n]))
		f.write("J\n")  
		f.write("#\n")
	elif restart_number != 0:
		f = open(output_file, "a")	
	for key in sorted(data_storage.keys()):
		data = data_storage[key]
		f.write("{:.1f}	".format(data[0]))
		for n in range(0, N_radii):
                        f.write("{:.2f} ".format(data[n+1]))	
		f.write("{:.2f}\n".format(data[N_radii+1]))
	f.close()
