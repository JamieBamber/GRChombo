import yt
import numpy as np
import math
from yt import derived_field
from yt.units import cm
import time
import sys
from matplotlib import pyplot as plt

#print("yt version = ",yt.__version__)

#yt.enable_parallelism()

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

# choose datasets to compare

"""add_data_dir(74, 0, 0, "0.7", "0.4")
add_data_dir(39, 1, 1, "0.7", "0.4")
add_data_dir(76, 5, 5, "0.7", "0.4")
add_data_dir(77, 2, 2, "0.7", "0.4")"""

#add_data_dir(78, 1, -1, "0.7", "0.4")
#add_data_dir(75, 1, 1, "0.7", "0.4", "0.5")
#add_data_dir(77, 2, 2, "0.7", "0.4")
#add_data_dir(80, 1, 1, "0", "0.4")

#add_data_dir(39, 1, 1, "0.7", "0.4")
#add_data_dir(73, 4, 4, "0.7", "0.4")
#add_data_dir(74, 0, 0, "0.7", "0.4")
#add_data_dir(71, 1, 1, "0.99", "0.4")
#add_data_dir(72, 1, -1, "0.99", "0.4")

#add_data_dir(67, 0, 0, "0", "1")
#add_data_dir(79, 0, 0, "0.7", "1")
#add_data_dir(68, 0, 0, "0.99", "1")

add_data_dir(101, 1, 1, "0.7", "0.4")
"""add_data_dir(102, 2, 2, "0.7", "0.4")
add_data_dir(103, 0, 0, "0.7", "0.4")
add_data_dir(104, 1, -1, "0.7", "0.4")
add_data_dir(105, 0, 0, "0.99", "0.4")
add_data_dir(106, 1, 1, "0.99", "0.4")
add_data_dir(107, 4, 4, "0.7", "0.4")
add_data_dir(108, 2, 2, "0.7", "0.8")
add_data_dir(109, 8, 8, "0.7", "0.4")
add_data_dir(110, 1, 1, "0.7", "0.05")
add_data_dir(111, 1, 1, "0.7", "1")"""

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"
M = 1
dr = 0.1
phi0 = 0.1
number = 950

output_dir = "data/compare_almmu_flux"

half_box = True

KS_or_cartesian_r=True
change_in_E = True
r_max = 450

if KS_or_cartesian_r:
	# use the correct horizon but with cartesian radial projection
	r_txt="KSr_v1"
else:
	r_txt="cartesian_R"

def spheroid_area(r, a, M):
	area = np.pi*( 2*M*r + (r**2)*np.sqrt(2*M*r)*np.arcsinh(a*M/r)/(a*M) )
	return area

