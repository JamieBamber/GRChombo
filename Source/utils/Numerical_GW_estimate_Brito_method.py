import numpy as np
import ctypes
import matplotlib.pyplot as plt
import sys
from scipy import special
from math import factorial

# define true radial solution function
M = 1
mu = 0.51
omega = 0.4
a = 0
l = 1
m = 1

#
Kerrlib = ctypes.cdll.LoadLibrary('/cosma/home/dp174/dc-bamb1/GRChombo/Source/utils/KerrBH_Rfunc_general_s.so')
# extern "C" double Rfunc(double M, double mu, double omega, double a, int l, int m, int s, bool ingoing, bool KS_or_BL, double t, double r)
# double *Rfunc_Re, double *Rfunc_Im){
# double *d_Rfunc_dr_Re, double *d_Rfunc_dr_Im, double *dd_Rfunc_ddr_Re, double *dd_Rfunc_ddr_Im
Kerrlib.Rfunc.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_double, ctypes.c_double,\
ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
Kerrlib.Rfunc.restype = None
#
Heunlib = ctypes.cdll.LoadLibrary('/cosma/home/dp174/dc-bamb1/GRChombo/Source/utils/HeunC_function_test.so')
# extern "C" double Rfunc(double M, double mu, double omega, double a, int l, int m, int s, bool ingoing, double r){
Heunlib.Rfunc.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double,\
ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
Heunlib.Rfunc.restype = None
#ctypes.c_double
#
compute_omega_CFlib = ctypes.cdll.LoadLibrary('/cosma/home/dp174/dc-bamb1/GRChombo/Source/utils/omega_QNM_continued_fraction.so')
compute_omega_CFlib.F_func.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double]
compute_omega_CFlib.F_func.restype = ctypes.c_double

# class to hold the output data
class Rfunc_data:
	def __init__(self):
		pass
		# self.Rfunc_Re
		# self.Rfunc_Im

# 
def Rfunc(M, mu, omega, a, l, m, s, sgn_alpha, sgn_beta, KS_or_BL, t, r):
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
		try:	
			Kerrlib.Rfunc(M, mu, np.real(omega), np.imag(omega), a, l, m, s, sgn_alpha, sgn_beta, KS_or_BL, t, r[i],\
			ctypes.byref(R_Re),ctypes.byref(R_Im),ctypes.byref(d_R_dr_Re),ctypes.byref(d_R_dr_Im),ctypes.byref(dd_R_ddr_Re),ctypes.byref(dd_R_ddr_Im))
		except:
			print("Rfunc error")
			R_Re = ctypes.c_double(0.0)
			R_Im = ctypes.c_double(0.0)
			d_R_dr_Re = ctypes.c_double(0.0)
			d_R_dr_Im = ctypes.c_double(0.0)
			dd_R_ddr_Re = ctypes.c_double(0.0)
			dd_R_ddr_Im = ctypes.c_double(0.0)
		result.Rfunc_Re[i] = R_Re.value
		result.Rfunc_Im[i] = R_Im.value
		result.d_Rfunc_dr_Re[i] = d_R_dr_Re.value
		result.d_Rfunc_dr_Im[i] = d_R_dr_Im.value
		result.dd_Rfunc_ddr_Re[i] = dd_R_ddr_Re.value
		result.dd_Rfunc_ddr_Im[i] = dd_R_ddr_Im.value		
	return result

# define Heun func solution without the prefactors
"""def HeunC_func(M, mu, omega, a, l, m, s, ingoing, r):
	result = np.zeros(r.size)
	for i in range(0, r.size):
		result[i] = Heunlib.Rfunc(M, mu, omega, a, l, m, s, ingoing, r[i])
	return result"""

def HeunC_func(M, mu, omega, a, l, m, s, sgn_alpha, sgn_beta, r):
	result = np.zeros(r.size)
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
		Heunlib.Rfunc(M, mu, np.real(omega), np.imag(omega), a, l, m, s, sgn_alpha, sgn_beta, r[i],\
        		ctypes.byref(R_Re),ctypes.byref(R_Im),ctypes.byref(d_R_dr_Re),ctypes.byref(d_R_dr_Im),ctypes.byref(dd_R_ddr_Re),ctypes.byref(dd_R_ddr_Im))
		result.Rfunc_Re[i] = R_Re.value
		result.Rfunc_Im[i] = R_Im.value
		result.d_Rfunc_dr_Re[i] = d_R_dr_Re.value
		result.d_Rfunc_dr_Im[i] = d_R_dr_Im.value
		result.dd_Rfunc_ddr_Re[i] = dd_R_ddr_Re.value
		result.dd_Rfunc_ddr_Im[i] = dd_R_ddr_Im.value
	return result.Rfunc_Re + 1j*result.Rfunc_Im
		
