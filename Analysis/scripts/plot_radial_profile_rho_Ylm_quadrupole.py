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
R_max = 500
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Ylm_integration_data/"
num = 800
plot_interval = 10
M = 1
phi0 = 0.1
lin_or_log = False
colours = ['r', 'b', 'g', 'm', 'c', 'y']
colours2 = ["k", "m", "y"]
styles = ["-", "--"]

Nphi=64
Ntheta=18
Theta_max=1.0

scale = ""
if (lin_or_log):
	scale = "linear"
else:
	scale = "log"

log_y = True

class data_dir:
	def __init__(self, num, l, m, a, mu, Al, nphi, ntheta, theta_max, l_, m_):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = float(mu)
		self.nphi = nphi
		self.ntheta = ntheta
		self.theta_max = float(theta_max)
		self.Al = Al
		self.l_ = l_
		self.m_ = m_
		self.name = "run{:04d}_l{:d}_m{:d}_a{:s}_Al{:s}_mu{:s}_M1_IsoKerr".format(num, l, m, a, Al, mu)
	#
	def load_data(self, number):
		file_name = self.name+"_rho_Ylm_integral_{:s}_r_plus_to_{:d}_nphi{:d}_ntheta{:d}_theta_max{:.1f}_l={:d}_m={:d}.dat".format(scale, R_max, self.nphi, self.ntheta, self.theta_max, self.l_, self.m_)
		dataset_path = data_root_path + file_name
		data = np.genfromtxt(dataset_path, skip_header=1)
		print("loaded " + file_name)
		R = data[0,1:]
		r_plus = M*(1 + np.sqrt(1 - self.a**2))
		self.r = R*(1 + r_plus/(4*R))**2
		row = int(number/plot_interval)
		self.time = data[row,0]
		rho = data[row,1:]
		rho0 = 0.5*(phi0**2)*(self.mu)**2
		self.rho = rho/rho0
		
data_dirs = []
def add_data_dir(num, l, m, a, mu, l_, m_):
	x = data_dir(num, l, m, a, mu, "0", Nphi, Ntheta, Theta_max, l_, m_)
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

#add_data_dir(5, 1, 1, "0.7", "0.4", 2, 0)
#add_data_dir(5, 1, 1, "0.7", "0.4", 2, 1)
add_data_dir(5, 1, 1, "0.7", "0.4", 2, 2)

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
		dd.load_data(num)
		if (lin_or_log):
			x = dd.r/M
		else:
	     		x = np.log10(dd.r/M)
		if log_y:
			y = np.log10(dd.rho*(dd.r/M)**2)
		else:
			y = dd.rho*(dd.r/M)**2
		label_="$l=${:d} $m=${:d}".format(dd.l_, dd.m_)
		ax1.plot(x, y, colours[i] + "-", label=label_, linewidth=1)
	if log_y:
		ax1.set_ylabel("$\\log_{10}((\\rho_{2m}/\\rho_0)(r^2/M^2))$", fontsize=label_size)
	else:
		ax1.set_ylim((0, 2000))
		ax1.set_ylabel("$(\\rho_{2m}/\\rho_0)(r^2/M^2)$", fontsize=label_size)
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
	ax1.legend(loc="best", fontsize=legend_font_size, labelspacing=0.1, handletextpad=0.2, borderpad=0.4)
	plt.xticks(fontsize=font_size)
	plt.yticks(fontsize=font_size)
	dd0 = data_dirs[0]
	title = "$\\rho$ quadrupole profile $M=1,\\mu=0.4,\\chi=0.7,l=m=1$" 
	ax1.set_title(title, fontsize=title_font_size)
	plt.tight_layout()
	if log_y:
			save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/IsoKerr_rho_profile_{:s}_Rmax={:d}_n={:d}_quadrupole_log_y.png".format(scale, R_max, num)
	else:
			save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/IsoKerr_rho_profile_{:s}_Rmax={:d}_n={:d}_quadrupole.png".format(scale, R_max, num)
	print("saved " + save_name)
	plt.savefig(save_name, transparent=False)
	plt.clf()
	
plot_graph()