def calculate_mass_flux_in_sphere(dd):
	data_sub_dir = dd.name
	a = dd.a	
	aM = a*M
	r_plus = M*(1 + math.sqrt(1 - a**2))
	min_R = np.sqrt(2*M*r_plus)
	r_min = r_plus

	start_time = time.time()
	
	# load dataset time series
	
	dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_{:06d}.3d.hdf5".format(number)
	dsi = yt.load(dataset_path) # this loads a dataset time series
	print("loaded data from ", dataset_path)
	print("time = ", time.time() - start_time)

	# set centre
	center = [512.0, 512.0, 0]
	L = 512.0	

	#if KS_or_cartesian_r:
	# derived fields
	@derived_field(name = "r_KS", units = "")
	def _r_KS(field, data):
		R = data["spherical_radius"]/cm
		z = data["z"]/cm
		r_KS_sqrd = (R**2 - aM**2)/2 + np.sqrt(((R**2 - aM**2)**2)/4 + (aM*z)**2)
		r_KS = np.sqrt(r_KS_sqrd)
		return r_KS
			
	current_time = dsi.current_time 
	dt = 2.5
	i = int(current_time/dt)
	#if (i % 2 == 0):
	time_0 = time.time()
	# store time
	
	# make sphere (defined by r_KS)
	ad = dsi.all_data()
	r = r_min
	shell = ad.cut_region(["(obj['r_KS'] < {:.7f}) & (obj['r_KS'] > {:.7f})".format(r+dr, r)])
	area = spheroid_area(r, a, M)
	shell_mass = shell.sum("cell_volume")
	print("shell_mass = ", shell_mass)
	#
	"""shell = dsi.sphere(center, min_R+dR) - dsi.sphere(center, min_R)
	area = 2*np.pi*min_R**2"""		
	# calculate radial (in terms of cartesian radius R) momentum and angular momentum flux in shell
	meanJ_r = shell.mean("J_rKS", weight="cell_volume")
	meanJ_azimuth_r = shell.mean("J_azimuth_rKS", weight="cell_volume")
	print("time = ", current_time)
	print("r = ", r)
	print("meanJ_r = ", meanJ_r)
	print("meanJ_azimuth_r = ", meanJ_azimuth_r)
	print("area = ", area)
	J_r = meanJ_r*area
	J_azimuth_r = meanJ_azimuth_r*area

	width=5.0
	#slice = dsi.r[:,512.0,:] # slice through xz axis
	p = yt.SlicePlot(shell, 'y', 'r_KS', center=[512.0, 512.0, 0.25*width])
	p.set_width((0.5*width, width))
	#p.set_zlim('r_KS', 0.01, 0.75*width)
	p.show_colorbar()
	p.set_minorticks('all', True)
	p.set_cbar_minorticks('r_KS', True)
	test_plot_name = "test_r_KS_plot"
	p.save(test_plot_name)
	plt.clf()
	
def load_data():
	# load data from csv files
	data = {}
	for dd in data_dirs:
		file_name = home_path + output_dir + "/" + dd.name + "_flux_{:s}_v1.csv".format(r_txt)
		data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		print("loaded data for " + dd.name)
	return data 	

def plot_graph():
	data = load_data()
	colours = ['r', 'b', 'g', 'm']
	i = 0
	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()	
	for dd in data_dirs:
		line_data = data[dd.num]
		t = line_data[:,0]
		mu = float(dd.mu)
		mass_flux = -line_data[:,1]
		ang_mom_flux = line_data[:,2]
		F0 = (mu**2)*phi0
		m = abs(dd.m)
		label_ = "ang. mom. flux $l=${:d} $m=${:d} $a=${:.2f}".format(dd.l, dd.m, dd.a)
		#label_ = "ang. mom. flux $l=${:d} $m=${:d} $a=${:.2f} Al={:s}".format(dd.l, dd.m, dd.a, dd.Al)
		ax1.plot(t,ang_mom_flux,colours[i]+"-", label=label_)
		label_ = "mass flux $l=${:d} $m=${:d} $a=${:.2f}".format(dd.l, dd.m, dd.a)
		#label_ = "mass flux $l=${:d} $m=${:d} $a=${:.2f} Al={:s}".format(dd.l, dd.m, dd.a, dd.Al)
		ax2.plot(t,mass_flux,colours[i]+"--", label=label_)
		i = i + 1
	ax1.set_xlabel("$t$")
	ax1.set_ylabel("$\\rho_{\phi}$ flux into BH")
	ax2.set_ylabel("$\\rho$ flux into BH")
	ax1.legend(loc='upper left', fontsize=8)
	ax2.legend(loc='upper right', fontsize=8)
	plt.title("Mass and Angular Mom. flux into horizon, $M=1$, $\\mu=0.4$")
	#plt.xlim((0, 450))
	#plt.ylim((0, 0.004))
	plt.tight_layout()
	save_path = home_path + "plots/mass_ang_mom_flux_into_BH_Kerr_Schild_{:s}.png".format(r_txt)
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()

for dd in data_dirs:
	calculate_mass_flux_in_sphere(dd)

#plot_graph()

