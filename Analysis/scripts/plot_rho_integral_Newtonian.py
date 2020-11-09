import numpy as np
import math
import time
import sys
from matplotlib import rc
rc('text', usetex=True)
from matplotlib import pyplot as plt

# set up parameters
data_root_path = "/cosma6/data/dp174/dc-bamb1/GRChombo_data/NewtonianBinaryBHScalar/"
home_path="/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots"

half_box = True

phi0 = 0.1
#R_min = 5
R_max = 300
average_time = False
av_n = 1
plot_mass=False
cumulative=True
Theta_max="1.0"
Ntheta=18
Nphi=64

r_max = 

class data_dir:
	def __init__(self, num, M, d, mu, dt):
		self.num = num
		self.M = M
		self.d = d
		self.mu = mu
		self.dt = dt
		self.name = "run{:04d}_M{:s}_d{:s}_mu{:s}_dt_mult{:s}".format(M, d, mu, dt)
	#
	def load_data(self):
		# load flux and mass data from csv files	
		file_name = data_root_path + self.name + "/outputs/" + "RhoIntegral.dat"
		data = np.genfromtxt(file_name, skip_header=1)
		print("loaded " + file_name)
		self.time = flux_data[:,0]
		mu = float(self.mu)
		E0 = 0.5*(4*np.pi*(self.r_max**3)/3)*(phi0*mu)**2
		self.rho_integral = (flux_data[:,1] - flux_data[0,1])/E0
		self.rhoJ_integral = (flux_data[:,2] - flux_data[0,2])/E0
				
data_dirs = []
def add_data_dir(num, M, d, mu, dt):
        x = data_dir(num, M, d, mu, dt)
        data_dirs.append(x)

# choose datasets to compare

add_data_dir(1, "0.1", "10", "0.014142136", "0.25")
add_data_dir(2, "0.1", "10", "0.005", "0.25")
add_data_dir(3, "0.1", "10", "0.02", "0.25")
add_data_dir(4, "0.1", "10", "0.1", "0.25")

def plot_graph():
	# plot setup
	ax1 = plt.axes()
	fig = plt.gcf()
	fig.set_size_inches(3.8,3)
	font_size = 10
	title_font_size = 10
	label_size = 10
	legend_font_size = 8
	rc('xtick',labelsize=font_size)
	rc('ytick',labelsize=font_size)
	#
	colours = ['r', 'b', 'g', 'm', 'c', 'y']
	i = 0
	for dd in data_dirs:
		dd.load_data()
		mu = float(dd.mu)
		label_ = "$\\mu$={:s} $m$={:d}".format(dd.l, dd.m)
		ax1.plot(dd.time,dd.rho_integral,colours[i]+"-", label=label_, linewidth=1)
		i = i + 1
	ax1.set_xlabel("$t$", fontsize=label_size)
	#ax1.set_xlim((0, 500))
	#ax1.set_ylim((-0.15, 0.15))
	ax1.set_ylabel("$change in \\rho$ integral / $E_0$", fontsize=label_size)
	ax1.set_title("Change in integrated density, $M=0.1,d=10", wrap=True, fontsize=title_font_size)
	save_path = home_path + "plots/Newtonian_Scalar_change_in_rho_integral_vs_mu.png".format(R_max)
	ax1.legend(loc='upper left', ncol=2, fontsize=legend_font_size)
	plt.xticks(fontsize=font_size)
	plt.yticks(fontsize=font_size)
	plt.tight_layout()
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()
	
plot_graph()

