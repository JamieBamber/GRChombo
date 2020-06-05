import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math
from scipy.fft import fft, fftshift

start_time = time.time()

# set up parameters 
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Y00_integration_data/"
start_number=0
mu = 1
M = 1
time = 0
n = 4
subdir = "run0068_KNL_l0_m0_a0.99_Al0_mu1_M1"
linlog=True
if linlog:
	scale = "linear"
else:
	scale = "log"

# get data
base_name = subdir + "_KS"
file_name = subdir + "_KerrSchild_phi_{:s}_n{:06d}.dat".format(scale, start_number)
dataset_path = data_root_path + file_name
data = np.genfromtxt(dataset_path, skip_header=1)
time = data[1:, 0]
dt = time[1] - time[0]
R = data[0,1:]
x = data[1:,1:]
print("loaded data")
print("x.shape = ", x.shape)

# Divide the time series into n chunks N long
def find_freq(x, dt, n):
	Nt, Nr = x.shape
	print("Nt, Nr = {:d},{:d}".format(Nt, Nr))
	out_t = np.zeros(n)
	Nchunk = int(float(Nt)/(2*n))
	out_w = np.zeros((2*Nchunk, Nr, n))
	for i in range(0, Nr):	
		# may need to separate real and imag components of w	
		x_chunk = x[0:2*Nchunk,i]
		w = fftshift(fft(x_chunk))/dt
		out_w[:,i,0] = w
		out_t[0] = dt*Nchunk
		for j in range(1, n-1):
			x_chunk = x[(2*j-1)*Nchunk:(2*j+1)*Nchunk,i]
			w = fft(x_chunk)/dt
			out_w[:,i,j] = w
			out_t[j] = dt*2*j*Nchunk
		x_chunk	= x[-2*Nchunk:-1,i]
		w = fftshift(fft(x_chunk))/dt
		out_w[:,i,n-1] = w
		out_t[-1] = dt*(Nt - Nchunk)
		print("done radius {:d} of {:d}".format(i, Nr))
	return (out_w, out_t)
		
out_w, out_t = find_freq(x, dt, 4)

# plot graph
cm = 'magma'
fig, axs = plt.subplots(n, sharex=True)
for i in range(0, n):
	xy = out_w[:,:,i]
	mesh = axs[i].pcolormesh(xy, cmap = cm)
	axs[i].set_ylabel("$\\Tilde{\\phi}(\omega), t={:.1f}".format(out_t[i]))
fig.xlabel("$r_{KS}$")
fig.subplots_adjust(bottom=0.1, top=0.9, left=0.1, right=0.8,hspace=0)
cb_ax = fig.add_axes([0.83, 0.1, 0.02, 0.8])
cbar = fig.colorbar(mesh, cax=cb_ax)
title = "Time Fourier transform of $\\phi$,  a=0.99, l=m=0, M=1, $\\mu$=1" 
plt.title(title)
plt.tight_layout()
# save plot
save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/" + base_name + "fourier_plot.png"
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
