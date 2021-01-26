import yt
import numpy as np
import matplotlib.pyplot as plt
import math
from sys import exit
from os import makedirs

yt.enable_parallelism()

# Newtonian Binaries

data_root_dir = "/p/project/pra116/bamber1/BinaryBHScalarField/"
plots_dir = "/p/scratch/pra116/bamber1/plots/GR_Binary_BH/"
output_data_dir = "/p/home/jusers/bamber1/juwels/GRChombo/Analysis/data/GR_Binary_BH_data/"
Newtonian_output_data_dir = "/p/home/jusers/bamber1/juwels/GRChombo/Analysis/data/Newtonian_Binary_BH_data/"

L=512
N1=64
abmax=20
z_position = 0.00
width = 100
N = 512

############################

# class to store the run information                                                                                                                      
class data_dir:
        def __init__(self, num, mu, delay, G, ratio, suffix):
                self.num = num
                self.mu = float(mu)
                self.delay = delay
                self.G = G
                self.ratio = ratio
                self.name = "run{:04d}_mu{:s}_delay{:d}_G{:s}_ratio{:d}{:s}".format(num, mu, delay, G, ratio, suffix)
#                                                                                                                                                          
data_dirs = []
def add_data_dir(num, mu, delay, G, ratio, restart=0):
        if restart:
                suffix = "_restart"
        else:
                suffix = ""
        x = data_dir(num, mu, delay, G, ratio, suffix)
        data_dirs.append(x)

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
#add_data_dir(22, "0.5", 0, "0", 1)
                
############################

def vecmag(v):
        out2 = 0
        for i in range(0, len(v)):
                out2 += v[i]*v[i]
        return np.sqrt(out2)

def ray_pos(t, M, d, width, z_position):
        omega_BBH = np.sqrt(2*M/d**3)
        start = [(L-width*np.cos(t*omega_BBH))/2,(L-width*np.sin(t*omega_BBH))/2,z_position]
        end = [(L+width*np.cos(t*omega_BBH))/2,(L+width*np.sin(t*omega_BBH))/2,z_position]
        return (start, end)
        
def make_ray(dsi, start, end, N):
        ray = dsi.r[start:end:N*1j]                                                                                          
        result = np.array(ray["rho"])
        #print("length = ", len(result))
        return result

def get_GR_BH_seperation(name, time):
        puncture_file_name = data_root_dir + name + "/BinaryBHSFChk_Punctures.dat"
        puncture_data = np.genfromtxt(puncture_file_name, skip_header=1)
        punture_dt = puncture_data[2,0] - puncture_data[1,0]
        punture_t0 = puncture_data[0,0]
        puncture_line = int((time - punture_t0)/punture_dt)
        puncture_positions = puncture_data[puncture_line,1:]
        p1 = puncture_positions[0:2]
        p2 = puncture_positions[3:5]
        # positions of the ray endpoints                                                                                                                           
        p = vecmag(p2 - p1)
        return p

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
        BinaryBH_dataset_path = data_root_dir + dd.name + "/BinaryBHSFPlot_*.3d.hdf5"
        ds = yt.load(BinaryBH_dataset_path)
        print("loaded data for " + dd.name)
        phi0 = 1
        rho0 = 0.5*(dd.mu*phi0)**2

        Nsteps = len(ds)

        # get puncture data
        puncture_file_name = data_root_dir + dd.name + "/BinaryBHSFChk_Punctures.dat"                                                                   
        puncture_data = np.genfromtxt(puncture_file_name, skip_header=1)  
        punture_dt = puncture_data[2,0] - puncture_data[1,0]
        punture_t0 = puncture_data[0,0]

        dt = 40
        
        data_storage = {}
        for sto, dsi in ds.piter(storage=data_storage):
                t = dsi.current_time
                n = int(t/dt)
                
                # get ray endpoints
                puncture_line = int((t - punture_t0)/punture_dt)
                puncture_positions = puncture_data[puncture_line,1:]
                p1 = puncture_positions[0:2]
                p2 = puncture_positions[3:5]
                # positions of the ray endpoints                                                                                                          
                p = vecmag(p2 - p1)
                centerBBH = np.array([L/2, L/2])
                if (p > 0.5):
                        BBHstart = centerBBH + (p1 - p2)*0.5*width/p
                        BBHend = centerBBH + (p2 - p1)*0.5*width/p
                else:
                        BBHstart = centerBBH + np.array([1, 0])*0.5*width
                        BBHend = centerBBH - np.array([1, 0])*0.5*width
                BBHstart = np.append(BBHstart, z_position)
                BBHend = np.append(BBHend, z_position)
                
                try:
                        ray = make_ray(dsi, BBHstart, BBHend, N)/rho0
                except Exception as excpt:
                        print("! ! ! Failed to make ray, error message = ")
                        print(excpt)
                        print("start = ", BBHstart)
                        print("end = ", BBHend)
                        print("time = ", t)
                        print("puncture time = ", puncture_data[puncture_line,0])
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

