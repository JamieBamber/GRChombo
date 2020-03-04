import numpy as np
import ctypes
import matplotlib.pyplot as plt
import sys

# define true radial solution function
M = 1
mu = 0.4
k = 0.1
omega = np.sqrt(mu**2 + k**2)
a = 0
l = 0
m = 0
Kerrlib = ctypes.cdll.LoadLibrary('/home/dc-bamb1/GRChombo/Source/utils/KerrBH_Rfunc_lib.so')
Kerrlib.Rfunc.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_bool, ctypes.c_double]
Kerrlib.Rfunc.restype = ctypes.c_double

r_plus = M*(1 + np.sqrt(1 - a**2))

ln_r = np.linspace(-5, 5)
r_BL = np.exp(ln_r) + r_plus

def True_stationary_Rfunc(index, reality, r):
	sol = np.zeros(r.size)
	factor = 1
	for i in range(0, r.size):
		sol[i] = factor*Kerrlib.Rfunc(M, mu, omega, a, l, m, index, reality, r[i])
		print(sol[i])
	sol = sol/sol[0]
	return sol

H1real = True_stationary_Rfunc(True, True, r_BL)
H1imag = True_stationary_Rfunc(True, False, r_BL)
H2real = True_stationary_Rfunc(False, True, r_BL) 
H2imag = True_stationary_Rfunc(False, False, r_BL)

plt.plot(ln_r, H1real, "r-", label="1st stationary solution (real part)")
plt.plot(ln_r, H2real, "b-", label="2nd stationary solution (real part)")
plt.plot(ln_r, H1imag, "g--", label="1st stationary solution (imag part)")
plt.plot(ln_r, H2imag, "c--", label="2nd stationary solution (imag part)")
plt.title("$\\mu=${:.1f} $\\omega=${:.1f} a={:.1f} l={:d} m={:d}".format(mu, omega, a, l, m))
plt.xlabel("$\\ln(r_{BL} - r_+)$")
plt.ylabel("true stationary solutions")
plt.ylim((-2, 2))
plt.legend()
save_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/"
save_name = "test_KerrBH_Rfunc.png"
plt.savefig(save_root_path + save_name)
print("saved plot as " + save_root_path + save_name)
plt.clf()
