import yt
import numpy as np
import math
from yt import derived_field
from yt.units import cm
import time
import sys
from matplotlib import pyplot as plt

#print("yt version = ",yt.__version__)

yt.enable_parallelism()

class data_dir:
	def __init__(self, num, l, m, a, mu, nphi, ntheta, suffix):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = mu
		self.nphi = nphi
		self.ntheta = ntheta
		self.suffix = suffix
		self.name = "run{:04d}_KNL_l{:d}_m{:d}_a{:s}_Al{:s}_mu{:s}_M1_KerrSchild".format(num, l, m, a, "0", mu)

data_dirs = []		
def add_data_dir(num, l, m, a, mu, nphi, ntheta, suffix=""):
	x = data_dir(num, l, m, a, mu, nphi, ntheta, suffix)
	data_dirs.append(x)

def time_average(x, n):
	N = len(x)
	n_chunks = int(np.floor(N/n))
	x_out = np.zeros(n_chunks)
	for i in range(0, n_chunks):
		x_out[i] = np.mean(x[i*n:(i+1)*n])
	x_out[-1] = np.mean(x[N-n:])
	return x_out

# choose datasets to compare

#add_data_dir(101, 1, 1, "0.7", "0.4", 75, 63)
#add_data_dir(101, 1, 1, "0.7", "0.4", 123, 123)
add_data_dir(103, 0, 0, "0.7", "0.4", 16, 32, "_theta_max1.0")
#add_data_dir(102, 2, 2, "0.7", "0.4")
#add_data_dir(103, 0, 0, "0.7", "0.4")
#add_data_dir(104, 1, -1, "0.7", "0.4")
#add_data_dir(105, 0, 0, "0.99", "0.4")
#add_data_dir(106, 1, 1, "0.99", "0.4")
#add_data_dir(107, 4, 4, "0.7", "0.4")
#add_data_dir(108, 2, 2, "0.7", "0.8")
#add_data_dir(109, 8, 8, "0.7", "0.4")
#add_data_dir(110, 1, 1, "0.7", "0.05")
#add_data_dir(111, 1, 1, "0.7", "1")

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"

output_dir = "data/flux_data"

half_box = True

KS_or_cartesian_r=True
phi0 = 0.1
r_max = 450
average_time = False
av_n = 1
cumulative=False
plot_mass=False

def load_flux_data():
	# load data from csv files
	data = {}
	ang_flux_data = {}
	for dd in data_dirs:
		file_name = home_path + output_dir + "/" + dd.name + "_J_rKS_linear_n000000_nphi{:d}_ntheta{:d}{:s}.dat".format(dd.nphi, dd.ntheta, dd.suffix)
		data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		#file_name = home_path + output_dir + "/" + dd.name + "_J_azimuth_rKS_linear_n000000.dat"
		#ang_flux_data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		print("loaded flux data for " + dd.name)
	return data 	

def load_mass_data():
        # load data from csv files
        data = {}
        print(data_dirs)
        for dd in data_dirs:
                file_name = home_path + "data/mass_data" + "/" + "{:s}_mass_in_r={:d}_chombo.dat".format(dd.name, r_max)
                data_line = np.genfromtxt(file_name, skip_header=1)
                data[dd.num] = data_line
                print("loaded mass data for " + file_name)
        return data

def plot_graph():
	flux_data = load_flux_data()
	if plot_mass:
		mass_data = load_mass_data()
	colours = ['r', 'b', 'g', 'm', 'y', 'c']
	i = 0
	fig, ax1 = plt.subplots()
	#ax2 = ax1.twinx()	
	for dd in data_dirs:
		flux_line_data = flux_data[dd.num]
		mu = float(dd.mu)
		tflux = flux_line_data[1:,0]
		#r_min = line_data[0,1]
		#r_max = line_data[0,2]
		E0 = 0.5*(4*np.pi*(r_max**3)/3)*(phi0*mu)**2
		inner_mass_flux = -flux_line_data[1:,1]*(4*np.pi)/E0
		outer_mass_flux = -flux_line_data[1:,2]*(4*np.pi)/E0
		if average_time:
			t1 = time_average(t1, av_n)
			inner_mass_flux = time_average(inner_mass_flux, av_n)
			outer_mass_flux = time_average(outer_mass_flux, av_n)
		if cumulative:
			inner_mass_flux = np.cumsum(inner_mass_flux)
			outer_mass_flux = np.cumsum(outer_mass_flux)
		net_flux = outer_mass_flux - inner_mass_flux
		#label_ = "$\\mu$={:.2f}".format(mu)
		label_ = "$l$={:d} $m$={:d}".format(dd.l, dd.m)
		ax1.plot(tflux,inner_mass_flux,colours[i]+"--", label="flux into BH " + label_)
		ax1.plot(tflux,outer_mass_flux,colours[i]+"-.", label="flux into r={:.1f} ".format(r_max)+label_)
		ax1.plot(tflux,net_flux,colours[i]+"-", label="net flux " + label_)
		#
		if plot_mass:
			mass_line_data = mass_data[dd.num]
			delta_mass = mass_line_data[1:,1] - mass_line_data[0,1]
			tmass = mass_line_data[1:,0]
			ax1.plot(tmass,delta_mass/E0,colours[i+1]+"-", label="change in mass $r_+<r<$"+str(r_max)+" "+label_)
		i = i + 1
	ax1.set_xlabel("$t$")
	#ax1.set_xlim((0, 300))
	#ax1.set_ylim((-0.0005, 0.0015))
	dd0 = data_dirs[0]
	if cumulative:
		ax1.set_ylabel("cumulative flux / $E_0$")
		plt.title("Cumulative mass flux, $M=1$, $a=0.7$, $\\mu=0.4$")
		save_path = home_path + "plots/mass_flux_Kerr_Schild_cumulative_nphi{:d}_ntheta{:d}{:s}.png".format(dd.nphi, dd.ntheta, dd.suffix)
	else:
		ax1.set_ylabel("flux / $E_0$")
		plt.title("Mass flux, $M=1$, $\\mu=0.4$ $n_{\\phi}=$"+str(dd.nphi)+" $n_{\\theta}=$"+str(dd.ntheta))
		save_path = home_path + "plots/mass_flux_Kerr_Schild_nphi{:d}_ntheta{:d}{:s}.png".format(dd.nphi, dd.ntheta, dd.suffix)
	ax1.legend(loc='upper left', fontsize=8)
	plt.tight_layout()
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()

plot_graph()

