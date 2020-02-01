import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math

start_time = time.time()

# set up parameters 
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Ylm_integration_data/"
file_name_root = "run0032_KNL_l1_m1_a0_Al0_mu0.4_M1_correct_Ylm_phi_Ylm_integral"
file_name_base = file_name_root + "_l={:d}_m={:d}.dat"
lm_list = [(1, 1), (3, 1), (5, 1)]
true_lm = [1, 1]
a = 0
mu = 0.4
M = 1
r_plus = M*(1 + math.sqrt(1 - a**2))
colours = ["r-", "g-", "b-", "m-"]

time = 0
### get data and plot profile for each lm
for i in range(0, len(lm_list)):
	l, m = lm_list[i]
	file_name = file_name_base.format(l, m)
	dataset_path = data_root_path + file_name
	data = np.genfromtxt(dataset_path, skip_header=1)
	time = data[1, 0]
	R = data[0,1:]
	phi_integral = data[1, 1:]
	r = R*(1 + r_plus/(4*R))**2
	plt.plot(np.log10(r - r_plus), phi_integral, colours[i], label="$l,m = $ {:d},{:d} mode".format(l, m))
plt.xlabel("$\\log_{10}(r_{BL}-r_+)$")
plt.ylabel("$\\phi$ integral")
plt.grid(axis='both')
#plt.ylim((-0.5, 0.5))
dt = 0.5
title = "l{:d}_m{:d}_a{:.1f}_Al0_mu{:.1f} Ylm integral, time = {:.1f}".format(true_lm[0], true_lm[1], a, mu, time) 
plt.title(title)
plt.legend()
plt.tight_layout()
save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/" + file_name_root + "t={:.1f}_plot.png".format(time)
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
