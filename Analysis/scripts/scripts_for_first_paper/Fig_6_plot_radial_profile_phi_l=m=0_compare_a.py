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

# 
tex_fonts = {
    # Use LaTeX to write all text
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": "Times",
    "mathtext.fontset": "custom",
    "mathtext.rm": "Times New Roman",
    # "font.serif": "ntx-Regular-tlf-t1",
    # Use 8pt font in plots, to match 8pt font in document
    "axes.labelsize": 8,
    "font.size": 8,
    # Make the legend/label fonts a little smaller
    "legend.fontsize": 7,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7
}

#plt.rc("text.latex", preamble=r'''
#       \usepackage{newtxmath}
#       ''')

plt.rcParams.update(tex_fonts)

# set up parameters 
phi0 = 0.1
R_min = 5
R_max = 500
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Y00_integration_data/"
number = 2430
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
	def load_data(self, number):
		file_name = self.name+"_phi_Y00_integral_{:s}_n{:06d}_r_plus_to_{:d}_nphi{:d}_ntheta{:d}_theta_max{:.2f}.dat".format(scale, number, R_max, self.nphi, self.ntheta, self.theta_max)
		dataset_path = data_root_path + file_name
		data = np.genfromtxt(dataset_path, skip_header=1)
		R = data[0,1:]
		r_plus = M*(1 + np.sqrt(1 - self.a**2))
		self.r = R*(1 + r_plus/(4*R))**2
		row = 1
		self.time = data[row,0]
		phi = data[row,1:]
		self.phi = phi/phi0
		
data_dirs = []
def add_data_dir(num, l, m, a, mu, Al, nphi, ntheta, suffix=""):
	x = data_dir(num, l, m, a, mu, Al)
	data_dirs.append(x)

# choose datasets to compare

add_data_dir(1, 0, 0, "0.0", "0.4", "0", 64, 64, "_theta_max0.99")
add_data_dir(2, 0, 0, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
add_data_dir(3, 0, 0, "0.99", "0.4", "0", 64, 64, "_theta_max0.99")

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
	ax.plot(x, y, colour + "--", label="_fitted Heun sol. l={:d} m={:d} a={:.2f}".format(dd.l, dd.m, dd.a), linewidth=1)

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
	label_size = 10
	legend_font_size = 10
	rc('xtick',labelsize=font_size)
	rc('ytick',labelsize=font_size)
	#	
	for i in range(0, len(data_dirs)):
		dd = data_dirs[i]
		dd.load_data(number)
		if (lin_or_log):
			x = dd.r/M
		else:
	     		x = np.log10(dd.r/M)
		if log_y:
			y = np.log10(dd.phi)
		else:
			y = dd.phi
		ax1.plot(x, y, colours[i] + "-", label="$\\chi=${:.2f}".format(dd.a), linewidth=1)
		# plot fitted solution
		#if (dd.a < 0.9):
		#	fit_comb_solution(ax1, dd, (1, 0.2, 0.2), colours[i])
		#impose_comb_solution(ax1, dd, (0, 1, 0.2), colours2[i])
		#impose_solution(ax1, dd, (1, 0), colours2[i])
	if log_y:
		ax1.set_ylabel("$\\log_{10}(\\varphi_{00}/\\Phi_0)$", fontsize=label_size)
	else:
		ax1.set_ylabel("$\\varphi_{00}/\\Phi_0$", fontsize=label_size)
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
	ax1.legend(loc="best", fontsize=legend_font_size)
	plt.xticks(fontsize=font_size)
	plt.yticks(fontsize=font_size)
	dd0 = data_dirs[0]
	title = "$\\varphi_{00}$" + " profile $M=1,\\mu=0.4,l=m=0,\\tau$={:.1f}".format(dd0.time*dd0.mu) 
	ax1.set_title(title, fontsize=title_font_size)
	plt.tight_layout()
	save_root_path="/home/dc-bamb1/GRChombo/Analysis/plots/plots_for_first_paper/"
	save_name="Fig_6_IsoKerr_mu{:.1f}_l=m=0_phi_{:s}_tau={:.1f}_plot.png".format(0.4, scale, dd0.time*dd0.mu)
	print("saved " + save_root_path + save_name)
	plt.savefig(save_root_path + save_name, transparent=False)
	plt.clf()
	
plot_graph()
