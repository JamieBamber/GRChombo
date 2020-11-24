import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math

start_time = time.time()

# set up parameters 
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Ylm_integration_data/"
file_names = {}
a_list = ["0", "0.99"]
file_names["0"] = "run0067_KNL_l0_m0_a0_Al0_mu1_M1_KerrSchild"
file_names["0.99"] = "run0068_KNL_l0_m0_a0.99_Al0_mu1_M1_KerrSchild"
#lm_list = [(0, 0), (1, 1) (2, 0), (2, 2), (3, 1), (3, 3), (4, 0)]
lm_list = [(0, 0), (2, 0), (4, 0)]
number = 1250
mu = 1
M = 1
phi0 = 0.1
lin_or_log = False
colours = ["r", "b", "g", "c", "m", "y", "k"]
styles = ["-", "--", "-."]
time = 0

### get data and plot profile for each a and each lm

scale = ""
if (lin_or_log):
	scale = "linear"
else:
	scale = "log"

for i in range(0, len(a_list)):
	a = float(a_list[i])
	r_plus = M*(1 + math.sqrt(1 - a**2))
	file_name = file_names[a_list[i]] + "_phi_Ylm_integral_KS_{:s}_n{:06d}_l={:d}_m={:d}.dat"
	dataset_path = data_root_path + file_name
	# generate phi data
	for j in range(0, len(lm_list)):
		l, m = lm_list[j]
		data = np.genfromtxt(dataset_path.format(scale, number, l, m), skip_header=1)
		time = data[1, 0]
		r = data[0,1:]/M
		phi = data[1, 1:]
		if (lin_or_log):
        		x = r
		else:
	     		x = np.log10(r)
		# plot phi
		plt.plot(x, np.log10(phi/phi0), colours[j] + styles[i], label="l={:d} m={:d} mode a={:.2f}".format(l, m, a))
		#
plt.legend(fontsize=8)
plt.ylabel("$\\log_{10}(\\phi_{lm}/\\phi_0)$")
if (lin_or_log):
	xlabel_ = "$r_{KS}/M$"
else:
	xlabel_ = "$\\log_{10}(r_{KS}/M)$"
plt.xlabel(xlabel_)
dt = 0.5
a_max = np.max([float(a_str) for a_str in a_list])
r_plus_min = 1 + np.sqrt(1 - a_max**2)
print("r_plus_min = ", r_plus_min)
if (lin_or_log) :
	plt.xlim((r_plus_min, 100))
else :
	plt.xlim(left=np.log10(r_plus_min))
title = "$\\phi_{lm}$" + " profile KerrSchild M=1 $\\mu$={:.1f}, time = {:.1f}".format(mu, time) 
plt.title(title)
plt.legend(fontsize=8)
plt.tight_layout()
save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/KerrSchild_M{:.1f}_mu{:.1f}_Ylm_m=0_phi_{:s}_t={:.1f}_plot.png".format(M, mu, scale, time)
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
