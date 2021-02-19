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

data_root_path = "/p/home/jusers/bamber1/juwels/GRChombo/Analysis/data/Newtonian_Binary_BH_data/"
plots_path = "/p/home/jusers/bamber1/juwels/GRChombo/Analysis/plots/Newtonian_Binary_BH/"

class data_dir:
        def __init__(self, num, M, d, mu, dt_mult, l, m, Al):
                self.num = num
                self.M = float(M)
                self.d = float(d)
                self.mu = float(mu)
                self.dt_mult = dt_mult
                self.l = l
                self.m = m
                self.Al = float(Al)
                self.name = "run{:04d}_M{:s}_d{:s}_mu{:s}_dt_mult{:s}_l{:d}_m{:d}_Al{:s}_L{:d}_N{:d}".format(num, M, d, mu, dt_mult, l, m, Al, L, N)

data_dirs = []
def add_data_dir(num, M, d, mu, dt_mult, l, m, Al):
        x = data_dir(num, M, d, mu, dt_mult, l, m, Al)
        data_dirs.append(x)

add_data_dir(10, "0.2", "10", "0.01", "0.5", 0, 0, "0")
add_data_dir(9, "0.2", "10", "0.015", "0.5", 0, 0, "0")
add_data_dir(7, "0.2", "10", "0.02", "0.5", 0, 0, "0")
add_data_dir(8, "0.2", "10", "0.025", "0.5", 0, 0, "0")
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
add_data_dir(23, "0.2", "10", "0.3", "0.0625", 0, 0, "0")
add_data_dir(20, "0.2", "10", "0.5", "0.0625", 0, 0, "0")
add_data_dir(18, "0.2", "10", "1", "0.0625", 0, 0, "0")

def time_average(x, n):
        N = len(x)
        n_chunks = int(np.floor(N/n))
        x_out = np.zeros(n_chunks)
        for i in range(0, n_chunks):
                x_out[i] = np.mean(x[i*n:(i+1)*n])
        x_out[-1] = np.mean(x[N-n:])
        return x_out

phi0=1
average_time = True
av_n = 5
cumulative= False
r_extract = 50

def load_data():
        # load data from csv files
        data = {}
        for dd in data_dirs:
                file_name = data_root_path + dd.name + "_mass_ang_mom_flux_r_" + str(r_extract) + ".dat"
                data[dd.num] = np.genfromtxt(file_name, skip_header=0)
                print("loaded data for " + dd.name)
        return data     

def plot_graph(mass_or_ang_mom):
        data = load_data()
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
                t1 = line_data[:,0]
                mu = float(dd.mu)
                E0 = 0.5*(phi0*mu)**2
                F0 = 4*np.pi*(r_extract**2)*E0
                if mass_or_ang_mom:
                        flux = -line_data[:,1]/F0
                else:
                        flux = -line_data[:,2]/(F0*mu)
                if average_time:
                        t1 = time_average(t1, av_n)
                        flux = time_average(flux, av_n)
                if cumulative:
                        flux = np.cumsum(flux)/(r_extract/3)
                label_ = "$\\mu=${:.3f}".format(dd.mu)
                ax1.plot(t1,flux,colours[i], label=label_)
                i = i + 1
        ax1.set_xlabel("$t$", fontsize=font_size)
        ax1.set_xlim((0,5000))
        if cumulative:
                ax1.set_ylabel("cumulative flux / $E_0$")
                plt.title("Cumulative mass flux into $R=${:d}".format(r_extract))
                save_path = plots_path + "Newtonian_BBH_mass_flux_cumulative.png"
        else:
                if mass_or_ang_mom:
                        ax1.set_ylabel("mass flux / $F_0 \\mu$", fontsize=font_size)
                        plt.title("Mass flux into $R=${:d}, $M=0.2,d=10$".format(r_extract))
                        save_path = plots_path + "Newtonian_BBH_mass_flux_vs_t_r{:d}.png".format(r_extract)
                else:
                        ax1.set_ylabel("ang. mom. flux / $F_0$", fontsize=font_size)
                        plt.title("Ang. mom. flux into $R=${:d}, $M=0.2,d=10$".format(r_extract))
                        save_path = plots_path + "Newtonian_BBH_ang_mom_flux_vs_t_r{:d}.png".format(r_extract)
        ax1.legend(loc='best', fontsize=legend_font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        plt.tight_layout()
        plt.savefig(save_path)
        print("saved plot as " + str(save_path))
        plt.clf()

plot_graph(True)
plot_graph(False)