r_test = np.array([2.0001, 5.0, 20.0])
print("HeunC_func(1.0, 0, 1.0, 0, 1, 1, -2, True, [2.01,	5.0, 6.0]) = ", HeunC_func(1.0, 0, 2*mu, 0, 1, 1, -2, 1, 1, r_test))

# Define hydrogen radial wavefunction
def hydrogen_Rfunc(M, mu, omega, n, l, m, r):
	r0 = M/(2*(M*mu)**2)
	Anl = (n+l+1)**(-3/2)*(factorial(n)/(2*(n+l+1)*factorial(n+2*l+1)))**(1/2)
	R = np.zeros(len(r))
	d_R_dr = np.zeros(len(r))
	dd_R_ddr = np.zeros(len(r))
	for i in range(0,len(r)):
		rtilde = r[i]/(r0*(n+l+1))
		R[i] = Anl * rtilde**l * np.exp(-rtilde/2.0) * special.genlaguerre(n,2*l+1,rtilde)
		if n<1:
			d_R_dr[i] = Anl * np.exp(-rtilde/2.0) * rtilde**(l-1) *((2*l*(l+n+1)-r[i]/r0)*special.genlaguerre(n,2*l+1,rtilde))/(2*(l+n+1)**2*r0)
		else:
			d_R_dr[i] = Anl * np.exp(-rtilde/2.0) * rtilde**(l-1) *((2*l*(l+n+1)-r[i]/r0)*special.genlaguerre(n,2*l+1,rtilde)-2*r[i]/r0*special.genlaguerre(n,2*l+2,rtilde))/(2*(l+n+1)**2*r0)
		if n==0:
			dd_R_ddr[i] = Anl*np.exp(-rtilde/2.0)*rtilde**l*(-4*l*(l+1)*r[i]/r0+4*(l-1)*l*(l+1)**2+(r[i]/r0)**2)/(4*(r[i]/r0)**2*(l+1)**2)
		elif n==1:
			dd_R_ddr[i] = Anl*np.exp(-rtilde/2.0)*rtilde**l*(8*l*(l**2-1)*(l+2)**3+6*(l+1)*(l+2)*(r[i]/r0)**2-12*l*(l+1)*(l+2)**2*r[i]/r0-(r[i]/r0)**3)/(4*(r[i]/r0)**2*(l+2)**3)			
		elif n>=2:
			dd_R_ddr[i] = Anl*np.exp(-rtilde/2.0)*rtilde**l*(4*(r[i]/r0)**2*special.genlaguerre(n-2,2*l+3,rtilde)+\
			(-4*l*r[i]/r0*(l+n+1)+4*(l-1)*l*(l+n+1)**2+(r[i]/r0)**2)*special.genlaguerre(n,2*l+1,rtilde)+\
			4*r/r0*(r[i]/r0-2*l*(l+n+1))*special.genlaguerre(n-1,2*l+2,rtilde))/(4*(r[i]/r0)**2*(l+n+1)**2)
	result = Rfunc_data()
	result.Rfunc_Re = R
	result.Rfunc_Im = np.zeros(len(r))
	result.d_Rfunc_dr_Re = d_R_dr
	result.dd_Rfunc_ddr_Re = dd_R_ddr
	result.d_Rfunc_dr_Im = np.zeros(len(r))
	result.dd_Rfunc_ddr_Im = np.zeros(len(r))
	return result

# Define bessel function approximation for the marginally bound radial function
def Bessel_marginal_Rfunc(M, mu, omega, n, l, m, r):
	r0 = M/(2*(M*mu)**2)
	rtilde = r/r0
	Bnl = np.sqrt(np.pi) * r0**(-3/4)
	#factorial(2*l+1)
	R = Bnl * rtilde**(-1/2) * special.jv(2*l+1,2*np.sqrt(rtilde)) 
	d_R_dr = Bnl*(r*special.jv(2*l,2*np.sqrt(rtilde))-r0*np.sqrt(r/r0)*special.jv(2*l+1,2*np.sqrt(rtilde))-r*special.jv(2*l+2,2*np.sqrt(rtilde)))/(2*r**2)
	dd_R_ddr = Bnl*np.sqrt(r/r0)*(-3*r0*np.sqrt(r/r0)*special.jv(2*l,2*np.sqrt(rtilde))+r*special.jv(2*l-1,2*np.sqrt(rtilde))-2*r*special.jv(2*l+1,2*np.sqrt(rtilde))+\
		3*r0*special.jv(2*l+1,2*np.sqrt(rtilde))+3*r0*np.sqrt(r/r0)*special.jv(2*l+2,2*np.sqrt(rtilde))+\
		r*special.jv(2*l+3,2*np.sqrt(rtilde)) )/(4*r**3)
	result = Rfunc_data()
	result.Rfunc_Re = R
	result.Rfunc_Im = np.zeros(len(r))
	result.d_Rfunc_dr_Re = d_R_dr
	result.dd_Rfunc_ddr_Re = dd_R_ddr
	result.d_Rfunc_dr_Im = np.zeros(len(r))
	result.dd_Rfunc_ddr_Im = np.zeros(len(r))
	return result

