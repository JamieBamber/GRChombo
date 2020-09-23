import numpy as np
import time
import sys
from matplotlib import rc
rc('text', usetex=True)
import matplotlib.pyplot as plt
import math
import ctypes
from scipy.optimize import curve_fit
start_time = time.time()

# set up parameters 
phi0 = 0.1
R_min = 5
R_max = 300
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Y00_integration_data/"
lm_list = [(1, 1)]
num = 800
plot_interval = 10
M = 1
phi0 = 0.1
lin_or_log = False
colours = ["r", "b", "g", "c"]
colours2 = ["k", "m", "y"]
styles = ["-", "--"]
scale = ""
if (lin_or_log):
	scale = "linear"
else:
	scale = "log"

log_y = False

class data_dir:
	def __init__(self, num, l, m, a, mu, Al, nphi, ntheta, theta_max):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = float(mu)
		self.nphi = nphi
		self.ntheta = ntheta
		self.theta_max = float(theta_max)
		self.Al = Al
		self.name = "run{:04d}_l{:d}_m{:d}_a{:s}_Al{:s}_mu{:s}_M1_IsoKerr".format(num, l, m, a, Al, mu)
	#
	def load_data(self, number):
		file_name = self.name+"_phi_Y00_integral_{:s}_r_plus_to_{:d}_nphi{:d}_ntheta{:d}_theta_max{:.1f}.dat".format(scale, R_max, self.nphi, self.ntheta, self.theta_max)
		dataset_path = data_root_path + file_name
		data = np.genfromtxt(dataset_path, skip_header=1)
		R = data[0,1:]
		r_plus = M*(1 + np.sqrt(1 - self.a**2))
		self.r = R*(1 + r_plus/(4*R))**2
		row = int(number/plot_interval)
		self.time = data[row,0]
		phi = data[row,1:]
		self.phi = phi/phi0
		
data_dirs = []
def add_data_dir(num, l, m, a, mu, Al, nphi, ntheta, theta_max):
	x = data_dir(num, l, m, a, mu, Al, nphi, ntheta, theta_max)
	data_dirs.append(x)

# choose datasets to compare

"""run0002_l0_m0_a0.7_Al0_mu0.4_M1_IsoKerr
run0005_l1_m1_a0.7_Al0_mu0.4_M1_IsoKerr
run0006_l1_m1_a0.99_Al0_mu0.4_M1_IsoKerr
run0007_l2_m2_a0.7_Al0_mu0.4_M1_IsoKerr
run0008_l4_m4_a0.7_Al0_mu0.4_M1_IsoKerr
run0009_l1_m-1_a0.7_Al0_mu0.4_M1_IsoKerr
run0010_l8_m8_a0.7_Al0_mu0.4_M1_IsoKerr
run0011_l1_m1_a0.7_Al0_mu2.0_M1_IsoKerr
run0012_l1_m1_a0.7_Al0_mu0.01_M1_IsoKerr
run0013_l2_m2_a0.7_Al0_mu0.8_M1_IsoKerr
run0014_l8_m8_a0.7_Al0_mu3.2_M1_IsoKerr
run0015_l1_m1_a0.7_Al0.5_mu0.4_M1_IsoKerr
run0016_l1_m-1_a0.99_Al0_mu0.4_M1_IsoKerr
run0017_l1_m1_a0.99_Al0.5_mu0.4_M1_IsoKerr
run0018_l1_m1_a0.99_Al0.25_mu0.4_M1_IsoKerr"""

#add_data_dir(1, 0, 0, "0.0", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(2, 0, 0, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(3, 0, 0, "0.99", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(5, 1, 1, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(7, 2, 2, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(8, 4, 4, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(9, 1, -1, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(15, 1, 1, "0.7", "0.4", "0.5", 64, 64, "_theta_max0.99")
#add_data_dir(6, 1, 1, "0.99", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(16, 1, -1, "0.99", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(17, 1, 1, "0.99", "0.4", "0.5", 64, 64, "_theta_max0.99")
#add_data_dir(18, 1, 1, "0.99", "0.4", "0.25", 64, 64, "_theta_max0.99")
add_data_dir(21, 0, 0, "0.7", "2.0", "0", 64, 18, "1.0")

# appropriate \int Ylm Ylm^* cos(2 theta) dtheta dphi factor for 0 <= l <= 10
cos2theta_integrals = [[-(1/3)],[1/5,-(3/5)],[1/21,-(1/7),-(5/7)],\
[1/45,-(1/15),-(1/3),-(7/9)],[1/77,-(3/77),-(15/77),-(5/11),-(9/11)],\
[1/117,-(1/39),-(5/39),-(35/117),-(7/13),-(11/13)],\
[1/165,-(1/55),-(1/11),-(7/33),-(21/55),-(3/5),-(13/15)],\
[1/221,-(3/221),-(15/221),-(35/221),-(63/221),-(99/221),-(11/17),-(15/17)],\
[1/285,-(1/95),-(1/19),-(7/57),-(21/95),-(33/95),-(143/285),-(13/19),-(17/19)],\
[1/357,-(1/119),-(5/119),-(5/51),-(3/17),-(33/119),-(143/357),-(65/119),-(5/7),-(19/21)],\
[1/437,-(3/437),-(15/437),-(35/437),-(63/437),-(99/437),-(143/437),-(195/437),-(255/437),-(17/23),-(21/23)]]

