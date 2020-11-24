import yt
import numpy as np
import math
from yt import derived_field
from yt.units import cm
import time
import sys
from matplotlib import pyplot as plt

#print("yt version = ",yt.__version__)

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"
subdir = "run0103_KNL_l0_m0_a0.7_Al0_mu0.4_M1_KerrSchild"

phi0 = 0.1
r_max = 450
mu = 0.4
E0 = 0.5*(4*np.pi*(r_max**3)/3)*(phi0*mu)**2

def load_mass_data(suffix):
        # load data from csv files
        file_name = home_path + "data/mass_data" + "/" + "{:s}_mass_in_r{:s}.dat".format(subdir, suffix)
        data = np.genfromtxt(file_name, skip_header=1)
        print("loaded mass data for " + file_name)
        return data

r_min_max_list = [("0", "10"), ("10", "450"), ("2.1", "450"), ("0", "2.1"), ("0", "450")]

for i in range(0, len(r_min_max_list)):
	rmin, rmax = r_min_max_list[i] 
	data = load_mass_data("{:s}_to_{:s}".format(rmin, rmax))
	print("t = ", data[0])
	print("mass {:s}<r<{:s} = ".format(rmin, rmax), data[1])

def plot_graph():
	colours = ['r', 'b', 'g', 'm', 'y', 'c']

	
	plt.plot(data1[:,0], data1[:,1]/E0, colours[0]+'-', label="mass in $r_+ < r < 450$")
	plt.plot(data2[0], data2[1]/E0, colours[1]+'-', label="mass in $4 < r < 450$")
	plt.plot(data3[0], data3[1]/E0, colours[2]+'-', label="mass in $10 < r < 450$")
	plt.plot(data4[0], data4[1]/E0, colours[3]+'-', label="mass in $0 < r < 10$")
	plt.xlabel("$t$")
	plt.ylabel("integrated mass / $E_0$")
	plt.title("Integrated mass $\\chi=0.7, l=m=0, \\mu=0.4, M=1$, KS coordinates")
	plt.legend(loc='upper left', fontsize=8)
	plt.tight_layout()
	save_path = home_path + "plots/" + subdir + "_test_mass_integrals.png"
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()

#plot_graph()

