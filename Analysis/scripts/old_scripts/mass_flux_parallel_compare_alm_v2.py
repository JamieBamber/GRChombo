import yt
import numpy as np
#from scipy.interpolate import interp1d
#from scipy.optimize import fsolve
import math
from yt import derived_field
from yt.units import cm
import time
import sys
from matplotlib import pyplot as plt
from os import makedirs

yt.enable_parallelism()

class data_dir:
	def __init__(self, num, l, m, a, mu, phase, dt):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = mu
		self.phase = phase
		if phase=="0":
			self.name = "run{:04d}_KNL_l{:d}_m{:d}_a{:s}_Al0_mu{:s}_M1_correct_Ylm".format(num, l, m, a, mu)
		elif phase!="0":
			self.name = "run{:04d}_KNL_l{:d}_m{:d}_a{:s}_Al0_mu{:s}_M1_phase{:s}".format(num, l, m, a, mu, phase)
	filename = ""
		
def add_data_dir(list, num, l, m, a, mu, phase, dt):
	x = data_dir(num, l, m, a, mu, phase, dt)
	list.append(x)

data_dirs = []
# choose datasets to compare
add_data_dir(data_dirs, 22, 0, 0, "0", "1", "0", 1.25)
add_data_dir(data_dirs, 64, 0, 0, "0", "1", "0.5", 2.5)

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"
max_R = 450
outer_thickness = 5 # box width = 8 
inner_thickness = 0.05 # min box width = 1/16 = 0.0625 
M = 1
phi0 = 0.1
output_dir = "data/compare_alm_flux"

half_box = True

def calculate_flux(dd, old_Jr):
	data_sub_dir = dd.name
	a = dd.a	
	r_plus = M*(1 + math.sqrt(1 - a**2))
	r_minus = M*(1 - math.sqrt(1 - a**2))
	min_R = r_plus/4

	start_time = time.time()
	
	# load dataset time series
	
	dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_*.3d.hdf5"
	ds = yt.load(dataset_path) # this loads a dataset time series
	print("loaded data from ", dataset_path)
	print("time = ", time.time() - start_time)
	N = len(ds)
	
	# set centre
	center = [512.0, 512.0, 0]
	L = 512.0	
		
	if old_Jr: 
		# derived fields
		@derived_field(name = "rho_Jr_eff", units = "")
		def _rho_Jr_eff(field, data):
			r_BL = (data["spherical_radius"]/cm)*(1 + r_plus*cm/(4*data["spherical_radius"]))**2
			Sigma2 = r_BL**2 + (data["z"]*a*M/(r_BL*cm))
			#Delta = r_BL**2 + (a*M)**2 - 2*M*r_BL		
			return ((data["spherical_radius"]**2/cm**2)*(r_BL - r_minus)/(Sigma2*r_BL))*data["S_r"]*pow(data["chi"],-3)
	
	elif not old_Jr:
		# derived fields
                @derived_field(name = "rho_Jr_eff", units = "")
                def _rho_Jr_eff(field, data):
                        return data["J_r"]

	data_storage = {}
	# iterate through datasets (forcing each to go to a different processor)
	for sto, dsi in ds.piter(storage=data_storage):
		time_0 = time.time()
		# store time
		current_time = dsi.current_time 
		output = [current_time]
		
		# make inner and outer shells
		outer_shell = dsi.sphere(center, max_R+0.5*outer_thickness) - dsi.sphere(center, max_R-0.5*outer_thickness)
		inner_shell = dsi.sphere(center, min_R+inner_thickness) - dsi.sphere(center, min_R)

		# calculate inner and outer flux
		Jr_outer = outer_shell.mean("rho_Jr_eff", weight="cell_volume")*4*math.pi*(max_R**2)
		Jr_inner = inner_shell.mean("rho_Jr_eff", weight="cell_volume")*4*math.pi*((r_plus/4)**2)
		output.append(Jr_outer)
		output.append(Jr_inner)
		
		# store output
		sto.result = output
		sto.result_id = str(dsi)
		dt = 1.25
		i = int(current_time/dt)
		print("done {:d} of {:d} in {:.1f} s".format(i+1, N, time.time()-time_0), flush=True)
	
	if yt.is_root():	
		# make data directory if it does not already exist
		makedirs(home_path + output_dir, exist_ok=True)
		# output to file
		if old_Jr:
			dd.filename = "l={:d}_m={:d}_a={:s}_phase={:s}_flux.csv".format(dd.l, dd.m, str(dd.a), dd.phase)
		elif not old_Jr:
			dd.filename = "l={:d}_m={:d}_a={:s}_phase={:s}_flux.csv".format(dd.l, dd.m, str(dd.a), dd.phase)
		output_path = home_path + output_dir + "/" + dd.filename 
		# output header to file
		f = open(output_path, "w+")
		f.write("# t	flux r={:.0f}	flux r={:.2f} \n".format(max_R, min_R))
		# output data
		for key in sorted(data_storage.keys()):
			data = data_storage[key]
			f.write("{:.3f}	".format(data[0]))
			f.write("{:.3f}	".format(data[1]))
			f.write("{:.3f}\n".format(data[2]))
		f.close()
		print("saved data to file " + str(output_path))
		
