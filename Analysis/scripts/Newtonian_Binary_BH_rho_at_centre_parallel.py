import yt
import numpy as np
import matplotlib.pyplot as plt
import math
from sys import exit
from os import makedirs

yt.enable_parallelism()

# Newtonian Binaries

data_root_dir = "/p/scratch/pra116/bamber1/NewtonianBinaryScalar/"
plots_dir = "/p/home/jusers/bamber1/juwels/GRChombo/Analysis/plots/Newtonian_Binary_BH/"
output_data_dir = "/p/home/jusers/bamber1/juwels/GRChombo/Analysis/data/Newtonian_Binary_BH_data/"

L=1024
N1=256
abmax=20
z_position = 0.00
width = 100
N = 512

############################

class data_dir:
        def __init__(self, num, M, d, mu, dt_mult, l, m, Al):
                self.num = num
                self.M = float(M)
                self.d = float(d)
                self.mu = float(mu)
                self.dt_mult = float(dt_mult)
                self.l = l
                self.m = m
                self.Al = float(Al)
                self.name = "run{:04d}_M{:s}_d{:s}_mu{:s}_dt_mult{:s}_l{:d}_m{:d}_Al{:s}_L{:d}_N{:d}".format(num, M, d, mu, dt_mult, l, m, Al, L, N1)

data_dirs = []
def add_data_dir(num, M, d, mu, dt_mult, l, m, Al):
        x = data_dir(num, M, d, mu, dt_mult, l, m, Al)
        data_dirs.append(x)

add_data_dir(5, "0.2", "10", "0.002", "0.5", 0, 0, "0")
#add_data_dir(6, "0.2", "10", "0.005", "0.5", 0, 0, "0")
add_data_dir(10, "0.2", "10", "0.01", "0.5", 0, 0, "0")
#add_data_dir(9, "0.2", "10", "0.015", "0.5", 0, 0, "0")
add_data_dir(7, "0.2", "10", "0.02", "0.5", 0, 0, "0")
#add_data_dir(8, "0.2", "10", "0.025", "0.5", 0, 0, "0")
add_data_dir(11, "0.2", "10", "0.03", "0.5", 0, 0, "0")
#add_data_dir(12, "0.2", "10", "0.02", "0.5", 1, -1, "0")
#add_data_dir(13, "0.2", "10", "0.02", "0.5", 1, 1, "0")
#add_data_dir(15, "0.48847892320123", "12.21358", "1", "0.0625", 0, 0, "0")
#add_data_dir(16, "0.48847892320123", "12.21358", "1", "0.0625", 1, -1, "0")
#add_data_dir(17, "0.48847892320123", "12.21358", "1", "0.0625", 1, 1, "0")
add_data_dir(21, "0.2", "10", "0.05", "0.25", 0, 0, "0")
add_data_dir(19, "0.2", "10", "0.1", "0.125", 0, 0, "0")
add_data_dir(24, "0.2", "10", "0.15", "0.0625", 0, 0, "0")
add_data_dir(22, "0.2", "10", "0.2", "0.0625", 0, 0, "0")
#add_data_dir(25, "0.2", "10", "0.25", "0.0625", 0, 0, "0")
#add_data_dir(23, "0.2", "10", "0.3", "0.0625", 0, 0, "0")
#add_data_dir(20, "0.2", "10", "0.5", "0.0625", 0, 0, "0")
#add_data_dir(18, "0.2", "10", "1", "0.03125", 0, 0, "0")
#add_data_dir(26, "0.2", "10", "2", "0.03125", 0, 0, "0")
#add_data_dir(27, "0.2", "10", "5", "0.015625", 0, 0, "0")

############################

def get_point_data(dd):
        BinaryBH_dataset_path = data_root_dir + dd.name + "/Newton_plt*.3d.hdf5"
        ds = yt.load(BinaryBH_dataset_path)
        print("loaded data for " + dd.name)
        phi0 = 1
        rho0 = 0.5*(dd.mu*phi0)**2

        Nsteps = len(ds)

        data_storage = {}
        for sto, dsi in ds.piter(storage=data_storage):
                t = dsi.current_time
                dt = 2 * dd.dt_mult * 40
                n = int(t/dt)
                pt = dsi.r[L/2, L/2, z_position]
                value = float(pt["rho"]/rho0)
                output = [t, value]
                sto.result = output
                sto.result_id = str(dsi)
                print("done {:d} of {:d}".format(n, Nsteps))
                
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
        line_positions = np.linspace(-width/2, width/2, N)
        #colours = ['r', 'g', 'b', 'm', 'c', 'y', 'k', 'r--', 'g--', 'b--', 'm--', 'c--', 'y--']
        colours = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
        font_size = 12
        title_font_size = 10
        label_size = 12
        legend_font_size = 12
        for i in range(0, len(data_dirs)):
                dd = data_dirs[i]
                # load data
                omega_BH = np.sqrt(2*dd.M/(dd.d**3))
                file_name = output_data_dir + dd.name + "_rho_at_centre.dat"
                data = np.genfromtxt(file_name, skip_header=1)
                t = data[:,0]
                rho = data[:,1]
                print("loaded data for ", file_name)
                ax.plot(t, np.log10(rho), colours[i], linewidth=1, label="$\\mu/\\omega_B$={:.2f}".format(dd.mu/omega_BH))
        title = "$\\rho$ at centre between BHs, Newtonian binary $M=0.2,d=10$"
        ax.set_title(title, fontsize=title_font_size)
        plt.legend(loc='best', fontsize=legend_font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        ax.minorticks_on()
        ax.set_xlim((0, 10000))
        ax.set_ylim((0, 2))
        ax.set_xlabel('t',fontsize=label_size, labelpad=0)
        ax.set_ylabel('$\\log_{10}(\\rho/\\rho_0)$', fontsize=label_size, labelpad=0)
        save_path = plots_dir + "Newtonian_BH_rho_centre_L{:d}_N{:d}_compare_mu_plot_v2.png".format(L, N1)
        fig.tight_layout()
        ax.margins(2)
        plt.savefig(save_path, transparent=False)
        print("saved " + save_path)
        plt.clf()

plot_graph()