def C1_func(l, omega, M):
	result = special.gamma(l+1.5)*np.exp(2*M*omega*np.pi)/((M*omega)**(l+1)*M*(l+1)*(l+2)*np.sqrt(np.pi)*2)
	return result
	
# Define the HeunC function RH function
def Heun_RH_function(M, omega, l, r):
	c1 = C1_func(l, omega, M)
	R = Rfunc(M, 0, omega, 0, l, l, -2, True, False, 0, r)
	return (R.Rfunc_Re + 1j*R.Rfunc_Im)/c1

# Define spherical bessel function approximation for the RH function
def bessel_RH_function(M, omega, l, r):
	result = omega*((2*1j*r**2*omega*((l+2)*r-(2*l+5)*M)+(l+1)*(l+2)*(r-2*M)**2-2*r**2*omega**2*(2*M**2-2*M*r+r**2))*special.spherical_jn(l,r*omega)+2*r*omega*(r-2*M)*(2*M+r*(-1-1j*r*omega))*special.spherical_jn(l+1,omega*r))
	return result

def scalar_Rfunc(M, mu, omega, n, l, m, sgn_alpha, sgn_beta, r):
	R = Rfunc(M, mu, omega, 0, l, l, 0, sgn_alpha, sgn_beta, False, 0, r)
	return R

def Cnl(n, l, m, mu, M, a):
	term = 0
	r_plus = M*(1 + np.sqrt(1 - a**2))
	for j in range(0,l,):
		term += j**2*(1-a**2)+(a*m - 2*mu*r_plus)**2
	result = (2**(4*l+2)*factorial(2*l+n+1))/((n+l+1)**(2*l+4)*factorial(n))*(factorial(l)/(factorial(2*l)*factorial(2*l+1)))**2*\
		term
	return result

def omega_estimate(M, mu, n, l, m, a):
	r_plus = M*(1 + np.sqrt(1 - a**2))
	omega = mu*(1-0.5*(mu*M/(n+l+1))**2) + (1j/M)*(a*m-2*mu*r_plus)*(M*mu)**(4*l+5)*Cnl(n,l,m,mu,M,a)
	return omega

