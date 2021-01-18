import numpy as np
import math
import time
import sys
from matplotlib import rc
rc('text', usetex=True)
from matplotlib import pyplot as plt

tex_fonts = {
    # Use LaTeX to write all text
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": "Times",
    "mathtext.fontset": "custom",
    "mathtext.rm": "Times New Roman",
    # "font.serif": "ntx-Regular-tlf-t1",
    # Use 8pt font in plots, to match 8pt font in document
    "axes.labelsize": 8,
    "font.size": 8,
    # Make the legend/label fonts a little smaller
    "legend.fontsize": 7,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7
}

# class to store the run information                                                                                                                                                              
class data_dir:
        def __init__(self, num, mu, delay, G, ratio):
                self.num = num
                self.mu = float(mu)
                self.delay = delay
                self.G = G
                self.ratio = ratio
                self.name = "run{:04d}_mu{:s}_delay{:d}_G{:s}_ratio{:d}".format(num, mu, delay, G, ratio)
                #

data_dirs = []
def add_data_dir(num, mu, delay, G, ratio):
        x = data_dir(num, mu, delay, G, ratio)
        data_dirs.append(x)
                                                                                                                                                                                               
# choose datasets to compare
add_data_dir(11, "1", 0, "0", 1)
#add_data_dir(12, "1", 10000, "0", 1)
#add_data_dir(13, "0.08187607564", 0, "0", 1)
add_data_dir(14, "1", 0, "0", 2)
#add_data_dir(15, "1", 10000, "0", 2)
add_data_dir(16, "0.5", 0, "0", 1)                                                                                                                                                               
#add_data_dir(17, "0.5", 10000, "0", 1)
#add_data_dir(18, "0.5", 0, "0.000001", 1)                                                                                                                                                        

def time_average(x, n):
	N = len(x)
	n_chunks = int(np.floor(N/n))
	x_out = np.zeros(n_chunks)
	for i in range(0, n_chunks):
		x_out[i] = np.mean(x[i*n:(i+1)*n])
	x_out[-1] = np.mean(x[N-n:])
	return x_out

data_root_path="/home/dc-bamb1/GRChombo/Analysis/data/GR_Binary_BH_data/"
plots_path="/home/dc-bamb1/GRChombo/Analysis/plots/GR_Binary_BH/"

phi0=1
average_time = False
av_n = 1
cumulative= False
r_extract = 50

def load_data():
	# load data from csv files
	data = {}
	for dd in data_dirs:
		file_name = data_root_path + dd.name + "_mass_ang_mom_flux_r=" + str(r_extract) + ".dat"
		data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		print("loaded data for " + dd.name)
	return data 	

def plot_graph():
	data = load_data()
	colours = ['r', 'b', 'g', 'm', 'y', 'c']
	i = 0
        ### plot mass flux graph
	fig, ax1 = plt.subplots()
        fig.set_size_inches(3.375,3)
        font_size = 10
        title_font_size = 10
        label_size = 10
        legend_font_size = 10
        rc('xtick',labelsize=font_size)
        rc('ytick',labelsize=font_size)
	for dd in data_dirs:
		line_data = data[dd.num]
		t1 = line_data[:,0]
		mu = float(dd.mu)
                E0 = 0.5*(phi0*mu)**2
		F0 = 4*np.pi*(r_extract**2)*E0
		mass_flux = -line_data[1:,1]/F0
		if average_time:
			t1 = time_average(t1, av_n)
			mass_flux = time_average(mass_flux, av_n)
		if cumulative:
			mass_flux = np.cumsum(mass_flux)/(r_extract/3)
		label_ = "$\\mu=${:s} mass ratio$=${:d}".format(dd.mu, dd.ratio)
		ax1.plot(t1,mass_flux,colours[i]+"-", label=label_)
		i = i + 1
	ax1.set_xlabel("$t$", fontsize=font_size)
	if cumulative:
		ax1.set_ylabel("cumulative flux / $E_0$")
		plt.title("Cumulative mass flux into $R=${:d}".format(r_extract))
		save_path = plots_path + "GR_BBH_mass_flux_cumulative.png"
	else:
                ax1.set_ylabel("mass flux / $F_0$", fontsize=font_size)
                plt.title("Mass flux into $R=${:d}".format(r_extract))
                save_path = plots_path + "GR_BBH_mass_flux.png"
	ax1.legend(loc='upper left', fontsize=legend_font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
	plt.tight_layout()
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()

plot_graph()

