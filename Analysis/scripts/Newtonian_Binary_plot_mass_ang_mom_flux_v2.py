import numpy as np
import math
import time
import sys
#from matplotlib import rc
#rc('text', usetex=True)
from matplotlib import pyplot as plt
from scipy import fft
from scipy.signal import argrelextrema

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

scratch_data_root_path = "/p/scratch/pra116/bamber1/NewtonianBinaryScalar/"
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

#add_data_dir(10, "0.2", "10", "0.01", "0.5", 0, 0, "0")
#add_data_dir(9, "0.2", "10", "0.015", "0.5", 0, 0, "0")
#add_data_dir(7, "0.2", "10", "0.02", "0.5", 0, 0, "0")
#add_data_dir(8, "0.2", "10", "0.025", "0.5", 0, 0, "0")
#add_data_dir(11, "0.2", "10", "0.03", "0.5", 0, 0, "0")
#add_data_dir(12, "0.2", "10", "0.02", "0.5", 1, -1, "0")
#add_data_dir(13, "0.2", "10", "0.02", "0.5", 1, 1, "0")
#add_data_dir(15, "0.48847892320123", "12.21358", "1", "0.0625", 0, 0, "0")
#add_data_dir(16, "0.48847892320123", "12.21358", "1", "0.0625", 1, -1, "0")
#add_data_dir(17, "0.48847892320123", "12.21358", "1", "0.0625", 1, 1, "0")
add_data_dir(21, "0.2", "10", "0.05", "0.25", 0, 0, "0")
add_data_dir(19, "0.2", "10", "0.1", "0.125", 0, 0, "0")
add_data_dir(24, "0.2", "10", "0.15", "0.0625", 0, 0, "0")
add_data_dir(22, "0.2", "10", "0.2", "0.0625", 0, 0, "0")
add_data_dir(25, "0.2", "10", "0.25", "0.0625", 0, 0, "0")
add_data_dir(23, "0.2", "10", "0.3", "0.0625", 0, 0, "0")
add_data_dir(20, "0.2", "10", "0.5", "0.0625", 0, 0, "0")
add_data_dir(18, "0.2", "10", "1", "0.03125", 0, 0, "0")
add_data_dir(26, "0.2", "10", "2", "0.03125", 0, 0, "0")
add_data_dir(27, "0.2", "10", "5", "0.015625", 0, 0, "0")

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
av_n = 100
cumulative= False
r_extract = 50

def load_data():
        # load data from csv files
        data = {}
        for dd in data_dirs:
                file_name = scratch_data_root_path + dd.name + "/outputs/Force_integrals.dat"
                data[dd.num] = np.genfromtxt(file_name, skip_header=2)
                print("loaded data for " + dd.name)
        return data     

def low_pass_filter(y, dt, omega_max):
        fft_y = fft.fft(y)
        N = len(y)
        fft_freq = 2*np.pi*fft.fftfreq(N, dt)
        fft_y_filtered = np.zeros(N)
        for i in range(0, N):
                if np.abs(fft_freq[i]) <= omega_max:
                        fft_y_filtered[i] = fft_y[i]
                else:
                        pass
        y_out = fft.ifft(fft_y_filtered, n=N)
        return y_out

def get_amplitude(t, y):
        maxima_indices = argrelextrema(y, np.greater)[0]
        minima_indices = argrelextrema(y, np.less)[0]
        print("n maxima = ", len(maxima_indices))
        print("n minima = ", len(minima_indices))
        n_maxmin = min(len(maxima_indices), len(minima_indices))
        amplitudes = np.zeros(n_maxmin)
        times = np.zeros(n_maxmin)
        for i in range(0,n_maxmin):
                amplitudes[i] = np.abs(y[maxima_indices[i]]-y[minima_indices[i]])
                times[i] = 0.5*(t[maxima_indices[i]]+t[minima_indices[i]])
        return (times, amplitudes)

