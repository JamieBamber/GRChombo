import yt
import numpy as np
import matplotlib.pyplot as plt
import math
from sys import exit
from os import makedirs

yt.enable_parallelism()

#
data_root_dir = "/cosma6/data/dp174/dc-bamb1/GRChombo_data/BinaryBHSF/"
plots_dir = "/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots/GR_Binary_BH/"
#
BinaryBH_dir = "run0023ICS_mu0.5_delay0_G0.0000000001_ratio1"
movie_folder = BinaryBH_dir + "_chi_movie_with_punctures"
try:
        makedirs(plots_dir + movie_folder)
except:
        pass

def get_puncture_data(BBHsubdir):
	file_name = data_root_dir + BBHsubdir + "/BinaryBHSFChk_Punctures.dat"
	data = np.genfromtxt(file_name, skip_header=1)	
	return data

z_position = 0.001

# load datasets
BinaryBH_dataset_path = data_root_dir + BinaryBH_dir + "/BinaryBHSFPlot_*.3d.hdf5"
dseriesB = yt.load(BinaryBH_dataset_path) 
print("loaded " + BinaryBH_dataset_path)
print("BBH series length = ", len(dseriesB))

plot_interval_BinaryBH = 5
dt_BinaryBH = 2.0
centerBBH = [256.0,256.0]

puncture_data = get_puncture_data(BinaryBH_dir)
print("loaded puncture data")

# iterate through dataseries
for dsB in dseriesB.piter():
	#for n_BinaryBH in range(100, 101):
	#dsB = dseriesB[n_BinaryBH]	
	t = dsB.current_time	
	n_BinaryBH = int(t/(dt_BinaryBH*plot_interval_BinaryBH))

	# get puncture position
	puncture_positions = puncture_data[n_BinaryBH*plot_interval_BinaryBH,1:]
	p1 = puncture_positions[0:2]
	p2 = puncture_positions[3:5]

	# convert BBH slice to fixed resolution array
	width = 32
	N = 512
	res = [N,N]
	# get mesh data
	slice = dsB.slice(2, 256.0)
	frbB = slice.to_frb(width, res, center=centerBBH)
	arrB = np.array(frbB['chi'])

	## plot the pseudocolor plot
	x_pos = np.linspace(centerBBH[0]-0.5*width,centerBBH[0]+0.5*width,N) 
	y_pos = x_pos
	cm = 'inferno'
	# puncture locations
	puncture_x = np.array([puncture_positions[0], puncture_positions[3]])
	puncture_y = np.array([puncture_positions[1], puncture_positions[4]])
	fig, ax = plt.subplots()
	chi_max=np.max(arrB)
	chi_min=np.min(arrB)
	#min_chi_loc = slice.argmin("chi")
	#print("min chi location = ", min_chi_loc)
	#print('max={:.2f} min={:.2f}'.format(chi_max, chi_min))
	mesh = ax.pcolormesh(x_pos, y_pos, arrB,cmap=cm,vmin=0,vmax=1.0) 
	fig.colorbar(mesh)
	## add the BH locations
	#print("puncture_x, puncture_y = ", puncture_x, puncture_y)
	ax.plot(puncture_x, puncture_y, 'cx', markersize=5, label="BH punctures")
	## add the min chi locations
	#ax.plot(min_chi_loc[0], min_chi_loc[1], 'r+', markersize=5,label="min $\\chi$")
	## add text
	#ax.text(0.02, 0.98, 'max={:.2f} min={:.2f}'.format(chi_max, chi_min), horizontalalignment='left',verticalalignment='top', transform=ax.transAxes, fontsize=12)
	## add ray location
	#plt.plot(xy[0],xy[1],'g--', label="ray") 
	ax.legend(loc="lower left", fontsize=12)
	title = "Binary BH $\\chi$ t = {:.1f}".format(t)
	ax.set_title(title) 
	fig.tight_layout()
	save_path = plots_dir + movie_folder + "/BBH_movie_{:06d}.png".format(n_BinaryBH)
	plt.savefig(save_path, transparent=False)
	print("saved " + save_path)
	plt.clf()
	plt.close('all')
