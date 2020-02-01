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
m_dirs["2_L=2048"] = "run25_KNL_L_2048_fixed_l0_m2_a0.99_Al0_M1"

number = 260
dt = 5*0.25

# choose m values to plot
m_list = ["2", "2_L=2048", "-2"]
label_list = ["m=2 L=1024", "m=2 L=2048", "m=-2 L=1024"]
data_sub_dirs = []
for m in m_list:
	data_sub_dirs.append(m_dirs[m])

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

# load datasets
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
ds0 = yt.load(data_root_path + "/" + data_sub_dirs[0] + "/KerrSFp_{:06d}.3d.hdf5".format(0))
dsi = yt.load(data_root_path + "/" + data_sub_dirs[0] + "/KerrSFp_{:06d}.3d.hdf5".format(5*number))
print("loaded data from ", data_sub_dirs[0])
dsi2 = yt.load(data_root_path + "/" + data_sub_dirs[1] + "/KerrSFp_{:06d}.3d.hdf5".format(5*number))
ds02 = yt.load(data_root_path + "/" + data_sub_dirs[1] + "/KerrSFp_{:06d}.3d.hdf5".format(0))
print("loaded data from ", data_sub_dirs[1])
print("time = ", time.time() - start_time)

def make_profile(ds):
	slice = ds.r[:,:,z_position]
	L = ds.domain_width.v[0]
	print(L)
	center = [0.5*L, 0.5*L, 0]
	slice.set_field_parameter("center", center)
	rp = yt.create_profile(slice, "cylindrical_radius", fields=["rho", "S_azimuth"], n_bins=N_bins, weight_field="weighting_field", extrema={"cylindrical_radius" : (r_min, r_max)})
	rho = rp["rho"].value
	rho_J = rp["S_azimuth"].value
	J = rho_J/rho
	R = rp.x.value
	print("made profile")
	return (R, rho, J)

def get_data(m):
	ds0 = yt.load(data_root_path + "/" + m_dirs[m] + "/KerrSFp_{:06d}.3d.hdf5".format(0))
	dsi = yt.load(data_root_path + "/" + m_dirs[m] + "/KerrSFp_{:06d}.3d.hdf5".format(int(5*number)))
	print("loaded data from ", m_dirs[m])
	R, rho0 = make_profile(ds0)[0:2]
	rho, J  = make_profile(dsi)[1:3]
	delta_rho = rho - rho0	
	return (R, delta_rho, J)

### plot delta rho profile vs r_BS

fig, ax = plt.subplots(nrows=2, sharex=True)
fig.subplots_adjust(hspace=0)
ax1, ax2 = ax
colours = ['r-', 'g-', 'm--']

R, delta_rho1, J1 = get_data(m_list[0])
delta_rho_list = [delta_rho1]
J_list = [J1]
for i in range(1, len(m_list)):
	delta_rho, J = get_data(m_list[i])[1:3]
	delta_rho_list.append(delta_rho)
	J_list.append(J)

#
r_BL = R*(1 + r_plus/(4*R))**2
r = r_BL
ln_r = np.log(r)

# make upper plot 
for i in range(0, len(m_list)):
	ax1.plot(ln_r, (r**2)*delta_rho_list[i], colours[i], label=label_list[i])
ax1.set_ylabel("${r_{BL}}^2\\Delta\\rho$")
ax1.grid(axis='both')
ax1.legend(fontsize=8)
ax1.set_ylim((-5, 35))

title = "m = +/- 2 profile, test B.Cs" + " time = {:.1f}".format(dt*number) 
ax1.set_title(title)

# make lower plot
for i in range(0, len(m_list)):
	ax2.plot(ln_r, J_list[i], colours[i], label=label_list[i])
ax2.set_ylabel("$\\rho_J/\\rho$")
ax2.set_xlabel("$\\ln(r_{BL})$")
ax2.grid(axis="both")
ax2.legend(fontsize=8)
#ax2.set_ylim((-5, 35))

plt.tight_layout()

save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/" 
save_name = save_root_path + "m=plus_minus_2_delta_rho_and_J_profile_number={:d}_test_BCs.png".format(number)
plt.savefig(save_name, transparent=False)
plt.clf()
print("saved " + str(save_name))