def load_data():
	# load data from csv files
	data = {}
	for dd in data_dirs:
		file_name = "l={:d}_m={:d}_a={:s}_phase={:s}_flux.csv".format(dd.l, dd.m, str(dd.a), dd.phase)
		file_path = home_path + output_dir + "/" + file_name
		data[dd.num] = np.genfromtxt(file_path, skip_header=1)
		print("loaded data for " + dd.name)
	return data 	

def predicted_flux(R, t, mu, M):
	r_BL = R*(1 + M/(2*R))**2
	T = mu*t # tau
	r = r_BL/(2*M) 
	S = np.sin(2*T)
	C = np.cos(2*T)
	# each order of solution up to order r^(-4)
	P0 = 1 - C
	P1 = C - S*T - 1
	P2 = (C*T**2)/2 + 3*S*T/4
	P3 = -(T**2)*(3*C*mu**2-4*C+4)/(12*mu**2)+(S*T**3)/6+(S*T)/8 
	P4 = (T**2)*(-27*C*mu**2-80*C+15*mu**2+80)/(128*mu**2)+(1/384)*(-15*C-1)*T**4+(35*(C-1))/128+(1/192)*(40/mu**2-13)*S*T**3+(41*S*T)/128
	solution = M*t*(1 - M**2/(2*R)**2)*(P0 + P1/r + P2/r**2 + P3/r**3 + P4/r**4)
	# "solution" is the inwards energy flux over the sphere radius R divided by ( 2*pi*mu^2*Phi0^2 i.e. 4pi rho_0 )
	return solution

def average(data, av_num):
	av_data = np.zeros(len(data) + 1 - av_num)
	for n in range(0,len(av_data)):
		av_data[n] = np.mean(data[n:n+av_num])
	return av_data

def plot_graph():
	data = load_data()
	colours1 = ['r-', 'b-'] 
	colours2 = ['c--', 'g--']
	av_num = 10
	i = 0
	for dd in data_dirs:
		mu = float(dd.mu)
		rho0 = 0.5*(mu*phi0)**2
		a = dd.a
		r_plus = M*(1 + math.sqrt(1 - a**2))
		min_R = r_plus/4
		line_data = data[dd.num]
		t = average(line_data[:,0],av_num)
		outer_flux = average(line_data[:,1]/(4*np.pi*rho0),av_num) 
		inner_flux = line_data[:,2]/(4*np.pi*rho0)
		label_ = "l={:d} m={:d} a={:s} phase={:s}".format(dd.l, dd.m, str(dd.a), dd.phase)
		plt.plot(t[:], outer_flux[:], colours1[i], label=label_+" Jr R={:.0f}".format(max_R))
		#plt.plot(t[:], inner_flux[:], colours2[i], label=label_+" Jr R={:.2f}".format(min_R))
		i = i + 1
	# plot predicted flux for a=m=l=0 and phase=0.5
	t_pred = data[data_dirs[1].num][:,0]
	pred_outer_flux = predicted_flux(max_R, t_pred, 1, M)
	av_t_pred = average(t_pred,av_num)
	av_pred_outer_flux = average(pred_outer_flux,av_num)
	plt.plot(av_t_pred, av_pred_outer_flux, 'k-.', label="predicted Jr R={:.0f} l=m=a=0 phase=0.5 to order $(\\mu t/r)^4$")
	#
	plt.xlabel("time")
	plt.xlim((0, 400))
	plt.ylim((0,400))
	plt.ylabel("inwards energy flux across R = {:.1f} / $(4\\pi \\rho_0)$".format(max_R))
	plt.legend(loc='upper left', fontsize=8)
	plt.title("inward energy flux, $M=1, \\mu=1$, averaged over {:d} timesteps".format(av_num))
	plt.tight_layout()
	save_path = home_path + "plots/flux_compare_phase_radius_r=" + str(max_R) + ".png"
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()

#calculate_flux(data_dirs[0],True)
#calculate_flux(data_dirs[1],False)

plot_graph()
