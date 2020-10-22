import yt
from yt import derived_field
from yt.units import cm
import numpy as np
import time
import matplotlib.pyplot as plt
import math
from os import makedirs
import sys
from scipy.interpolate import interp1d

yt.enable_parallelism()

start_time = time.time()

""" # load inputs
input1 = sys.argv[1]
if len(sys.argv) < 3:
        input2 = 0
else:
     	input2 = sys.argv[2] """

data_sub_dir = "run2.2_KNL_l0_m0_a0.99_Al0"

# load dataset time series
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_*.3d.hdf5"
ds = yt.load(dataset_path) 
print("loaded data from ", dataset_path)
print("time = ", time.time() - start_time)

# set centre
center = [512.0, 512.0, 0]
L = max(ds[0].domain_width.v)

# set up parameters
z_position = 0.001	# s position of slice
r_outer_horizon = 0.25	# R_outer = r_+ / 4 ~= 1 / 4 for an extremal Kerr BH
r_min = r_outer_horizon
r_max = 500
N_bins = 128
a = 0.99
r_plus = 1 + math.sqrt(1 - a**2)

# root directory for saving 
save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/" 
frames_dir = data_sub_dir + "_phi_profile_movie"
try:
	makedirs(save_root_path + frames_dir)
except:
	pass

### derived fields
# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
@derived_field(name = "weighting_field", units = "")
def _rho_E_eff(field, data):
        return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* data["cylindrical_radius"]*(r_max - r_min)*cm)

# iterate through datasets (forcing each to go to a different processor)
dt = 0.25*5
i = 0
for dsi in ds.piter():
	# make slice 
	slice = dsi.r[:,:,z_position]
	slice.set_field_parameter("center", center)
	current_time = dsi.current_time	
	number = int(current_time/dt)
	print("plotting number {:06d}".format(number))	
	
	# make profile
	rp = yt.create_profile(slice, "spherical_radius", fields=["phi"], n_bins=128, weight_field="weighting_field", extrema={"spherical_radius" : (r_min, r_max)})

	### plot phi profile vs ln(r_BS - 1)
	R = rp.x.value
	r_BL = R*(1 + r_plus/(4*R))**2
	plt.plot(np.log(r_BL-1), rp["phi"].value, 'r-')
	plt.xlabel("$\\ln(r_{BL}-1)$")
	plt.ylabel("$\\phi$")
	plt.grid(axis='both')
	plt.ylim((-0.75, 0.75))

	title = data_sub_dir + " time = {:.1f}".format(current_time) 

	plt.title(title)
	plt.tight_layout()

	save_name = save_root_path + frames_dir + "/frame_{:06d}.png".format(number)
	plt.savefig(save_name, transparent=False)
	plt.clf()
	i = i + 1
	print("saved " + str(save_name))

