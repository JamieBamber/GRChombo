# Script to plot the integrated Ylm components of phi vs radius and vs time
# for the Newtonian binary

import numpy as np
from matplotlib import pyplot as plt

# 

subdir = "run0020_M0.2_d10_mu0.5_dt_mult0.0625_l0_m0_Al0_L1024_N256"
home_dir = "/cosma/home/dp174/dc-bamb1/"
plots_path = home_dir + "GRChombo/Analysis/plots/Newtonian_Binary_BH/"

data_dir = home_dir + "GRChombo/Analysis/ReprocessingTools/SphericalExtraction_v2/outputs/"

lm_list = [(1,1), (2,1), (2,2), (4,2), (4,4), (6,4), (6,6)]

r_min = 50
r_max = 400
n_r = 64

def load_data():
	data = []
	for i in range(0, len(lm_list)):
		l = lm_list[i][0]
		m = lm_list[i][1]
		filename = subdir + "_phi_integrals/" + "Phi_integral_{:s}_lm_{:d}{:d}.dat".format(subdir,l,m)
		line_data = np.genfromtxt(data_dir + filename, skip_header=1)
		data.append(line_data)
	print("loaded data")
	return data
	
def plot_graph_fixed_r():
	data = load_data()
	r_index = 4
	r = np.linspace(r_min, r_max, n_r)[r_index]
	colours = ["r-", "b-", "g-", "m-", "c-", "y-", "k-"] 
	for i in range(0, len(lm_list)):
		l = lm_list[i][0]
		m = lm_list[i][1]
		line_data = data[i]
		t = line_data[:,0]
		phi = line_data[:,1+r_index]
		plt.plot(t, np.log(np.abs(phi)), colours[i], label="l,m = {:d},{:d}".format(l,m))
	plt.title("Newtonian binary, $\\phi$ Ylm component, r={:.2f}".format(r))
	plt.xlabel("t")
	plt.ylabel("$\\ln(|4\\pi \\phi_{lm}|)$")
	plt.legend(loc='best')
	plt.tight_layout()
	save_path = plots_path + "Phi_Ylm_vs_t_r{:.2f}_{:s}.png".format(r, subdir)
	plt.savefig(save_path)
	plt.clf()
	print("saved plot as ", save_path)
	
plot_graph_fixed_r()
