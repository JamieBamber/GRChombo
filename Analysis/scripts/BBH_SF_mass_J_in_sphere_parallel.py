import yt
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve
from yt import derived_field
import time
import sys

yt.enable_parallelism()

start_time = time.time()

run_number=1
mu="1"
G=0
plot_interval=1
dt_multiplier=0.125
dt=8*dt_multiplier

# load dataset time series
data_root_path = "/hppfs/work/pn34tu/di76bej/GRChombo_data/BinaryBHScalarField/"
data_sub_dir = "run{:04d}_FlatScalar_mu{:s}_G{:d}".format(run_number, mu, G)
output_root_path="/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Analysis/data/BBH_SF_mass_J_in_sphere/"

dataset_path = data_root_path + data_sub_dir + "/BinaryBHSFPlot_*.3d.hdf5"
ds = yt.load(dataset_path) # this loads a dataset time series
print("loaded data from ", dataset_path)
print("time = ", time.time() - start_time)

# ds0 = ds[0] # get the first dataset 

L=512

# set centre
center = [0.5*L, 0.5*L, 0]

# set up parameters
N_radii = 5
N = len(ds)
sphere_radius=100

# output file
output_file = data_sub_dir + "_mass_J_in_sphere_r=" + str(sphere_radius) +".dat"

# derived fields
@derived_field(name = "rho_E_eff", units = "")
def _rho_E_eff(field, data):
	return data["rho"]*pow(data["chi"],-3)

@derived_field(name = "rho_J_eff", units = "")
def _rho_J_eff(field, data):
        return data["S_azimuth"]*pow(data["chi"],-3)

data_storage = {}
# iterate through datasets (forcing each to go to a different processor)
for sto, dsi in ds.piter(storage=data_storage):
	time_0 = time.time()
	# store time
	current_time = dsi.current_time 
	i = int(current_time/(dt*plot_interval))
	output = [current_time]
	
	# iterate over sphere radii
	sphere = dsi.sphere(center, sphere_radius)
	volume = sphere.sum("cell_volume")
	volume = 2*volume
		
	# calculate energy inside sphere
	meanE = sphere.mean("rho_E_eff", weight="cell_volume")
	E = volume*meanE
	output.append(E)
	#
	
	# find angular momentum inside largest sphere
	meanJ =	sphere.mean("rho_J_eff", weight="cell_volume")
	J = volume*meanJ
	output.append(J)

	# store output
	sto.result = output
	sto.result_id = str(dsi)
	print("done {:d} of {:d} in {:.1f} s".format(i+1, N, time.time()-time_0))

if yt.is_root():	
	print("writing to file")
	# output to file
	output_path = data_root_path + output_file
	#if restart_number == 0:
	# output header to file
	f = open(output_path, "w+")
	f.write("# time	E	J /n")
	f.write("#\n")
	for key in sorted(data_storage.keys()):
		data = data_storage[key]
		f.write("{:.1f}	".format(data[0]))
		f.write("{:.4f}	".format(data[1]))
		f.write("{:.4f}\n".format(data[2]))
	f.close()
