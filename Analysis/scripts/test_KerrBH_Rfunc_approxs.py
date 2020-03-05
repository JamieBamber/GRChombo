import numpy as np
import ctypes
import matplotlib.pyplot as plt
import sys
import cmath

# define true radial solution function
M = 1
mu = 0.4
omega = 0.6
k = cmath.sqrt(omega**2 - mu**2)
a = 0
l = 0
m = 0

Kerrlib = ctypes.cdll.LoadLibrary('/home/dc-bamb1/GRChombo/Source/utils/KerrBH_Rfunc_lib.so')
Kerrlib.Rfunc.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_bool, ctypes.c_double]
Kerrlib.Rfunc.restype = ctypes.c_double

r_plus = M*(1 + np.sqrt(1 - a**2))
r_minus = M*(1 - np.sqrt(1 - a**2))
ln_r = np.linspace(-20, 0, 128) # = ln(r - r_plus)
r_BL = np.exp(ln_r) + r_plus
large_r = np.linspace(r_plus+1, 50, 256)
r = np.concatenate((r_BL, large_r))
#r_star = r_BL + 2*(r_plus*np.log(r_BL - r_plus) - r_minus*np.log(r_BL - r_minus))/(r_plus - r_minus)
r_star = r + np.log(r - r_plus)

def True_stationary_Rfunc(index, reality, r):
	sol = np.zeros(r.size)
	factor = 1
	for i in range(0, r.size):
		sol[i] = factor*Kerrlib.Rfunc(M, mu, omega.real, omega.imag, a, l, m, index, reality, r[i])
	sol = sol/np.max(np.abs(sol))
	return sol

def test_solution(r_star, k, omega):
	result = np.zeros(r_star.size)
	for i in range(0,r_star.size):
		if r_star[i] <= 0:
			result[i] = np.cos(2*M*omega.real*(r_star[i]))/(1 + 0.1*np.exp(r_star[i]))
		elif r_star[i] > 0:
			result[i] = np.cos(2*M*k.real*(r_star[i]))/(2 + r_star[i])
	return result

#def test_r

H1real = True_stationary_Rfunc(True, True, r)
H1imag = True_stationary_Rfunc(True, False, r)
approx = test_solution(r_star, k, omega)

plt.plot(r_star, H1real, "r-", label="1st stationary solution (real part)")
plt.plot(r_star, H1imag, "g-", label="1st stationary solution (imag part)")
plt.plot(r_star, 2.0/r, "b--", label=" 1/r ")
plt.plot(r_star, -2.0/r, "b--")
plt.plot(r_star, approx, "k-", label="approximation matching to asymptotic limits")
plt.title("$\\mu=${:.1f} k={:.3f} a={:.1f} l={:d} m={:d}".format(mu, k, a, l, m))
plt.xlabel("$r_*$")
plt.ylabel("solutions")
plt.ylim((-2, 2))
plt.legend()
save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/"
save_name = "test_KerrBH_Rfunc_approxs.png"
plt.savefig(save_root_path + save_name)
print("saved plot as " + save_root_path + save_name)
plt.clf()

plt.plot(r_star, r, "r-", label="r")
plt.xlabel("$r_*$")
plt.ylim((-2, 25))
