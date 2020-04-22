import yt
from yt import derived_field
from yt.units import cm
import numpy as np
import time
import matplotlib.pyplot as plt
import math
from os import makedirs
import sys
#from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import ctypes

start_time = time.time()

a_dirs = {}
a_dirs["0"] = "run0022_KNL_l0_m0_a0_Al0_mu1_M1_correct_Ylm"

z_position = 0.001	# z position of slice
number = 1460
dt = 0.25
t = number*dt

# choose a values to plot
a_list = ["0"]

# set centre
center = [512.0, 512.0, 0]

# set up parameters
R_max = 200
N_bins = 67

#
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"

M = 1
mu = 1
omega = 1
phi0 = 0.1

sphere_or_slice = False
# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
if sphere_or_slice:
        @derived_field(name = "weighting_field", units = "")
        def _weighting_field(field, data):
                return data["cell_volume"].in_base("cgs") * N_bins / (2*math.pi* (data["spherical_radius"]**2)*cm)
elif not sphere_or_slice:
        @derived_field(name = "weighting_field", units = "")
        def _weighting_field(field, data):
                return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*math.pi* (data["cylindrical_radius"])*cm)

def get_data(a_str, number):
	a = float(a_str)
	r_plus = 1 + math.sqrt(1 - float(a)**2)
	R_min = r_plus/4*(1.01)	
	data_sub_dir = a_dirs[a_str]
	dsi = yt.load(data_root_path + "/" + data_sub_dir + "/KerrSFp_{:06d}.3d.hdf5".format(number))
	print("loaded dataset number " + str(number) + " for " + data_sub_dir) 
	if sphere_or_slice:
		data = dsi.sphere(center, R_max) - dsi.sphere(center, R_min)
		rp = yt.create_profile(data, "spherical_radius", fields=["phi"], n_bins=N_bins, weight_field="weighting_field", extrema={"spherical_radius" : (R_min, R_max)})
	elif not sphere_or_slice:
		data = dsi.r[:,:,z_position]
		data.set_field_parameter("center", center)
		rp = yt.create_profile(data, "cylindrical_radius", fields=["phi"], n_bins=N_bins, weight_field="weighting_field", extrema={"cylindrical_radius" : (R_min, R_max)})
	phi = rp["phi"].value
	#/(R_max - R_min)
	R = rp.x.value
	print("made profile")
	return (R, phi)

def get_chombo_data(a_str):
	file_name = a_dirs[a_str] + "_phi.dat"
	chombo_data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/SphericalPhiData/"
	dataset_path = chombo_data_root_path + file_name
	data = np.genfromtxt(dataset_path, skip_header=1)
	time = data[1, 0]
	R = data[0,1:]
	phi_integral = data[1, 1:]/(2*np.pi)
	return (time, R, phi_integral) 
	
phi_list = []
R_list = []
for i in range(0, len(a_list)):
	#R, phi = get_data(a_list[i], number)
	t, R, phi = get_chombo_data(a_list[i])
	R_list.append(R)
	phi_list.append(phi)
	print("got profile for a=" + a_list[i], flush=True)
	print("t = ", t)	

# Stationary solution
Kerrlib = ctypes.cdll.LoadLibrary('/home/dc-bamb1/GRChombo/Source/utils/KerrBH_Rfunc_lib.so')
Kerrlib.Rfunc.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_bool, ctypes.c_double]
Kerrlib.Rfunc.restype = ctypes.c_double

def HeunC(index, reality, a, omega, r):
	# arguments (M, mu, omega.real, omega.imag, a, l, m, index, reality, r)
        sol = np.zeros(r.size)
        factor = 1
        for i in range(0, r.size):
                sol[i] = factor*Kerrlib.Rfunc(M, mu, omega, 0, a, 0, 0, index, reality, r[i])
        sol = sol/np.max(np.abs(sol))
        return sol

### plot phi profiles vs r_BS
colours = ['r-', 'b-', 'g-']
colours2 = ['k--', 'm--', 'c--']
# make  plot 

for i in range(0, len(a_list)):
	a = a_list[i]
	r_plus = 1 + math.sqrt(1 - float(a)**2)
	r_minus = 1 - math.sqrt(1 - float(a)**2)
	R = R_list[i][1:]
	phi = phi_list[i][1:]
	r = R*(1 + r_plus/(4*R))**2
	def r_star_func(r):
		return r + ((r_plus**2)*np.log(r - r_plus) - (r_minus**2)*np.log(r - r_minus))/(r_plus - r_minus)	
	r_star = r_star_func(r)
	x = r_star
	plt.plot(x, phi, colours[i], markersize=2, label="a = " + a_list[i])
	###
	# --- fit stationary solution(s)
	r_plot_1 = r_plus + np.exp(np.linspace(r_star[0]/r_plus, 1, 64))
	r_plot_2 = np.linspace(r_plot_1[-1],60,64)[1:]
	r_plot = np.concatenate((r_plot_1,r_plot_2))
	r_star_plot = r_star_func(r_plot)
	A = np.max(np.abs(phi))
	def Stationary_sol(r, phase):
		omega = mu
		HR = HeunC(0, 0, float(a), omega, r)
		HI = HeunC(0, 1, float(a), omega, r)
		result = -A*(HR*np.sin(omega*t-phase) - HI*np.cos(omega*t-phase))
		return result	
	popt, pconv = curve_fit(Stationary_sol, r, phi, p0=(0))
	phi_fit = Stationary_sol(r_plot, popt[0])
	plt.plot(r_star_plot, phi_fit, colours2[i], linewidth=1, label="stationary solution, a={:s}, A={:.2f} phase={:.2}".format(a, A, popt[0]))		
plt.ylabel("$\\phi$")
plt.legend(fontsize=8)
plt.xlim((-20, 60))
plt.ylim((-0.75, 0.75))
title = "$\\Phi$ profile, $M\mu=M\omega=1$ $l=m=0$ time={:.1f}".format(t) 
plt.title(title)
plt.xlabel("$r_*$")
#plt.xlabel("$\\ln(r_{BL} - r_+)$")
#plt.xlabel("$r_* - r_{BL}$")
plt.grid(axis="both")
plt.tight_layout()

save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/" 
save_name = "phi_profile_vs_r_star_compare_Heun_t={:.2f}.png".format(t)
save_path = save_root_path + save_name
plt.savefig(save_path, transparent=False)
plt.clf()
print("saved " + str(save_path))
