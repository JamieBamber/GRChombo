import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
import ctypes

start_time = time.time()

# set up parameters 
data_root_path = "../data/SphericalPhiData/"
subdir = "run0004_FlatScalar_mu0.4_G0"
variable = "phi"
scale = "log"
number = 595
file_name_root = subdir + "_" + variable + "_" + scale
mu = 0.4
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
Kerrlib.Rfunc.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_bool, ctypes.c_double]
Kerrlib.Rfunc.restype = ctypes.c_double

def HeunC(index, reality, M, a, omega, r):
        # arguments (M, mu, omega.real, omega.imag, a, l, m, index, reality, r)
        sol = np.zeros(r.size)
        factor = 1
        for i in range(0, r.size):
                sol[i] = factor*Kerrlib.Rfunc(M, mu, omega, 0, a, 0, 0, index, reality, r[i])
        sol = sol/np.max(np.abs(sol))
        return sol

def a_func(a_param):
	return 1 - np.exp(-a_param)

def M_func(M_param):
	return M_initial*0.5*(1 + np.tanh(M_param))

def Stationary_sol_KS(r, A, M, a, phase):
	r_plus = M + M*np.sqrt(1 - a**2);
	r_minus = M - M*np.sqrt(1 - a**2);
	omega = mu
	t = time
	print("testing A,M,a,phase = {:.2f},{:.2f},{:.2f},{:.2f}".format(A, M, a, phase))
	HR = HeunC(0, 0, M, a, omega, r)
	HI = HeunC(0, 1, M, a, omega, r)
	r_factor = 2*M*(r_plus*np.log(r/r_plus - 1) - r_minus*np.log(r - r_minus))/(r_plus - r_minus)
	result = -A*(HR*np.sin(omega*(t-r_factor)-phase) - HI*np.cos(omega*(t-r_factor)-phase))
	return result

def Stationary_sol_KS_fit(r, A, M_param, a_param, phase):
	a = a_func(a_param)
	M = M_func(M_param)
	result = Stationary_sol_KS(r, A, M, a, phase)
	return result
	
# fit KS solution to data
popt, pconv = curve_fit(Stationary_sol_KS_fit, R, phi, p0=(55, 1, 2, -1))
plt.plot(R, phi, 'r-', label="numerical results")
A = popt[0]
M = M_func(popt[1])
a = a_func(popt[2])
phase=popt[3]
print("A={:.2f}, M={:.2f}, a={:.2f}, phase={:.2f}".format(A, M, a, phase))
phi_fit = Stationary_sol_KS_fit(R, popt[0], popt[1], popt[2], popt[3])
plt.plot(R, phi_fit, 'g--', label="fitted stationary solution, A={:.2f}, M={:.2f}, a={:.2f}, phase={:.2f}".format(A, M, a, phase)) 
def phi_test(colour, A_, M_, a_, phase_):
	phi_test = Stationary_sol_KS(R, A_, M_, a_, phase_)
	print("testing A,M,a,phase = {:.2f},{:.2f},{:.2f},{:.2f}".format(A_, M_, a_, phase_))
	plt.plot(R, phi_test, colour, label="stat. sol., A={:.2f}, M={:.2f}, a={:.2f}, phase={:.2f}".format(A_, M_, a_, phase_))
phi_test('c-.', 51.2, M_initial, 0.83, -0.94)
plt.legend(fontsize=8)
plt.xlabel("$R$")
plt.ylabel("$\\phi$")
plt.grid(axis='both')
#plt.ylim((-0.5, 0.5))
dt = 0.5
title = "Binary BH Scalar Field profile $Y^0_0$ mode, $\\mu={:.2}$, time = {:.1f}".format(mu, time) 
plt.title(title)
plt.tight_layout()
save_name =  "../plots/BBHSF_" + subdir + "_phi_Y00_mode_t={:.1f}.png".format(time)
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
