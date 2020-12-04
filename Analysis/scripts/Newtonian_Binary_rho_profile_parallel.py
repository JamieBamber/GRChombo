import yt
from yt import derived_field
import numpy as np
import matplotlib.pyplot as plt
import math
from sys import exit
from os import makedirs
import time

yt.enable_parallelism()

#
data_root_path = "/cosma6/data/dp174/dc-bamb1/GRChombo_data/NewtonianBinaryBHScalar/"
plots_dir = "/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots/Newtonian_Binary_BH/"
output_dir ="/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/data/Newtonian_Binary_BH_data"

class data_dir:
        def __init__(self, num, M, d, mu, dt_mult):
                self.num = num
                self.M = float(M)
                self.d = float(d)
                self.mu = float(mu)
                self.dt_mult = dt_mult
                self.name = "run{:04d}_M{:s}_d{:s}_mu{:s}_dt_mult{:s}".format(num, M, d, mu, dt_mult)

data_dirs = []
def add_data_dir(num, M, d, mu, dt_mult):
        x = data_dir(num, M, d, mu, dt_mult)
        data_dirs.append(x)

add_data_dir(7, "0.2", "10", "0.02", "0.5")
add_data_dir(8, "0.2", "10", "0.025", "0.5")
add_data_dir(9, "0.2", "10", "0.015", "0.5")
add_data_dir(10, "0.2", "10", "0.01", "0.5")
add_data_dir(11, "0.2", "10", "0.03", "0.5")

# Base parameters
L = 256.0
z_position = 0.001
center = np.array([L/2, L/2, 0])

"""@derived_field(name = "rho_eff")
def _rho_E_eff(field, data):
        return pow(data["chi"],-3.0/2)*data["rho"]"""

def get_puncture_data_BH_N(dd, t):
	output = np.zeros(6)
	omega = np.sqrt(2*dd.M/(dd.d**3))
	output[0] = center[0] + dd.d*np.cos(omega*t)
	output[1] = center[1] +	dd.d*np.sin(omega*t)
	output[2] = center[2]
	output[3] = center[0] -	dd.d*np.cos(omega*t)
	output[4] = center[1] - dd.d*np.sin(omega*t)
	output[5] = center[2]
	return output
	
def get_puncture_data_BH_GR(BBHsubdir):
	file_name = data_root_path + BBHsubdir + "/BinaryBHSFChk_Punctures.dat"
	data = np.genfromtxt(file_name, skip_header=1)	
	return data

def vecmag(v):
	out2 = 0
	for i in range(0, len(v)):
		out2 += v[i]*v[i]
	return np.sqrt(out2)

def make_ray(ds, start, end, N, var):
	start_list = []
	end_list = []
	for i in range(0, 3):
		start_list += start[i]
		end_list += end[i]
	print("making ray")
	ray = ds.r[start:end:N*1j]
	return np.array(ray[var])

# convert BBH slice to fixed resolution array
width = 50
N = 1024
res = [N, N] # 1024 by 1024 box
dx = width/N

def make_plot(arr, title, name, puncture_positions):
	## plot the pseudocolor plot
	x_pos = np.linspace(center[0]-0.5*width,center[0]+0.5*width,N)
	y_pos = x_pos
	cm = 'inferno'
	puncture_x = np.array([puncture_positions[0], puncture_positions[3]])
	puncture_y = np.array([puncture_positions[1], puncture_positions[4]])
	fig, ax = plt.subplots()
	val_max=np.max(arr)
	val_min=np.min(arr)
	print('max={:.2f} min={:.2f}'.format(val_max, val_min))
	mesh = ax.pcolormesh(x_pos, y_pos, np.log10(arr),cmap=cm,vmin=-1,vmax=1)
	fig.colorbar(mesh)
	## add the BH locations
	print("puncture_x, puncture_y = ", puncture_x, puncture_y)
	ax.plot(puncture_x, puncture_y, 'yx', markersize=7, label="BH positions")
	## add text
	ax.text(0.02, 0.98, 'max={:.2f} min={:.2f}'.format(val_max, val_min), horizontalalignment='left',verticalalignment='top', transform=ax.transAxes, fontsize=12)
	## add other bits
	ax.legend(loc="lower left", fontsize=12)
	ax.set_title(title)
	fig.tight_layout()
	save_path = plots_dir + name
	plt.savefig(save_path, transparent=False)
	print("saved " + save_path)
	plt.clf()
	
