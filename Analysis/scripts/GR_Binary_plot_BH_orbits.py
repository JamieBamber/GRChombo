import numpy as np
import math
import time
import sys
#from matplotlib import rc
#rc('text', usetex=True)
from matplotlib import pyplot as plt

"""tex_fonts = {
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
}"""

# class to store the run information
L=512
N=256

width=15

analysis_data_root_path = "/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/data/GR_Binary_BH_data/"
#"/p/home/jusers/bamber1/juwels/GRChombo/Analysis/data/GR_Binary_BH_data/"
#plots_path = "/p/home/jusers/bamber1/juwels/GRChombo/Analysis/plots/GR_Binary_BH/"
plots_path="/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots/GR_Binary_BH/"
#data_root_path="/p/project/pra116/bamber1/BinaryBHScalarField/"
data_root_path="/cosma6/data/dp174/dc-bamb1/GRChombo_data/BinaryBHSF/"

# class to store the run information                                                                                                     
class data_dir:
        def __init__(self, num, mu, delay, G, ratio, ICSsuffix, restart, l, m, Al):
                self.num = num
                self.mu = float(mu)
                self.delay = delay
                self.G = G
                self.ratio = ratio
                self.l = l
                self.m = m
                self.Al = Al
                self.ICSsuffix = ICSsuffix
                if restart:
                        suffix = "_restart"
                else:
                        suffix = ""
                if (l != 0):
                        lm_suffix = "_l{:d}_m{:d}_Al{:s}".format(l, m, Al)
                else:
                        lm_suffix = ""
                self.name = "run{:04d}{:s}_mu{:s}_delay{:d}_G{:s}_ratio{:d}{:s}{:s}".format(num, ICSsuffix, mu, delay, G, ratio, lm_suffix, suffix)
#                                                                                                                                        
data_dirs = []
def add_data_dir(num, mu, delay, G, ratio, ICSsuffix='', restart=0, l=0, m=0, Al="0"):
        if restart:
                suffix = "_restart"
        else:
                suffix = ""
        x = data_dir(num, mu, delay, G, ratio, ICSsuffix, restart, l, m, Al)
        data_dirs.append(x)
#                                                  
add_data_dir(23, "0.5", 0, "0.0000000001", 1) # 10^{-10}     
add_data_dir(23, "0.5", 0, "0.0000000001", 1, "ICS") # 10^{-10}     
#add_data_dir(35, "0.5", 0, "0.00000000000001", 1, "ICS") # 10^{-14}
#add_data_dir(34, "0.5", 0, "0.000000000001", 1) # 10^{-12}

def time_average(x, n):
        N = len(x)
        n_chunks = int(np.floor(N/n))
        x_out = np.zeros(n_chunks)
        for i in range(0, n_chunks):
                x_out[i] = np.mean(x[i*n:(i+1)*n])
        x_out[-1] = np.mean(x[N-n:])
        return x_out

average_time = True
av_n = 20
cumulative= False
r_extract = 200
M = 1.0

def load_data():
        # load BH puncture data from
        data = []
        for dd in data_dirs:
                file_name = data_root_path + dd.name + "/BinaryBHSFChk_Punctures.dat"
                data.append(np.genfromtxt(file_name, skip_header=1))
                print("loaded data for " + dd.name)
        return data     

def plot_graph():
        data = load_data()
        #colours = ['r-', 'b-', 'g-', 'm-', 'y-', 'c-', 'k-', 'r--', 'b--', 'g--', 'm--', 'y--', 'c--']
        colours = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6']
        i = 0
        ### plot mass flux graph
        fig, ax1 = plt.subplots()
        fig.set_size_inches(6,6)
        font_size = 10
        title_font_size = 10
        label_size = 10
        legend_font_size = 8
        #rc('xtick',labelsize=font_size)
        #rc('ytick',labelsize=font_size)
        for dd in data_dirs:
                line_data = data[i]
                x1 = line_data[:,1] - L/2
                y1 = line_data[:,2] - L/2
                x2 = line_data[:,4] - L/2
                y2 = line_data[:,5] - L/2
                label_ = "$m=${:.1f} $G=${:.0g} {:s}".format(dd.mu, float(dd.G), dd.ICSsuffix)
                ax1.plot(x1,y1,colours[i], label=label_, linewidth=1)
                ax1.plot(x2,y2,colours[i], label="_", linewidth=1)
                i = i + 1
        ax1.set_xlabel("$x$", fontsize=font_size)
        ax1.set_ylabel("$y$", fontsize=font_size)
        ax1.set_xlim((-width/2, width/2))
        ax1.set_ylim((-width/2, width/2))
        plt.title("Paths of BH punctures")
        save_path = plots_path + "GR_BBH_punctures_path_compare_with_ICS.png"
        ax1.legend(loc='best', fontsize=legend_font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        plt.tight_layout()
        plt.savefig(save_path)
        print("saved plot as " + str(save_path))
        plt.clf()

plot_graph()