def plot_graph(mass_or_ang_mom, use_low_pass_filter=False, omega_max=0.01):
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
                        flux = -line_data[:,2]/F0
                if average_time:
                        t1 = time_average(t1, av_n)
                        flux = time_average(flux, av_n)
                if cumulative:
                        flux = np.cumsum(flux)/(r_extract/3)
                if use_low_pass_filter:
                        dt = t1[2] - t1[1]
                        flux = low_pass_filter(flux, dt, omega_max)
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
                        ax1.set_ylabel("mass flux / $F_0$", fontsize=font_size)
                        plt.title("Mass flux into $R=${:d}, $M=0.2,d=10$".format(r_extract))
                        if use_low_pass_filter:
                                save_path = plots_path + "Newtonian_BBH_mass_flux_vs_t_r{:d}_lpf_omega_max{:.3f}.png".format(r_extract, omega_max)
                        else:
                                save_path = plots_path + "Newtonian_BBH_mass_flux_vs_t_r{:d}_compare_mu_avn{:d}_v2.png".format(r_extract, av_n)
                else:
                        ax1.set_ylabel("ang. mom. flux / $F_0$", fontsize=font_size)
                        plt.title("Ang. mom. flux into $R=${:d}, $M=0.2,d=10$".format(r_extract))
                        if use_low_pass_filter:
                                save_path = plots_path + "Newtonian_BBH_ang_mom_flux_vs_t_r{:d}_lpf_omega_max{:.3f}.png".format(r_extract, omega_max)
                        else:
                                save_path = plots_path + "Newtonian_BBH_ang_mom_flux_vs_t_r{:d}_compare_mu_avn{:d}_v2.png".format(r_extract, av_n)
                                #save_path = plots_path + "Newtonian_BBH_ang_mom_flux_vs_t_r{:d}_compare_mu.png".format(r_extract)
        ax1.legend(loc='best', fontsize=legend_font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        plt.tight_layout()
        plt.savefig(save_path)
        print("saved plot as " + str(save_path))
        plt.clf()

def plot_graph_lm(mass_or_ang_mom, use_low_pass_filter=False, omega_max=0.01):
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
                        flux = -line_data[:,2]/F0
                if average_time:
                        t1 = time_average(t1, av_n)
                        flux = time_average(flux, av_n)
                if use_low_pass_filter:
                        dt = t1[2] - t1[1]
                        flux = low_pass_filter(flux, dt, omega_max)
                label_ = "$\\mu=${:.3f} l,m={:d},{:d}".format(dd.mu, dd.l, dd.m)
                ax1.plot(t1,flux,colours[i], label=label_)
                i = i + 1
        ax1.set_xlabel("$t$", fontsize=font_size)
        ax1.set_xlim((0,5000))
        if mass_or_ang_mom:
                ax1.set_ylabel("mass flux / $F_0$", fontsize=font_size)
                plt.title("Mass flux into $R=${:d}, $M\\sim 0.5,d\\sim 12$".format(r_extract))
                if use_low_pass_filter:
                        save_path = plots_path + "Newtonian_BBH_mass_flux_vs_t_r{:d}_lpf_omega_max{:.3f}.png".format(r_extract, omega_max)
                else:
                        save_path = plots_path + "Newtonian_BBH_mass_flux_vs_t_r{:d}_compare_lm.png".format(r_extract)
        else:
                ax1.set_ylabel("ang. mom. flux / $F_0$", fontsize=font_size)
                plt.title("Ang. mom. flux into $R=${:d}, $M\\sim 0.5,d\sim 12$".format(r_extract))
                if use_low_pass_filter:
                        save_path = plots_path + "Newtonian_BBH_ang_mom_flux_vs_t_r{:d}_lpf_omega_max{:.3f}.png".format(r_extract, omega_max)
                else:
                        #save_path = plots_path + "Newtonian_BBH_ang_mom_flux_vs_t_r{:d}_compare_lm_avn{:d}_v2.png".format(r_extract, av_n)                                      
                        save_path = plots_path + "Newtonian_BBH_ang_mom_flux_vs_t_r{:d}_compare_lm.png".format(r_extract)
        ax1.legend(loc='best', fontsize=legend_font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        plt.tight_layout()
        plt.savefig(save_path)
        print("saved plot as " + str(save_path))
        plt.clf()
                        
def plot_amplitude_graph(mass_or_ang_mom):
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
                t = line_data[:,0]
                mu = float(dd.mu)
                E0 = 0.5*(phi0*mu)**2
                F0 = 4*np.pi*(r_extract**2)*E0
                if mass_or_ang_mom:
                        flux = -line_data[:,1]/F0
                else:
                        flux = -line_data[:,2]/F0
                t1, amp = get_amplitude(t, flux)
                label_ = "$\\mu=${:.3f}".format(dd.mu)
                ax1.plot(t1,amp,colours[i], label=label_)
                i = i + 1
        ax1.set_xlabel("$t$", fontsize=font_size)
        ax1.set_xlim((0,5000))
        if mass_or_ang_mom:
                ax1.set_ylabel("mass flux (amplitude) / $F_0$", fontsize=font_size)
                plt.title("Mass flux into $R=${:d}, $M=0.2,d=10$".format(r_extract))
                save_path = plots_path + "Newtonian_BBH_mass_flux_vs_t_r{:d}_amplitude.png".format(r_extract, av_n)
        else:
                ax1.set_ylabel("ang. mom. flux / $F_0$", fontsize=font_size)
                plt.title("Ang. mom. flux into $R=${:d}, $M=0.2,d=10$".format(r_extract))
                save_path = plots_path + "Newtonian_BBH_ang_mom_flux_vs_t_r{:d}_amplitude.png".format(r_extract, av_n)
        ax1.legend(loc='best', fontsize=legend_font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        plt.tight_layout()
        plt.savefig(save_path)
        print("saved plot as " + str(save_path))
        plt.clf()

#plot_amplitude_graph(True)
#plot_amplitude_graph(False)
        
plot_graph(True, False, 0.01)
plot_graph(False, False, 0.01)

def plot_fft_graph(mass_or_ang_mom, real_or_imag):
        data = load_data()
        # colours = ['r-', 'b-', 'g-', 'm-', 'y-', 'c-', 'k-', 'r--', 'b--', 'g--', 'm--', 'y--', 'c--']
        colours = ['r', 'b', 'g', 'm', 'y', 'c']
        cmap = plt.get_cmap("tab10")
        #
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
                dt = t1[2] - t1[1]
                print("dt = ", dt)
                om_Ny = 2*np.pi*0.5/dt
                print("omega_Nyquist = ", om_Ny)
                mu = float(dd.mu)
                E0 = 0.5*(phi0*mu)**2
                F0 = 4*np.pi*(r_extract**2)*E0
                if mass_or_ang_mom:
                        flux = -line_data[:,1]/F0
                else:
                        flux = -line_data[:,2]/F0
                N = len(flux)
                print("N = ", N)
                print("Delta omega = ", 2*np.pi/(N*dt))
                fft_freq = 2*np.pi*fft.fftfreq(N,dt)
                label_ = "$\\mu=${:.3f}".format(dd.mu)
                if real_or_imag:
                        fft_flux = np.real(fft.fft(flux))
                        ax1.plot(fft_freq[:N//2],np.abs(fft_flux[:N//2]),color=cmap(i), linestyle="-", label=label_)
                else:
                        fft_flux = fft.fftshift(np.imag(fft.fft(flux)))
                        fft_freq = fft.fftshift(fft_freq)
                        ax1.plot(fft_freq,fft_flux,color=cmap(i), linestyle="-", label=label_)
                print("fft_freq[:4] = ", fft_freq[:4])
                plt.vlines(om_Ny, 0, 50, color=cmap(i), linestyle="--", label="_")
                plt.text(om_Ny, 50, "Nyq.")
                i = i + 1
        ax1.set_xlabel("$\\omega$", fontsize=font_size)
        if mass_or_ang_mom:
                if real_or_imag:
                        ax1.set_ylabel("|Re(FFT of mass flux) / $F_0$|", fontsize=font_size)
                        save_path = plots_path + "Newtonian_BBH_mass_flux_vs_t_r{:.0f}_fft_Re.png".format(r_extract, av_n)
                        ax1.set_xlim((0,2))
                else:
                        ax1.set_xlim((-0.02,0.02))
                        ax1.set_ylim((-50,50))
                        ax1.set_ylabel("|Im(FFT of mass flux) / $F_0$|", fontsize=font_size)
                        save_path = plots_path + "Newtonian_BBH_mass_flux_vs_t_r{:.0f}_fft_Im.png".format(r_extract, av_n)
                plt.title("Mass flux into $R=${:d}, $M=0.2,d=10$".format(r_extract))
                
        else:
                if real_or_imag:
                        ax1.set_ylabel("|Re(FFT of ang. mom. flux) / $F_0$|", fontsize=font_size)
                        save_path = plots_path + "Newtonian_BBH_ang_mom_flux_vs_t_r{:.0f}_fft_Re.png".format(r_extract, av_n)
                else:   
                        ax1.set_ylabel("|Im(FFT of ang. mom. flux) / $F_0$|", fontsize=font_size)
                        save_path = plots_path + "Newtonian_BBH_ang_mom_flux_vs_t_r{:.0f}_fft_Im.png".format(r_extract, av_n)
                ax1.set_ylabel("|FFT of ang. mom. flux / $F_0$|", fontsize=font_size)
                plt.title("Ang. mom. flux into $R=${:d}, $M=0.2,d=10$".format(r_extract))
        ax1.legend(loc='best', fontsize=legend_font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        plt.tight_layout()
        plt.savefig(save_path)
        print("saved plot as " + str(save_path))
        plt.clf()

#plot_fft_graph(True, True)
#plot_fft_graph(True, False)
#plot_fft_graph(False, True)
#plot_fft_graph(False, False)
