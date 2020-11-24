import yt
import numpy as np
# from scipy.interpolate import interp1d
# from scipy.optimize import fsolve
from yt import derived_field
import time
# import sys
import matplotlib.pyplot as plt
import math
from yt.units import cm

start_time = time.time()

# load dataset
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
data_sub_dir = "run2.2_KNL_l0_m0_a0.99_Al0"
number = "000595"
dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_" + number + ".3d.hdf5"
ds = yt.load(dataset_path) 
print("loaded data from ", dataset_path)
print("time = ", time.time() - start_time)

# set centre
center = [512.0, 512.0, 0]
L = max(ds.domain_width.v)

# set up parameters
z_position = 0.001	# s position of slice
r_outer_horizon = 0.25	# R_outer = r_+ / 4 ~= 1 / 4 for an extremal Kerr BH
r_min = r_outer_horizon
r_max = 500
N_bins = 128

### derived fields

# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
@derived_field(name = "weighting_field", units = "")
def _rho_E_eff(field, data):
        return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* data["cylindrical_radius"]*(r_max - r_min)*cm)

"""@derived_field(name = "rho_E_eff", units = "")
def _rho_E_eff(field, data):
	return data["rho"]*pow(data["chi"],-3)

@derived_field(name = "rho_J_eff", units = "")
def _rho_J_eff(field, data):
        return data["S_azimuth"]*pow(data["chi"],-3)

@derived_field(name = "rho_J_prime_eff", units = "")
def _rho_J_prime_eff(field, data):
        return data["S_azimuth_prime"]*pow(data["chi"],-3)"""

# make slice 
slice = ds.r[:,:,z_position]
slice.set_field_parameter("center", center)

# make profile
rp_1 = yt.create_profile(slice, "spherical_radius", fields=["phi"], n_bins=128, weight_field="weighting_field", extrema={"spherical_radius" : (r_min, r_max)})

### plot profile
fig, ax1 = plt.subplots()

colours = ['r', 'b']

"""# plot phi
R = rp_1.x.value
r_plus = 1 + math.sqrt(1 - 0.99**2)
r_BL = R*(1 + r_plus/(4*R))**2
r_star = r_BL + np.log(r_BL)
r_3_4 = r_BL**(3.0/4)
ax1.plot(np.log(r_BL), rp_1["phi"].value, colours[0] + '-')
ax1.set_xlabel("$\\ln(r_{BL})$")
ax1.set_ylabel("$\\phi$")
#ax1.set_ylim((-0.5, 0.5))"""

# plot ln(phi)
R = rp_1.x.value
r_plus = 1 + math.sqrt(1 - 0.99**2)
r_BL = R*(1 + r_plus/(4*R))**2
ln_r_BL = np.log(r_BL)

phi = rp_1["phi"].value
ln_min = 0.00000001
ln_phi = np.log(np.abs(phi) + ln_min)

A = -0.3
B = -0.75

test_line = A + B*ln_r_BL

ax1.plot(ln_r_BL, ln_phi, colours[0] + '-', label="$\\ln(|\\phi|+${:f}$)$".format(ln_min))
ax1.plot(ln_r_BL, test_line, 'k--', label=str(A) + " + " + str(B) + "x")
plt.legend()
ax1.set_xlabel("$\\ln(r_{BL})$")
# ax1.set_ylabel("$\\ln(|\\phi|+0.000001$")
ax1.set_ylim((-3, -0.7))
plt.grid('both')

# plot angular momentum
""" ax2 = ax1.twinx()
ax2.plot(rp.x.value, rp["S_azimuth"].value/rp["rho"].value, colours[1] + '-')
ax2.tick_params(axis='y', colors=colours[1])
ax2.set_ylabel("$\\rho_J \\; / \\;\\rho$", color=colours[1])
ax2.set_ylim((-1.0, 0)) """

dt = 0.25
title = data_sub_dir + " time = {:.1f}".format(int(number)*dt) 
plt.title(title)
fig.tight_layout()

save_name = "plots/" + data_sub_dir + "_" + number + "_ln_phi_profile.png"
plt.savefig(save_name, transparent=False)

