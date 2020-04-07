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

IK = "run0022_KNL_l0_m0_a0_Al0_mu1_M1_correct_Ylm"
KS = "run0022_KNL_l0_m0_a0_Al0_mu1_M1_KerrSchild"

# root directory for saving 
movie_name = "phi_a=l=0_IsoKerr_vs_KerrSchild_movie"
save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/" 
frames_dir =  movie_name
try:
	makedirs(save_root_path + frames_dir)
except:
	pass

# set centre
center = [512.0, 512.0, 0]

# set up parameters
z_position = 0.0001	# s position of slice
R_min_IK = 0.5
R_min_KS = 2.0 
R_max = 100
N_bins = 100
r_s = 2
y_lim = (-1, 1)

def r_star(r):
	return r/r_s + np.log(r/r_s - 1)

### derived fields
# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
@derived_field(name = "weighting_field_IK", units = "")
def _rho_E_eff(field, data):
        return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* data["cylindrical_radius"]*(R_max - R_min_IK)*cm)

@derived_field(name = "weighting_field_KS", units = "")
def _rho_E_eff(field, data):
        return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* data["cylindrical_radius"]*(R_max - R_min_KS)*cm)

# load dataset time series for Isotropic Kerr
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
dataset_path = data_root_path + "/" + IK + "/KerrSFp_*.3d.hdf5"
ds = yt.load(dataset_path) 
print("loaded data from ", dataset_path)
print("time = ", time.time() - start_time)

# iterate through datasets (forcing each to go to a different processor)
dt = 0.25*5
for dsi in ds.piter():
	# make slice 
	slice = dsi.r[:,:,z_position]
	slice.set_field_parameter("center", center)
	current_time = dsi.current_time	
	number = int(current_time/dt)
	print("creating profile for number {:06d}".format(number))	
	
	# make first profile
	rp = yt.create_profile(slice, "spherical_radius", fields=["phi"], n_bins=N_bins, weight_field="weighting_field_IK", extrema={"spherical_radius" : (R_min_IK, R_max)})
	R1 = rp.x.value
	phi1 = rp["phi"].value
	
	# open second dataset
	new_dataset_path = data_root_path + "/" + KS + "/KerrSFp_{:06d}.3d.hdf5".format(5*number)
	dsi2 = yt.load(new_dataset_path)

	# make second profile
	slice = dsi2.r[:,:,z_position]
	slice.set_field_parameter("center", center)
	rp = yt.create_profile(slice, "spherical_radius", fields=["phi"], n_bins=N_bins, weight_field="weighting_field_KS", extrema={"spherical_radius" : (R_min_KS, R_max)})
	R2 = rp.x.value
	phi2 = rp["phi"].value	

	### plot rho profile vs r_BS
	r1 = R1*(1 + r_s/(4*R1))**2
	r2 = R2
	rstar1 = r_star(r1)
	rstar2 = r_star(r2)
	fig, ax = plt.subplots(nrows=2, sharex=True)
	fig.subplots_adjust(hspace=0)
	ax1, ax2 = ax
	colours = ['r-', 'b-']

	# make upper plot 
	ax1.plot(rstar1, phi1, colours[0], label="Isotropic Kerr")
	ax1.set_ylabel("$\\phi$ Isotropic Kerr")
	ax1.grid(axis='both')
	ax1.set_ylim(y_lim)

	title = "$\\phi$ profiles, time = {:.1f}".format(current_time) 
	ax1.set_title(title)

	# make lower plot
	ax2.plot(rstar2, phi2, colours[1], label="Kerr Schild")
	ax2.set_ylabel("$\\phi$ Kerr Schild")
	ax2.set_xlabel("$r_*$")
	ax2.grid()
	ax2.set_ylim(y_lim)

	plt.legend()
	plt.tight_layout()

	save_name = save_root_path + frames_dir + "/frame_{:06d}.png".format(number)
	plt.savefig(save_name, transparent=False)
	plt.clf()
	print("saved " + str(save_name))
