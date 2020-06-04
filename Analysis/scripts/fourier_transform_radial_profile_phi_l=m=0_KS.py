import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math
from scipy.fft import fft

start_time = time.time()

# set up parameters 
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Y00_integration_data/"
start_number=0
mu = 1
M = 1
time = 0
subdir = "run0068_KNL_l0_m0_a0.99_Al0_mu1_M1"
linlog=True
if linlog:
	scale = "linear"
else:
	scale = "log"

# get data
file_name = subdir + "_KerrSchild_phi_{:s}_n{:06d}.dat".format(scale, start_number)
dataset_path = data_root_path + file_name
data = np.genfromtxt(dataset_path, skip_header=1)
time = data[1:, 0]
dt = time[1] - time[0]
R = data[0,1:]
x = data[1:,1:]

# Divide the time series into n chunks N long
def find_freq(x, dt, n)
	Nt, Nr = x.shape
	out_w = np.zeros((Nr, Nt, n))
	out_t = np.zeros(n)
	Nchunk = 2*int(Nt/(2*n))
	for i in range(1, n):
		for j in range(0, Nr):		

	w = fft(x)


# plot graph
plt.plot(r_star, phi_integral, colours[i] + styles[i], label="$a = 0 $l,m = 0$")
plt.xlabel("$r_*$")
plt.ylabel("$\\phi$ integral")
plt.grid(axis='both')
#plt.ylim((-0.5, 0.5))
dt = 0.5
title = "$\\Phi$ profile KerrSchild a=l=m=0 M=$\\mu$=1, time = {:.1f}".format(true_lm[0], true_lm[1], mu, time) 
plt.title(title)
plt.legend(fontsize=8)
plt.tight_layout()
save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/" + file_names["0"] + "_t={:.1f}_plot.png".format(time)
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
