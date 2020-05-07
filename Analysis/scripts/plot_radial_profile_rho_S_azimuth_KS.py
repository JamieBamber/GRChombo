import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math

start_time = time.time()

# set up parameters 
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Y00_integration_data/"
file_names = {}
a_list = ["0", "0.99"]
file_names["0"] = "run0067_KNL_l0_m0_a0_Al0_mu1_M1_KerrSchild"
file_names["0.99"] = "run0068_KNL_l0_m0_a0.99_Al0_mu1_M1_KerrSchild"
number = 1250
mu = 1
M = 1
lin_or_log = False
rho_colours = ["r-", "g--"]
J_colours = ["b-", "b--"]
time = 0

### get data and plot profile for each a and each lm

scale = ""
if (lin_or_log):
	scale = "linear"
else:
	scale = "log"

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
for i in range(0, len(a_list)):
	a = float(a_list[i])
	r_plus = M*(1 + math.sqrt(1 - a**2))
	file_name = file_names[a_list[i]] + "_{:s}_{:s}_n{:06d}.dat"
	dataset_path = data_root_path + file_name
	# generate rho data
	data = np.genfromtxt(dataset_path.format("rho", scale, number), skip_header=1)
	time = data[1, 0]
	r = data[0,1:]/M
	rho = data[1, 1:]
	if (lin_or_log):
        	x = r
	else:
	     	x = np.log10(r)
	# generate S_azimuth data	
	data = np.genfromtxt(dataset_path.format("J_azimuth", "linear", number), skip_header=1)
	S_azimuth = data[1, 1:]		
	# plot rho
	ax1.plot(x, np.log10(rho), rho_colours[i], label="$\\ln(\\rho_E)$ l=m=0 a={:.2f}".format(a))
	# plot S_azimuth
	ax2.plot(x, S_azimuth, J_colours[i], label="$\\rho_J$ l=m=0 a={:.2f}".format(a))
	#
ax1.legend(fontsize=8, loc="upper left")
ax2.legend(fontsize=8, loc="upper right")
ax2.set_ylabel("$\\rho_J$")
ax1.set_ylabel("$\\ln(\\rho_E)$")
if (lin_or_log):
	xlabel_ = "$r_{KS}/M$"
else:
	xlabel_ = "$\\log_{10}(r_{KS}/M)$"
ax1.set_xlabel(xlabel_)
dt = 0.5
ax2.set_ylim((-10**-6, 10**-6))
a_max = np.max([float(a_str) for a_str in a_list])
r_plus_min = 1 + np.sqrt(1 - a_max**2)
print("r_plus_min = ", r_plus_min)
if (lin_or_log) :
	plt.xlim((1.0, 100))
else :
	plt.xlim(left=np.log10(r_plus_min))
title = "$\\rho_E$ and $\\rho_J$ profile KerrSchild M=1 $\\mu$={:.1f}, time = {:.1f}".format(mu, time) 
plt.title(title)
plt.legend(fontsize=8)
plt.tight_layout()
save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/KerrSchild_M{:.1f}_mu{:.1f}_l0_m0_rho_S_azimuth_{:s}_t={:.1f}_plot.png".format(M, mu, scale, time)
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
