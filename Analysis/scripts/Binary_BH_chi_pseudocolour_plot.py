import yt
from yt import derived_field
import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.colors as colors
#from matplotlib import rc
#rc('text', usetex=True)
import matplotlib.pyplot as plt

# 
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

#plt.rc("text.latex", preamble=r'''
#       \usepackage{newtxmath}
#       ''')

#plt.rcParams.update(tex_fonts)

width = 200
L = 512.0

# load data
data_root_path = "/p/scratch/pra116/bamber1/NewtonianBinaryScalar/"
#"/p/project/pra116/bamber1/BinaryBHScalarField/"
# data_sub_dir = "basic_public_code_params"
data_sub_dir = "run0215_M10.3194742895317072_M20.654181589210298_d10.0_mu1_dt_mult0.03125_l0_m0_Al0_L1024_N256"
#run0023v2_mu0.5_delay0_G0.0000000001_ratio1"
plots_root_path = "/p/scratch/pra116/bamber1/plots/Newtonian_Binary_BH/"
phi0 = 1
abs_max = 2
number = 0

chk_or_plot = True

if chk_or_plot:
        suffix = "Chk"
else:
        suffix = "Plot"

filename = "Newton_plt{:06d}.3d.hdf5".format(number)
#filename = "BinaryBHSF{:s}_{:06d}.3d.hdf5".format(suffix,number)
#filename = "InitialConditionsFinal.3d.hdf5"
dsi = yt.load(data_root_path + data_sub_dir + "/" + filename)

### derived fields
#@derived_field(name = "norm_phi", units = "")
#def _norm_rho(field, data):
#	return data["phi"]/phi0

def plot_graph(dsi):
        # plot setup
        ax1 = plt.axes()
        fig = plt.gcf()
        fig.set_size_inches(3.375,3)
        font_size = 12
        title_font_size = 10
        label_size = 12
        legend_font_size = 10
        #rc('xtick',labelsize=font_size)
        #rc('ytick',labelsize=font_size)
        # extract slice data                                                                                               
        N = 1024
        dx = width/N
        res = [N, N] # 1024 by 1024 box                                                                                    
        centerBH = np.array([L/2, L/2])
        z_position = 0.001      # s position of slice                                                                      
        slice = dsi.slice(2, z_position)
        frb1 = slice.to_frb(width, res, center=centerBH)
        arr1 = np.array(frb1['chi'])
        cm = 'inferno'
        rho_max=np.max(arr1)
        rho_min=np.min(arr1)
        x_pos = np.linspace(-0.5*width,0.5*width,N)
        y_pos = x_pos
        #print('max={:.2f} min={:.2f}'.format(phi_max, phi_min))
        zmin=0
        zmax=1
        mesh = ax1.pcolormesh(x_pos, y_pos,arr1,cmap=cm,vmin=zmin,vmax=zmax)
        fig.colorbar(mesh, pad=0.01)
        #ax1.text(0.9, 0.00, 'max={:.2f}\nmin={:.2f}'.format(phi_max, phi_min), horizontalalignment='left',verticalalignment='top', transform=ax1.transAxes, fontsize=font_size)
        ## add other bits
        #ax.legend(loc="lower left", fontsize=12)
        title = "t = {:.2f}".format(dsi.current_time)
        ax1.set_title(title)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        ax1.minorticks_on()
        ax1.set_xlabel('x',fontsize=label_size, labelpad=0)     
        ax1.set_ylabel('y', fontsize=label_size, labelpad=-10)  
        save_path = plots_root_path + data_sub_dir + "_chi_{:s}_n{:06d}.png".format(suffix,number)
        fig.tight_layout()
        ax1.margins(2)
        plt.savefig(save_path, transparent=False)
        print("saved " + save_path)
        plt.clf()
        
plot_graph(dsi)