# Define the Teukolsky source function for Schwarzschild background
def Teukolsky_22w_source_function(M, n, l, m, mu, omegaR1, omegaR2, Rfunc1, Rfunc2, r):
	R1 = Rfunc1(M, mu, omega, n, l, m, r)
	R2 = Rfunc2(M, mu, omega, n, l, m, r)
	result = (1/np.sqrt(5))*2*np.pi**(3/2)*(R1.Rfunc_Im*(R2.Rfunc_Im*(8*M**2+2*M*r*(-4-3*1j*r*(omegaR1-omegaR2))+r**2*(r**2*(-omegaR1**2+2*omegaR1*omegaR2+omegaR2**2)+2*1j*r*(omegaR1-omegaR2)+2))-1j*R2.Rfunc_Re*(8*M**2+2*M*r*(-4-3*1j*r*(omegaR1-omegaR2))+r**2*(r**2*(-omegaR1**2+2*omegaR1*omegaR2+omegaR2**2)+2*1j*r*(omegaR1-omegaR2)+2))-r*(2*M-r)*(R2.d_Rfunc_dr_Im*(4*M-2*1j*r**2*(omegaR1+omegaR2)-2*r)-r*(r-2*M)*(R2.dd_Rfunc_ddr_Im-1j*R2.dd_Rfunc_ddr_Re)+R2.d_Rfunc_dr_Re*(-4*1j*M-2*r*(r*(omegaR1+omegaR2)-1j))))+R1.Rfunc_Re*(-1j*R2.Rfunc_Im*(8*M**2+2*M*r*(-4-3*1j*r*(omegaR1-omegaR2))+r**2*(r**2*(-omegaR1**2+2*omegaR1*omegaR2+omegaR2**2)+2*1j*r*(omegaR1-omegaR2)+2))-R2.Rfunc_Re*(8*M**2+2*M*r*(-4-3*1j*r*(omegaR1-omegaR2))+r**2*(r**2*(-omegaR1**2+2*omegaR1*omegaR2+omegaR2**2)+2*1j*r*(omegaR1-omegaR2)+2))+r*(2*M-r)*(R2.d_Rfunc_dr_Re*(4*M-2*1j*r**2*(omegaR1+omegaR2)-2*r)+r*(2*M-r)*(R2.dd_Rfunc_ddr_Re+1j*R2.dd_Rfunc_ddr_Im)+2*R2.d_Rfunc_dr_Im*(2*1j*M+r*(r*(omegaR1+omegaR2)-1j))))+r*(2*M-r)*(R2.Rfunc_Im*(R1.d_Rfunc_dr_Im*(4*M-2*1j*r**2*(omegaR1-omegaR2)-2*r)+r*(2*M-r)*(R1.dd_Rfunc_ddr_Im-1j*R1.dd_Rfunc_ddr_Re)+2*R1.d_Rfunc_dr_Re*(r*(r*(omegaR2-omegaR1)+1j)-2*1j*M))+R2.Rfunc_Re*(2*R1.d_Rfunc_dr_Re*(-2*M+1j*r**2*(omegaR1-omegaR2)+r)-1j*r*(2*M-r)*(R1.dd_Rfunc_ddr_Im-1j*R1.dd_Rfunc_ddr_Re)+2*R1.d_Rfunc_dr_Im*(r*(-r*omegaR1+r*omegaR2+1j)-2*1j*M))-2*r*(2*M-r)*(R1.d_Rfunc_dr_Im-1j*R1.d_Rfunc_dr_Re)*(R2.d_Rfunc_dr_Im-1j*R2.d_Rfunc_dr_Re)))
	return result

#
r_plus = M*(1 + np.sqrt(1 - a**2))
r_minus = M*(1 - np.sqrt(1 - a**2))
ln_r = np.linspace(-6, 6, 512)
r_BL = (np.exp(ln_r) + 1.0)*r_plus

def factor_func(r):
	Delta = (r - r_plus)*(r - r_minus)
	result = Delta**2 * r**2
	return result

factor = factor_func(r_BL)

## check the ingoing and outgoing Heun functions behave as expected.

#for i in range(0,len(r_BL)):
#	print("r = ", r_BL[i])
#	print("Rfunc_outgoing = ", Rfunc(M, 0, omega, 0, 1, 1, -2, False, True, 0, np.array([r_BL[i]])).Rfunc_Re)

"""Heun_R = HeunC_func(M, 0, omega, 0, 1, 1, -2, True, r_BL)
RH_ingoing_R = Rfunc(M, 0, omega, 0, 1, 1, -2, True, False, 0, r_BL)
RH_ingoing_R_KS = Rfunc(M, 0, omega, 0, 1, 1, -2, True, True, 0, r_BL)
#RH_outgoing_R = Rfunc(M, 0, omega, 0, 1, 1, -2, False, True, 0, r_BL)
RH_ingoing = RH_ingoing_R.Rfunc_Re + 1j*RH_ingoing_R.Rfunc_Im
RH_ingoing_KS = RH_ingoing_R_KS.Rfunc_Re + 1j*RH_ingoing_R_KS.Rfunc_Im
#RH_outgoing = RH_outgoing_R.Rfunc_Re + 1j*RH_outgoing_R.Rfunc_Im
r_star = r_BL + r_plus*np.log(r_BL/r_plus - 1)
plt.plot(ln_r, np.real(Heun_R), "g-", "Heun function")
plt.plot(ln_r, np.real(np.exp(1j*omega*r_star)*RH_ingoing*20/(Heun_R*factor)), "r-", label="np.real(e^iwr_star * RH_ingoing*20/(Heun_R*factor))")
plt.plot(ln_r, np.real(RH_ingoing*20/(Heun_R*factor)), "b-", label="np.real(RH_ingoing*20/(Heun_R*factor))")
#plt.plot(ln_r, np.real(RH_outgoing*0.05), "b-", label="np.imag(RH_ingoing*20/(Heun_R*factor))")
plt.xlabel("$\\ln(r_{BL}/r_+ - 1)$")
plt.ylabel("RH test")
plt.ylim((-2, 2))
plt.legend()
save_root_path = "/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots/"
save_name = "test_RHfunc_ingoing_outgoing.png"
plt.savefig(save_root_path + save_name)
print("saved plot as " + save_root_path + save_name)
plt.clf()

## compare the HeunC and bessel function approximations for the marginally bound state
y_Heun = scalar_Rfunc(M, mu, mu, 100, 1, 1, r_BL).Rfunc_Re
y_bessel = Bessel_marginal_Rfunc(M, mu, mu, 100, 1, 1, r_BL).Rfunc_Re
plt.plot(ln_r, y_Heun * r_BL**(3/4), "r-", label="Heun sol (real part)")
plt.plot(ln_r, y_bessel * r_BL**(3/4), "b-", label="Bessel sol (real part)")
plt.title("$\\mu=${:.1f} $\\omega=${:.1f} a={:.1f} l={:d} m={:d}".format(mu, omega, a, l, m))
plt.xlabel("$\\ln(r_{BL}/r_+ - 1)$")
plt.ylabel("marginally bound Rfunc sol * r^(3/4)")
#plt.ylim((-4, 4))
plt.legend()
save_root_path = "/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots/"
save_name = "test_KerrBH_marginal_Rfunc_general_s_KS.png"
plt.savefig(save_root_path + save_name)
print("saved plot as " + save_root_path + save_name)
plt.clf()"""

