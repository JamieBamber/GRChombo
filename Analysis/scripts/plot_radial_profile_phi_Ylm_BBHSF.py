import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math

start_time = time.time()

# set up parameters 
data_root_path = "../data/Ylm_integration_data/"
file_name_root = "run0004_FlatScalar_mu0.4_G0_phi"
lm_list = [(0, 0), (1, 1), (2, 2)]
mu = 0.4
colours = ["r", "g", "b", "m"]
styles = ["--", "-", "-."]
time = 0

### get data and plot profile for each a and each lm

log_x = False

file_name_base = file_name_root + "_Ylm_integral_l={:d}_m={:d}.dat"
for j in range(0, len(lm_list)):
	i = 1
	l, m = lm_list[j]
	file_name = file_name_base.format(l, m)
	dataset_path = data_root_path + file_name
	data = np.genfromtxt(dataset_path, skip_header=1)
	time = data[1, 0]
	R = data[0,1:]
	phi_integral = data[1, 1:]
	if log_x:
		plt.plot(np.log10(R), np.log10(phi_integral), colours[j] + styles[i], label="$l,m = $ {:d},{:d} mode".format(l, m))
	else:	
		plt.plot(R, np.log10(phi_integral), colours[j] + styles[i], label="$l,m = $ {:d},{:d} mode".format(l, m))
if log_x:
	plt.xlabel("$\\log_{10}(R)$")
else:
	plt.xlabel("$R$")
plt.ylabel("$\\log_{10}(\\phi_{lm})$")
plt.grid(axis='both')
#plt.ylim((-0.5, 0.5))
dt = 0.5
title = "Binary BH Scalar Field mu{:.1f} G0 Ylm integral, time = {:.1f}".format(mu, time) 
plt.title(title)
plt.legend(fontsize=8)
plt.tight_layout()
if log_x:
	save_name = "../plots/" + file_name_root + "_phi_Ylm_integral_log10_t={:.1f}_plot.png".format(time)
else:
	save_name =  "../plots/" + file_name_root + "_phi_Ylm_integral_t={:.1f}_plot.png".format(time)
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