largest_dt = 20

plot_n = 50

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
                data = np.genfromtxt(file_name, skip_header=1)
                print("loaded data for ", file_name)
                dt = data[2,0] - data[1,0]
                line = int(time / dt)
                print("t = ", data[line+1,0])
                rho_data = data[line+1,1:]
                ax.plot(line_positions, np.log10(rho_data), color=colours[i], linestyle='-', linewidth=1, label="$\\mu$={:.3f}".format(dd.mu))

        title = "$\\rho$ profile along the line of the BHs, GR binary, ratio 1, t = {:d}".format(time)
        ax.set_title(title, fontsize=title_font_size)
        plt.legend(loc='best', fontsize=legend_font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        ax.minorticks_on()
        ax.set_xlim(-width/2, width/2)
        ax.set_ylim(-1, 3)
        ax.set_xlabel('displacement from centre',fontsize=label_size, labelpad=0)
        ax.set_ylabel('$\\log_{10}(\\rho/\\rho_0)$', fontsize=label_size, labelpad=0)
        save_path = plots_dir + "GR_BH_rho_profiles_plot_t={:d}.png".format(time)
        fig.tight_layout()
        ax.margins(2)
        plt.savefig(save_path, transparent=False)
        print("saved " + save_path)
        plt.clf()

# plot_graph(plot_n)

def plot_graph_vs_Newtonian(plot_n):
        time = 5 * plot_n
        # GR file
        GR_name = "run0011_mu1_delay0_G0_ratio1"
        GR_data = np.genfromtxt(output_data_dir + GR_name + "_rho_profile_along_binary.dat", skip_header=1)
        GR_dt = GR_data[2,0] - GR_data[1,0]
        #
        Newt_name = "run0015_M0.48847892320123_d12.21358_mu1_dt_mult0.0625_l0_m0_Al0_L1024_N256"
        Newt_data = np.genfromtxt(Newtonian_output_data_dir + Newt_name + "_rho_profile_along_binary.dat", skip_header=1)
        Newt_dt = Newt_data[2,0] - Newt_data[1,0]
        #
        GR_line = int(time/GR_dt)+1
        print("GR time = ", GR_data[GR_line, 0])
        Newt_line = int(time/Newt_dt)+1
        print("Newt time = ", Newt_data[Newt_line, 0])
        #
        fig, ax = plt.subplots()
        line_positions = np.linspace(-width/2, width/2, N)
        colours = ['r', 'g', 'b', 'm', 'y', 'k', '0.5']
        font_size = 12
        title_font_size = 10
        label_size = 12
        legend_font_size = 10
        ax.plot(line_positions, np.log10(GR_data[GR_line,1:]), 'r-', linewidth=1, label="GR binary")
        ax.plot(line_positions, np.log10(Newt_data[Newt_line,1:]), 'b-', linewidth=1, label="Newtonian binary")
        # plot BH positions
        d = 12.21358
        d_GR = get_GR_BH_seperation(GR_name, time)
        plt.vlines(np.array([-d_GR/2, d_GR/2]), -2, 5, color='g', linestyle='-', linewidth=1, label="GR BH positions")
        plt.vlines(np.array([-d/2, d/2]), -2, 5, color='k', linestyle='--', linewidth=1, label="Newtonian BH positions")
        # 
        title = "$\\rho$ profile GR vs Newtonian binary, ratio 1, t = {:d}".format(time)
        ax.set_title(title, fontsize=title_font_size)
        plt.legend(loc='best', fontsize=legend_font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        ax.minorticks_on()
        ax.set_xlim(-width/2, width/2)
        ax.set_ylim(-1, 5)
        ax.set_xlabel('displacement from centre',fontsize=label_size, labelpad=0)
        ax.set_ylabel('$\\log_{10}(\\rho/\\rho_0)$', fontsize=label_size, labelpad=0)
        #save_path = plots_dir + "GR_vs_Newtonian_BH_rho_profiles_plot_t={:d}.png".format(time)
        save_path = plots_dir + "GR_vs_Newtonian_BH_rho_profiles_movie/frame_{:06d}.png".format(plot_n)
        fig.tight_layout()
        ax.margins(2)
        plt.savefig(save_path, transparent=False)
        print("saved " + save_path)
        plt.clf()

#plot_graph_vs_Newtonian(1000)

def plot_movie_GR_vs_Newtonian():
        # GR file                                                                                                                                                         
        GR_name = "run0011_mu1_delay0_G0_ratio1"
        GR_data = np.genfromtxt(output_data_dir + GR_name + "_rho_profile_along_binary.dat", skip_header=1)
        GR_dt = GR_data[2,0] - GR_data[1,0]
        #                                                                                                                                                                 
        Newt_name = "run0015_M0.48847892320123_d12.21358_mu1_dt_mult0.0625_l0_m0_Al0_L1024_N256"
        Newt_data = np.genfromtxt(Newtonian_output_data_dir + Newt_name + "_rho_profile_along_binary.dat", skip_header=1)
        Newt_dt = Newt_data[2,0] - Newt_data[1,0]
        #
        for plot_n in range(0,len(GR_data[1:,0])):
                time = 5 * plot_n
                GR_line = int(time/GR_dt)+1
                print("GR time = ", GR_data[GR_line, 0])
                Newt_line = int(time/Newt_dt)+1
                print("Newt time = ", Newt_data[Newt_line, 0])
                #                                                                                                                                                         
                fig, ax = plt.subplots()
                line_positions = np.linspace(-width/2, width/2, N)
                colours = ['r', 'g', 'b', 'm', 'y', 'k', '0.5']
                font_size = 12
                title_font_size = 10
                label_size = 12
                legend_font_size = 10
                ax.plot(line_positions, np.log10(GR_data[GR_line,1:]), 'r-', linewidth=1, label="GR binary")
                ax.plot(line_positions, np.log10(Newt_data[Newt_line,1:]), 'b-', linewidth=1, label="Newtonian binary")
                # plot BH positions                                                                                                                                       
                d = 12.21358
                d_GR = get_GR_BH_seperation(GR_name, time)
                plt.vlines(np.array([-d_GR/2, d_GR/2]), -2, 5, color='g', linestyle='-', linewidth=1, label="GR BH positions")
                plt.vlines(np.array([-d/2, d/2]), -2, 5, color='k', linestyle='--', linewidth=1, label="Newtonian BH positions")
                #                                                                                                                                                      
                title = "$\\rho$ profile GR vs Newtonian binary, ratio 1, t = {:d}".format(time)
                ax.set_title(title, fontsize=title_font_size)
                plt.legend(loc='best', fontsize=legend_font_size)
                plt.xticks(fontsize=font_size)
                plt.yticks(fontsize=font_size)
                ax.minorticks_on()
                ax.set_xlim(-width/2, width/2)
                ax.set_ylim(-1, 5)
                ax.set_xlabel('displacement from centre',fontsize=label_size, labelpad=0)
                ax.set_ylabel('$\\log_{10}(\\rho/\\rho_0)$', fontsize=label_size, labelpad=0)
                save_path = plots_dir + "GR_vs_Newtonian_BH_rho_profiles_movie/frame_{:06d}.png".format(plot_n)
                fig.tight_layout()
                ax.margins(2)
                plt.savefig(save_path, transparent=False)
                print("saved " + save_path)
                plt.clf()

plot_movie_GR_vs_Newtonian()
