import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math

start_time = time.time()

# set up parameters 
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Ylm_integration_data/"
file_name_roots = {}
a_list = ["0"]
file_name_roots["0"] = "run0022_KNL_l0_m0_a0_Al0_mu1_M1" + "_phi_Ylm_integral"
lm_list = [(0, 0)]
true_lm = [0, 0]
mu = 1
M = 1
colours = ["r", "g", "b", "m"]
styles = ["-", "--", "-."]
time = 0

### get data and plot profile for each a and each lm

for i in range(0, len(a_list)):
	a = float(a_list[i])
	r_plus = M*(1 + math.sqrt(1 - a**2))
	file_name_root = file_name_roots[a_list[i]]
	file_name_base = file_name_root + "_l={:d}_m={:d}.dat"
	for j in range(0, len(lm_list)):
		l, m = lm_list[j]
		file_name = file_name_base.format(l, m)
		dataset_path = data_root_path + file_name
		data = np.genfromtxt(dataset_path, skip_header=1)
		time = data[1, 0]
		R = data[0,1:]
		phi_integral = data[1, 1:]
		r = R*(1 + r_plus/(4*R))**2
		r_star = r/r_plus + np.log(r/r_plus - 1)
		plt.plot(r_star, phi_integral, colours[j] + styles[i], label="$a = ${:.2f} $l,m = $ {:d},{:d} mode".format(a, l, m))
plt.xlabel("$r_*$")
plt.ylabel("$\\phi$ integral")
plt.grid(axis='both')
plt.xlim((-10, 50))
#plt.ylim((-0.5, 0.5))
dt = 0.5
title = "l{:d}_m{:d}_Al0_mu{:.1f} Ylm integral, time = {:.1f}".format(true_lm[0], true_lm[1], mu, time) 
plt.title(title)
plt.legend(fontsize=8)
plt.tight_layout()
save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/phi_Ylm_integral_l={:d}_m={:d}_t={:.1f}_plot.png".format(true_lm[0], true_lm[1], time)	
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