### analytic phi
def analytic_phi(t, r, a, mu):
	## calculate the Boyer Lindquist r
	## assume M = 1
	# r_plus = 1 + np.sqrt(1 - a*a)
	# r = R*(1 + r_plus/(4.0*R))**2
	## calculate the perturbative flux at large radius to order 
	cos2theta = -1/3
	l=0
	m=0
	L = l*(l+1)/(mu**2)
	tau = mu*t
	""" #
	Integrating factor of 
        	\int Ylm Ylm^* cos(2 theta) dtheta dphi
	assuming the spherical harmonics are normalised so that 
        	\int Ylm Ylm^* cos(2 theta) dtheta dphi = 1 
	# """
	F0=np.cos(tau)
	F1=(tau*np.sin(tau))/r
	F2=-1/2*tau*((L-2)*np.sin(tau)+np.sin(tau))-1/2*tau**2*np.cos(tau)
	F3=-((tau*np.sin(tau)*(a**2*mu*cos2theta+3*a**2*mu+4*a*m-(L+1)*mu))/(2*mu))-4*a**2*(np.cos(tau)-1)+1/2*(L-1)*tau**2*np.cos(tau)-1/6*tau**3*np.sin(tau)
	F4=-((a**2*(4*mu**2+m**2)*(np.cos(tau)-1))/mu**2)+(tau**2*np.cos(tau)*(4*a**2*mu**2*cos2theta+mu**2*(-(-12*a**2+L*(L+2)+5))+16*a*mu*m+2*L))/(8*mu**2)+(1/(8*mu**2))*tau*np.sin(tau)*(2*a**2*(L+2)*mu**2*cos2theta+mu**2*(2*a**2*(L-18)+L*(L+2)+5)-16*a*mu*m-2*L)+1/12*tau**3*(3*L-2/mu**2-3)*np.sin(tau)+1/24*tau**4*np.cos(tau)
	Phi = F0 + F1/r + F2/r**2 + F3/r**3 + F4/r**4
	return Phi	
	
### 
Kerrlib = ctypes.cdll.LoadLibrary('/home/dc-bamb1/GRChombo/Source/utils/KerrBH_Rfunc_lib.so')
Kerrlib.Rfunc.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_bool, ctypes.c_double, ctypes.c_double]
Kerrlib.Rfunc.restype = ctypes.c_double

def Stationary_sol(r, t, a, mu, l, m, ingoing, A, phase):
	# double M, double mu, double omega, double a, int l, int m, bool ingoing, bool KS_or_BL, double t, double r
	sol = np.zeros(r.size)
	omega = mu
	r_plus = M*(1 - np.sqrt(1 - a**2))
	for i in range(0, r.size):
		if (r[i]<=r_plus):
			sol[i] = 0
		else:
     			sol[i] = Kerrlib.Rfunc(M, mu, omega, a, l, m, ingoing, False, t - 2*np.pi*phase/omega, r[i])
	sol = A*sol
	return sol

### get data and plot profile for each 

def fit_ingoing_solution(ax, dd, p0_, colour):
	def Stationary_sol_fit(r, A, phase):
		phase_in = 0
		phase_out = 0
		print("testing A={:.2f} phase={:.2f}".format(A, phase))
		ingoing_phi = Stationary_sol(r, dd.time, dd.a, dd.mu, dd.l, dd.m, True, A, phase)
		return np.abs(ingoing_phi)
	popt, pconv = curve_fit(Stationary_sol_fit, dd.r, dd.phi, p0=p0_)
	A = popt[0]
	phase = popt[1]
	phi_fitted = Stationary_sol_fit(dd.r, A, phase)
	if (lin_or_log):
		x = dd.r/M
	else:
		x = np.log10(dd.r/M)
	if log_y:
		y = np.log10(phi_fitted)
	else:
		y = phi_fitted
	ax.plot(x, y, colour + "--", label="fitted Heun sol. ampl.={:.2f} phase={:.2f} l={:d} m={:d} a={:.2f}".format(A, phase, dd.l, dd.m, dd.a), linewidth=1)

def fit_comb_solution(ax, dd, p0_, colour):
	def Stationary_sol_fit(r, A_in, A_out, phase):
		phase_in = phase
		phase_out = phase
		print("testing A_in={:.2f} A_out={:.2f} phase={:.2f}".format(A_in, A_out, phase))
		ingoing_phi = Stationary_sol(r, dd.time, dd.a, dd.mu, dd.l, dd.m, True, A_in, phase)
		outgoing_phi = Stationary_sol(r, dd.time, dd.a, dd.mu, dd.l, dd.m, False, A_out, phase)
		return ingoing_phi + outgoing_phi
	popt, pconv = curve_fit(Stationary_sol_fit, dd.r, dd.phi, p0=p0_)
	A_in = popt[0]
	A_out = popt[1]
	phase = popt[2]
	phi_fitted = Stationary_sol_fit(dd.r, A_in, A_out, phase)
	if (lin_or_log):
		x = dd.r/M
	else:
		x = np.log10(dd.r/M)
	if log_y:
		y = np.log10(phi_fitted)
	else:
		y = phi_fitted
	ax.plot(x, y, colour + "--", label="_fitted stationary sol.".format(dd.l, dd.m, dd.a), linewidth=1)

