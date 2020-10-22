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

# load datasets
KerrBH_dir = "run0001_l0_m0_a0_Al0_mu1_M0.48847892320123_phase0_KerrSchild"
BinaryBH_dir = "run0005_FlatScalar_mu1_G0"
#
n_BinaryBH = 1000
abmax=30
z_position = 0.001
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
p2 = puncture_positions[3:5]
print("puncture 1 position = ", p1)

# convert BBH slice to fixed resolution array
width = 100
N = 1024
dx = width/N
centerBBH = np.array([256.0, 256.0])
centerKBH = np.array([256.0, 256.0])
c1 = centerKBH + (centerBBH - p1)
c2 = centerKBH - (centerBBH - p1)
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
plots_dir = "/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Analysis/plots/Binary_BH/"

## plot the pseudocolor plot
line_pos = np.linspace(-0.5*width,+0.5*width,N) 
t = dt_BinaryBH * n_BinaryBH
suffix=BinaryBH_dir + "_n{:06d}.png".format(n_BinaryBH)

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
plt.tight_layout()
name = "Compare_ray_profile_phi_"+suffix
save_path = plots_dir + name
plt.savefig(save_path, transparent=False)
print("saved " + save_path)
plt.clf()
