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
	def __init__(self, num, l, m, a, mu, Al):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = mu
		self.Al = Al
		self.name = "run{:04d}_KNL_l{:d}_m{:d}_a{:s}_Al{:s}_mu{:s}_M1_KerrSchild".format(num, l, m, a, Al, mu)

data_dirs = []		
def add_data_dir(num, l, m, a, mu, Al="0"):
	x = data_dir(num, l, m, a, mu, Al)
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

add_data_dir(101, 1, 1, "0.7", "0.4")
add_data_dir(102, 2, 2, "0.7", "0.4")
add_data_dir(103, 0, 0, "0.7", "0.4")
add_data_dir(104, 1, -1, "0.7", "0.4")

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"

output_dir = "data/Y00_integration_data"

half_box = True

KS_or_cartesian_r=True
phi0 = 0.1

inner_or_outer_radius=False
average_time = True
av_n = 1
cumulative=True

def load_data():
	# load data from csv files
	mass_flux_data = {}
	ang_flux_data = {}
	for dd in data_dirs:
		file_name = home_path + output_dir + "/" + dd.name + "_J_rKS_linear_n000000.dat"
		mass_flux_data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		file_name = home_path + output_dir + "/" + dd.name + "_J_azimuth_rKS_linear_n000000.dat"
		ang_flux_data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		print("loaded data for " + dd.name)
	return (mass_flux_data, ang_flux_data) 	

def plot_graph():
	mass_flux_data, ang_flux_data = load_data()
	colours = ['r', 'b', 'g', 'm']
	i = 0
	fig, ax1 = plt.subplots()
	#ax2 = ax1.twinx()	
	for dd in data_dirs:
		t1 = mass_flux_data[dd.num][1:,0]
		t2 = ang_flux_data[dd.num][1:,0]
		mu = float(dd.mu)
		r_min = mass_flux_data[dd.num][0,1]
		r_max = mass_flux_data[dd.num][0,2]
		E0 = 0.5*(4*np.pi*(r_max**3)/3)*(phi0*mu)**2
		if inner_or_outer_radius:
			mass_flux = -mass_flux_data[dd.num][1:,1]*(4*np.pi*r_min**2)/E0
			ang_mom_flux = -ang_flux_data[dd.num][1:,1]*(4*np.pi*r_min**2)/E0
		else:
			mass_flux = -mass_flux_data[dd.num][1:,2]*(4*np.pi*r_max**2)/E0
			ang_mom_flux = -ang_flux_data[dd.num][1:,2]*(4*np.pi*r_max**2)/E0
		if average_time:
			t1 = time_average(t1, av_n)
			t2 = time_average(t2, av_n)
			mass_flux = time_average(mass_flux, av_n)
			ang_mom_flux = time_average(ang_mom_flux, av_n)
		m = abs(dd.m)
		if (dd.m < 0):
			a = -dd.a
		else:
			a = dd.a
		label_ = "ang. mom. flux $l=${:d} $m=${:d} $a=${:.2f}".format(dd.l, dd.m, dd.a)
		#label_ = "ang. mom. flux $l=${:d} $m=${:d} $a=${:.2f} Al={:s}".format(dd.l, dd.m, dd.a, dd.Al)
		ax1.plot(t2,ang_mom_flux,colours[i]+"-", label=label_)
		label_ = "mass flux $l=${:d} $m=${:d} $a=${:.2f}".format(dd.l, dd.m, dd.a)
		#label_ = "mass flux $l=${:d} $m=${:d} $a=${:.2f} Al={:s}".format(dd.l, dd.m, dd.a, dd.Al)
		ax1.plot(t1,mass_flux,colours[i]+"--", label=label_)
		i = i + 1
	ax1.set_xlabel("$t$")
	if cumulative:
		if inner_or_outer_radius:
			ax1.set_ylabel("flux into BH / $E_0$")
			plt.title("Integrated mass and ang. mom. flux into horizon, $M=1$, $\\mu=0.4$")
			save_path = home_path + "plots/mass_ang_mom_flux_into_BH_Kerr_Schild.png"
		else:
			ax1.set_ylabel("flux into r={:.1f}".format(r_max))
			plt.title("Integrated mass and ang. mom. flux into r={:.1f}, $M=1$, $\\mu=0.4$".format(r_max))
			save_path = home_path + "plots/mass_ang_mom_flux_into_r={:.1f}_Kerr_Schild.png".format(r_max)
	else:	
		if inner_or_outer_radius:
			ax1.set_ylabel("flux into BH / $E_0$")
			plt.title("Mass and ang. mom. flux into horizon, $M=1$, $\\mu=0.4$")
			save_path = home_path + "plots/mass_ang_mom_flux_into_BH_Kerr_Schild.png"
		else:
			ax1.set_ylabel("flux into r={:.1f}".format(r_max))
			plt.title("Mass and ang. mom. flux into r={:.1f}, $M=1$, $\\mu=0.4$".format(r_max))
			save_path = home_path + "plots/mass_ang_mom_flux_into_r={:.1f}_Kerr_Schild.png".format(r_max)
	#ax2.set_ylabel("$\\rho$ flux into BH")
	ax1.legend(loc='upper left', fontsize=8)
	#ax2.legend(loc='upper right', fontsize=8)
	#plt.xlim((0, 450))
	#ax1.set_ylim((-5, 5))
	#ax2.set_ylim((-0.05, 0.05))
	plt.tight_layout()
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()

plot_graph()