## compare the approximations for the n=0 state
r_star_m_r = 2*M*np.log(r_BL/(2*M) - 1)
omega_nlm_011 = omega_estimate(M, mu, 0, 1, 1, 0)
omega_nlm_011_real = np.real(omega_estimate(M, mu, 0, 1, 1, 0))
print("omega_nlm_011 = ", omega_nlm_011)
KS_factor = np.exp(1j*omega_nlm_011_real*r_star_m_r)
y_Heun_func_alpha_beta_11 = HeunC_func(M, mu, omega_nlm_011, 0, 1, 1, 0, 1, 1, r_BL)
y_Heun_func_alpha_beta_m11 = HeunC_func(M, mu, omega_nlm_011, 0, 1, 1, 0, -1, 1, r_BL)
y_Heun_R_alpha_beta_11 = scalar_Rfunc(M, mu, omega_nlm_011, 0, 1, 1, 1, 1, r_BL)
y_Heun_R_alpha_beta_m11 = scalar_Rfunc(M, mu, omega_nlm_011, 0, 1, 1, -1, 1, r_BL)
y_hydrogen_R = hydrogen_Rfunc(M, mu, omega_nlm_011_real, 0, 1, 1, r_BL)
y_Heun_alpha_beta_11 = y_Heun_R_alpha_beta_11.Rfunc_Re + 1j*y_Heun_R_alpha_beta_11.Rfunc_Im
y_Heun_alpha_beta_m11 = y_Heun_R_alpha_beta_m11.Rfunc_Re + 1j*y_Heun_R_alpha_beta_m11.Rfunc_Im
y_hydrogen = y_hydrogen_R.Rfunc_Re + 1j*y_hydrogen_R.Rfunc_Im
plt.plot(ln_r, np.log(np.abs(y_Heun_alpha_beta_11*KS_factor)), "r-", label="Heun sol (sgn_alpha=1) (mag)")
plt.plot(ln_r, np.log(np.abs(y_Heun_alpha_beta_m11*KS_factor)), "y--", label="Heun sol (sgn_alpha=-1) (mag)")
plt.plot(ln_r, np.log(np.abs(y_hydrogen)), "b-", label="hydrogen sol (mag)")
plt.plot(ln_r, np.log(np.abs(y_Heun_func_alpha_beta_11)), "g-", label="Heun function (sgn_alpha=1) part (mag)")
plt.plot(ln_r, np.log(np.abs(y_Heun_func_alpha_beta_m11)), "m-", label="Heun function (sgn_alpha=-1) part (mag)")
plt.title("$\\mu=${:.1f} $\\omega=${:.1f} a={:.1f} l={:d} m={:d}".format(mu, omega, a, l, m))
plt.xlabel("$\\ln(r_{BL}/r_+ - 1)$")
plt.ylabel("n=0 bound Rfunc sol")
plt.ylim((-2, 10))
plt.legend()
save_root_path = "/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots/"
save_name = "test_KerrBH_n0_Rfunc_general_s_KS.png"
plt.savefig(save_root_path + save_name)
print("saved plot as " + save_root_path + save_name)
plt.clf()

