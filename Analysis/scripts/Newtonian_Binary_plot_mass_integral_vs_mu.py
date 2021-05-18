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

add_data_dir(6, "0.2", "10", "0.005", "0.5", 0, 0, "0")
add_data_dir(10, "0.2", "10", "0.01", "0.5", 0, 0, "0")
add_data_dir(9, "0.2", "10", "0.015", "0.5", 0, 0, "0")
add_data_dir(7, "0.2", "10", "0.02", "0.5", 0, 0, "0")
add_data_dir(8, "0.2", "10", "0.025", "0.5", 0, 0, "0")
#add_data_dir(11, "0.2", "10", "0.03", "0.5", 0, 0, "0")

#add_data_dir(15, "0.48847892320123", "12.21358", "1", "0.0625", 0, 0, "0")
#add_data_dir(16, "0.48847892320123", "12.21358", "1", "0.0625", 1, -1, "0")
#add_data_dir(17, "0.48847892320123", "12.21358", "1", "0.0625", 1, 1, "0")
add_data_dir(21, "0.2", "10", "0.05", "0.25", 0, 0, "0")
#add_data_dir(19, "0.2", "10", "0.1", "0.125", 0, 0, "0")
#add_data_dir(24, "0.2", "10", "0.15", "0.0625", 0, 0, "0")
#add_data_dir(22, "0.2", "10", "0.2", "0.0625", 0, 0, "0")
#add_data_dir(23, "0.2", "10", "0.3", "0.0625", 0, 0, "0")
#add_data_dir(20, "0.2", "10", "0.5", "0.0625", 0, 0, "0")
#add_data_dir(18, "0.2", "10", "1", "0.03125", 0, 0, "0")
#add_data_dir(26, "0.2", "10", "2", "0.03125", 0, 0, "0")
#add_data_dir(27, "0.2", "10", "5", "0.015625", 0, 0, "0")

def time_average(x, n):
        N = len(x)
        n_chunks = int(np.floor(N/n))
        x_out = np.zeros(n_chunks)
        for i in range(0, n_chunks):
                x_out[i] = np.mean(x[i*n:(i+1)*n])
        x_out[-1] = np.mean(x[N-n:])
        return x_out

phi0=1
average_time = False
av_n = 1
r_min = 0
r_max = 50

def load_rho_integral_data():
        # load data from csv files
        data = {}
        for dd in data_dirs:
                file_name = data_root_path + dd.name + "_mass_rmin_{:d}_rmax_{:d}_chombo.dat".format(r_min, r_max)
                data[dd.num] = np.genfromtxt(file_name, skip_header=2)
                print("loaded data for " + dd.name)
        return data     

"""def load_ang_mom_data():
        # load data from csv files                                                                                                                                                  
        data = {}
        for dd in data_dirs:
                file_name = data_root_path + dd.name + "_ang_mom_rmin_{:d}_rmax_{:d}_chombo.dat".format(r_min, r_max)
                data[dd.num] = np.genfromtxt(file_name, skip_header=2)
                print("loaded data for " + dd.name)
        return data

def load_Cphi_data():
        # load data from csv files                                                                                                   
        data = {}
        for dd in data_dirs:
                file_name = data_root_path + dd.name + "_Cphi_rmin_{:d}_rmax_{:d}_chombo.dat".format(r_min, r_max)
                data[dd.num] = np.genfromtxt(file_name, skip_header=2)
                print("loaded data for " + dd.name)
        return data"""

def load_flux_data():
        #
        data = {}
        filename_base = "/p/scratch/pra116/bamber1/NewtonianBinaryScalar/"
        for dd in data_dirs:
                file_name = filename_base + dd.name + "/outputs/Force_integrals.dat"
                data[dd.num] = np.genfromtxt(file_name, skip_header=1)
                print("loaded data for " + dd.name)
        return data

def cumulative(y, dt):
        y_out = np.zeros(len(y))
        for i in range(0, len(y)):
                y_out[i] = dt*np.sum(y[0:i])
        return y_out

"""def load_rho_integral_data():
        #
        data = {}
        filename_base = "/p/scratch/pra116/bamber1/NewtonianBinaryScalar/"
        for dd in data_dirs:
                #file_name = filename_base + dd.name + "/outputs/RhoIntegrals_r{:d}.dat".format(r_max)
                file_name = filename_base + dd.name + "/outputs/RhoIntegral.dat"
                data[dd.num] = np.genfromtxt(file_name, skip_header=1)
                print("loaded data for " + dd.name)
        return data"""

def analytic_cumulative_flux(t, r, mu, M, s):
        tau = t*mu
        Cumulative_Flux = (tau**2*(45*r**5*mu**2 + 30*M**2*r*(-1533 + 204*r**2*mu**2 - 106*tau**2) + 10*M**3*(6462 + 6192*r**2*mu**2 + 2289*tau**2 - 14*tau**4) +\
                                   5*M**4*r*mu**2*(156582 - 3675*tau**2 + 2*tau**4) - 20*M**5*mu**2*(-1395 - 25053*tau**2 + 73*tau**4) + 6*M*(90*r**4*mu**2 - 9*s**4*mu**2 - 5*r**2*(18 + tau**2))))/(90*r**5*mu**2)
        #Cumulative_Flux = tau**2/2
        return 4*np.pi*phi0**2*Cumulative_Flux*M
        
