import yt
import numpy as np
import matplotlib.pyplot as plt
import math
from sys import exit
from os import makedirs

yt.enable_parallelism()

#
data_root_dir = "/hppfs/work/pn34tu/di76bej/GRChombo_data/"
plots_dir = "/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Analysis/plots/Binary_BH/"
#
KerrBH_dir = "run0001_l0_m0_a0_Al0_mu1_M0.48847892320123_phase0_KerrSchild"
BinaryBH_dir = "run0005_FlatScalar_mu1_G0"
movie_folder = "BBH_run0005/BBH_chi_with_ray_loc_run0005_movie"
try:
        makedirs(plots_dir + movie_folder)
except:
        pass

def get_puncture_data(BBHsubdir):
	file_name = data_root_dir + "BinaryBHScalarField/" + BBHsubdir + "/BinaryBHSFChk_Punctures.dat"
	data = np.genfromtxt(file_name, skip_header=1)	
	return data

def vecmag(v):
	out2 = 0
	for i in range(0, len(v)):
		out2 += v[i]*v[i]
	return np.sqrt(out2)

def make_ray(ds, start, end, N, pos=False):
	print("making ray")
	ray = ds.r[start:end:N*1j]
	if pos:
		xy = (np.array(ray["x"]), np.array(ray["y"]))
		return (np.array(ray["chi"]), xy)
	else:
		return np.array(ray["chi"])

#
z_position = 0.001

# load datasets
BinaryBH_dataset_path = data_root_dir + "BinaryBHScalarField/" + BinaryBH_dir + "/BinaryBHSFPlot_*.3d.hdf5"
KerrBH_dataset_path = data_root_dir + "KerrSF/" + KerrBH_dir + "/KerrSFp_*.3d.hdf5"
dseriesB = yt.load(BinaryBH_dataset_path) 
dseriesK = yt.load(KerrBH_dataset_path) 
print("loaded " + BinaryBH_dataset_path)
print("loaded " + KerrBH_dataset_path)
print("BBH series length = ", len(dseriesB))
print("KerrBH series length = ", len(dseriesK)/2)
Nts = min(len(dseriesB), int(len(dseriesK)/2))
#if int(len(dseriesK)/2) < len(dseriesB):
#	dseriesB = dseriesB[288:Nts]

plot_interval_KerrBH = 10
plot_interval_BinaryBH = 5
dt_KerrBH = 0.25
dt_BinaryBH = 1.0

puncture_data = get_puncture_data(BinaryBH_dir)
print("loaded puncture data")

# iterate through dataseries
for dsB in dseriesB.piter():
	#for n_BinaryBH in range(100, 101):
	#dsB = dseriesB[n_BinaryBH]	
	t = dsB.current_time	
	n_BinaryBH = int(t/(dt_BinaryBH*plot_interval_BinaryBH))
	# get Kerr data
	dsK = dseriesK[2*n_BinaryBH]

	# get puncture position
	puncture_positions = puncture_data[n_BinaryBH*plot_interval_BinaryBH,1:]
	print("puncture_positions = ", puncture_positions) 
	p1 = puncture_positions[0:2]
	p2 = puncture_positions[3:5]
	print("puncture 1 position = ", p1)
	print("puncture 2 position = ", p2)

	# convert BBH slice to fixed resolution array
	width = 32
	N = 512
	res = [N, N] # N by N box
	dx = width/N
	centerBBH = np.array([256.0, 256.0])
	centerKBH = np.array([256.0, 256.0])
	c1 = centerKBH + (centerBBH - p1)
	c2 = centerKBH + (centerBBH - p2)
	print("centerKBH 1 position = ", c1)
	print("centerKBH 2 position = ", c2)
	# 

	# positions of the ray endpoints
	p = vecmag(p2 - p1)
	BBHstart = centerBBH + (p1 - p2)*0.5*width/p
	BBHend = centerBBH + (p2 - p1)*0.5*width/p
	BBHstart = np.append(BBHstart, z_position)
	BBHend = np.append(BBHend, z_position)
	print("BBHstart = ", BBHstart)
	print("BBHend = ", BBHend)

	# get ray data
	ray_arrB, xy = make_ray(dsB, BBHstart, BBHend, N, True)
	print("made all rays")

	# get mesh data
	slice = dsB.slice(2, z_position)
	print("made BBH slice",flush=True)
	frbB = slice.to_frb(width, res, center=centerBBH)
	print("made BBH frb",flush=True)
	arrB = np.array(frbB['chi'])
	print("made BBH array",flush=True)

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
	min_chi_loc = slice.argmin("chi")
	print("min chi location = ", min_chi_loc)
	print('max={:.2f} min={:.2f}'.format(chi_max, chi_min))
	mesh = ax.pcolormesh(x_pos, y_pos, arrB,cmap=cm,vmin=0,vmax=1.0) 
	fig.colorbar(mesh)
	## add the BH locations
	print("puncture_x, puncture_y = ", puncture_x, puncture_y)
	ax.plot(puncture_x, puncture_y, 'cx', markersize=5, label="BH punctures")
	## add the min chi locations
	ax.plot(min_chi_loc[0], min_chi_loc[1], 'r+', markersize=5,label="min $\\chi$")
	## add text
	ax.text(0.02, 0.98, 'max={:.2f} min={:.2f}'.format(chi_max, chi_min), horizontalalignment='left',verticalalignment='top', transform=ax.transAxes, fontsize=12)
	## add ray location
	plt.plot(xy[0],xy[1],'g--', label="ray") 
	ax.legend(loc="lower left", fontsize=12)
	title = "Binary BH $\\chi$ t = {:.1f}".format(t)
	ax.set_title(title) 
	fig.tight_layout()
	save_path = plots_dir + movie_folder + "/BBH_movie_{:06d}.png".format(n_BinaryBH)
	plt.savefig(save_path, transparent=False)
	print("saved " + save_path)
	plt.clf()
	plt.close('all')
