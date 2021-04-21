#import yt
import numpy as np
#from scipy.interpolate import interp1d
#from scipy.optimize import fsolve
import math
#from yt import derived_field
import time
import sys
from matplotlib import pyplot as plt
from os import makedirs

#yt.enable_parallelism()

L=1024
N1=256

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
                self.name = "run{:04d}_M{:s}_d{:s}_mu{:s}_dt_mult{:s}_l{:d}_m{:d}_Al{:s}_L{:d}_N{:d}".format(num, M, d, mu, dt_mult, l, m, Al, L, N1)

data_dirs = []
def add_data_dir(num, M, d, mu, dt_mult, l, m, Al):
        x = data_dir(num, M, d, mu, dt_mult, l, m, Al)
        data_dirs.append(x)

add_data_dir(6, "0.2", "10", "0.005", "0.5", 0, 0, "0")
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
#add_data_dir(24, "0.2", "10", "0.15", "0.0625", 0, 0, "0")
add_data_dir(22, "0.2", "10", "0.2", "0.0625", 0, 0, "0")
#add_data_dir(25, "0.2", "10", "0.25", "0.0625", 0, 0, "0")
add_data_dir(23, "0.2", "10", "0.3", "0.0625", 0, 0, "0")
add_data_dir(20, "0.2", "10", "0.5", "0.0625", 0, 0, "0")
add_data_dir(18, "0.2", "10", "1", "0.03125", 0, 0, "0")
add_data_dir(26, "0.2", "10", "2", "0.03125", 0, 0, "0")
add_data_dir(27, "0.2", "10", "5", "0.015625", 0, 0, "0")

# set up parameters

data_root_path = "/p/scratch/pra116/bamber1/NewtonianBinaryScalar/"
#"/cosma6/data/dp174/dc-bamb1/GRChombo_data/NewtonianBinaryBHScalar/"
plots_path="/p/home/jusers/bamber1/juwels/GRChombo/Analysis/plots/Newtonian_Binary_BH/"
#"/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/"

max_radius = 50

output_dir = "/p/home/jusers/bamber1/juwels/GRChombo/Analysis/data/Newtonian_Binary_BH_data/"

#change_in_E = True

def calculate_mass_in_sphere(dd):
        data_sub_dir = dd.name

        start_time = time.time()
        
        # load dataset time series
        
        dataset_path = data_root_path + data_sub_dir + "/Newton_plt*.3d.hdf5"
        ds = yt.load(dataset_path) # this loads a dataset time series
        print("loaded data from ", dataset_path)
        print("time = ", time.time() - start_time)
        N = len(ds)
        
        ds0 = ds[0] # get the first dataset 
        
        # set centre
        L = 256.0       
        center = [L/2, L/2, 0]
        rho0 = 0.5*(dd.mu**2)
        
        data_storage = {}
        # iterate through datasets (forcing each to go to a different processor)
        for sto, dsi in ds.piter(storage=data_storage):
                time_0 = time.time()
                # store time
                current_time = dsi.current_time 
                output = [current_time]
                
                # make sphere
                sphere = dsi.sphere(center, max_radius)
                        
                # calculate energy inside sphere
                meanE = sphere.mean("rho", weight="cell_volume")
                output.append(meanE)
                
                # calculate angular momentum inside sphere
                meanJ = sphere.mean("rhoJ", weight="cell_volume")
                output.append(meanJ/rho0)

                # store output
                sto.result = output
                sto.result_id = str(dsi)
                dt = 2.0 * float(dd.dt_mult)
                i = int(current_time/dt)
                print("done {:d} of {:d} in {:.1f} s".format(i+1, N, time.time()-time_0), flush=True)
        
        if yt.is_root():        
                # make data directory if it does not already exist
                makedirs(home_path + output_dir, exist_ok=True)
                # output to file
                dd.filename = "{:s}_mean_rho_rhoJ_in_r={:d}.csv".format(dd.name, max_radius)
                output_path = home_path + output_dir + "/" + dd.filename 
                # output header to file
                f = open(output_path, "w+")
                f.write("# t    mean rho        mean rhoJ       in " + str(max_radius) + " #\n")
                # output data
                for key in sorted(data_storage.keys()):
                        data = data_storage[key]
                        f.write("{:.3f} ".format(data[0]))
                        f.write("{:.8f} ".format(data[1]))
                        f.write("{:.8f}\n".format(data[2]))
                f.close()
                print("saved data to file " + str(output_path))
                
def load_data_v1():
        # load data from csv files
        data = {}
        for dd in data_dirs:
                file_name = output_dir + "{:s}_mean_rho_rhoJ_in_r={:d}.csv".format(dd.name, max_radius)
                data[dd.num] = np.genfromtxt(file_name, skip_header=1)
                print("loaded data for " + dd.name)
        return data     

