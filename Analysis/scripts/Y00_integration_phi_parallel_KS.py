import yt
from yt import derived_field
from yt.units import cm
import numpy as np
import time
import math
import sys

yt.enable_parallelism()

#start_time = time.time()

run_number=67
a_str="0"
mu_str="1"
M=1

data_sub_dir = "run{:04d}_KNL_l0_m0_a{:s}_Al0_mu{:s}_M1_KerrSchild".format(run_number, a_str, mu_str)

# load dataset time series
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_*.3d.hdf5"
ds = yt.load(dataset_path) 
N = len(ds)
print("loaded data from ", dataset_path)

# set centre
center = [512.0, 512.0, 0]

# set up parameters
z_position = 0.001	# s position of slice
a = float(a_str)
r_plus = M*(1 + np.sqrt(1 - a*a))
r_min = r_plus
r_max = 200
N_bins = 128

### derived fields

# r_KS
@derived_field(name = "r_KS", units = "")
def _r_KS(field, data):
	R2 = data["spherical_radius"]**2
	z = data["z"]
	a2 = (a*M*cm)**2
	r2 = 0.5*(R2 - a2) + np.sqrt(0.25*(R2 - a2)**2 + a2*z**2)
	r = np.sqrt(r2)/cm
	return r

# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
@derived_field(name = "weighting_field", units = "")
def _weighting_field(field, data):
        return pow(data["cell_volume"].in_base("cgs"),2.0/3)*N_bins / (2*math.pi*data["r_KS"]*(r_max - r_min)*cm**2)

# iterate through datasets (forcing each to go to a different processor)
dt = 0.25*5

data_storage = {}
for sto, dsi in ds.piter(storage=data_storage):
	# store time
	current_time = dsi.current_time
	output = [current_time]
	
	# make slice 
	slice = dsi.r[:,:,z_position]
	slice.set_field_parameter("center", center)
	current_time = dsi.current_time	
	number = int(current_time/dt)
	print("plotting number {:06d}".format(number), flush=True)	
	
	# make profile
	rp = yt.create_profile(slice, "r_KS", fields=["phi"], n_bins=128, weight_field="weighting_field", extrema={"r_KS" : (r_min, r_max)})
	### data
	phi = rp["phi"].value
	output.append(phi)
	if (current_time == 0.0):
		output.append(rp.x.value)

	# store output
	sto.result = output
	sto.result_id = str(dsi)
	i = int(current_time/dt)
	print("done {:d} of {:d}".format(i+1, N), flush=True)

if yt.is_root():
	data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Y00_integration_data/"	
	file_name = data_sub_dir + "_phi_{:s}_n{:06d}.dat".format("linear", 0)
	# output header to file
	output_path = data_root_path + file_name
	f = open(output_path, "w+")
	f.write("# t	r = ...\n")
	key0 = sorted(data_storage.keys())[0]
	r = data_storage[key0][2]
	# write r line
	f.write("0	")
	for i in range(0,len(r)-1):
		f.write("{:.6e}      ".format(r[i]))
	f.write("{:.6e}\n".format(r[-1]))	
	# output data
	for key in sorted(data_storage.keys()):
		data = data_storage[key]
		f.write("{:.6e}	".format(data[0]))
		for i in range(0,len(r)-1):
			f.write("{:.6e}	".format(data[1][i]))
		f.write("{:.6e}\n".format(data[1][-1]))
	f.close()
	print("saved data to file " + str(output_path))
	
