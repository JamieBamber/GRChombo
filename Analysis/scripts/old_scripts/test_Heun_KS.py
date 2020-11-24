import numpy as np
import time
import sys
from matplotlib import rc
rc('text', usetex=True)
import matplotlib.pyplot as plt
import cmath
import ctypes
from scipy.optimize import curve_fit
start_time = time.time()

### 
Kerrlib = ctypes.cdll.LoadLibrary('/home/dc-bamb1/GRChombo/Source/utils/KerrBH_Rfunc_lib.so')
Kerrlib.Rfunc.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_bool, ctypes.c_double, ctypes.c_double]
Kerrlib.Rfunc.restype = ctypes.c_double

def Heun_sol(r, t, omega, mu, phase):
	# double M, double mu, double omega, double a, int l, int m, bool ingoing, bool KS_or_BL, double t, double r
	sol = np.zeros(r.size)
	r_plus = 2
	for i in range(0, r.size):
     			sol[i] = Kerrlib.Rfunc(1, mu, omega, 0, 0, 0, True, True, t - 2*np.pi*phase/omega, r[i])
	return sol

omega = 0.2
mu = 0.2

def test_sol(r, t, omega, mu, reality):
	if reality:
		sol = r**(-3/4)*np.cos(2*omega*np.sqrt(2*r))
		return sol
	else:
		sol = -r**(-3/4)*np.sin(2*omega*np.sqrt(2*r))
		return sol
			
def plot_graph():
	# plot setup
	ax1 = plt.axes()
	fig = plt.gcf()
	fig.set_size_inches(3.8,3)
	font_size = 10
	title_font_size = 10
	label_size = 10
	legend_font_size = 10
	rc('xtick',labelsize=font_size)
	rc('ytick',labelsize=font_size)
	#	
	r = np.linspace(2,50,400)
	H_real = Heun_sol(r, 0, omega, mu, 0)
	H_imag = Heun_sol(r, 0, omega, mu, -0.25)
	ax1.plot(r, H_real, "k-", label="real part", linewidth=1)
	ax1.plot(r, H_imag, "r-", label="imaginary part", linewidth=1)	
	ax1.plot(r, test_sol(r,0,omega,mu,True), "k--", label="test sol. real part", linewidth=1)
	ax1.plot(r, test_sol(r,0,omega,mu,False), "r--", label="test sol. imag part", linewidth=1)
	ax1.set_ylabel("Heun solution in ingoing EF coordinates", fontsize=label_size)
	xlabel_ = "$r_{BL}/M$"
	plt.xlabel(xlabel_, fontsize=label_size)
	ax1.legend(loc="best", fontsize=legend_font_size)
	plt.xticks(fontsize=font_size)
	plt.yticks(fontsize=font_size)
	title = "Heun solution in EF coordinates" 
	ax1.set_title(title, fontsize=title_font_size)
	plt.tight_layout()
	save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/Heun_sol_EF_coordinates.png"
	print("saved " + save_name)
	plt.savefig(save_name, transparent=False)
	plt.clf()
	
plot_graph()
