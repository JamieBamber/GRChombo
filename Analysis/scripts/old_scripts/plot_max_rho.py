import numpy as np
import math
import time
import sys
from matplotlib import rc
rc('text', usetex=True)
from matplotlib import pyplot as plt

#print("yt version = ",yt.__version__)

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"

output_dir = "data/max_rho_data"

half_box = True

KS_or_cartesian_r=True
phi0 = 0.1
R_min = 5
R_max = 500
average_time = False
av_n = 1
plot_mass=False
log_y=True

class data_dir:
	def __init__(self, num, l, m, a, mu, Al, N):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = float(mu)
		self.Al = float(Al)
		self.N = N
		if (N==128):
			Nfix = ""
		else:
			Nfix = "_N{:d}".format(N)
		self.name = "run{:04d}_l{:d}_m{:d}_a{:s}_Al{:s}_mu{:s}_M1_IsoKerr{:s}".format(num, l, m, a, Al, mu, Nfix)
	#
	def load_data(self):
		# load flux and mass data from csv files	
		file_name = home_path + output_dir + "/" + self.name + "_max_rho_full_region.dat"
		data = np.genfromtxt(file_name, skip_header=1)
		print("loaded " + file_name)
		mu = float(self.mu)
		self.t = data[1:,0]
		self.max_rho = data[1:,1]/(0.5*(phi0*mu)**2)
				
data_dirs = []
def add_data_dir(num, l, m, a, mu, Al="0", N=128):
        x = data_dir(num, l, m, a, mu, Al, N)
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

add_data_dir(2, 0, 0, "0.7", "0.4")
#add_data_dir(4, 1, 1, "0.0", "0.4")
add_data_dir(5, 1, 1, "0.7", "0.4")
#add_data_dir(6, 1, 1, "0.99", "0.4")
add_data_dir(7, 2, 2, "0.7", "0.4")
add_data_dir(9, 1, -1, "0.7", "0.4")
add_data_dir(8, 4, 4, "0.7", "0.4")
add_data_dir(10, 8, 8, "0.7", "0.4")
#add_data_dir(15, 1, 1, "0.7", "0.4", "0.5", 64, 64, "0.99")
#add_data_dir(6, 1, 1, "0.99", "0.4", "0", 64, 64, "0.99")
#add_data_dir(16, 1, -1, "0.99", "0.4", "0", 64, 64, "0.99")
#add_data_dir(17, 1, 1, "0.99", "0.4", "0.5", 64, 64, "0.99")
#add_data_dir(18, 1, 1, "0.99", "0.4", "0.25", 64, 64, "0.99")

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
	colours = ['r', 'b', 'g', 'm', 'c', 'y']
	colours2 = ['k', 'm', 'c']
	i = 0
	for dd in data_dirs:
		dd.load_data()
		mu = float(dd.mu)
		label_="$l=${:d} $m=${:d}".format(dd.l, dd.m)
		#label_="$\\chi=${:.2f}".format(dd.a)
		tau = dd.mu*dd.t
		if log_y:
			ax1.plot(tau,np.log10(dd.max_rho),colours[i]+"-", label=label_, linewidth=1)
		else:
			ax1.plot(tau,np.dd.max_rho,colours[i]+"-", label=label_, linewidth=1)
		i = i + 1
	ax1.set_xlabel("$\\tau$", fontsize=label_size)
	ax1.set_xlim((0, 400))
	#ax1.set_ylim((-1.0, 1.0))
	if log_y:
		ax1.set_ylabel("$\\log_{10}($max $\\rho / \\rho_0)$", fontsize=label_size)
	else:
		ax1.set_ylabel("max $\\rho$ / $\\rho_0$", fontsize=label_size)
	ax1.set_title("Max energy density, $M=1$, $\\mu=0.4$, $\\chi=0.7$", wrap=True, fontsize=title_font_size)
	save_path = home_path + "plots/max_rho_IsoKerr_compare_lm.png"
	ax1.legend(loc='best', fontsize=legend_font_size, labelspacing=0.1, handletextpad=1, columnspacing=1)
	plt.xticks(fontsize=font_size)
	plt.yticks(fontsize=font_size)
	plt.tight_layout()
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()
	
plot_graph()

