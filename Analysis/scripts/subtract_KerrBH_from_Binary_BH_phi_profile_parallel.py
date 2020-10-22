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
run_number = 7
BinaryBH_dir = "run0007_FlatScalar_mu1_G0_delay1500"
movie_folder = "BBH_run0007/Compare_ray_profile_phi_run0007_movie"
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

def make_ray(ds, start, end, N):
	start_list = []
	end_list = []
	for i in range(0, 3):
		start_list += start[i]
		end_list += end[i]
	print("making ray")
	ray = ds.r[start:end:N*1j]
	return np.array(ray["phi"])

#
abmax=20
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
if int(len(dseriesK)/2) < len(dseriesB):
	dseriesB = dseriesB[160:Nts]

plot_interval_KerrBH = 10
plot_interval_BinaryBH = 5
dt_KerrBH = 0.25
dt_BinaryBH = 1.0

puncture_data = get_puncture_data(BinaryBH_dir)
print("loaded puncture data")

# iterate through dataseries
for dsB in dseriesB.piter():
	#for n_BinaryBH in range(62, 63):
	#dsB = dseriesB[n_BinaryBH]	
	t = dsB.current_time	
	n_BinaryBH = int(t/(dt_BinaryBH*plot_interval_BinaryBH))
	# get Kerr data
	dsK = dseriesK[2*n_BinaryBH]

	# get puncture position
	puncture_positions = puncture_data[n_BinaryBH*plot_interval_BinaryBH,1:]
	p1 = puncture_positions[0:2]
	p2 = puncture_positions[3:5]
	print("puncture 1 position = ", p1)
	print("puncture 2 position = ", p2)

	# convert BBH slice to fixed resolution array
	width = 100
	N = 1024
	dx = width/N
	centerBBH = np.array([256.0, 256.0])
	centerKBH = np.array([256.0, 256.0])
	c1 = centerKBH + (centerBBH - p1)
	c2 = centerKBH - (centerBBH - p1)
	print("centerKBH 1 position = ", c1)
	print("centerKBH 2 position = ", c2)
	# 

	# positions of the ray endpoints
	p = vecmag(p2 - p1)
	BBHstart = centerBBH + (p1 - p2)*0.5*width/p
	BBHend = centerBBH + (p2 - p1)*0.5*width/p
	BBHstart = np.append(BBHstart, z_position)
	BBHend = np.append(BBHend, z_position)
	d1 = vecmag(c1 - centerKBH)
	d2 = vecmag(c2 - centerKBH)
	Kstart1 = c1 - (c1 - centerKBH)*0.5*width/d1
	Kend1 = c1 + (c1 - centerKBH)*0.5*width/d1
	Kstart2 = c2 + (c2 - centerKBH)*0.5*width/d1
	Kend2 = c2 - (c2 - centerKBH)*0.5*width/d1
	Kstart1 = np.append(Kstart1, z_position)
	Kend1 = np.append(Kend1, z_position)
	Kstart2 = np.append(Kstart2, z_position)
	Kend2 = np.append(Kend2, z_position)

	# get ray data
	arrK1 = make_ray(dsK, Kstart1, Kend1, N)
	arrK2 = make_ray(dsK, Kstart2, Kend2, N)
	arrB = make_ray(dsB, BBHstart, BBHend, N)
	print("made all rays")

	# convert to numpy arrays
	arrKmean = 0.5*(arrK1 + arrK2)
	print("made numpy arrays",flush=True)
	# combine
	out_arr = arrB - arrKmean
	print("made combined array",flush=True)

	########### plot graph
	print("plotting graph...",flush=True)
	line_pos = np.linspace(-0.5*width,+0.5*width,N) 
	fig, ax = plt.subplots()
	ax.plot(line_pos, arrK1, 'c--', label="single BH 1")
	ax.plot(line_pos, arrK2, 'g--', label="single BH 2")
	ax.plot(line_pos, arrKmean, 'b-', label="mean of single BHs")
	ax.plot(line_pos, arrB, 'r-', label="Binary BHs")

	phi_max=np.max(arrB)
	phi_min=np.min(arrB)	
	ax.text(0.02, 0.98, 'BBH max={:.2f} min={:.2f}'.format(phi_max, phi_min), horizontalalignment='left',verticalalignment='top', transform=ax.transAxes, fontsize=12)
	title = "Compare 1D ray $\\phi$ profiles for binary and two single BHs, t={:.1f}".format(t)
	plt.legend(fontsize=10)
	plt.title(title)
	ax.set_xlabel("line position from centre")
	ax.set_ylabel("$\\phi$")
	ax.set_ylim((-abmax, abmax))
	plt.tight_layout()
	save_path = plots_dir + movie_folder + "/BBH_movie_{:06d}.png".format(n_BinaryBH)
	plt.savefig(save_path, transparent=False)
	print("saved " + save_path)
	plt.clf()
	plt.close('all')
