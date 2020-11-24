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

data_sub_dir = "run0022_KNL_l0_m0_a0_Al0_mu1_M1"

save_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/"

def calculate_data():
	# load dataset time series
	data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
	dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_*.3d.hdf5"
	ds = yt.load(dataset_path) 
	N = len(ds)
	print("loaded data from ", dataset_path)
	print("time = ", time.time() - start_time)
	
	# set centre
	center = [512.0, 512.0, 0]
	
	# set up parameters
	z_position = 0.001	# s position of slice
	N_bins = 128
	a = 0
	M = 1
	mu = 1
	r_plus = M*(1 + np.sqrt(1 - a**2))
	R_min = 1.05*(r_plus/4)
	R_max = 100
	
	### derived fields
	# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
	@derived_field(name = "weighting_field", units = "")
	def _rho_E_eff(field, data):
        	return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* data["cylindrical_radius"]*(R_max - R_min)*cm)
	
	# iterate through datasets (forcing each to go to a different processor)
	dt = 0.25
	amplitude = 0.1
	
	data_storage = {}
	for sto, dsi in ds.piter(storage=data_storage):
		time0 = time.time()
		# make slice 
		slice = dsi.r[:,:,z_position]
		slice.set_field_parameter("center", center)
		current_time = dsi.current_time	
		number = int(current_time/dt)
		
		# make profile
		rp = yt.create_profile(slice, "spherical_radius", fields=["phi"], n_bins=N_bins, weight_field="weighting_field", extrema={"spherical_radius" : (R_min, R_max)})
	
		### plot phi profile vs ln(r_BS - 1)
		R = rp.x.value
		phi = rp["phi"].value
		r_BL = R*(1 + r_plus/(4*R))**2
		r_star = r_BL/r_plus + np.log(r_BL/r_plus - 1)
		"""plt.plot(np.log(r_star, phi, 'r-')
		plt.xlabel("$r_*$")
		plt.ylabel("$\\phi$")
		plt.grid(axis='both')
		title = data_sub_dir + " time = {:.1f}".format(current_time) 
		plt.title(title)
		plt.tight_layout()"""
	
		Abest = np.max((phi/amplitude - 1)*r_BL/r_plus)
		output = [current_time, Abest]
		# store output
		sto.result = output
		sto.result_id = str(dsi)	
		print("done number {:d} of {:d} in time {:.2f}".format(number, N*5, time.time() - time0))
	
	if yt.is_root():
		# output to file
		filename = data_sub_dir + "_fitted_a_amplitude_vs_time.dat"	
		output_path = save_root_path + filename
		# output header to file
		f = open(output_path, "w+")
		f.write("# t    a	#\n")
		# output data
		for key in sorted(data_storage.keys()):
        		data = data_storage[key]
        		f.write("{:.3f} ".format(data[0]))
        		f.write("{:.4f}\n".format(data[1]))
		f.close()
		print("saved data to file " + str(output_path))
	
def load_data():
	# load data from dat file
	file_name = save_root_path +  data_sub_dir + "_fitted_a_amplitude_vs_time.dat"
	data = np.genfromtxt(file_name, skip_header=1)
	print("loaded data for " + data_sub_dir)
	return data
	
def plot_data():
	data = load_data()
	t = data[:,0]
	a = data[:,1]
	plt.plot(t, a, "b-")
	plt.ylabel("fitted $a$ coefficient for $(1 + a/r)$ envelope")
	plt.xlabel("time")
	plt.title(data_sub_dir + " fitted envelope growth")
	save_plot_path = "/home/dc-bamb1/GRChombo/Analysis/plots/"
	filename = data_sub_dir + "_fitted_a_amplitude_vs_time.png"
	plt.savefig(save_plot_path + filename)
	print("saved plot as" + save_plot_path + filename)
	plt.clf()

plot_data()
