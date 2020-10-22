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
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/"
lm_list = [(0, 0), (2,0), (4,0)]
number = 2430
plot_interval = 10
M = 1
phi0 = 0.1
lin_or_log = False
colours = ["r", "b", "g", "c"]
colours2 = ["k", "m", "y"]
styles = ["-", "--", "-."]
scale = ""
if (lin_or_log):
	scale = "linear"
else:
	scale = "log"

log_y = True

Ntheta=18
Nphi=64
Theta_max="1.0"

class data_dir:
	def __init__(self, num, l, m, a, mu, Al, nphi, ntheta, theta_max):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = float(mu)
		self.nphi = nphi
		self.ntheta = ntheta
		self.theta_max = theta_max
		self.Al = Al
		self.name = "run{:04d}_l{:d}_m{:d}_a{:s}_Al{:s}_mu{:s}_M1_IsoKerr".format(num, l, m, a, Al, mu)
	#
	def load_data(self, l_, m_):
		if (l_ != 0):
			file_name = "Ylm_integration_data/"+self.name+"_phi_Ylm_integral_{:s}_r_plus_to_{:d}_nphi{:d}_ntheta{:d}_theta_max{:s}_l={:d}_m={:d}.dat".format(scale, R_max, self.nphi, self.ntheta, self.theta_max, l_, m_)
		else:
			file_name = "Y00_integration_data/"+self.name+"_phi_Y00_integral_{:s}_n{:06d}_r_plus_to_{:d}_nphi64_ntheta64_theta_max0.99.dat".format(scale, number, R_max)			
		dataset_path = data_root_path + file_name
		data = np.genfromtxt(dataset_path, skip_header=1)
		R = data[0,1:]
		r_plus = M*(1 + np.sqrt(1 - self.a**2))
		self.r = R*(1 + r_plus/(4*R))**2
		if (l_ != 0):
			dt = data[2,0] - data[1,0]
			#row = int((tau/self.mu-data[1,0])/dt)
			row = int(number/plot_interval - data[1,0]/dt)
		else:
			row=1
		self.time = data[row,0]
		phi = data[row,1:]
		self.phi = phi/phi0
		
data_dirs = []
def add_data_dir(num, l, m, a, mu, Al, nphi=Nphi, ntheta=Ntheta, theta_max=Theta_max):
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

add_data_dir(1, 0, 0, "0.0", "0.4", "0")
add_data_dir(2, 0, 0, "0.7", "0.4", "0")
add_data_dir(3, 0, 0, "0.99", "0.4", "0")

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
		for j in range(0, len(lm_list)):
			l, m = lm_list[j]
			dd.load_data(l, m)
			if (lin_or_log):
				x = dd.r/M
			else:
	     			x = np.log10(dd.r/M)
			if log_y:
				y = np.log10(np.abs(dd.phi))
			else:
				y = np.abs(dd.phi)
			if i == 0:
				prefix=""
			else:
				prefix="_"
			ax1.plot(x, y, colours[i] + styles[j], label=prefix+"$\\chi=${:.0f} $l=${:d} $m=$0".format(dd.a, l), linewidth=1)
			# plot fitted solution
	if log_y:
		plt.ylabel("$\\log_{10}(|\\varphi_{lm}|/\\varphi_0)$", fontsize=label_size)
	else:
		plt.ylabel("$|\\varphi_{lm}|/\\varphi_0$", fontsize=label_size)
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
	#ax1.legend(loc="best", fontsize=legend_font_size)
	plt.xticks(fontsize=font_size)
	plt.yticks(fontsize=font_size)
	dd0 = data_dirs[0]
	title = "$\\varphi_{lm}$" + " profiles $M=1,\\mu=0.4,l=m=1,\\tau=${:.1f}".format(dd0.time*dd0.mu) 
	ax1.set_title(title, fontsize=title_font_size)
	plt.tight_layout()
	save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/IsoKerr_mu{:.1f}_l=m=0_lm_phi_{:s}_tau={:.1f}_plot.png".format(0.4, scale, dd0.time*dd0.mu)
	print("saved " + save_name)
	plt.savefig(save_name, transparent=False)
	plt.clf()
	
plot_graph()
