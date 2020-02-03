import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math

start_time = time.time()

# set up parameters 
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Ylm_integration_data/"
file_name_roots = {}
a_list = ["0", "0.99"]
file_name_roots["0"] = "run0036_KNL_l10_m1_a0_Al0_mu0.4_M1_correct_Ylm_phi_Ylm_integral"
file_name_roots["0.7"] = "run0040_KNL_l10_m1_a0.7_Al0_mu0.4_M1_correct_Ylm_phi_Ylm_integral"
file_name_roots["0.99"] = "run0038_KNL_l10_m1_a0.99_Al0_mu0.4_M1_correct_Ylm_phi_Ylm_integral"
lm_list = [(10, 1), (8, 1), (2, 1)]
true_lm = [10, 1]
mu = 0.4
M = 1
colours = ["r", "g", "b", "m"]
styles = ["--", "-."]
time = 0

### get data and plot profile for each a and each lm

log_x = False

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
		if log_x:
			plt.plot(np.log10(r - r_plus), phi_integral, colours[j] + styles[i], label="$a = ${:.2f} $l,m = $ {:d},{:d} mode".format(a, l, m))
		else:	
			plt.plot(r - r_plus, phi_integral, colours[j] + styles[i], label="$a = ${:.2f} $l,m = $ {:d},{:d} mode".format(a, l, m))
if log_x:
	plt.xlabel("$\\log_{10}(r_{BL}-r_+)$")
else:
	plt.xlabel("$r_{BL}-r_+$")
plt.ylabel("$\\phi$ integral")
plt.grid(axis='both')
#plt.ylim((-0.5, 0.5))
dt = 0.5
title = "l{:d}_m{:d}_Al0_mu{:.1f} Ylm integral, time = {:.1f}".format(true_lm[0], true_lm[1], mu, time) 
plt.title(title)
plt.legend(fontsize=8)
plt.tight_layout()
if log_x:
	save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/phi_Ylm_integral_log10_l={:d}_m={:d}_t={:.1f}_plot.png".format(true_lm[0], true_lm[1], time)
else:
	save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/phi_Ylm_integral_l={:d}_m={:d}_t={:.1f}_plot.png".format(true_lm[0], true_lm[1], time)	
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
