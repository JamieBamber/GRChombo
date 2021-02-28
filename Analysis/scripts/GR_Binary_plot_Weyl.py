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
L=1024
N=256

analysis_data_root_path = "/p/home/jusers/bamber1/juwels/GRChombo/Analysis/data/GR_Binary_BH_data/"
plots_path = "/p/home/jusers/bamber1/juwels/GRChombo/Analysis/plots/GR_Binary_BH/"
data_root_path="/p/project/pra116/bamber1/BinaryBHScalarField/"

# class to store the run information                                                                                                     
class data_dir:
        def __init__(self, num, mu, delay, G, ratio, restart, l, m, Al):
                self.num = num
                self.mu = float(mu)
                self.delay = delay
                self.G = G
                self.ratio = ratio
                self.l = l
                self.m = m
                self.Al = Al
                if restart:
                        suffix = "_restart"
                else:
                        suffix = ""
                if (l != 0):
                        lm_suffix = "_l{:d}_m{:d}_Al{:s}".format(l, m, Al)
                else:
                        lm_suffix = ""
                self.name = "run{:04d}_mu{:s}_delay{:d}_G{:s}_ratio{:d}{:s}{:s}".format(num, mu, delay, G, ratio, lm_suffix, suffix)
#                                                                                                                                        
data_dirs = []
def add_data_dir(num, mu, delay, G, ratio, restart=0, l=0, m=0, Al="0"):
        if restart:
                suffix = "_restart"
        else:
                suffix = ""
        x = data_dir(num, mu, delay, G, ratio, restart, l, m, Al)
        data_dirs.append(x)
#                                                  
#add_data_dir(11, "1", 0, "0", 1)
#add_data_dir(12, "1", 10000, "0", 1)
#add_data_dir(13, "0.08187607564", 0, "0", 1)
#add_data_dir(14, "1", 0, "0", 2)
#add_data_dir(15, "1", 10000, "0", 2)
#add_data_dir(16, "0.5", 0, "0", 1)
#add_data_dir(17, "0.5", 10000, "0", 1)
#add_data_dir(19, "1", 0, "0", 1, 1) # resume from stationary BH distribution
#add_data_dir(20, "0.5", 0, "0", 1, 1) # resume from stationary BH distribution
#add_data_dir(21, "0.5", 0, "0.01", 1)
#add_data_dir(22, "0.5", 0, "0", 1)
add_data_dir(25, "0.5", 0, "0", 1, 0, 1, 1)
#add_data_dir(24, "0.5", 0, "0.00000000000000000001", 1, 1)
#add_data_dir(18, "0.5", 0, "0.000001", 1)
#add_data_dir(28, "0.5", 0, "0.00000001", 1)                         
#add_data_dir(31, "0.5", 0, "0.0000000000000000000000001", 1) # 10^{-25}
#add_data_dir(32, "0.5", 0, "0.000000000000000000000000000001", 1) # 10^{-30}
add_data_dir(33, "0.5", 0, "0.000000001", 1) # 10^{-9}
add_data_dir(23, "0.5", 0, "0.0000000001", 1) # 10^{-10}     
#add_data_dir(34, "0.5", 0, "0.000000000001", 1) # 10^{-12}
#add_data_dir(35, "0.5", 0, "0.00000000000001", 1) # 10^{-14}
#add_data_dir(26, "0.5", 0, "0.000000000000001", 1) # 10^{-15}
#add_data_dir(27, "0.5", 0, "0.00000000000000000001", 1) # 10^{-20}

#add_data_dir(29, "1", 0, "0.0000000001", 1)

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

def load_data(l,m):
        # load data from csv files
        data = {}
        for dd in data_dirs:
                file_name = data_root_path + dd.name + "/outputs/Weyl_integral_{:d}{:d}.dat".format(l,m)
                data[dd.num] = np.genfromtxt(file_name, skip_header=2)
                print("loaded data for " + dd.name)
        return data     

def realign_data(t,W):
        # find maximum
        #print("t.shape = ", t.shape)
        #print("W.shape = ", W.shape)
        # add a stack of nans to the front of W
        nmax = np.argmin(W)
        #print("nmax = ", nmax)
        tmax = t[nmax]
        nextra = 1000
        W = np.concatenate((np.nan*np.ones(nextra),W))
        t = np.concatenate((np.nan*np.ones(nextra),t))
        W1 = W[nmax+nextra-1000:nmax+nextra+100]
        t1 = t[nmax+nextra-1000:nmax+nextra+100]
        t1 = t1 - tmax
        #print("t1.shape = ", t1.shape)
        #print("W1.shape = ", W1.shape)
        output = (t1, W1)
        return output