def load_data_v3(mass_or_ang_mom):
        # load data from csv files                                                                
        data = {}
        for dd in data_dirs:
                if mass_or_ang_mom:
                        file_name = output_dir + dd.name + "_mass_rmin_{:d}_rmax_{:d}_chombo.dat".format(0, max_radius)
                else:
                        file_name = output_dir + dd.name + "_ang_mom_rmin_{:d}_rmax_{:d}_chombo.dat".format(0, max_radius)
                data[dd.num] = np.genfromtxt(file_name, skip_header=2)
                print("loaded data for " + dd.name)
        return data

def load_data_v2():
        # load data from csv files                                                                                                                                                      
        data = {}
        for dd in data_dirs:
                file_name = data_root_path + dd.name + "/outputs/RhoIntegral.dat"
                data[dd.num] = np.genfromtxt(file_name, skip_header=1)
                print("loaded data for " + dd.name)
        return data

def plot_graph(change_in_E, mass_or_ang_mom):
        data = load_data_v3(mass_or_ang_mom)
        colours = ['r-', 'b-', 'g-', 'm-', 'c-', 'y-', 'k-', 'r--', 'b--', 'g--', 'm--', 'c--', 'y--', 'k--'] 
        i = 0
        phi0 = 1
        ### plot mass flux graph                                                           
        fig, ax1 = plt.subplots()
        fig.set_size_inches(6.5,6)
        font_size = 14
        title_font_size = 14
        label_size = 14
        legend_font_size = 14
        #rc('xtick',labelsize=font_size)
        #rc('ytick',labelsize=font_size) 
        for dd in data_dirs:
                line_data = data[dd.num]
                t = line_data[:,0]
                rho0 = 0.5*(phi0**2)*(dd.mu**2)
                V = (4*np.pi/3)*(max_radius**3)
                omega_B = np.sqrt(2*dd.M/(dd.d**3))
                E0 = V*rho0
                mass = line_data[:,1]/E0 #- line_data[0,1]
                print("mass data = ", mass[:10])
                #ang_mom = line_data[:,2]/E0 #- line_data[0,1]
                label_ = "$\\mu/\\omega_B$={:.2f}".format(dd.mu/omega_B)
                if mass_or_ang_mom:
                        if change_in_E:
                                ax1.plot(t[1:], mass[1:] - mass[0], colours[i], label=label_)
                                plt.ylim((0, 20)) 
                        else:
                                ax1.plot(t, mass/mass[0], colours[i], label=label_)
                                plt.ylim((1.0, 3.0))
                else:
                        if change_in_E:
                                ax1.plot(t[1:], mass[1:] - mass[0], colours[i], label=label_)
                                #plt.ylim((0, 20))
                        else:
                                ax1.plot(t, mass, colours[i], label=label_)
                                #plt.ylim((1.0, 3.0))
                i = i + 1
        plt.xlabel("time", fontsize=label_size)
        plt.xlim((0, 4000))
        if mass_or_ang_mom:
                if change_in_E:
                        ax1.set_ylabel("$\\Delta E$ in $r < $" + "{:.0f} / $E_0$".format(max_radius), fontsize=label_size)
                else:
                        ax1.set_ylabel("$E$ in $r$ < " + "{:d} / $E(t=0)$".format(max_radius),fontsize=label_size)
        else:
                if change_in_E:
                        ax1.set_ylabel("$\\Delta J_{\\phi}$ in $R < $" + "{:.0f} / $E_0$".format(max_radius), fontsize=label_size)
                else:
                        ax1.set_ylabel("$J_{\\phi}$ in $R$ < " + "{:d} / $E(t=0)$".format(max_radius),fontsize=label_size)
        plt.legend(loc='upper right', fontsize=legend_font_size)
        if mass_or_ang_mom:
                plt.title("Scalar field energy inside a sphere vs time, $M=0.2,d=10$", fontsize=title_font_size)
        else:
                plt.title("Angular momentum inside a sphere vs time, $M=0.2,d=10$", fontsize=title_font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        plt.tight_layout()
        if change_in_E:
                if mass_or_ang_mom:
                        save_path = plots_path + "Newtonian_binary_delta_mean_rho_in_sphere_radius_" + str(max_radius) + "_v3.png"
                else:
                        save_path = plots_path + "Newtonian_binary_delta_ang_mom_in_sphere_radius_" + str(max_radius) + "_v3.png"
        else:
                if mass_or_ang_mom:
                        save_path = plots_path + "Newtonian_binary_mean_rho_in_sphere_radius_" + str(max_radius) + "_v3.png"
                else:
                        save_path = plots_path + "Newtonian_binary_ang_mom_in_sphere_radius_" + str(max_radius) + "_v3.png"
        plt.savefig(save_path)
        print("saved plot as " + str(save_path))
        plt.clf()

#for dd in data_dirs[1:]:
#       calculate_mass_in_sphere(dd)

plot_graph(True, True)
plot_graph(True, False)
plot_graph(False, True)
plot_graph(False, False)
