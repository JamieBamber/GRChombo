import numpy as np
import time
import sys
from matplotlib import rc
rc('text', usetex=True)
import matplotlib.pyplot as plt
import math
from scipy.signal import argrelextrema

# set up parameters 
phi0 = 0.1
R_min = 5
R_max = 500
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
log_x = False

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
	def load_data(self):
		file_name = self.name+"_phi_Y00_integral_{:s}_r_plus_to_{:d}_nphi{:d}_ntheta{:d}_theta_max{:.1f}.dat".format(scale, R_max, self.nphi, self.ntheta, self.theta_max)
		dataset_path = data_root_path + file_name
		data = np.genfromtxt(dataset_path, skip_header=1)
		start_num = 10
		self.time = data[start_num:,0]
		self.max_extrema = np.zeros(len(self.time))
		R = data[0,1:]
		r_plus = M*(1 + np.sqrt(1 - self.a**2))
		self.r = R*(1 + r_plus/(4*R))**2
		for i in range(0, len(self.time)):
			# local maxima and minima
			max_indices = argrelextrema(data[start_num+i,1:], np.greater)
			min_indices = argrelextrema(data[start_num+i,1:], np.less)
			max_extrema_index = max(np.max(max_indices), np.max(min_indices)) 
			self.max_extrema[i] = self.r[max_extrema_index]
		print("got data for " + file_name)		

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

#add_data_dir(16, 1, -1, "0.99", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(17, 1, 1, "0.99", "0.4", "0.5", 64, 64, "_theta_max0.99")
#add_data_dir(18, 1, 1, "0.99", "0.4", "0.25", 64, 64, "_theta_max0.99")
add_data_dir(21, 0, 0, "0.7", "2.0", "0", 64, 18, "1.0")

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
		dd.load_data()
		if log_x:
			x = np.log10(dd.time/M)
		else:
			x = dd.time/M
		if log_y:
			y = np.log10(dd.max_extrema/M)
			y_free_fall = np.log10((np.sqrt(2)*dd.time/(M*np.pi))**(2/3))
			y_light = np.log10((dd.time/M))
		else:
			y = dd.max_extrema/M
			y_free_fall = (np.sqrt(2)*dd.time/(M*np.pi))**(2/3)
			y_light = dd.time/M
		ax1.plot(x, y, colours[0] + "x", label="_turning point", linewidth=1)
		ax1.plot(x, y_free_fall, colours[1] + "-.", label="freefall distance", linewidth=2)
		ax1.plot(x, y_light, colours[2] + "--", label="light travel distance", linewidth=2)
	if log_y:
		ax1.set_ylabel("$\\log_{10}(r_{\\textup{turning point}}/M)$", fontsize=label_size)
	else:
		ax1.set_ylabel("$r_{\\textup{turning point}}/M$", fontsize=label_size)
	if log_x:
		xlabel_ = "$\\log_{10}(t/M)$"
	else:
		xlabel_ = "$t/M$"
	plt.xlabel(xlabel_, fontsize=label_size)
	ax1.legend(loc="best", fontsize=legend_font_size)
	plt.xticks(fontsize=font_size)
	plt.yticks(fontsize=font_size)
	dd0 = data_dirs[0]
	title = "Outermost $\\varphi$ turning point vs time \n $M=1,\\mu=2.0,\\chi=0.7,l=m=0$" 
	ax1.set_title(title, fontsize=title_font_size)
	plt.tight_layout()
	save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/IsoKerr_mu{:.1f}_l=m=0_phi_{:s}_Rmax={:d}_propagation_speed_linear.png".format(2.0, scale, R_max)
	print("saved " + save_name)
	plt.savefig(save_name, transparent=False)
	plt.clf()
	
plot_graph()
