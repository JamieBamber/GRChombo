import numpy as np
import time
import sys
from matplotlib import rc
rc('text', usetex=True)
import matplotlib.pyplot as plt
import math
from os import makedirs
import ctypes
from scipy.optimize import curve_fit
import multiprocessing as mp

# set up parameters 
phi0 = 0.1
R_max = 500
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Ylm_integration_data/"
plots_root_path = "/home/dc-bamb1/GRChombo/Analysis/plots/"
#lm_list = [(1, 1)]
l = 1
m = 1
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

log_y = True

movie_folder_name = "run0005_phi_profile_vs_Heun_" + scale + "_movie"

try:
    	makedirs(plots_root_path + movie_folder_name)
except:
       	pass

class data_dir:
	def __init__(self, num, l, m, a, mu, Al):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = float(mu)
		self.nphi = 64
		self.ntheta = 64
		self.theta_max = 0.99
		self.Al = Al
		self.name = "run{:04d}_l{:d}_m{:d}_a{:s}_Al{:s}_mu{:s}_M1_IsoKerr".format(num, l, m, a, Al, mu)
	#
	def load_data(self, l_, m_):
		file_name = self.name+"_phi_Ylm_integral_{:s}_r_plus_to_{:d}_nphi{:d}_ntheta{:d}_theta_max{:.2f}_l={:d}_m={:d}.dat".format(scale, R_max, self.nphi, self.ntheta, self.theta_max, l_, m_)
		dataset_path = data_root_path + file_name
		data = np.genfromtxt(dataset_path, skip_header=1)
		R = data[0,1:]
		r_plus = M*(1 + np.sqrt(1 - self.a**2))
		self.r = R*(1 + r_plus/(4*R))**2
		self.time = data[1:,0]
		phi = data[1:,1:]
		self.phi = phi/phi0
		
data_dirs = []
def add_data_dir(num, l, m, a, mu, Al, nphi, ntheta, suffix=""):
	x = data_dir(num, l, m, a, mu, Al)
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

#add_data_dir(2, 0, 0, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
add_data_dir(5, 1, 1, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(7, 2, 2, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(8, 4, 4, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(9, 1, -1, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(15, 1, 1, "0.7", "0.4", "0.5", 64, 64, "_theta_max0.99")
#add_data_dir(6, 1, 1, "0.99", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(16, 1, -1, "0.99", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(17, 1, 1, "0.99", "0.4", "0.5", 64, 64, "_theta_max0.99")
#add_data_dir(18, 1, 1, "0.99", "0.4", "0.25", 64, 64, "_theta_max0.99")

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

def fit_comb_solution(ax, dd, N, p0_, colour):
	t = dd.time[N]
	phi = dd.phi[N,:]
	def Stationary_sol_fit(r, A_in, A_out, phase):
		phase_in = phase
		phase_out = phase
		#print("testing A_in={:.2f} A_out={:.2f} phase={:.2f}".format(A_in, A_out, phase))
		ingoing_phi = Stationary_sol(r, t, dd.a, dd.mu, dd.l, dd.m, True, A_in, phase)
		outgoing_phi = Stationary_sol(r, t, dd.a, dd.mu, dd.l, dd.m, False, A_out, phase)
		return np.abs(ingoing_phi + outgoing_phi)
	popt, pconv = curve_fit(Stationary_sol_fit, dd.r, phi, p0=p0_)
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
	ax.plot(x, y, colour + "--", label="fitted Heun sol. ampl(in)={:.2f} ampl(out)={:.2f} \n phase={:.2f} l={:d} m={:d} a={:.2f}".format(A_in, A_out, phase, dd.l, dd.m, dd.a), linewidth=1)

def impose_comb_solution(ax, dd, N, p0, colour):
	t = 0
	def Stationary_sol_fit(r, A_in, A_out, phase):
		phase_in = phase
		phase_out = phase
		print("testing A_in={:.2f} A_out={:.2f} phase={:.2f}".format(A_in, A_out, phase))
		ingoing_phi = Stationary_sol(r, t, dd.a, dd.mu, dd.l, dd.m, True, A_in, phase)
		outgoing_phi = Stationary_sol(r, t, dd.a, dd.mu, dd.l, dd.m, False, A_out, phase)
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

# load data
dd = data_dirs[0]
dd.load_data(l, m)

def plot_graph(N):
	# plot setup
	ax1 = plt.axes()
	fig = plt.gcf()
	fig.set_size_inches(8,6)
	font_size = 12
	title_font_size = 12
	label_size = 12
	legend_font_size = 12
	rc('xtick',labelsize=font_size)
	rc('ytick',labelsize=font_size)
	#	
	if (lin_or_log):
		x = dd.r/M
	else:
	     	x = np.log10(dd.r/M)
	if log_y:
		y = np.log10(dd.phi[N,:])
	else:
		y = dd.phi[N,:]
	ax1.plot(x, y, colours[0] + '-', label="l={:d} m={:d} a={:.2f}".format(dd.l, dd.m, dd.a), linewidth=1)
	# plot fitted solution
	impose_comb_solution(ax1, dd, N, (1, 0, 0.24), colours2[0])
	#impose_solution(ax1, dd, (1, 0), colours2[i])
	if log_y:
		plt.ylabel("$\\log_{10}(\\phi_{lm}/\\phi_0)$", fontsize=label_size)
	else:
		plt.ylabel("$|\\phi_{lm}|/\\phi_0$", fontsize=label_size)
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
	plt.ylim((-2, 2))
	ax1.legend(loc="best", fontsize=legend_font_size)
	plt.xticks(fontsize=font_size)
	plt.yticks(fontsize=font_size)
	#dd0 = data_dirs[0]
	title = "$\\phi_{lm}$" + " profile M=1, $\\mu$=0.4, time = {:.1f}".format(dd.time[N]) 
	ax1.set_title(title, fontsize=title_font_size)
	plt.tight_layout()
	save_name = plots_root_path + movie_folder_name + "/frame_{:06d}.png".format(N)
	print("saved " + save_name)
	plt.savefig(save_name, transparent=False)
	plt.clf()
	
# plot the frames in parallel

ds_size = len(dd.time)
print("ds_size = ", ds_size)

#a_pool = mp.Pool(processes=8)

#a_pool.map(plot_graph, range(0, ds_size))

for i in range(0, ds_size):
	plot_graph(i)
