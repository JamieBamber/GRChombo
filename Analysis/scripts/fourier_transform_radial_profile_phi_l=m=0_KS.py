import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math
from scipy.fft import fft, fftshift, fftfreq

start_time = time.time()

# set up parameters 
data_root_path = "/home/dc-bamb1/GRChombo/Analysis/data/Y00_integration_data/"
start_number=0
mu = 1
M = 1
time = 0
n = 2
subdir = "run0067_KNL_l0_m0_a0_Al0_mu1_M1"
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
dt = time[2] - time[1]
print("dt = ", dt)
R = data[0,1:]
x = data[1:,1:]
print("loaded data")
print("x.shape = ", x.shape)

#
def my_fft(xc, Nc):
	return np.abs(np.real(fft(xc)[0:Nc]))

# Divide the time series into n chunks N long
def find_freq(x, dt, n):
	Nt, Nr = x.shape
	print("Nt, Nr = {:d},{:d}".format(Nt, Nr))
	out_t = np.zeros(n)
	Nchunk = int(float(Nt)/(n+1))
	out_ft = np.zeros((Nchunk, Nr, n))
	w_freq = fftfreq(2*Nchunk, dt)[0:Nchunk]*2*np.pi
	for i in range(0, Nr):	
		# may need to separate real and imag components of w	
		x_chunk = x[0:2*Nchunk,i]
		ft = my_fft(x_chunk, Nchunk)
		out_ft[:,i,0] = ft
		out_t[0] = dt*Nchunk
		if (n > 2):
			for j in range(1, n-1):
				x_chunk = x[(2*j-1)*Nchunk:(2*j+1)*Nchunk,i]
				ft = my_fft(x_chunk, Nchunk)
				out_ft[:,i,j] = ft
				out_t[j] = dt*2*j*Nchunk
		x_chunk	= x[Nt-2*Nchunk:Nt,i]
		ft = my_fft(x_chunk, Nchunk)
		out_ft[:,i,n-1] = ft
		out_t[n-1] = dt*(Nt - Nchunk)
		print("done radius {:d} of {:d}".format(i, Nr))
	return (out_ft, out_t, w_freq)
		
out_ft, out_t, w_freq = find_freq(x, dt, 4)

# plot graph
cm = 'Blues'
fig, axs = plt.subplots(n, sharex=True)
for i in range(0, n):
	xy = out_ft[:,:,i]
	mesh = axs[i].pcolormesh(R, w_freq, xy, cmap = cm)
	axs[i].set_ylabel("{:d}:$\\omega$, t={:.1f}".format(i, out_t[i]))
	axs[i].set_ylim((0.8, 1.2))
	axs[i].set_xlim((0, 200))
axs[0].set_xlabel("$r_{KS}$")
fig.subplots_adjust(bottom=0.1, top=0.9, left=0.1, right=0.8,hspace=0, wspace=0.1)
cb_ax = fig.add_axes([0.83, 0.1, 0.02, 0.8])
cbar = fig.colorbar(mesh, cax=cb_ax)
title = "Time Fourier transform of $\\phi$,  a=0.99, l=m=0, M=1, $\\mu$=1" 
fig.suptitle(title)
#plt.tight_layout()
# save plot
save_name = "/home/dc-bamb1/GRChombo/Analysis/plots/" + base_name + "fourier_plot_n={:d}.png".format(n)
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
