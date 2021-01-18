import yt
import numpy as np
import matplotlib.pyplot as plt
import math
from sys import exit
from os import makedirs

yt.enable_parallelism()

# Newtonian Binaries

data_root_dir = "/p/scratch/pra116/bamber1/NewtonianBinaryScalar/"
plots_dir = "/p/scratch/pra116/bamber1/plots/Newtonian_Binary_BH/"
data_dir = "/p/home/jusers/bamber1/juwels/GRChombo/Analysis/data/Newtonian_Binary_BH_data/"

L=1024
N1=256
abmax=20
z_position = 0.001
width = 100
N = 256

############################

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
                
#add_data_dir(7, "0.2", "10", "0.02", "0.5", 0, 0, "0")                                                                                                        
#add_data_dir(8, "0.2", "10", "0.025", "0.5", 0, 0, "0")                                                                                                       
#add_data_dir(9, "0.2", "10", "0.015", "0.5", 0, 0, "0")                                                                                                       
#add_data_dir(10, "0.2", "10", "0.01", "0.5", 0, 0, "0")                                                                                                       
#add_data_dir(11, "0.2", "10", "0.03", "0.5", 0, 0, "0")                                                                                                       
#add_data_dir(12, "0.2", "10", "0.02", "0.5", 1, -1, "0")                                                                                                      
#add_data_dir(13, "0.2", "10", "0.02", "0.5", 1, 1, "0")                                                                                                        
add_data_dir(15, "0.48847892320123", "12.21358", "1", "0.0625", 0, 0, "0")
#add_data_dir(16, "0.48847892320123", "12.21358", "1", "0.0625", 1, -1, "0")
#add_data_dir(17, "0.48847892320123", "12.21358", "1", "0.0625", 1, 1, "0")
#add_data_dir(18, "0.2", "10", "1", "0.0625", 0, 0, "0")
#add_data_dir(19, "0.2", "10", "0.1", "0.125", 0, 0, "0")
#add_data_dir(20, "0.2", "10", "0.5", "0.0625", 0, 0, "0")
                
############################

def ray_pos(t, M, d, width):
        omega_BBH = np.sqrt(2*M/d**3)
        start = [(L-width*np.cos(t*omega_BBH))/2,(L-width*np.sin(t*omega_BBH))/2,z_position]
        end = [(L+width*np.cos(t*omega_BBH))/2,(L+width*np.sin(t*omega_BBH))/2,z_position]
        return (start, end)
        
"""def get_puncture_data(BBHsubdir):
	file_name = data_root_dir + BBHsubdir + "/BinaryBHSFChk_Punctures.dat"
	data = np.genfromtxt(file_name, skip_header=1)	
	return data"""

def make_ray(ds, start, end, N):
        print("making ray")
        print("start = ",start)
        print("end = ",end)
        ray = ds.r[start:end:N*1j]
        return np.array(ray["rho"])
#
def get_line_data(dd):
        BinaryBH_dataset_path = data_root_dir + dd.name + "/Newton_plt*.3d.hdf5"
        ds = yt.load(BinaryBH_dataset_path)
        print("loaded data for " + dd.name)
        phi0 = 1
        rho0 = 0.5*(dd.mu*phi0)**2

        Nsteps = len(ds)
        
        data_storage = {}
        for sto, dsi in ds.piter(storage=data_storage):
                t = dsi.current_time
                n = int(t/5.0)
                start, end = ray_pos(t, dd.M, dd.d, width)
                ray = make_ray(dsi, start, end, N)/rho0
                output = [t, ray]
                sto.result = output
                sto.result_id = str(dsi)
                print("done {:d} of {:d}".format(n, Nsteps))
                
        if yt.is_root():
                # output to file                                                                                                                                
                filename = dd.name + "_rho_profile_along_binary.dat"
                output_path = data_dir + filename
                # output header to file                                                                                                                          
                f = open(output_path, "w+")
                f.write("# t    rho at displacement = ...    #\n")
                # r positions (relative to centre of binary)
                f.write("0\t")
                for pos in np.linspace(-width/2, width/2, N):
                        f.write("{:.5f}\t".format(pos))
                f.write("\n")
                # write out data
                for key in sorted(data_storage.keys()):
                        data = data_storage[key]
                        f.write("{:.3f}".format(data[0]))
                        for i in range(0, N):
                                f.write("\t{:.4f}".format(data[1][i]))
                        f.write("\n")
                f.close()
                print("saved data to file " + str(output_path))
#

for dd in data_dirs:
        get_line_data(dd)