def impose_comb_solution(ax, dd, p0, colour):
	def Stationary_sol_fit(r, A_in, A_out, phase):
		phase_in = phase
		phase_out = phase
		print("testing A_in={:.2f} A_out={:.2f} phase={:.2f}".format(A_in, A_out, phase))
		ingoing_phi = Stationary_sol(r, dd.time, dd.a, dd.mu, dd.l, dd.m, True, A_in, phase)
		outgoing_phi = Stationary_sol(r, dd.time, dd.a, dd.mu, dd.l, dd.m, False, A_out, phase)
		return np.abs(ingoing_phi + outgoing_phi)
	A_in = p0[0]
	A_out = p0[1]
	phase = p0[2]
	phi_fitted = Stationary_sol_fit(dd.r, A_in, A_out, phase)
	if (lin_or_log):
		x = dd.r/M
	else:
		x = np.log10(dd.r/M)
	if log_y:
		y = np.log10(phi_fitted)
	else:
		y = phi_fitted
	ax.plot(x, y, colour + "--", label="Heun sol. ampl(in)={:.2f} ampl(out)={:.2f} \n phase={:.2f} l={:d} m={:d} a={:.2f}".format(A_in, A_out, phase, dd.l, dd.m, dd.a), linewidth=1)

def plot_graph():
	# plot setup
	ax1 = plt.axes()
	fig = plt.gcf()
	fig.set_size_inches(3.8,3)
	font_size = 10
	title_font_size = 10
	label_size = 11
	legend_font_size = 9
	rc('xtick',labelsize=font_size)
	rc('ytick',labelsize=font_size)
	#	
	for i in range(0, len(data_dirs)):
		dd = data_dirs[i]
		numbers=[40, 800, 1600]
		for j in range(0, len(numbers)):
			number=numbers[j]
			dd.load_data(number)
			if (lin_or_log):
				x = dd.r/M
			else:
	     			x = np.log10(dd.r/M)
			if log_y:
				y = np.log10(dd.phi)
			else:
				y = dd.phi
			# plot fitted solution
			if (dd.a < 0.9):
				fit_comb_solution(ax1, dd, (1, 0.2, 0.2), colours[j])
			# find limit where dd.r > 10
			n_cutoff = 0
			cutoff = 0.25*dd.mu*dd.time
			for i in range(0, len(dd.r)):
				if (dd.r[i] > cutoff):
					n_cutoff = i
					break
			analytic_y = analytic_phi(dd.time, dd.r[n_cutoff:], dd.a, dd.mu)
			ax1.plot(x[n_cutoff:], analytic_y, colours[j] + "-.", label="_pertubative sol.".format(dd.l, dd.m, dd.a), linewidth=1)
			ax1.plot(x, y, colours[j] + "-", label="t={:.1f}".format(dd.time), linewidth=1)
			#impose_comb_solution(ax1, dd, (0, 1, 0.2), colours2[i])
			#impose_solution(ax1, dd, (1, 0), colours2[i])
	if log_y:
		ax1.set_ylabel("$\\log_{10}(\\phi_{lm}/\\phi_0)$", fontsize=label_size)
	else:
		ax1.set_ylabel("$\\phi_{00}/\\phi_0$", fontsize=label_size)
	if (lin_or_log):
		xlabel_ = "$r_{BL}/M$"
	else:
		xlabel_ = "$\\log_{10}(r_{BL}/M)$"
	plt.xlabel(xlabel_, fontsize=label_size)
	#a_max = np.max([float(a_str) for a_str in a_list])
	#r_plus_min = 1 + np.sqrt(1 - a_max**2)
	#print("r_plus_min = ", r_plus_min)
	#if (lin_or_log) :
	#	plt.xlim((r_plus_min, 100))
	#else :
	#	plt.xlim(left=np.log10(r_plus_min))
	plt.ylim((-3, 3))
	ax1.legend(loc="best", fontsize=legend_font_size)
	plt.xticks(fontsize=font_size)
	plt.yticks(fontsize=font_size)
	dd0 = data_dirs[0]
	title = "$\\phi_{00}$" + " profile M=1, $\\mu$=2.0, $\\chi=0.7$, $l=m=0$" 
	ax1.set_title(title, fontsize=title_font_size)
	plt.tight_layout()
	save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/IsoKerr_mu{:.1f}_l=m=0_phi_{:s}_plot_vs_Heun_v3.png".format(2.0, scale)
	print("saved " + save_name)
	plt.savefig(save_name, transparent=False)
	plt.clf()
	
plot_graph()
