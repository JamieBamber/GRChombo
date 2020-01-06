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

m_dirs = {}
m_dirs["-3"] = "run10_KNL_l0_m-3_a0.99_Al0_M1"
m_dirs["-2"] = "run7_KNL_l0_m-2_a0.99_Al0_M1"
m_dirs["-1"] = "run1_KNL_l0_m-1_a0.99_Al0_M1"
m_dirs["0"] = "run2.2_KNL_l0_m0_a0.99_Al0"
m_dirs["1"] = "run5_KNL_l0_m1_a0.99_Al0_M1"
m_dirs["2"] = "run3_KNL_l0_m2_a0.99_Al0_M1"
m_dirs["3"] = "run4_KNL_l0_m3_a0.99_Al0_M1"
m_dirs["10"] = "run9_KNL_l0_m10_a0.99_Al0_M1"

# choose m values to plot
m_list = ["3", "-3"]
data_sub_dirs = []
for m in m_list:
	data_sub_dirs.append(m_dirs[m])

# root directory for saving 
movie_name = "m=plus_minus_3_delta_rho_and_J_profile_movie"
save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/" 
frames_dir =  movie_name
try:
	makedirs(save_root_path + frames_dir)
except:
	pass

# set centre
center = [512.0, 512.0, 0]

# set up parameters
z_position = 0.001	# s position of slice
r_outer_horizon = 0.25	# R_outer = r_+ / 4 ~= 1 / 4 for an extremal Kerr BH
r_min = r_outer_horizon
r_max = 250
N_bins = 128
a = 0.99
r_plus = 1 + math.sqrt(1 - a**2)

### derived fields
# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
@derived_field(name = "weighting_field", units = "")
def _weighting_field(field, data):
        return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* data["cylindrical_radius"]*(r_max - r_min)*cm)

def get_profile_data(ds):
	slice = ds.r[:,:,z_position]
	slice.set_field_parameter("center", center)
	rp = yt.create_profile(slice, "cylindrical_radius", fields=["rho", "S_azimuth"], n_bins=12, weight_field="weighting_field", extrema={"cylindrical_radius" : (r_min, r_max)})
	rho = rp["rho"].value
	rho_J = rp["S_azimuth"].value
	J = rho_J/rho
	R = rp.x.value
	return (R, rho, J)

# load dataset time series for first m value
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
ds = yt.load(data_root_path + "/" + data_sub_dirs[0] + "/KerrSFp_*.3d.hdf5") 
print("loaded data from ", data_sub_dirs[0])
print("time = ", time.time() - start_time)

# get initial data for first m value
ds0 = ds[0]
R, rho01 = get_profile_data(ds0)[0:2]
print("calculated rho0 data for m = ", m_list[0])
# initial data for second m value
ds02 = yt.load(data_root_path + "/" + data_sub_dirs[1] + "/KerrSFp_{:06d}.3d.hdf5".format(0))
print("loaded initial data for m = ", m_list[1])
rho02 = get_profile_data(ds02)[1]
print("calculated rho0 data for m = ", m_list[1])

# iterate through datasets (forcing each to go to a different processor)
dt = 0.25*5
for dsi in ds.piter():
	# make slice 
	current_time = dsi.current_time	
	number = int(current_time/dt)
	print("creating profile for number {:06d}".format(number))	
	
	# open second dataset
	try:
		dsi2 = yt.load(data_root_path + "/" + data_sub_dirs[1] + "/KerrSFp_{:06d}.3d.hdf5".format(5*number))
	except:
		break
	else:
		rho1, J1 = get_profile_data(dsi)[1:3]
		rho2, J2 = get_profile_data(dsi2)[1:3]
		delta_rho1 = rho1 - rho01
		delta_rho2 = rho2 - rho02	
	
		### plot delta rho profile vs r_BS
		r_BL = R*(1 + r_plus/(4*R))**2
		r = r_BL
		ln_r = np.log(r_BL)
	
		fig, ax = plt.subplots(nrows=2, sharex=True)
		fig.subplots_adjust(hspace=0)
		ax1, ax2 = ax
		colours = ['c-', 'g--']
	
		# make upper plot 
		ax1.plot(ln_r, (r**2)*delta_rho1, colours[0], label="m = " + m_list[0])
		ax1.plot(ln_r, (r**2)*delta_rho2, colours[1], label="m = " + m_list[1])
		ax1.set_ylabel("${r_{BL}}^2\\Delta\\rho$   m = " + m_list[0] + "," + m_list[1])
		ax1.grid(axis='both')
		ax1.legend(fontsize=8)
		ax1.set_ylim((-7.5, 35))
	
		title = "m = +/- 3 profile," + " time = {:.1f}".format(dt*number)
		ax1.set_title(title)
		
		# make lower plot
		ax2.plot(ln_r, J1, 'b-', label="m = " + m_list[0])
		ax2.plot(ln_r, J2, 'g-', label="m = " + m_list[1])
		ax2.set_ylabel("$\\rho_J/\\rho$")
		ax2.set_xlabel("$\\ln(r_{BL})$")
		ax2.grid(axis="both")
		ax2.legend(fontsize=8)
		#ax2.set_ylim((-5, 35))
	
		plt.tight_layout()
	
		save_name = save_root_path + frames_dir + "/frame_{:06d}.png".format(number)
		plt.savefig(save_name, transparent=False)
		plt.clf()
		print("saved " + str(save_name))
	