def get_line_data(dd):
	data_sub_dir = dd.name
	start_time = time.time()
	# load dataset time series
	dataset_path = data_root_path + data_sub_dir + "/Newton_plt*.3d.hdf5"
	ds = yt.load(dataset_path) # this loads a dataset time series
	print("loaded data from ", dataset_path)
	print("time = ", time.time() - start_time)
	Nts = len(ds)	
	rho0 = 0.5*dd.mu**2
		
	# output to file
	filename = "{:s}_rho_profile.csv".format(dd.name)
	output_path = output_dir + "/" + filename
	# output header to file
	f = open(output_path, "w+")
	f.write("# t    position = ...  #\n")
	# write header data
	ray_pos = np.linspace(-width/2, width/2, N)
	f.write("0	")	
	for i in range(0, N):
		f.write("{:.3f} ".format(ray_pos[i]))
	f.write("\n")

	data_storage = {}
	# iterate through datasets (forcing each to go to a different processor)
	#for sto, dsi in ds.piter(storage=data_storage):
	for dsi in ds[1000:1001]:
		#for n_BinaryBH in range(256, Nts):
		#dsB = dseriesB[n_BinaryBH]	
		t = dsi.current_time	
		#n_BinaryBH = int(t/(dt_BinaryBH*plot_interval_BinaryBH))
		
		# get puncture position
		puncture_positions = get_puncture_data_BH_N(dd, t)
		p1 = puncture_positions[0:3]
		p2 = puncture_positions[3:6]
		#print("puncture 1 position = ", p1)
		#print("puncture 2 position = ", p2)
		
		# positions of the ray endpoints
		p = vecmag(p2 - p1)
		BBHstart = center + (p1 - p2)*0.5*width/p
		BBHend = center + (p2 - p1)*0.5*width/p
		
		# get ray data
		ray_val = make_ray(dsi, BBHstart, BBHend, N, "rho")/rho0
		print("made ray for t = ", t)
		output = [t, ray_val]
		#sto.result = output
		#sto.result_id = str(dsi)

		slice = dsi.slice(2, z_position)
		frbB = slice.to_frb(width, res, center=center)
		print("made BBH frb",flush=True)
		arrB = np.array(frbB['rho'])*(1/rho0)
		make_plot(arrB, "Newtonian Binary run{:04d} t={:.1f}".format(dd.num, t), dd.name + "_rho_2D_plot.png", puncture_positions)
		
	#if yt.is_root():
	
		# output data
		#for key in sorted(data_storage.keys()):
		#data = data_storage[key]
		f.write("{:.3f} ".format(output[0]))
		ray_val = output[1]
		for i in range(0, len(ray_val)):
        		f.write("{:.6f} ".format(ray_val[i]))
		f.write("\n")
	f.close()
	print("saved data to file " + str(output_path))

#for dd in data_dirs:	
get_line_data(data_dirs[0])

def plot_graph():	
	########### plot graph
	print("plotting graph...",flush=True)
	line_pos = np.linspace(-0.5*width,+0.5*width,N) 
	fig, ax = plt.subplots()
	ax.plot(line_pos, np.log10(arrK1), 'c--', label="single BH 1")
	ax.plot(line_pos, np.log10(arrK2), 'g--', label="single BH 2")
	ax.plot(line_pos, np.log10(arrKmean), 'b-', label="mean of single BHs")
	ax.plot(line_pos, np.log10(arrB), 'r-', label="Binary BHs")

	rho_max=np.max(arrB)
	rho_min=np.min(arrB)	
	ax.text(0.02, 0.98, 'BBH max={:.2g} min={:.2g}'.format(rho_max, rho_min), horizontalalignment='left',verticalalignment='top', transform=ax.transAxes, fontsize=12)
	title = "Compare 1D ray $\\rho$ profiles for binary and two single BHs, t={:.1f}".format(t)
	plt.legend(fontsize=10)
	plt.title(title)
	ax.set_xlabel("line position from centre")
	ax.set_ylabel("$\\log_{10}(\\rho)$")
	ax.set_ylim((np.log10(0.01), 7))
	plt.tight_layout()
	save_path = plots_dir + movie_folder + "/BBH_movie_{:06d}.png".format(n_BinaryBH)
	plt.savefig(save_path, transparent=False)
	print("saved " + save_path)
	plt.clf()
	plt.close('all')
