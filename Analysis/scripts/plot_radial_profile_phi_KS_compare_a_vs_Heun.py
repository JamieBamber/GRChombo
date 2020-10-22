import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
import ctypes

start_time = time.time()

# set up parameters 
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Y00_integration_data/"
file_names = {}
a_list = ["0"]
file_names["0"] = "run0067_KNL_l0_m0_a0_Al0_mu1_M1_KerrSchild"
file_names["0.99"] = "run0068_KNL_l0_m0_a0.99_Al0_mu1_M1_KerrSchild"
number = 1250
mu = 1
M = 1
phi0 = 0.1
lin_or_log = True
colours = ["r-", "b-"]
colours2 = ["k--", "g--"]
time = 0

# Stationary solution
Kerrlib = ctypes.cdll.LoadLibrary('/home/dc-bamb1/GRChombo/Source/utils/KerrBH_Rfunc_lib.so')
Kerrlib.Rfunc.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_bool, ctypes.c_double]
Kerrlib.Rfunc.restype = ctypes.c_double

def HeunC(index, reality, a, mu, omega, r):
	# arguments (M, mu, omega.real, omega.imag, a, l, m, index, reality, r)
	sol = np.zeros(r.size)
	factor = 1
	for i in range(0, r.size):
        	sol[i] = factor*Kerrlib.Rfunc(M, mu, omega, 0, a, 0, 0, index, reality, r[i])
	print("HeunC sol = ", sol)
	return sol
	
### get data and plot profile for each a and each lm

scale = ""
if (lin_or_log):
	scale = "linear"
else:
	scale = "log"

l=2
m=0
for i in range(0, len(a_list)):
	a = float(a_list[i])
	r_plus = M*(1 + np.sqrt(1 - a**2))
	r_minus = M*(1 - np.sqrt(1 - a**2))
	file_name = file_names[a_list[i]] + "_{:s}_{:s}_n{:06d}"
	dataset_path = data_root_path + file_name
	# generate phi data
	data = np.genfromtxt(dataset_path.format("phi", scale, number), skip_header=1)
	time = data[1, 0]
	r = data[0,1:]/M
	phi = data[1, 1:]/phi0
	if (lin_or_log):
        	x = r
	else:
	     	x = np.log10(r)
	# plot phi
	plt.plot(x, phi, colours[i], label="$\\phi$ l=m=0 a={:.2f}".format(a))
	#
	A = 5
	t = 885.0
	def Stationary_sol_KS(r, mu_, phase):
		omega = mu_
		HR = HeunC(0, 0, float(a), mu_, omega, r)
		HI = HeunC(0, 1, float(a), mu_, omega, r)
		r_factor = 2*M*(r_plus*np.log(r/r_plus - 1) - r_minus*np.log(r - r_minus))/(r_plus - r_minus)
		result = -(HR*np.sin(omega*(t-r_factor)-phase) - HI*np.cos(omega*(t-r_factor)-phase))
		result = A*result/np.max(np.abs(result))
		return result
	r_out = np.linspace(2.01, 100, 256)
	#phi_out = r[10:]
	x_out = r_out 
	#popt, pconv = curve_fit(Stationary_sol_KS, r_out, phi_out, p0=(0))
	#popt = [0.0]
	phase = -1.5
	phi_stationary_KS = Stationary_sol_KS(r_out, 0.4, phase)
	print("phi_stationary_KS = ", phi_stationary_KS)
	#if (i==0):
	plt.plot(x_out, phi_stationary_KS, colours2[i], linewidth=1, label="KS stationary solution, mu=0.4, a={:.2f}, A={:.2f} phase={:.2}".format(a, A, phase))
plt.legend(fontsize=8)
plt.ylabel("$\\phi_00/\\phi_0$")
plt.ylim((-6, 6))
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
title = "$\\phi$ profile $Y^0_0$ mode KerrSchild M=1 $\\mu$={:.1f}, time = {:.1f}".format(mu, time) 
plt.title(title)
plt.legend(fontsize=8)
plt.tight_layout()
save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/KerrSchild_M{:.1f}_mu{:.1f}_l0_m0_phi_{:s}_t={:.1f}_plot.png".format(M, mu, scale, time)
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