def plot_graph(align=False):
        data = load_data(2,2)
        colours = ['r-', 'b-', 'g-', 'm-', 'y-', 'c-', 'k-', 'r--', 'b--', 'g--', 'm--', 'y--', 'c--']
        i = 0
        ### plot mass flux graph
        fig, ax1 = plt.subplots()
        fig.set_size_inches(6.5,6)
        font_size = 10
        title_font_size = 10
        label_size = 10
        legend_font_size = 8
        #rc('xtick',labelsize=font_size)
        #rc('ytick',labelsize=font_size)
        for dd in data_dirs:
                line_data = data[dd.num]
                r0 = r_extract + 2*M*np.log(r_extract/(2*M)-1.0)
                t = line_data[:,0] - r0
                Weyl_Re = line_data[:,3]
                Weyl_Im = line_data[:,4]
                if align:
                        t1, W1 = realign_data(t,Weyl_Re)
                else:
                        t1 = t
                        W1 = Weyl_Re
                label_ = "$m=${:.1f} $G=${:.0g}".format(dd.mu, float(dd.G))
                ax1.plot(t1,W1,colours[i], label=label_, linewidth=1)
                i = i + 1
        ax1.set_xlabel("$t$", fontsize=font_size)
        ax1.set_ylabel("Re($\\Psi_4$) 22 mode")
        if align:
                ax1.set_xlim((-1000, 200))
        else:
                ax1.set_xlim((0, 2200))
        plt.title("Weyl scalar at $R=${:d}".format(r_extract))
        if align:
                save_path = plots_path + "GR_BBH_Weyl_Re_22_aligned.png"
        else:
                save_path = plots_path + "GR_BBH_Weyl_Re_22.png"
        ax1.legend(loc='best', fontsize=legend_font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        plt.tight_layout()
        plt.savefig(save_path)
        print("saved plot as " + str(save_path))
        plt.clf()

def plot_diff_graph(use_log):
        data = load_data(2,2)
        colours = ['r-', 'b-', 'g-', 'm-', 'y-', 'c-', 'k-', 'r--', 'b--', 'g--', 'm--', 'y--', 'c--']
        i = 0
        ### plot mass flux graph                                                                                                                                                    
        fig, ax1 = plt.subplots()
        fig.set_size_inches(6.5,6)
        font_size = 10
        title_font_size = 10
        label_size = 10
        legend_font_size = 12
        #rc('xtick',labelsize=font_size)                                                                                                                                            
        #rc('ytick',labelsize=font_size)
        # get G = 0 data
        line_data = data[data_dirs[0].num]
        t = line_data[:,0]
        Weyl_Re = line_data[:,3]
        t0, W0 = realign_data(t,Weyl_Re)
        print("t0.shape = ", t0.shape)
        print("W0.shape = ", W0.shape)
        for dd in data_dirs[1:]:
                line_data = data[dd.num]
                r0 = r_extract + 2*M*np.log(r_extract/(2*M)-1.0)
                t = line_data[:,0] - r0
                Weyl_Re = line_data[:,3]
                Weyl_Im = line_data[:,4]
                t1, W1 = realign_data(t,Weyl_Re)
                label_ = "$m=${:.1f} $G=${:.0g}".format(dd.mu, float(dd.G))
                if use_log:
                        ax1.plot(t1,np.log10(np.abs(W1-W0)),colours[i+1], label=label_)
                else:
                        ax1.plot(t1,W1-W0,colours[i+1], label=label_)
                i = i + 1
        ax1.set_xlabel("$t$", fontsize=font_size)
        if use_log:
                ax1.set_ylabel("$\\log_{10}$($\\Delta$ Re($\\Psi_4$) 22 mode)")
                save_path = plots_path + "GR_BBH_Weyl_Re_22_G_diff_log.png"
        else:
                ax1.set_ylabel("$\\Delta$ Re($\\Psi_4$) 22 mode")
                save_path = plots_path + "GR_BBH_Weyl_Re_22_G_diff.png"
        ax1.set_xlim((-1000, 100))
        plt.title("change in Weyl scalar at $R=${:d} vs $G=0$".format(r_extract))
        ax1.legend(loc='best', fontsize=legend_font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        plt.tight_layout()
        plt.savefig(save_path)
        print("saved plot as " + str(save_path))
        plt.clf()
        
plot_graph(True)
plot_diff_graph(False)
