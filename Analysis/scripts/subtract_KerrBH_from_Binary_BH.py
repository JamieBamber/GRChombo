import yt
import numpy as np
import matplotlib.pyplot as plt
import math
from sys import exit

#start_time = time.time()

#
data_root_dir = "/hppfs/work/pn34tu/di76bej/GRChombo_data/"

def get_puncture_data(BBHsubdir):
	file_name = data_root_dir + "BinaryBHScalarField/" + BBHsubdir + "/BinaryBHSFChk_Punctures.dat"
	data = np.genfromtxt(file_name, skip_header=1)	
	return data

# load datasets
KerrBH_dir = "run0001_l0_m0_a0_Al0_mu1_M0.48847892320123_phase0_KerrSchild"
BinaryBH_dir = "run0005_FlatScalar_mu1_G0"
#
n_BinaryBH = 1000
abmax=30
#
BinaryBH_dataset_path = data_root_dir + "BinaryBHScalarField/" + BinaryBH_dir + "/BinaryBHSFPlot_{:06d}.3d.hdf5".format(n_BinaryBH)
KerrBH_dataset_path = data_root_dir + "KerrSF/" + KerrBH_dir + "/KerrSFp_{:06d}.3d.hdf5".format(n_BinaryBH*4)
dsB = yt.load(BinaryBH_dataset_path) 
dsK = yt.load(KerrBH_dataset_path) 
print("loaded " + BinaryBH_dataset_path)
print("loaded " + KerrBH_dataset_path)

dt_KerrBH = 0.25
dt_BinaryBH = 1.0

# get puncture position
puncture_data = get_puncture_data(BinaryBH_dir)
print("loaded puncture data")
puncture_positions = puncture_data[n_BinaryBH,1:]
p1 = puncture_positions[0:2]
print("puncture 1 position = ", p1)

# convert BBH slice to fixed resolution array
width = 64
N = 1024
dx = width/N
res = [N, N] # 1024 by 1024 box
centerBBH = np.array([256.0, 256.0])
centerKBH = np.array([256.0, 256.0])
c1 = centerKBH + (centerBBH - p1)
c2 = centerKBH - (centerBBH - p1)
# 

# extract slice data
z_position = 0.001      # s position of slice
slice = dsK.slice(2, z_position)
frbK1 = slice.to_frb(width, res, center=c1)
frbK2 = slice.to_frb(width, res, center=c2)
print("made KerrBH frbs", flush=True)
arrK1 = np.array(frbK1['phi'])
arrK2 = np.array(frbK2['phi'])
print("made KerrBH arrays",flush=True)
slice = dsB.slice(2, z_position)
print("made BBH slice",flush=True)
frbB = slice.to_frb(width, res, center=centerBBH)
print("made BBH frb",flush=True)
arrB = np.array(frbB['phi'])
print("made BBH array",flush=True)

# convert to numpy arrays
arrKmean = 0.5*(arrK1 + arrK2)
print("made numpy arrays",flush=True)
# combine
out_arr = arrB - arrKmean
print("made combined array",flush=True)

########### plot graph
print("plotting graph...",flush=True)
plots_dir = "/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Analysis/plots/Binary_BH/"

## plot the pseudocolor plot
x_pos = np.linspace(centerBBH[0]-0.5*width,centerBBH[0]+0.5*width,N) 
y_pos = x_pos
cm = 'RdBu'
# puncture locations
puncture_x = np.array([puncture_positions[0], puncture_positions[3]])
puncture_y = np.array([puncture_positions[1], puncture_positions[4]])
t = dt_BinaryBH * n_BinaryBH
suffix=BinaryBH_dir + "_n{:06d}.png".format(n_BinaryBH)
residual_title="Residual $\\phi$ field from Binary BH - Kerr BHs, $\\mu=1$, t={:.2f}".format(t)
residual_name="Residual_phi_"+suffix
BinaryBH_title="Binary BH $\\phi$ field (initially uniform) $\\mu=1$, t={:.2f}".format(t)
BinaryBH_name="Binary_phi_"+suffix
two_Kerr_title="Mean $\\phi$ field from two individual BH profiles $\\mu=1$, t={:.2f}".format(t)
single_Kerr_title="$\\phi$ field from a single BH $\\mu=1$, t={:.2f}".format(t)

def make_plot(arr, title, name):
	fig, ax = plt.subplots()
	phi_max=np.max(arr)
	phi_min=np.min(arr)
	print('max={:.2f} min={:.2f}'.format(phi_max, phi_min))
	mesh = ax.pcolormesh(x_pos, y_pos, arr,cmap=cm,vmin=-abmax,vmax=abmax) 
	fig.colorbar(mesh)
	## add the BH locations
	print("puncture_x, puncture_y = ", puncture_x, puncture_y)
	ax.plot(puncture_x, puncture_y, 'yx', markersize=7, label="BH positions")
	## add text
	ax.text(0.02, 0.98, 'max={:.2f} min={:.2f}'.format(phi_max, phi_min), horizontalalignment='left',verticalalignment='top', transform=ax.transAxes, fontsize=12)
	## add other bits
	ax.legend(loc="lower left", fontsize=12)
	ax.set_title(title) 
	fig.tight_layout()
	save_path = plots_dir + name
	plt.savefig(save_path, transparent=False)
	print("saved " + save_path)
	plt.clf()

make_plot(out_arr, residual_title, "Residual_phi_"+suffix)
make_plot(arrB, BinaryBH_title, "Binary_phi_"+suffix)
make_plot(arrKmean, two_Kerr_title, "Two_Kerr_phi_"+suffix) 
make_plot(arrK1, single_Kerr_title, "Single_Kerr_phi_"+suffix) 
