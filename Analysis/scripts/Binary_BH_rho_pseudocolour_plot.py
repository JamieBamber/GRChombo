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

width = 64
L = 512.0

# load data
data_root_path = "/p/project/pra116/bamber1/BinaryBHScalarField/"
data_sub_dir = "run0019_mu1_delay1_G0_ratio1_restart"
plots_root_path = "/p/scratch/pra116/bamber1/plots/GR_Binary_BH/"
phi0 = 1
mu = 1
number = 1800
dsi = yt.load(data_root_path + data_sub_dir + "/BinaryBHSFPlot_{:06d}.3d.hdf5".format(number))

### derived fields
@derived_field(name = "norm_rho", units = "")
def _norm_rho(field, data):
	return data["rho"]/(0.5*(phi0**2)*(mu**2))

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
        arr1 = np.array(frb1['norm_rho'])
        cm = 'inferno'
        rho_max=np.max(arr1)
        rho_min=np.min(arr1)
        x_pos = np.linspace(-0.5*width,0.5*width,N)
        y_pos = x_pos
        #print('max={:.2f} min={:.2f}'.format(phi_max, phi_min))
        zmin=0.1
        zmax=10000
        mesh = ax1.pcolormesh(x_pos, y_pos,arr1,cmap=cm,norm=colors.LogNorm(zmin, zmax),vmin=zmin,vmax=zmax)
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
        save_path = plots_root_path + data_sub_dir + "_rho_n{:06d}.png".format(number)
        fig.tight_layout()
        ax1.margins(2)
        plt.savefig(save_path, transparent=False)
        print("saved " + save_path)
        plt.clf()
        
plot_graph(dsi)
