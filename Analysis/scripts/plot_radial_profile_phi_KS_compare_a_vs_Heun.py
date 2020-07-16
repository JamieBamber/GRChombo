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
a_dirs["0"] = "run0067_KNL_l0_m0_a0_Al0_mu1_M1_KerrSchild"
a_dirs["0.7"] = "run0079_KNL_l0_m0_a0.7_Al0_mu1_M1_KerrSchild"
a_dirs["0.99"] = "run0068_KNL_l0_m0_a0.99_Al0_mu1_M1_KerrSchild"

number = 1250
dt = 0.5
t = number*dt
lin_or_log=True

# choose a values to plot
a_list = ["0", "0.7", "0.99"]

# set centre
center = [512.0, 512.0, 0]

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
Kerrlib.Rfunc.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_bool, ctypes.c_double, ctypes.c_double]
Kerrlib.Rfunc.restype = ctypes.c_double

def Stationary_sol_KS(r, A, a, phase, ingoing, t):
        # double M, double mu, double omega, double a, int l, int m, bool ingoing, bool KS_or_BL, double t, double r
        sol = np.zeros(r.size)
        omega = mu
        r_plus = M*(1 + np.sqrt(1 - a*a))
        for i in range(0, r.size):
                if (r[i]<=r_plus):
                        sol[i] = 0
                else:
                     	sol[i] = Kerrlib.Rfunc(M, mu, omega, a, 0, 0, ingoing, True, t - 2*np.pi*phase/omega, r[i])
        sol = np.abs(A)*sol
        return sol
	
### plot phi profiles vs r_BS
colours = ['b-', 'r-', 'g-']
colours2 = ['k--', 'm--', 'c--']
# make  plot 

for i in range(0, len(a_list)):
	a = float(a_list[i])
	r_plus = M*(1 + math.sqrt(1 - a**2))
	r_minus = M*(1 - math.sqrt(1 - a**2))
	t, r, phi = get_chombo_data(a_list[i])
	if lin_or_log:
		x = r/M
	else:
		x = np.log10(r/M)	
	plt.plot(x, phi, colours[i], markersize=2, label="a = " + a_list[i])
	###
	# --- fit stationary solution(s)
	if (a<0.9):
		A0 = 7.9
		def Stationary_sol_KS_fit(r, A, phase):
			print("testing A={:.2f} phase={:.2f}".format(A, phase))
			return Stationary_sol_KS(r, A, a, phase, True, t)
		popt, pconv = curve_fit(Stationary_sol_KS_fit, r, phi, p0=(A0, 0))
		phi_fitted = Stationary_sol_KS_fit(r, popt[0], popt[1])
		A = popt[0]
		phase = popt[1]		
		plt.plot(x, phi_fitted, colours2[i], linewidth=1, label="KS stat. sol., a={:.2f}, amplitude={:.2f} phase={:.2}".format(a, A, phase))		
plt.ylabel("$\\phi_{00}/\\phi_0$")
plt.legend(fontsize=8)
plt.xlim((0, 100))
#plt.ylim((-7.5, 7.5))
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
