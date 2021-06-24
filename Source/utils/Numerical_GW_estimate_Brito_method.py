import numpy as np
import ctypes
import matplotlib.pyplot as plt
import sys
from scipy import special
from math import factorial

# define true radial solution function
M = 1
mu = 1.0
omega = 1.0
a = 0
l = 0
m = 0

#
Kerrlib = ctypes.cdll.LoadLibrary('/cosma/home/dp174/dc-bamb1/GRChombo/Source/utils/KerrBH_Rfunc_general_s.so')
# extern "C" double Rfunc(double M, double mu, double omega, double a, int l, int m, int s, bool ingoing, bool KS_or_BL, double t, double r)
# double *Rfunc_Re, double *Rfunc_Im){
# double *d_Rfunc_dr_Re, double *d_Rfunc_dr_Im, double *dd_Rfunc_ddr_Re, double *dd_Rfunc_ddr_Im
Kerrlib.Rfunc.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_bool, ctypes.c_double, ctypes.c_double,\
ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
Kerrlib.Rfunc.restype = Nonw
#
Heunlib = ctypes.cdll.LoadLibrary('/cosma/home/dp174/dc-bamb1/GRChombo/Source/utils/


# class to hold the output data
class Rfunc_data:
	def __init__(self):
		pass
		# self.Rfunc_Re
		# self.Rfunc_Im

r_plus = M*(1 + np.sqrt(1 - a**2))

ln_r = np.linspace(-2, 10)
r_BL = np.exp(ln_r) + r_plus

# 
def Rfunc(M, mu, omega, a, l, m, s, ingoing, t, r):
	result = Rfunc_data()
	result.Rfunc_Re = np.zeros(r.size)
	result.Rfunc_Im = np.zeros(r.size)
	result.d_Rfunc_dr_Re = np.zeros(r.size)
	result.d_Rfunc_dr_Im = np.zeros(r.size)
	result.dd_Rfunc_ddr_Re = np.zeros(r.size)
	result.dd_Rfunc_ddr_Im = np.zeros(r.size)
	for i in range(0, r.size):
		R_Re = ctypes.c_double()
		R_Im = ctypes.c_double()
		d_R_dr_Re = ctypes.c_double()
		d_R_dr_Im = ctypes.c_double()
		dd_R_ddr_Re = ctypes.c_double()
		dd_R_ddr_Im = ctypes.c_double()
		Kerrlib.Rfunc(M, mu, omega, a, l, m, s, ingoing, False, t, r[i],\
		ctypes.byref(R_Re),ctypes.byref(R_Im),ctypes.byref(d_R_dr_Re),ctypes.byref(d_R_dr_Im),ctypes.byref(dd_R_ddr_Re),ctypes.byref(dd_R_ddr_Im))
		result.Rfunc_Re[i] = R_Re
		result.Rfunc_Im[i] = R_Im
		result.d_Rfunc_dr_Re[i] = d_R_dr_Re
		result.d_Rfunc_dr_Im[i] = d_R_dr_Im
		result.dd_Rfunc_ddr_Re[i] = dd_R_ddr_Re
		result.dd_Rfunc_ddr_Im[i] = dd_R_ddr_Im		
	return result

# Define hydrogen radial wavefunction
def hydrogen_Rfunc(M, mu, n, l, r):
	r0 = M/(M*(M*mu)**2)
	rtilde = r/(r0*(n+l+1))
	Anl = (n+l+1)**(-3/2)*(factorial(n)/(2*(n+l+1)*factorial(n+2*l+1)))**(1/2)
	result = Anl * rtilde**l * np.exp(-rtilde/2.0) * special.genlaguerre(n,2*l+1,rtilde)
	return result

# Define bessel function approximation for the marginally bound radial function
def Bessel_marginal_Rfunc(M, mu, omega, l, r):
	r0 = M/(M*(M*mu)**2)
	rtilde = r/r0
	Bnl = np.sqrt(2/np.pi) * factorial(2*l+1)
	result = Bnl * rtilde**(-1/2) * special.jv(2*l+1,2*np.sqrt(rtilde)) 
	return result

# Define spherical bessel function approximation for the RH function
def bessel_RH_function(M, omega, l, r):
	result = omega*((2*1j*r**2*omega*((l+2)*r-(2*l+5)*M)+(l+1)*(l+2)*(r-2*M)**2-2*r**2*omega**2*(2*M**2-2*M*r+r**2))*special.spherical_jn(l,r*omega)+2*r*omega*(r-2*M)*(2*M+r*(-1-1j*r*omega))*special.spherical_jn(l+1,omega*r))
	return result

def scalar_Rfunc(M, mu, omega, l, r):
	R = Rfunc(M, mu, mu, 0, l, l, 0, ingoing, 0, r)
	return R

# Define the Teukolsky source function
def Teukolsky_22w_source_function(M, omegaR1, omegaR2, Rfunc1, Rfunc2, r):
	R1 = Rfunc1(M, mu, omega, l, r)
	R2 = Rfunc2(M, mu, omega, l, r)
	result = (1/np.sqrt(5))*2*np.pi**(3/2)*(R1.Rfunc_Im(r)*(R2.Rfunc_Im(r)*(8*M**2+2*M*r*(-4-3*1j*r*(omegaR1-omegaR2))+r**2*(r**2*(-omegaR1**2+2*omegaR1*omegaR2+omegaR2**2)+2*1j*r*(omegaR1-omegaR2)+2))-1j*R2.Rfunc_Re(r)*(8*M**2+2*M*r*(-4-3*1j*r*(omegaR1-omegaR2))+r**2*(r**2*(-omegaR1**2+2*omegaR1*omegaR2+omegaR2**2)+2*1j*r*(omegaR1-omegaR2)+2))-r*(2*M-r)*(R2.d_Rfunc_dr_Im(r)*(4*M-2*1j*r**2*(omegaR1+omegaR2)-2*r)-r*(r-2*M)*(R2.dd_Rfunc_ddr_Im(r)-1j*R2.dd_Rfunc_ddr_Re(r))+R2.d_Rfunc_dr_Re(r)*(-4*1j*M-2*r*(r*(omegaR1+omegaR2)-I))))+R1.Rfunc_Re(r)*(-1j*R2.Rfunc_Im(r)*(8*M**2+2*M*r*(-4-3*1j*r*(omegaR1-omegaR2))+r**2*(r**2*(-omegaR1**2+2*omegaR1*omegaR2+omegaR2**2)+2*1j*r*(omegaR1-omegaR2)+2))-R2.Rfunc_Re(r)*(8*M**2+2*M*r*(-4-3*1j*r*(omegaR1-omegaR2))+r**2*(r**2*(-omegaR1**2+2*omegaR1*omegaR2+omegaR2**2)+2*1j*r*(omegaR1-omegaR2)+2))+r*(2*M-r)*(R2.d_Rfunc_dr_Re(r)*(4*M-2*1j*r**2*(omegaR1+omegaR2)-2*r)+r*(2*M-r)*(R2.dd_Rfunc_ddr_Re(r)+1j*R2.dd_Rfunc_ddr_Im(r))+2*R2.d_Rfunc_dr_Im(r)*(2*1j*M+r*(r*(omegaR1+omegaR2)-I))))+r*(2*M-r)*(R2.Rfunc_Im(r)*(R1.d_Rfunc_dr_Im(r)*(4*M-2*1j*r**2*(omegaR1-omegaR2)-2*r)+r*(2*M-r)*(R1.dd_Rfunc_ddr_Im(r)-1j*R1.dd_Rfunc_ddr_Re(r))+2*R1.d_Rfunc_dr_Re(r)*(r*(r*(omegaR2-omegaR1)+I)-2*1j*M))+R2.Rfunc_Re(r)*(2*R1.d_Rfunc_dr_Re(r)*(-2*M+1j*r**2*(omegaR1-omegaR2)+r)-1j*r*(2*M-r)*(R1.dd_Rfunc_ddr_Im(r)-1j*R1.dd_Rfunc_ddr_Re(r))+2*R1.d_Rfunc_dr_Im(r)*(r*(-r*omegaR1+r*omegaR2+I)-2*1j*M))-2*r*(2*M-r)*(R1.d_Rfunc_dr_Im(r)-1j*R1.d_Rfunc_dr_Re(r))*(R2.d_Rfunc_dr_Im(r)-1j*R2.d_Rfunc_dr_Re(r))))
	return result

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
