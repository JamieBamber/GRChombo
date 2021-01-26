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
                
#add_data_dir(10, "0.2", "10", "0.01", "0.5", 0, 0, "0")
#add_data_dir(9, "0.2", "10", "0.015", "0.5", 0, 0, "0")
#add_data_dir(7, "0.2", "10", "0.02", "0.5", 0, 0, "0")
#add_data_dir(8, "0.2", "10", "0.025", "0.5", 0, 0, "0")
#add_data_dir(11, "0.2", "10", "0.03", "0.5", 0, 0, "0")
#add_data_dir(12, "0.2", "10", "0.02", "0.5", 1, -1, "0")
#add_data_dir(13, "0.2", "10", "0.02", "0.5", 1, 1, "0")
add_data_dir(15, "0.48847892320123", "12.21358", "1", "0.0625", 0, 0, "0")
add_data_dir(16, "0.48847892320123", "12.21358", "1", "0.0625", 1, -1, "0")
add_data_dir(17, "0.48847892320123", "12.21358", "1", "0.0625", 1, 1, "0")
#add_data_dir(18, "0.2", "10", "1", "0.0625", 0, 0, "0")
#add_data_dir(19, "0.2", "10", "0.1", "0.125", 0, 0, "0")
#add_data_dir(20, "0.2", "10", "0.5", "0.0625", 0, 0, "0")
                
############################

def ray_pos(t, M, d, width, z_position):
        omega_BBH = np.sqrt(2*M/d**3)
        start = [(L-width*np.cos(t*omega_BBH))/2,(L-width*np.sin(t*omega_BBH))/2,z_position]
        end = [(L+width*np.cos(t*omega_BBH))/2,(L+width*np.sin(t*omega_BBH))/2,z_position]
        return (start, end)
        
"""def get_puncture_data(BBHsubdir):
	file_name = data_root_dir + BBHsubdir + "/BinaryBHSFChk_Punctures.dat"
	data = np.genfromtxt(file_name, skip_header=1)	
	return data"""

def make_ray(dsi, start, end, N):
        ray = dsi.r[start:end:N*1j]                                                                                          
        result = np.array(ray["rho"])
        #print("length = ", len(result))
        return result

def advanced_make_ray(dsi, t, M, d, width, z_position, N):
        ### First make a ray between the two black holes
        # dx = width / N
        dx = width / N
        exclusion_radius = M
        # space between BH = d - 2*R_s
        space_between_BH = d - 2*exclusion_radius
        inner_num = int(np.floor(space_between_BH/(2*dx)))
        num_between_BH = 2*inner_num   # assume N is even, make sure num_between_BH is also even
        inner_ray_length = dx*num_between_BH
        inner_start, inner_end = ray_pos(t, M, d, inner_ray_length, z_position)
        inner_ray_raw = dsi.r[inner_start:inner_end:num_between_BH*1j]
        inner_ray = np.array(inner_ray_raw["rho"])
        ### Then make the ray bits either side of the black holes
        outer_num = int(np.ceil((d/2+exclusion_radius)/dx))
        outer_start, outer_end = ray_pos(t, M, d, 2*outer_num*dx, z_position)
        edge_start, edge_end = ray_pos(t, M, d, width, z_position)
        outer_ray_N = N/2 - outer_num
        outer_ray_1 = np.array(dsi.r[edge_start:outer_start:outer_ray_N*1j]["rho"])
        outer_ray_2 = np.array(dsi.r[outer_end:edge_end:outer_ray_N*1j]["rho"])
        filler_array = np.zeros(outer_num - inner_num)
        ###
        #print("inner_num = ", inner_num)
        #print("outer_num = ", outer_num)
        total_ray = np.concatenate((outer_ray_1, filler_array, inner_ray, filler_array, outer_ray_2),axis=0)
        #print("length of total ray = ", len(total_ray)) # this should be N
        return total_ray
        
"""def make_ray(dsi, start, end, N):
        try:
                ray = dsi.r[start:end:N*1j]
                result = np.array(ray["rho"])
                #print("length = ", len(result))
                return result
        except Exception as excpt:
                print(" ! ! ! ! ! Failed to make ray")
                print("Error message = ")
                print(excpt)
                print("#")
                print("start = ",start)
                print("end = ",end)
                print("#")
                # Trying again
                print("Trying again:")
                try:
                        ray = dsi.r[start:end:N*1j]
                        result = np.array(ray["rho"])
                        return result
                except Exception as excpt:
                        print(" ! ! ! ! ! Failed to make ray for second time")
                        print("Error message = ")
                        print(excpt)
                        print("#")
                        print("start = ",start)
                        print("end = ",end)
                        print("#")
                        return np.nan * np.ones(N)"""

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
                dt = 2 * dd.dt_mult * 40
                n = int(t/dt)
                try:
                        ray = advanced_make_ray(dsi, t, dd.M, dd.d, width, z_position, N)/rho0
                except Exception as excpt:
                        print("! ! ! Failed to make ray, error message = ")
                        print(excpt)
                        ray = np.zeros(N)
                output = [t, ray]
                sto.result = output
                sto.result_id = str(dsi)
                print("done {:d} of {:d}".format(n, Nsteps))
                
        if yt.is_root():
                # output to file
                
                filename = dd.name + "_rho_profile_along_binary.dat"
                output_path = output_data_dir + filename
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

#for dd in data_dirs:
#        get_line_data(dd)

largest_dt = 40

plot_n = 200
        
def plot_graph(time):
        ##### plot graph
        print("plotting graph ... ")
        fig, ax = plt.subplots()
        line_positions = np.linspace(-width/2, width/2, N)
        colours = ['r', 'g', 'b', 'm', 'y', 'k', '0.5']
        font_size = 12
        title_font_size = 10
        label_size = 12
        legend_font_size = 10
        
        for i in range(0, len(data_dirs)):
                dd = data_dirs[i]
                # load data
                file_name = output_data_dir + dd.name + "_rho_profile_along_binary.dat"
                data = np.genfromtxt(file_name)
                print("loaded data for ", file_name)
                dt = data[2,0] - data[1,0]
                line = int(time / dt)
                print("t = ", data[line+1,0])
                rho_data = data[line+1,1:]
                ax.plot(line_positions, np.log10(rho_data), color=colours[i], linestyle='-', linewidth=1, label="$\\mu$={:.2f}, l = {:d}, m = {:d}".format(dd.mu, dd.l, dd.m))

        title = "$\\rho$ profile along the line of the BHs, Newtonian binary $M~0.5,d~12$, t = {:d}".format(time)
        ax.set_title(title, fontsize=title_font_size)
        plt.legend(loc='best', fontsize=legend_font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        ax.minorticks_on()
        ax.set_xlim(-width/2, width/2)
        ax.set_ylim(-1, 4)
        ax.set_xlabel('displacement from centre',fontsize=label_size, labelpad=0)
        ax.set_ylabel('$\\log_{10}(\\rho/\\rho_0)$', fontsize=label_size, labelpad=0)
        save_path = plots_dir + "Newtonian_BH_rho_profiles_compare_lm_plot_t={:d}.png".format(time)
        fig.tight_layout()
        ax.margins(2)
        plt.savefig(save_path, transparent=False)
        print("saved " + save_path)
        plt.clf()

plot_graph(1000)
