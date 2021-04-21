import yt
import numpy as np
import matplotlib.pyplot as plt
import math
from sys import exit
from os import makedirs

yt.enable_parallelism()

# Newtonian Binaries

data_root_dir = "/p/project/pra116/bamber1/BinaryBHScalarField/"
plots_dir = "/p/home/jusers/bamber1/juwels/GRChombo/Analysis/plots/GR_Binary_BH/"
output_data_dir = "/p/home/jusers/bamber1/juwels/GRChombo/Analysis/data/GR_Binary_BH_data/"

L=512
N1=64
abmax=20
z_position = 0.00
width = 100
N = 256

############################

class data_dir:
        def __init__(self, num, mu, delay, G, ratio, restart, l, m, Al):
                self.num = num
                self.mu = float(mu)
                self.delay = delay
                self.G = float(G)
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

add_data_dir(11, "1", 0, "0", 1)                                                                                                                                                       
#add_data_dir(12, "1", 10000, "0", 1)                                                                                                                                                   
#add_data_dir(13, "0.08187607564", 0, "0", 1)                                                                                                                                           
#add_data_dir(14, "1", 0, "0", 2)                                                                                                                                                       
#add_data_dir(15, "1", 10000, "0", 2)                                                                                                                                                   
add_data_dir(16, "0.5", 0, "0", 1)                                                                                                                                                     
#add_data_dir(17, "0.5", 10000, "0", 1)                                                                                                                                                 
#add_data_dir(18, "0.5", 0, "0.000001", 1)                                                                                                                                              
#add_data_dir(19, "1", 0, "0", 1, 1) # resume from stationary BH distribution                                                                                                           
#add_data_dir(20, "0.5", 0, "0", 1, 1) # resume from stationary BH distribution                                                                                                         
#add_data_dir(21, "0.5", 0, "0.01", 1)
#add_data_dir(23, "0.5", 0, "0.0000000001", 1)
#add_data_dir(24, "0.5", 0, "0.00000000000000000001", 1, 1)
add_data_dir(25, "0.5", 0, "0", 1, 0, 1, 1)
#add_data_dir(28, "0.5", 0, "0.00000001", 1)
add_data_dir(30, "0.5", 0, "0", 1, 0, 2, 2)
#add_data_dir(34, "0.5", 0, "0.000000000001", 1)
add_data_dir(36, "0.5", 0, "0", 1, 0, 1, -1)

############################

def get_point_data(dd):
        BinaryBH_dataset_path = data_root_dir + dd.name + "/BinaryBHSFPlot_*.3d.hdf5"
        ds = yt.load(BinaryBH_dataset_path)
        print("loaded data for " + dd.name)
        phi0 = 1
        rho0 = 0.5*(dd.mu*phi0)**2

        Nsteps = len(ds)

        data_storage = {}
        for sto, dsi in ds.piter(storage=data_storage):
                t = dsi.current_time
                #dt = 2 * dd.dt_mult * 40
                #n = int(t/dt)
                pt = dsi.r[L/2, L/2, z_position]
                value = float(pt["rho"]/rho0)
                output = [t, value]
                sto.result = output
                sto.result_id = str(dsi)
                print("done time {:f}".format(t))
                
        if yt.is_root():
                # output to file
                
                filename = dd.name + "_rho_at_centre.dat"
                output_path = output_data_dir + filename
                # output header to file
                
                f = open(output_path, "w+")
                f.write("# t    rho at centre\n")
                # r positions (relative to centre of binary)
                for key in sorted(data_storage.keys()):
                        data = data_storage[key]
                        f.write("{:.3f}".format(data[0]))
                        f.write("\t")
                        f.write("{:.4f}".format(data[1]))
                        f.write("\n")
                f.close()
                print("saved data to file " + str(output_path))
#

#for dd in data_dirs:
#        get_point_data(dd)

def plot_graph():
        ##### plot graph
        print("plotting graph ... ")
        fig, ax = plt.subplots()
        colours = ['r', 'g', 'b', 'm', 'c--', 'y', 'k', 'r--', 'g--', 'b--', 'm--', 'c--', 'y--']
        font_size = 12
        title_font_size = 10
        label_size = 12
        legend_font_size = 6
        for i in range(0, len(data_dirs)):
                dd = data_dirs[i]
                # load data
                file_name = output_data_dir + dd.name + "_rho_at_centre.dat"
                data = np.genfromtxt(file_name, skip_header=1)
                t = data[:,0]
                rho = data[:,1]
                print("loaded data for ", file_name)
                label_="$\\mu$={:.2f} $l,m$={:d},{:d} G=0".format(dd.mu, dd.l, dd.m)
                #label_="$\\mu$={:.2f} $G$={:.1e}".format(dd.mu, dd.G)
                ax.plot(t, np.log10(rho), colours[i], linewidth=1, label=label_)
        title = "$\\rho$ at centre between BHs, GR binary mass ratio 1"
        ax.set_title(title, fontsize=title_font_size)
        plt.legend(loc='best', fontsize=legend_font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        ax.minorticks_on()
        ax.set_xlim((0, 2200))
        ax.set_ylim((-1.5, 4))
        ax.set_xlabel('t',fontsize=label_size, labelpad=0)
        ax.set_ylabel('$\\log_{10}(\\rho/\\rho_0)$', fontsize=label_size, labelpad=0)
        save_path = plots_dir + "GR_BH_rho_centre_compare_lm_G_plot.png"
        fig.tight_layout()
        ax.margins(2)
        plt.savefig(save_path, transparent=False)
        print("saved " + save_path)
        plt.clf()

plot_graph()

