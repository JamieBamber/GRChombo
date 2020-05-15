import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
import ctypes

start_time = time.time()

# set up parameters 
data_root_path = "../data/Circular_Extraction_data/"
run_number = "1"
mu_str = "1"
mu = float(mu_str)
subdir = "run000{:s}_FlatScalar_mu{:s}_G0".format(run_number, mu_str)
variable = "phi"
scale = "linear"
number = 1004
file_name_root = subdir + "_" + variable + "_" + scale
colours = ["r", "b", "b", "m"]
styles = ["-", "--", "-."]
time = 0

### get data and plot profile for each a and each lm

log_x = False

file_name = file_name_root + "_n{:06d}".format(number) + ".dat"
dataset_path = data_root_path + file_name
data = np.genfromtxt(dataset_path, skip_header=1)
time = data[1, 0]
R = data[0,1:]
phi = data[1, 1:]

### Kerr-Schild stationary solution

BH_initial_mass = 0.488489232
M_initial = BH_initial_mass*2
seperation = 2*6.10679
BH_initial_p = 0.0841746
J_initial = BH_initial_p*seperation
a_guess = 0.7 #J_initial/(M_guess**2)
M_guess = 0.9
print("M_guess = ", M_guess)
print("a_guess = ", a_guess)
print("R[0] = ", R[0])

Kerrlib = ctypes.cdll.LoadLibrary('/home/dc-bamb1/GRChombo/Source/utils/KerrBH_Rfunc_lib.so')
Kerrlib.Rfunc.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_bool, ctypes.c_double, ctypes.c_double]
Kerrlib.Rfunc.restype = ctypes.c_double

def Stationary_sol_KS(R, A, M, a, phase, ingoing):
	# double M, double mu, double omega, double a, int l, int m, bool ingoing, bool KS_or_BL, double t, double r
	r = np.sqrt((a*M)**2 + R**2)
	sol = np.zeros(r.size)
	omega = mu
	t = time
	r_plus = M*(1 + np.sqrt(1 - a*a))
	for i in range(0, r.size):
		if (r[i]<=r_plus):
			sol[i] = 0
		else:
			sol[i] = Kerrlib.Rfunc(M, mu, omega, a, 0, 0, ingoing, True, t - 2*np.pi*phase/omega, r[i])
	sol = np.abs(A)*sol
	return sol
	
def a_func(a_param):
	return 0.5*(1 + np.tanh(a_param))
	#return 1 - np.exp(-a_param)

def M_func(M_param):
	return M_initial*0.5*(1 + np.tanh(M_param))

#A = 18

def Stationary_sol_KS_fit_ingoing(R, M_param, a_param, Ain, phase_in):
	a = a_func(a_param)
	M = M_func(M_param)
	print("testing M, a, Ain, phase_in = {:.2f},{:.2f},{:.2f},{:.2f}".format(M, a, Ain, phase_in))
	result = Stationary_sol_KS(R, Ain, M, a, phase_in, True) #+ out_factor*Stationary_sol_KS(R, Aout, M, a, phase_out, False)
	return result

def Stationary_sol_KS_fit(R, M_param, a_param, Ain, Aout, phase_in, phase_out):
	a = a_func(a_param)
	M = M_func(M_param)
	print("testing M, a, Ain, Aout, phase_in, phase_out = {:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}".format(M, a, Ain, Aout, phase_in, phase_out))
	result = Stationary_sol_KS(R, Ain, M, a, phase_in, True) + Stationary_sol_KS(R, Aout, M, a, phase_out, False)
	return result
	
# fit KS solution to data
R_fit = R[5:]
phi_fit = phi[5:]
fit_ingoing_only=True

plt.plot(R, phi, 'r-', label="numerical results")
if fit_ingoing_only:
	popt, pconv = curve_fit(Stationary_sol_KS_fit_ingoing, R_fit, phi_fit, p0=(2, 1, 45, 4))
	M = M_func(popt[0])
	a = a_func(popt[1])
	Ain = popt[2]
	phase_in=popt[3]
	phi_sol_in = Stationary_sol_KS(R, Ain, M, a, phase_in, True)
	plt.plot(R, phi_sol_in, 'b--', label="fitted stat. solution (ingoing), A={:.2f}, M={:.2f}, a={:.2f}, phase={:.2f}".format(Ain, M, a, phase_in)) 
else:
	popt, pconv = curve_fit(Stationary_sol_KS_fit, R_fit, phi_fit, p0=(4, 2, 5, 10, 0, 0))
	M = M_func(popt[0])
	a = a_func(popt[1])
	Ain = popt[2]
	Aout = popt[3]
	phase_in=popt[4]
	phase_out = popt[5]
	phi_sol_in = Stationary_sol_KS(R, Ain, M, a, phase_in, True)
	plt.plot(R, phi_sol_in, 'g-', label="fitted stat. solution (ingoing), A={:.2f}, M={:.2f}, a={:.2f}, phase={:.2f}".format(Ain, M, a, phase_in)) 
	phi_sol_out = Stationary_sol_KS(R, Aout, M, a, phase_out, False)
	print("max phi_sol_out = ", np.max(phi_sol_out))
	plt.plot(R, phi_sol_out, 'c-', label="fitted stat. solution (outgoing), A={:.2f}, M={:.2f}, a={:.2f}, phase={:.2f}".format(Aout, M, a, phase_out)) 
	phi_sol = Stationary_sol_KS_fit(R, popt[0], popt[1], Ain, Aout, phase_in, phase_out)
	plt.plot(R, phi_sol, 'b--', label="fitted stat. solution") 

def phi_test(colour, M_, a_):
	def Stationary_sol_KS_fit_ingoing_A_phase_only(R, Ain, phase_in):
		print("M, a = {:.2f},{:.2f}, testing A, phase = {:.2f},{:.2f}".format(M_, a_, Ain, phase_in))
		result = Stationary_sol_KS(R, Ain, M_, a_, phase_in, True)
		return result
	popt, pconv = curve_fit(Stationary_sol_KS_fit_ingoing_A_phase_only, R_fit, phi_fit, p0=(40, 0))
	phi_test = Stationary_sol_KS(R, popt[0], M_, a_, popt[1], True)
	plt.plot(R, phi_test, colour, label="stat. sol. (ingoing), A={:.2f}, M={:.2f}, a={:.2f}, phase={:.2f}".format(popt[0], M_, a_, popt[1]))

phi_test('c-.', M_initial, 0.82)

plt.legend(fontsize=8)
plt.xlabel("$R$")
plt.ylabel("$\\phi$")
plt.grid(axis='both')
plt.ylim((-30, 30))
plt.xlim((0, 25))
dt = 0.5
title = "Binary BH Scalar Field profile, z=0, $\\mu={:.2}$, time = {:.1f}".format(mu, time) 
plt.title(title)
plt.tight_layout()
save_name =  "../plots/BBHSF_" + subdir + "_phi_profile_mode_t={:.1f}.png".format(time)
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
