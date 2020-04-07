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
from scipy.optimize import curve_fit
import ctypes

start_time = time.time()

# data directories
IsoKerr = "run0022_KNL_l0_m0_a0_Al0_mu1_M1_correct_Ylm"
KerrSchild = "run0022_KNL_l0_m0_a0_Al0_mu1_M1_KerrSchild" 

#
z_position = 0.001	# z position of slice
number = 885
dt = 0.25
t = number*dt

# set centre
center = [512.0, 512.0, 0]

# set up parameters
N_bins = 513

#
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"

# define stationary radial solution function
"""M = 1
mu = 0.4
omega = 0.4
Kerrlib = ctypes.cdll.LoadLibrary('/home/dc-bamb1/GRChombo/Source/utils/KerrBH_Rfunc_lib.so')
Kerrlib.Rfunc.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_bool, ctypes.c_double]
Kerrlib.Rfunc.restype = ctypes.c_double

def true_stationary_phi(x, C1, C2):
		# x = ln(r - r_plus)
		r_BL = r_plus + np.exp(x)
		sol1 = np.zeros(r_BL.size)
		sol2 = np.zeros(r_BL.size)
		for i in range(0, r_BL.size):
        		sol1[i] = 100*Kerrlib.Rfunc(M, mu, omega, float(a), 0, 0, True, True, r_BL[i])
        		sol2[i] = 100*Kerrlib.Rfunc(M, mu, omega, float(a), 0, 0, True, False, r_BL[i])
		return C1*sol1 + C2*sol2
	popt, pcov = curve_fit(true_stationary_phi, lnr, phi)
	lnr_fitted = np.linspace(np.min(lnr), np.max(lnr), 256) 
	fitted_phi = true_stationary_phi(lnr_fitted, popt[0], popt[1])
	plt.plot(lnr_fitted, fitted_phi, "k-", label="fitted stationary solution, R1={:.2f} I1={:.2f} a ={:s}".format(popt[0], popt[1], a_list[i]
"""

def get_data(data_sub_dir, number, R_min, R_max):
	dsi = yt.load(data_root_path + "/" + data_sub_dir + "/KerrSFp_{:06d}.3d.hdf5".format(number))
	print("loaded dataset number " + str(number) + " for " + data_sub_dir) 
	slice = dsi.r[:,:,z_position]
	slice.set_field_parameter("center", center)
	# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
	@derived_field(name = "weighting_field", units = "", force_override=True)
	def _weighting_field(field, data):
	        return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* data["cylindrical_radius"]*(R_max - R_min)*cm)
	rp = yt.create_profile(slice, "cylindrical_radius", fields=["phi"], n_bins=128, weight_field="weighting_field", extrema={"cylindrical_radius" : (R_min, R_max)})
	phi = rp["phi"].value
	R = rp.x.value
	print("made profile")
	return (R, phi)

R1, phi1  = get_data(IsoKerr, number, 0.5, 100)
R2, phi2  = get_data(KerrSchild, number, 2.0, 100)
print("got profiles")

# 
r_plus = 2
r1 = R1*(1 + r_plus/(4*R1))**2
r2 = R2

def r_star(r):
	r_s = 2
	return r/r_s + np.log(r/r_s - 1)

### plot phi profiles vs r
plt.plot(r_star(r1), phi1, 'r-', label="Isotropic Kerr")
plt.plot(r_star(r2), phi2, 'b-', label="Kerr Schild")
plt.xlabel("$r_{*}$")
plt.ylabel("$\\phi$")
plt.legend(fontsize=8)
#plt.ylim((-5, 35))
title = "$\\phi$ profile, $\\mu$=$\\omega$=$M$=1 a=l=m=0 time={:.1f}".format(t) 
plt.title(title)
plt.grid(axis="both")
plt.tight_layout()
save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/" 
save_name = "phi_profile_r_star_IsoKerr_vs_KerrSchild_t={:.2f}.png".format(t)
save_path = save_root_path + save_name
plt.savefig(save_path, transparent=False)
plt.clf()
print("saved " + str(save_path))