## check if we can find solutions where the ingoing Heun solution at the horizon also goes to zero at infinity 
## i.e. for the quasinormal modes we should have B_in = 0
# set the real part of the frequency to omega_nlm_011_real
r_test = np.array([2*M*200])
x = np.linspace(-2, 2,256)
omega_list = omega_nlm_011_real*(1 + 0.001*x*1j)
true_ratio = np.imag(omega_nlm_011)/np.real(omega_nlm_011)*1.0/0.001
y_abs = np.zeros(len(omega_list))
for i in range(0, len(omega_list)):
	R = scalar_Rfunc(M, mu, omega_list[i], 0, 1, 1, -1, 1, r_test)
	y_abs[i] = np.log10(np.abs(R.Rfunc_Re[0] + 1j*R.Rfunc_Im[0])) 
plt.plot(x, y_abs, "r-", label="r = {:.0f}".format(r_test[0]))
plt.vlines([-true_ratio, true_ratio], min(y_abs), max(y_abs), linestyles ="dashed", colors ="k", label="QNM ratio. est")
plt.xlabel("$10^3\\omega_I/\\omega_R$")
plt.ylabel("$\\log_{10}(|R_{in}(r_{test})|)$")
plt.legend()
save_root_path = "/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots/"
save_name = "test_KerrBH_n0_Rfunc_QNM_frequencies.png"
plt.savefig(save_root_path + save_name)
print("saved plot as " + save_root_path + save_name)
plt.clf()

### now try covering the complex plane (for real part > 0)
omega_re_max = mu
N_re = 256
N_im = 256
# estimate QNM frequencies using Brito formula
N = 10
omega_est_l0 = []
omega_est_l1 = []
for n in range(0, 10):
	omega_est_l0.append(omega_estimate(M, mu, n, 0, 0, 0))
	omega_est_l1.append(omega_estimate(M, mu, n, 1, 1, 0))
omega_re_min = np.min(np.real(omega_est_l1))
omega_im_max = np.max(np.concatenate((np.abs(np.imag(omega_est_l0)),np.abs(np.imag(omega_est_l1)))))
y_min = 1 - 1.01*(mu - omega_re_min)/mu
x_max = omega_im_max*1.01/(mu*0.001)
print("y_min = ", y_min)
print("x_max = ", x_max)
x = np.linspace(-x_max, x_max,N_im)
y = np.linspace(y_min, 1, N_re)
y_abs = np.zeros((N_im, N_re))
for i in range(0, N_im):
	for j in range(0, N_re):
		omega = mu*y[j] + 1j*mu*0.001*x[i]
		#print("x,y = {:f},{:f}".format(x[i],y[j]))
		try:
			R = scalar_Rfunc(M, mu, omega, 0, 1, 1, -1, 1, r_test)
		except:
			y_abs[j,i] = nan
		else:
			y_abs[j,i] = np.log10(np.abs(R.Rfunc_Re[0] + 1j*R.Rfunc_Im[0]))
ax1 = plt.axes()
fig = plt.gcf()
cm = 'inferno'
rho_max=np.max(y_abs)
rho_min=np.min(y_abs)
#print('max={:.2f} min={:.2f}'.format(phi_max, phi_min))
zmin=0
zmax=1
mesh = ax1.pcolormesh(x, y,y_abs,cmap=cm)
fig.colorbar(mesh, pad=0.01)
ax1.scatter(np.imag(omega_est_l0)/(mu*0.001), np.real(omega_est_l0)/mu, s=20, c="g", marker="+", label="QNM estimate l=m=0")
ax1.scatter(np.imag(omega_est_l1)/(mu*0.001), np.real(omega_est_l1)/mu, s=20, c="c", marker="x", label="QNM estimate l=m=1")
plt.ylim((y_min, 1))
plt.legend(loc="best")
plt.xlabel("$10^3\\omega_I/\\mu$")
plt.ylabel("$\\omega_R/\\mu$")
plt.title("$\\log_{10}(|R_{in}(r_{test}=$" + "{:.0f}".format(r_test[0]) + "$)|)$ " + "$\\mu = $" + str(mu))
save_root_path = "/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots/"
save_name = "test_KerrBH_n0_Rfunc_QNM_frequencies_complex_plane_mu{:.2f}.png".format(mu)
plt.savefig(save_root_path + save_name)
print("saved plot as " + save_root_path + save_name)
plt.clf()

