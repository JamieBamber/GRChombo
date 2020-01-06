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

number = 300
dt = 5*0.25

# choose m values to plot
m_list = ["2", "-2"]
data_sub_dirs = []
for m in m_list:
	data_sub_dirs.append(m_dirs[m])

# root directory for saving 
movie_name = "m=plus_minus_2_delta_rho_profile_movie"
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
def _rho_E_eff(field, data):
        return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* data["cylindrical_radius"]*(r_max - r_min)*cm)

# load datasets
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
ds0 = yt.load(data_root_path + "/" + data_sub_dirs[0] + "/KerrSFp_{:06d}.3d.hdf5".format(0))
dsi = yt.load(data_root_path + "/" + data_sub_dirs[0] + "/KerrSFp_{:06d}.3d.hdf5".format(5*number))
print("loaded data from ", data_sub_dirs[0])
dsi2 = yt.load(data_root_path + "/" + data_sub_dirs[1] + "/KerrSFp_{:06d}.3d.hdf5".format(5*number))
ds02 = yt.load(data_root_path + "/" + data_sub_dirs[1] + "/KerrSFp_{:06d}.3d.hdf5".format(0))
print("loaded data from ", data_sub_dirs[1])
print("time = ", time.time() - start_time)

def get_profile_data(ds):
	slice = ds.r[:,:,z_position]
	slice.set_field_parameter("center", center)
	rp = yt.create_profile(slice, "spherical_radius", fields=["rho"], n_bins=128, weight_field="weighting_field", extrema={"spherical_radius" : (r_min, r_max)})
	rho = rp["rho"].value
	R = rp.x.value
	return (R, rho)

R, rho01 = get_profile_data(ds0)
rho1 = get_profile_data(dsi)[1]
rho02 = get_profile_data(ds02)[1]
rho2 = get_profile_data(dsi2)[1]

delta_rho1 = rho1 - rho01
delta_rho2 = rho2 - rho02

### plot delta rho profile vs r_BS
r_BL = R*(1 + r_plus/(4*R))**2
r = r_BL
ln_r = np.log(r)

fig, ax = plt.subplots(nrows=2, sharex=True)
fig.subplots_adjust(hspace=0)
ax1, ax2 = ax
colours = ['r-', 'r--']

# make upper plot 
ax1.plot(ln_r, (r**2)*delta_rho1, colours[0], label="m = " + m_list[0])
ax1.set_ylabel("${r_{BL}}^2\\Delta\\rho$   m = " + m_list[0])
ax1.grid(axis='both')
ax1.set_ylim((-5, 35))

title = "m = +/- 2 profile," + " time = {:.1f}".format(dt*number) 
ax1.set_title(title)

# make lower plot
ax2.plot(ln_r, (r**2)*delta_rho2, colours[1], label="m = " + m_list[1])
ax2.set_ylabel("${r_{BL}}^2\\Delta\\rho$   m = " + m_list[1])
ax2.set_xlabel("$\\ln(r_{BL})$")
ax2.grid(axis="both")
ax2.set_ylim((-5, 35))

plt.tight_layout()

save_name = save_root_path + frames_dir + "/frame_{:06d}.png".format(number)
plt.savefig(save_name, transparent=False)
plt.clf()
print("saved " + str(save_name))

