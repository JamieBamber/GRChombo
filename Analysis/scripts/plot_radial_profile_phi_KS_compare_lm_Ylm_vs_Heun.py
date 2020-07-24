import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math
import ctypes
from scipy.optimize import curve_fit
start_time = time.time()

# set up parameters 
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Ylm_integration_data/"
file_names = {}
a_list = ["0", "0.99"]
file_names["0"] = "run0080_KNL_l1_m1_a0_Al0_mu0.4_M1_KerrSchild"
file_names["0.99"] = "run0071_KNL_l1_m1_a0.99_Al0_mu0.4_M1_KerrSchild"
#lm_list = [(0, 0), (1, 1) (2, 0), (2, 2), (3, 1), (3, 3), (4, 0)]
lm_list = [(1, 1)]
number = 1085
mu = 0.4
M = 1
phi0 = 0.1
lin_or_log = True
colours = ["r", "b", "g", "c", "m", "y", "k"]
styles = ["-", "--"]
time = 0

log_y = False

### 

Kerrlib = ctypes.cdll.LoadLibrary('/home/dc-bamb1/GRChombo/Source/utils/KerrBH_Rfunc_lib.so')
Kerrlib.Rfunc.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_bool, ctypes.c_double, ctypes.c_double]
Kerrlib.Rfunc.restype = ctypes.c_double

def Stationary_sol_KS(r, A, a, l, m, phase, ingoing):
        # double M, double mu, double omega, double a, int l, int m, bool ingoing, bool KS_or_BL, double t, double r
        sol = np.zeros(r.size)
        omega = mu
        t = time
        r_plus = M*(1 + np.sqrt(1 - a*a))
        for i in range(0, r.size):
                if (r[i]<=r_plus):
                        sol[i] = 0
                else:
                     	sol[i] = Kerrlib.Rfunc(M, mu, omega, a, l, m, ingoing, True, t - 2*np.pi*phase/omega, r[i])
        sol = np.abs(A)*np.abs(sol)
        return sol

### get data and plot profile for each a and each lm

scale = ""
if (lin_or_log):
	scale = "linear"
else:
	scale = "log"

for i in range(0, len(a_list)):
	a = float(a_list[i])
	r_plus = M*(1 + math.sqrt(1 - a**2))
	file_name = file_names[a_list[i]] + "_phi_Ylm_integral_KS_{:s}_n{:06d}_l={:d}_m={:d}.dat"
	dataset_path = data_root_path + file_name
	# generate phi data
	for j in range(0, len(lm_list)):
		l, m = lm_list[j]
		data = np.genfromtxt(dataset_path.format(scale, number, l, m), skip_header=1)
		time = data[1, 0]
		r = data[0,1:]/M
		phi = data[1, 1:]
		if (lin_or_log):
        		x = r
		else:
	     		x = np.log10(r)
		# plot phi
		if log_y:
			y = np.log10(phi/phi0)
		else:
			y = phi/phi0
		plt.plot(x, y, colours[i] + styles[j], label="l={:d} m={:d} mode a={:.2f}".format(l, m, a))
		### fit stationary solution to the a=0.99 case 
		if (a==0.0):
			def Stationary_sol_KS_fit(r, A, phase):
				print("testing A={:.2f} phase={:.2f}".format(A, phase))
				return Stationary_sol_KS(r, A, a, l, m, phase, True)
			popt, pconv = curve_fit(Stationary_sol_KS_fit, r*M, phi, p0=(10, 0))
			A = popt[0]
			phase = popt[1]
			phi_fitted = Stationary_sol_KS_fit(r, A, phase)
			if log_y:
        			y = np.log10(phi_fitted/phi0)
			else:
        			y = phi_fitted/phi0
			plt.plot(x, y, "k--", label="fitted Heun sol. A={:.2f} phase={:.2f} l={:d} m={:d} a={:.2f}".format(A, phase, l, m, a))	
plt.legend(fontsize=8)
if log_y:
	plt.ylabel("$\\log_{10}(\\phi_{lm}/\\phi_0)$")
else:
	plt.ylabel("$|\\phi_{lm}|/\\phi_0$")
if (lin_or_log):
	xlabel_ = "$r_{KS}/M$"
else:
	xlabel_ = "$\\log_{10}(r_{KS}/M)$"
plt.xlabel(xlabel_)
dt = 0.5
a_max = np.max([float(a_str) for a_str in a_list])
r_plus_min = 1 + np.sqrt(1 - a_max**2)
print("r_plus_min = ", r_plus_min)
if (lin_or_log) :
	plt.xlim((r_plus_min, 100))
else :
	plt.xlim(left=np.log10(r_plus_min))
title = "$\\phi_{lm}$" + " profile KerrSchild M=1 $\\mu$={:.1f}, time = {:.1f}".format(mu, time) 
plt.title(title)
plt.legend(fontsize=8)
plt.tight_layout()
save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/KerrSchild_M{:.1f}_mu{:.1f}_Ylm_l=m=1_phi_{:s}_t={:.1f}_plot_vs_Heun.png".format(M, mu, scale, time)
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