def plot_graph(mass_or_ang_mom, use_cumulative):
        #data = load_rho_integral_data()
        flux_data = load_flux_data()
        colours = ['r', 'b', 'g', 'm', 'y', 'c', 'k', '0.5']
        #colours = ['r-', 'b-', 'g-', 'm-', 'y-', 'c-', 'k-', 'r--', 'b--', 'g--','y--','c--']
        i = 0
        ### plot mass flux graph
        fig, ax1 = plt.subplots()
        fig.set_size_inches(6.5,6)
        font_size = 10
        title_font_size = 10
        label_size = 10
        legend_font_size = 10
        #rc('xtick',labelsize=font_size)
        #rc('ytick',labelsize=font_size)
        for i in range(0,len(data_dirs)):
                dd = data_dirs[i]
                #line_data = data[dd.num]
                mu = float(dd.mu)
                #t_mass = line_data[:,0]
                rho0 = 0.5*(phi0**2)*(dd.mu**2)
                V = (4*np.pi/3)*(r_max**3)
                omega_B = np.sqrt(2*dd.M/(dd.d**3))
                E0 = V*rho0
                """dt = t_mass[2] - t_mass[1]
                if mass_or_ang_mom:
                        mass = line_data[:,1]*2 # the 2 is from it being a half sphere ??
                else:
                        mass = line_data[:,2]*2"""
                mass_norm = E0
                #mass_norm = mass[0] # mass at t=0 (or thereabouts)
                """delta_mass = mass[1:] - mass[0]
                dmass_dt = (mass[1:] - mass[:-1])/dt
                #
                omega_B = np.sqrt(2*dd.M/(dd.d**3))
                ## need the cumulative Cphi
                Cphi = line_data[:,3]
                dt = t_mass[2] - t_mass[1]
                Cphi_cumulative = cumulative(Cphi, dt)
                if mass_or_ang_mom:
                        Cphi_cumulative = Cphi_cumulative*omega_B
                else:
                        pass"""
                ## now we need the cumulative flux
                flux_line_data = flux_data[dd.num]
                t_flux = flux_line_data[:-1,0]
                dt_flux = t_flux[2] - t_flux[1]
                if mass_or_ang_mom:
                        if (r_max==50):
                                flux = flux_line_data[:-1,1]
                        elif (r_max==120):
                                flux = flux_line_data[:-1,3]
                else:
                        if (r_max==50):
                                flux = flux_line_data[:-1,2]
                        elif (r_max==120):
                                flux = flux_line_data[:-1,4]
                flux_cumulative = cumulative(flux, dt_flux)
                #
                label_ = "$\\mu/\\omega_B=${:.2f}".format(dd.mu/0.02)
                # plot the lines
                if use_cumulative:
                        #analytic_c_flux = analytic_cumulative_flux(t_flux, r_max, dd.mu, dd.M, dd.d)
                        #ax1.plot(t_mass,Cphi_cumulative/mass_norm,"g-", label=label_+" cumul. $C_0$")
                        ax1.plot(t_flux,flux_cumulative/mass_norm,color=colours[i],linestyle="solid", label=label_+" cumul. flux")
                        #ax1.plot(dd.mu*t_flux,analytic_c_flux/mass_norm,color=colours[i],linestyle="-.", label=label_+" analytic cumul. flux")  
                        #ax1.plot(dd.mu*t_mass[1:],delta_mass/mass_norm,color=colours[i],linestyle="solid",label=label_)
                        #ax1.plot(t_mass[1:],(delta_mass-Cphi_cumulative[1:])/mass_norm,"k--", label=label_+" $\\Delta E$ - cumul. $C_0$")
                else:
                        ax1.plot(t_flux,flux,"b-", label=label_+" flux")
                        #ax1.plot(t_mass,Cphi,"g-", label=label_+" $C_0$")
                        ax1.plot(t_mass[1:],dmass_dt,"r-", label=label_+" $dE/dt$") 
                        #ax1.plot(t_mass[1:],(dmass_dt-Cphi[1:]),"k--", label=label_+" $dE/dt - C_0$")
        #ax1.set_xlabel("$\\tau$", fontsize=font_size)
        ax1.set_xlabel("time", fontsize=font_size)
        if mass_or_ang_mom:
                if use_cumulative:
                        ax1.set_ylabel("$\\Delta E / E_0$", fontsize=font_size)
                        plt.title("Mass inside $R=${:d}, $M=0.2,d=10$".format(r_max))
                        save_path = plots_path + "Newtonian_BBH_mass_inside_r={:d}_compare_mu.png".format(r_max)
                else:
                        ax1.set_ylabel("$dE/dt$", fontsize=font_size)
                        plt.title("Rate of change of mass inside $R=${:d}, $M=0.2,d=10$".format(r_max))
                        save_path = plots_path + "Newtonian_BBH_{:s}_dmass_dt_inside_r={:d}_compare_mu_vs_analytic.png".format(r_max)
        else:
                if use_cumulative:
                        ax1.set_ylabel("$\\log_{10}$(|ang. mom. enclosed| / $E(t=0)$", fontsize=font_size)
                        plt.title("Ang. mom. inside $R=${:d}, $M=0.2,d=10$".format(r_max))
                        save_path = plots_path + "Newtonian_BBH_{:s}_ang_mom_inside_r={:d}_compare_mu_vs_analytic.png".format(r_max)
                else:
                        ax1.set_ylabel("$dJ/dt$", fontsize=font_size)
                        plt.title("Rate of change of ang. mom. inside $R=${:d}, $M=0.2,d=10$".format(r_max))
                        save_path = plots_path + "Newtonian_BBH_{:s}_dang_mom_dt_inside_r={:d}_compare_mu_vs_analytic.png".format(r_max)
        ax1.legend(loc='best', fontsize=legend_font_size)
        ax1.set_xlim((0,20000))
        #ax1.set_ylim((0,40000))
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        plt.tight_layout()
        plt.savefig(save_path)
        print("saved plot as " + str(save_path))
        plt.clf()

plot_graph(True, True)
#plot_graph(False, True)
#plot_graph(True, False)
#plot_graph(False, False)
