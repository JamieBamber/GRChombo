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
a_dirs["0"] = "run0067_KNL_l0_m0_a0_Al0_mu1_M1_KerrSchild_wrong_rho"
a_dirs["0.99"] = "run0068_KNL_l0_m0_a0.99_Al0_mu1_M1_KerrSchild"

z_position = 0.001	# z position of slice
number = 2165
dt = 0.5
t = number*dt
lin_or_log=True

# choose a values to plot
a_list = ["0"]

# set centre
center = [512.0, 512.0, 0]

# set up parameters
R_max = 200
N_bins = 67

#
M = 1
mu = 1
omega = 1
phi0 = 0.1

if lin_or_log:
	scale = "linear"
else:
	scale = "log"

def get_chombo_data(a_str):
	file_name = a_dirs[a_str] + "_phi_{:s}_n{:06d}.dat".format(scale, number)
	data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Y00_integration_data/"
	dataset_path = data_root_path + file_name
	data = np.genfromtxt(dataset_path, skip_header=1)
	time = data[1, 0]
	R = data[0,1:]
	phi = data[1, 1:]/phi0
	return (time, R, phi) 
	
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
	print("sol = ", sol)
	return sol
	
### plot phi profiles vs r_BS
colours = ['b-', 'r-', 'g-']
colours2 = ['k--', 'm--', 'c--']
# make  plot 

for i in range(0, len(a_list)):
	a = a_list[i]
	r_plus = 1 + math.sqrt(1 - float(a)**2)
	r_minus = 1 - math.sqrt(1 - float(a)**2)
	t, r, phi = get_chombo_data(a_list[i])
	if lin_or_log:
		x = r
	else:
		x = np.log10(r)	
	plt.plot(x, phi, colours[i], markersize=2, label="a = " + a_list[i])
	###
	# --- fit stationary solution(s)
	A = np.max(phi)
	def Stationary_sol_KS(r, phase):
		omega = mu
		HR = HeunC(0, 0, float(a), omega, r)
		HI = HeunC(0, 1, float(a), omega, r)
		r_factor = 2*M*(r_plus*np.log(r/r_plus - 1) - r_minus*np.log(r - r_minus))/(r_plus - r_minus) 
		result = -(HR*np.sin(omega*(t-r_factor)-phase) - HI*np.cos(omega*(t-r_factor)-phase))
		result = A*result/np.max(result)
		return result	
	r = r[2:]
	phi = phi[2:]
	x = x[2:]
	#popt, pconv = curve_fit(Stationary_sol_KS, r, phi, p0=(0))
	#popt = [0.0]
	phase = -3.1
	phi_stationary_KS = Stationary_sol_KS(r, phase)
	print("phi_stationary_KS = ", phi_stationary_KS)
	if (a=="0"):
		plt.plot(x, phi_stationary_KS, 'k--', linewidth=1, label="KS stationary solution, a={:s}, A={:.2f} phase={:.2}".format(a, A, phase))		
plt.ylabel("$\\phi_{00}/\\phi_0$")
plt.legend(fontsize=8)
plt.xlim((0, 100))
plt.ylim((-7.5, 7.5))
title = "$\\Phi$ profile, Kerr-Schild coordinates, $M\mu=M\omega=1$ $l=m=0$ time={:.1f}".format(t) 
plt.title(title)
if lin_or_log:
	plt.xlabel("$r_{KS}/M$")
else:
	plt.xlabel("$\\log_{10}(r_{KS}/M)$")
plt.grid(axis="both")
plt.tight_layout()
save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/" 
save_name = "phi_profile_compare_a_vs_Heun_KS_{:s}_t={:.1f}_rmax_100_v2.png".format(scale, t)
save_path = save_root_path + save_name
plt.savefig(save_path, transparent=False)
plt.clf()
print("saved " + str(save_path))