## compare the RH functions
"""omega = 0.01*2*mu
RH_Heun = Heun_RH_function(M, omega, 1, r_BL)
RH_bessel = bessel_RH_function(M, omega, 1, r_BL)
plt.plot(ln_r, np.log(np.abs(RH_Heun*r_BL**2/factor)), "r-", label="Heun sol (magnitude part)")
plt.plot(ln_r, np.log(np.abs(RH_bessel*r_BL**2/factor)), "b-", label="Bessel sol (magnitude part)")
plt.title("$\\mu=${:.1f} $\\omega=${:.1f} a={:.1f} l={:d} m={:d}".format(mu, omega, a, l, m))
plt.xlabel("$\\ln(r_{BL}/r_+ - 1)$")
plt.ylabel("RH func / r^2 f^2")
#plt.ylim((-25, -15))
plt.legend()
save_root_path = "/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots/"
save_name = "test_RH_func_KS.png"
plt.savefig(save_root_path + save_name)
print("saved plot as " + save_root_path + save_name)
plt.clf()

## determine RH normalisation
# compare values at r = 2*M + np.exp(-2)
r_test = np.array([2*M*(1 + np.exp(-2))])
omega_list = np.exp(np.log(10)*np.linspace(-5, 0, 64))/(2*M)
RH_Heun_omega = np.zeros(len(omega_list))
RH_bessel_omega = np.zeros(len(omega_list))
for i in range(0, len(omega_list)):
	RH_Heun_omega[i] = Heun_RH_function(M, omega_list[i], 1, r_test)[0]
	RH_bessel_omega[i] = bessel_RH_function(M, omega_list[i], 1, r_test)[0]
ratio = RH_Heun_omega/RH_bessel_omega
print("omega_list = ", omega_list)
print("ratio = ", ratio)
plt.plot(np.log10(omega_list*2*M),np.log10(np.abs(ratio)), "r-", label="magnitude")
plt.legend()
plt.title("r_test = {:.3f}".format(r_test[0]))
plt.xlabel("$\\log_{10}(M\\omega)$")
plt.ylabel("$\\log_{10}(|R^H_{Heun}(r_{test})/R^H_{bessel}(r_{test})|)$")
save_root_path = "/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots/"
save_name = "test_RH_func_normalisation.png"
plt.savefig(save_root_path + save_name)
print("saved plot as " + save_root_path + save_name)
plt.clf()

## Compare the source functions for a Schwarzschild background and the n=0 l=m=1 annihilation case
source_hydrogen = Teukolsky_22w_source_function(M, 0, 1, 1, mu, omega_nlm_011_real, omega_nlm_011_real, hydrogen_Rfunc, hydrogen_Rfunc, r_BL)
source_Heun = Teukolsky_22w_source_function(M, 0, 1, 1, mu, omega_nlm_011_real, omega_nlm_011_real, scalar_Rfunc, scalar_Rfunc, r_BL)
RH_Heun = Heun_RH_function(M, 2*omega_nlm_011_real, 1, r_BL)
RH_bessel = bessel_RH_function(M, 2*omega_nlm_011_real, 1, r_BL)
r_max = 200
r_linear = np.linspace(r_plus*1.001, r_max, 1024)
dr = (r_max - r_plus)/1024
source_hydrogen_linear = Teukolsky_22w_source_function(M, 0, 1, 1, mu, omega_nlm_011_real, omega_nlm_011_real, hydrogen_Rfunc, hydrogen_Rfunc, r_linear)
source_Heun_linear = Teukolsky_22w_source_function(M, 0, 1, 1, mu, omega_nlm_011_real, omega_nlm_011_real, scalar_Rfunc, scalar_Rfunc, r_linear)
RH_Heun_linear = Heun_RH_function(M, 2*omega_nlm_011_real, 1, r_linear)
RH_bessel_linear = bessel_RH_function(M, 2*omega_nlm_011_real, 1, r_linear)
factor_linear = factor_func(r_linear)
omega = 2*omega_nlm_011_real
r_star_m_r_linear = 2*M*np.log(r_linear/(2*M) - 1)
KS_factor = np.exp(1j*2*omega*r_star_m_r)
KS_factor_linear = np.exp(1j*2*omega*r_star_m_r_linear)
integral_Heun = dr*np.cumsum(np.real(source_Heun_linear*RH_Heun_linear*KS_factor_linear/factor_linear))
integral_hydrogen = dr*np.cumsum(np.real(source_hydrogen_linear*RH_bessel_linear*KS_factor_linear/factor_linear))
## first try plotting just the source functions
plt.plot(ln_r, np.log(np.abs(source_Heun)), "r-", label="source using Heun func (real)")
plt.plot(ln_r, np.log(np.abs(source_hydrogen)), "b-", label="source using hydrogen func (real)")
plt.title("$\\mu=${:.1f} $\\omega=${:.1f} a={:.1f} l={:d} m={:d}".format(mu, omega, a, l, m))
plt.xlabel("$\\ln(r_{BL}/r_+ - 1)$")
plt.ylabel("$\\ln(|T_{22\\omega}|)$")
#plt.ylim((-50, 50))
plt.legend()
save_root_path = "/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots/"
save_name = "test_Brito_source_func_n0_KS.png"
plt.savefig(save_root_path + save_name)
print("saved plot as " + save_root_path + save_name)
plt.clf()
### then try whole integrand (and integral)
plt.plot(ln_r, np.real(source_Heun*RH_Heun*KS_factor/factor), "r-", label="integrand using Heun func (real)")
plt.plot(ln_r, np.imag(source_Heun*RH_Heun*KS_factor/factor), "m-", label="integrand using Heun func (imag)")
plt.plot(ln_r, np.real(source_hydrogen*RH_bessel)/factor, "b-", label="integrand using hydrogen func and bessel func")
#plt.plot(ln_r, np.real(source_Heun*np.exp(-1j*omega*r_star_m_r)/factor), "c-", label="integrand using Heun with KS (real)")
#plt.plot(ln_r, np.real(RH_Heun*np.exp(1j*omega*r_star_m_r)/factor**2), "y-", label="integrand using Heun with KS (real)")
plt.plot(np.log(r_linear/r_plus-1), integral_Heun, "r--", label="integral using Heun func")
plt.plot(np.log(r_linear/r_plus-1), integral_hydrogen, "b--", label="integral using hydrogen func and bessel func")
#plt.plot(ln_r, np.real(KS_factor), "g-", label="np.real(exp(-i*w*(r_*-r))")
plt.title("$\\mu=${:.1f} $\\omega=${:.1f} a={:.1f} l={:d} m={:d}".format(mu, omega, a, l, m))
plt.xlabel("$\\ln(r_{BL}/r_+ - 1)$")
plt.ylabel("T22$\\omega R_H/r^2 f^2$ integrand (real part)")
plt.ylim((-50, 50))
plt.legend()
save_root_path = "/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots/"
save_name = "test_Brito_integral_n0_KS.png"
plt.savefig(save_root_path + save_name)
print("saved plot as " + save_root_path + save_name)
plt.clf()

## Compare the source functions for a Schwarzschild background and the marginally bound l=m=1 annihilation case
source_bessel = Teukolsky_22w_source_function(M, 0, 1, 1, mu, mu, mu, Bessel_marginal_Rfunc, Bessel_marginal_Rfunc, r_BL)
source_Heun = Teukolsky_22w_source_function(M, 0, 1, 1, mu, mu, mu, scalar_Rfunc, scalar_Rfunc, r_BL)
RH_Heun = Heun_RH_function(M, 2*mu, 1, r_BL)
RH_bessel = bessel_RH_function(M, 2*mu, 1, r_BL)
source_bessel_linear = Teukolsky_22w_source_function(M, 0, 1, 1, mu, mu, mu, Bessel_marginal_Rfunc, Bessel_marginal_Rfunc, r_linear)
source_Heun_linear = Teukolsky_22w_source_function(M, 0, 1, 1, mu, mu, mu, scalar_Rfunc, scalar_Rfunc, r_linear)
RH_Heun_linear = Heun_RH_function(M, 2*mu, 1, r_linear)
RH_bessel_linear = bessel_RH_function(M, 2*mu, 1, r_linear)
factor_linear = factor_func(r_linear)
integral_Heun = dr*np.cumsum(np.real(source_Heun_linear*RH_Heun_linear/factor_linear))
integral_bessel = dr*np.cumsum(np.real(source_bessel_linear*RH_bessel_linear/factor_linear))
plt.plot(ln_r, np.real(source_Heun)*RH_Heun/factor, "r-", label="using Heun funcs")
plt.plot(ln_r, np.real(source_bessel)*RH_bessel/factor, "b-", label="using bessel funcs")
plt.plot(np.log(r_linear/r_plus-1), integral_Heun, "r--", label="integral using Heun func")
plt.plot(np.log(r_linear/r_plus-1), integral_bessel, "b--", label="integral using bessel func")
plt.title("$\\mu=${:.1f} $\\omega=${:.1f} a={:.1f} l={:d} m={:d}".format(mu, omega, a, l, m))
plt.xlabel("$\\ln(r_{BL}/r_+ - 1)$")
plt.ylabel("T22$\\omega R_H/r^2 f^2$ integrand (real part)")
plt.ylim((-5, 5))
plt.legend()
save_root_path = "/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots/"
save_name = "test_Brito_integral_marginally_bound_KS.png"
plt.savefig(save_root_path + save_name)
print("saved plot as " + save_root_path + save_name)
plt.clf()"""


