import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math

start_time = time.time()

# set up parameters 
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Ylm_integration_data/"
file_name_roots = {}
a_list = ["0.99"]
file_name_roots["0.99"] = "run0022_KNL_l0_m0_a0_Al0_mu1_M1_KerrSchild_phi_Ylm_integral"
lm_list = [(0, 0), (2, 0), (4, 0)]
true_lm = [0, 0]
mu = 0.4
M = 1
colours = ["r-", "g--", "b-.", "m"]
styles = ["--", "-", "-."]
time = 0

### get data and plot profile for each a and each lm

use_r_star = True

for i in range(0, len(a_list)):
	a = float(a_list[i])
	r_plus = M*(1 + math.sqrt(1 - a**2))
	r_minus = M*(1 - math.sqrt(1 - a**2))
	file_name_root = file_name_roots[a_list[i]]
	file_name_base = file_name_root + "_l={:d}_m={:d}.dat"
	for j in range(0, len(lm_list)):
		l, m = lm_list[j]
		file_name = file_name_base.format(l, m)
		dataset_path = data_root_path + file_name
		data = np.genfromtxt(dataset_path, skip_header=1)
		time = data[1, 0]
		R = data[0,1:]
		phi_integral = np.log(data[1, 1:])
		r = R*(1 + r_plus/(4*R))**2
		r_star = r + ((r_plus**2)*np.log(r - r_plus) - (r_minus**2)*np.log(r - r_minus))/(r_plus - r_minus) 
		if use_r_star:
			plt.plot(r_star, phi_integral, colours[j], label="$a = ${:.2f} $l,m = $ {:d},{:d} mode".format(a, l, m))
		else:	
			plt.plot(r - r_plus, phi_integral, colours[j] + styles[i], label="$a = ${:.2f} $l,m = $ {:d},{:d} mode".format(a, l, m))
if use_r_star:
	plt.xlabel("$r_*$")
else:
	plt.xlabel("$r_{BL}-r_+$")
plt.ylabel("ln($\\phi$ integral)")
plt.grid(axis='both')
#plt.ylim((-0.5, 0.5))
title = "l={:d} m={:d} $\mu=${:.1f} $Y^m_l$ integral, time = {:.1f}".format(true_lm[0], true_lm[1], mu, time) 
plt.title(title)
plt.legend(fontsize=8)
plt.tight_layout()
subdir = file_name_roots[a_list[0]]
if use_r_star:
	save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/phi_Ylm_integral_r_star_{:s}_t={:.1f}_log.png".format(subdir, time)
else:
	save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/phi_Ylm_integral_l={:d}_m={:d}_t={:.1f}_plot_v2.png".format(true_lm[0], true_lm[1], time)	
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
