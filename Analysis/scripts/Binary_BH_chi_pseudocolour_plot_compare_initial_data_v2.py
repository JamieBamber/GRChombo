import yt
from yt import derived_field
import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.colors as colors
#from matplotlib import rc
#rc('text', usetex=True)
import matplotlib.pyplot as plt

from sys import exit

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

width = 32
L = 512.0

# load data
plots_path="/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots/GR_Binary_BH/"
data_root_path="/cosma6/data/dp174/dc-bamb1/GRChombo_data/BinaryBHSF/"

phi0 = 1
abs_max = 2
number = 0
suffix = "Plot" #"Chk"

filename = "BinaryBHSF{:s}_{:06d}.3d.hdf5".format(suffix,number)

subdir1 = "run0011_mu1_delay0_G0_ratio1"
subdirICS = "run0036ICS_mu0.5_delay0_G0_ratio1"

dsi1 = yt.load(data_root_path + subdir1 + "/" + filename)
dsi2 = yt.load(data_root_path + subdirICS + "/" + filename)

print("loaded data")

def u0_func(M,r):
	result = M**4 + 10*(M**3)*r+40*(M**2)*(r**2)+80*M*r**3+80*r**4
	return result

def u2_func(M,r):
	result = (M/(5*r**3))*(42*M**5*r+378*M**4*r**2+1316*M**3*r**3+2156*M**2*r**4+1536*M*r**5\
+240*r**6+21*M*(M+2*r)**5*np.log(M/(M+2*r)))
	return result

def uP_func(M,P,r,costheta):
	result = M*P/(8*(M+2*r)**5)*(u0_func(M,r) + u2_func(M,r)*(1.5*costheta**2-0.5)) 
	return result

def quasi_analytic_chi(M1,M2,p1,p2,c1,c2,xvec,yvec):
	# radial distance to each BH
	N_ = len(xvec)
	x = np.tile(xvec,(N_,1))
	y = np.transpose(np.tile(yvec,(N_,1)))
	#print("x =", x[:5,:5])
	#print("y =", y[:5,:5])
	r1 = np.sqrt((x-c1[0])**2 + (y-c1[1])**2)
	r2 = np.sqrt((x-c2[0])**2 + (y-c2[1])**2)
	# magnitude of the momenta
	P1 = np.sqrt(p1[0]**2 + p1[1]**2 + p1[2]**2)
	P2 = np.sqrt(p2[0]**2 +	p2[1]**2 + p2[2]**2)
	# 
	costheta1 = (p1[0]*(x - c1[0]) + p1[1]*(y - c1[1]))/P1	
	costheta2 = (p2[0]*(x - c2[0]) + p2[1]*(y - c2[1]))/P2	
	uP1 = uP_func(M1,P1,r1,costheta1)
	uP2 = uP_func(M2,P2,r2,costheta2)
	psi = 1 + M1/(2*r1) + M2/(2*r2) + uP1 + uP2
	chi = 1/(psi**2)
	return chi

M1 = 0.48847892320123
c1 = (0.0,6.10679,0.0)
p1 = (-0.0841746,-0.000510846,0.0)

M2 = 0.48847892320123
c2 = (0.0,-6.10679,0.0)
p2 = (0.0841746,0.000510846,0.0)

def get_arr(dsi,N,z_position):
	dx = width/N
	res = [N, N] # 1024 by 1024 box                                                                      $
	centerBH = np.array([L/2, L/2])
	slice = dsi.slice(2, z_position)
	frb1 = slice.to_frb(width, res, center=centerBH)
	arr1 = np.array(frb1['chi'])
	return arr1

## make data
N = 1024
arr_noICS = get_arr(dsi1,N,0.001)
arr_ICS = get_arr(dsi2,N,256)
#cm = 'inferno'
x_pos = np.linspace(-0.5*width,0.5*width,N)
y_pos = x_pos
## Now make the analytic chi array
arr_analytic = quasi_analytic_chi(M1,M2,p1,p2,c1,c2,x_pos,y_pos)
print("arr_analytic.shape = ", arr_analytic.shape)
#
	
def plot_graph(arr1,arr2,title,name):
	# plot setup
	ax1 = plt.axes()
	fig = plt.gcf()
	fig.set_size_inches(6,6)
	font_size = 12
	title_font_size = 10
	label_size = 12
	legend_font_size = 10
	#rc('xtick',labelsize=font_size)
	#rc('ytick',labelsize=font_size)
	dchi_max=np.max(arr2-arr1)
	dchi_min=np.min(arr2-arr1)
	abs_max=np.max(np.abs([dchi_max,dchi_min]))
	print("dchi_max = ", dchi_max)
	print("dchi_min = ", dchi_min)
	print("abs_max = ", abs_max)
	#print('max={:.2f} min={:.2f}'.format(phi_max, phi_min))
	cm = 'RdBu'
	zmin=-abs_max
	zmax=abs_max
	# extract slice data                                                                                               
	mesh = ax1.pcolormesh(x_pos, y_pos,arr2-arr1,cmap=cm,vmin=zmin,vmax=zmax)
	fig.colorbar(mesh, pad=0.01)
	#ax1.text(0.9, 0.00, 'max={:.2f}\nmin={:.2f}'.format(phi_max, phi_min), horizontalalignment='left',verticalalignment='top', transform=ax1.transAxes, fontsize=font_size)
	## add other bits
	#ax.legend(loc="lower left", fontsize=12)
	ax1.set_title(title)
	plt.xticks(fontsize=font_size)
	plt.yticks(fontsize=font_size)
	ax1.minorticks_on()
	ax1.set_xlabel('x',fontsize=label_size, labelpad=0)     
	ax1.set_ylabel('y', fontsize=label_size, labelpad=-10)  
	save_path = plots_path + "{:s}.png".format(name)
	fig.tight_layout()
	ax1.margins(2)
	plt.savefig(save_path, transparent=False)
	print("saved " + save_path)
	plt.clf()

def plot_single_graph(arr,title,name):
	# plot setup
	ax1 = plt.axes()
	fig = plt.gcf()
	fig.set_size_inches(6,6)
	font_size = 12
	title_font_size = 10
	label_size = 12
	legend_font_size = 10
	#rc('xtick',labelsize=font_size)
	#rc('ytick',labelsize=font_size)
	cm = 'inferno'
	zmin=0
	zmax=1
	# extract slice data                                                                                               
	mesh = ax1.pcolormesh(x_pos,y_pos,arr,cmap=cm,vmin=zmin,vmax=zmax)
	fig.colorbar(mesh, pad=0.01)
	#ax1.text(0.9, 0.00, 'max={:.2f}\nmin={:.2f}'.format(phi_max, phi_min), horizontalalignment='left',verticalalignment='top', transform=ax1.transAxes, fontsize=font_size)
	## add other bits
	#ax.legend(loc="lower left", fontsize=12)
	ax1.set_title(title)
	plt.xticks(fontsize=font_size)
	plt.yticks(fontsize=font_size)
	ax1.minorticks_on()
	ax1.set_xlabel('x',fontsize=label_size, labelpad=0)     
	ax1.set_ylabel('y', fontsize=label_size, labelpad=-10)  
	save_path = plots_path + "{:s}.png".format(name)
	fig.tight_layout()
	ax1.margins(2)
	plt.savefig(save_path, transparent=False)
	print("saved " + save_path)
	plt.clf()

#plot_single_graph(arr_noICS,"$\\chi$ t=0","chi_GR_binary_t0")
#plot_single_graph(arr_ICS,"$\\chi$ ICS t=0","chi_GR_binary_ICS")
plot_single_graph(arr_analytic,"$\\chi$ analytic t=0","analytic_chi_GR_binary")
#plot_graph(arr_noICS,arr_ICS,"$\\Delta \\chi$ no ICS vs ICS","delta_chi_on_using_ICS")
plot_graph(arr_analytic,arr_ICS,"$\\Delta \\chi$ analytic vs ICS","delta_chi_analytic_vs_ICS")
plot_graph(arr_analytic,arr_noICS,"$\\Delta \\chi$ analytic vs no ICS","delta_chi_analytic_vs_no_ICS")
