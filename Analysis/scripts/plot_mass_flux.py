import yt
import numpy as np
import math
from yt import derived_field
from yt.units import cm
import time
import sys
from matplotlib import pyplot as plt

#print("yt version = ",yt.__version__)

yt.enable_parallelism()

class data_dir:
        def __init__(self, num, l, m, a, mu, nphi, ntheta, suffix):
                self.num = num
                self.l = l
                self.m = m
                self.a = float(a)
                self.mu = mu
                self.nphi = nphi
                self.ntheta = ntheta
                self.suffix = suffix
                self.name = "run{:04d}_l{:d}_m{:d}_a{:s}_Al{:s}_mu{:s}_M1_KerrSchild".format(num, l, m, a, "0", mu)

data_dirs = []
def add_data_dir(num, l, m, a, mu, nphi, ntheta, suffix=""):
        x = data_dir(num, l, m, a, mu, nphi, ntheta, suffix)
        data_dirs.append(x)

# appropriate \int Ylm Ylm^* cos(2 theta) dtheta dphi factor for 0 <= l <= 10
cos2theta_integrals = [[-(1/3)],[1/5,-(3/5)],[1/21,-(1/7),-(5/7)],\
[1/45,-(1/15),-(1/3),-(7/9)],[1/77,-(3/77),-(15/77),-(5/11),-(9/11)],\
[1/117,-(1/39),-(5/39),-(35/117),-(7/13),-(11/13)],\
[1/165,-(1/55),-(1/11),-(7/33),-(21/55),-(3/5),-(13/15)],\
[1/221,-(3/221),-(15/221),-(35/221),-(63/221),-(99/221),-(11/17),-(15/17)],\
[1/285,-(1/95),-(1/19),-(7/57),-(21/95),-(33/95),-(143/285),-(13/19),-(17/19)],\
[1/357,-(1/119),-(5/119),-(5/51),-(3/17),-(33/119),-(143/357),-(65/119),-(5/7),-(19/21)],\
[1/437,-(3/437),-(15/437),-(35/437),-(63/437),-(99/437),-(143/437),-(195/437),-(255/437),-(17/23),-(21/23)]]

def analytic_flux(t, r, l, m, a, mu, cumulative):	
	## calculate the perturbative flux at large radius to order 
	cos2theta = cos2theta_integrals[l][int(np.abs(m))]
	L = l*(l+1)
	tau = mu*t
	""" #
	Integrating factor of 
		\int Ylm Ylm^* cos(2 theta) dtheta dphi
	assuming the spherical harmonics are normalised so that 
		\int Ylm Ylm^* cos(2 theta) dtheta dphi = 1 
	# """
	if (m!=0):
		if not cumulative:
			F0 = 0.5*mu*tau - 0.5*mu*np.sin(tau)*np.cos(tau)
			F1 = 0.25*(L-1)*mu*np.sin(2*tau) - 0.5*mu*tau*(L-2*np.cos(2*tau)+1)
			#
			F2 = 0.25*(0.5*np.sin(2*tau)-tau)*(3*(a**2)*mu*cos2theta + 7*(a**2)*mu + 12*a*m)\
			-3*(2*L-1)*mu*tau*np.cos(2*tau)+7*L*mu*tau+0.125*np.sin(2*tau)*(12*tau**2-L-3)
			#
			F3 = 0.5*tau*((a**2)*mu*((5-2*np.cos(2*tau))*cos2theta - L - 4*np.cos(2*tau)+16)\
			+4*a*m(5-2*np.cos(2*tau))+0.5*(L**2)*mu(np.cos(2*tau)-1)-mu*(2*L+5*np.cos(2*tau)+10))\
			-0.25*np.sin(2*tau)*(3*(a**2)*mu*cos2theta+mu*(a**2)*(12-L)+12*a*m+3*(L-5)*mu)\
			-(mu/6.0)*(tau**3)*(3*L+7*np.cos(2*tau)-4)-0.25*(tau**2)*(9*L-1)*mu*np.sin(2*tau)
			#
			F4 = 1/8*tau*((a**2)*(-(6*(a**2)*mu*cos2theta+6*a*(3*a*mu+4*m)\
			+(6*L-11)*mu*np.cos(2*tau)-19*mu))-2*(np.sin(tau)**2)*((a**2)*(5*L+9)*mu*cos2theta+mu*((a**2)*(9*L+38)-6*L**2+L-35)\
			+4*a*(5*L+9)*m))+1/24*tau**3*(3*(a**2)*mu*cos2theta+mu*(9*(a**2)+L*(3*L+35)-59)+12*a*m+5*(8*L+1)*mu*np.cos(2*tau))\
			-1/16*tau**2*np.sin(2*tau)*(15*(a**2)*mu*cos2theta+mu*(21*(a**2)-L*(15*L+41)+52)+60*a*m)\
			+3/8*(a**2)*np.sin(2*tau)*((a**2)*mu*cos2theta+mu*(3*(a**2)+L-5)+4*a*m)+(mu*tau**5)/24-25/48*mu*tau**4*np.sin(2*tau)	
			#
		elif cumulative:
			F0 = 0.25*mu*tau**2 - 0.25*mu*np.sin(tau)**2
			#
			F1 = -1/4*(L+1)*mu*tau**2+1/4*(L-3)*mu*(np.sin(tau)**2)+mu*tau*np.sin(tau)*np.cos(tau) 
			#
			F2 = 1/8*tau**2*(-3*a**2*mu*cos2theta-7*a**2*mu-12*a*m+7*L*mu-6*mu*np.cos(2*tau))+1/8*(np.sin(tau)**2)*(3*a**2*mu*cos2theta+7*a**2*mu+12*a*m+(5*L-12)*mu)+3/4*(3-2*L)*mu*tau*np.sin(tau)*np.cos(tau)
			#
			F3 = 1/8*tau**2*(10*a**2*mu*cos2theta-2*a**2*L*mu+32*a**2*mu+40*a*m-L**2*mu+(9*L-8)*mu*np.cos(2*tau)-4*L*mu-20*mu)-1/8*(np.sin(tau)**2)*(2*a**2*mu*cos2theta-2*a**2*(L-8)*mu+8*a*m+(L**2+7*L-32)*mu)-1/8*tau*np.sin(2*tau)*(4*a**2*mu*cos2theta+8*a**2*mu+16*a*m-(L**2+L-2)*mu)+1/24*(4-3*L)*mu*tau**4-7/6*mu*tau**3*np.sin(tau)*np.cos(tau)
			#
			F4 = 1/96*tau**4*(3*a**2*mu*cos2theta+9*a**2*mu+12*a*m+3*L**2*mu+35*L*mu+25*mu*np.cos(2*tau)-59*mu)+1/32*tau*np.sin(2*tau)\
			*(a**2*(10*L+3)*mu*cos2theta+a**2*(6*L+77)*mu+4*a*(10*L+3)*m+3*(L**2+L-34)*mu)+1/64*tau**2*(-72*a**4*mu-96*a**3*m\
			-4*a**2*mu*(6*a**2+5*L+9)*cos2theta+30*a**2*mu*cos2theta*np.cos(2*tau)*-36*a**2*L*mu+42*a**2*mu*np.cos(2*tau)\
			-76*a**2*mu-80*a*L*m+120*a*m*np.cos(2*tau)-144*a*m-30*L**2*mu*np.cos(2*tau)+24*L**2*mu-2*L*mu*np.cos(2*tau)-4*L*mu+64*mu*np.cos(2*tau)+140*mu)+1/32*(np.sin(tau)**2)*(36*a**4*mu+48*a**3*m+a**2*mu*(12*a**2-10*L-3)*cos2theta+a**2*(6*L-137)*mu-4*a*(10*L+3)*m-3*(L**2+L-34)*mu)+5/6*(2*L-1)*mu*tau**3*np.sin(tau)*np.cos(tau)+(mu*tau**6)/144
	elif (m==0):
		if not cumulative:
			F0 = mu*tau*(np.cos(tau)**2)-mu*np.sin(tau)*np.cos(tau)
			F1 = mu*np.sin(2*tau)*tau**2+(-2*mu*(np.cos(tau)**2)-1/2*mu*(L+(L-2)*np.cos(2*tau)-2*np.cos(2*tau)-2))*tau+2*mu*np.cos(tau)*np.sin(tau)+mu*((L-2)*np.cos(tau)-np.cos(tau))*np.sin(tau)
			F2 = -mu*np.cos(2*tau)*tau**3+(1/2*mu*((4-3*L)*np.sin(2*tau)+3*np.sin(2*tau))-2*mu*np.sin(2*tau))*tau**2+(a**2*mu*(np.cos(tau)**2)+mu*(L+(L-2)*np.cos(2*tau)-2*np.cos(2*tau)-2)+1/8*(-18*mu*a**2-6*mu*cos2theta*a**2-6*mu*cos2theta*np.cos(2*tau)*a**2-18*mu*np.cos(2*tau)*a**2+16*mu-2*(6*L-11)*mu*np.cos(2*tau)+22*mu*np.cos(2*tau)))*tau-a**2*mu*np.cos(tau)*np.sin(tau)-2*mu*((L-2)*np.cos(tau)-np.cos(tau))*np.sin(tau)+1/2*((9*mu*a**2+3*mu*cos2theta*a**2-7*mu)*np.cos(tau)+mu*(3*(L-3)*np.cos(tau)+np.cos(tau)))*np.sin(tau)
			F3 = 1/4*mu*tau**2*np.sin(2*tau)*(-4*a**2*cos2theta-8*a**2+(L-1)*(L+5))+1/4*mu*tau*(2*a**2*cos2theta*(np.cos(2*tau)+5)+(-2*a**2*(L-7)+L*(L+6)-25)*np.cos(2*tau)-2*a**2*(L-17)-(L-6)*L-35)+mu*np.sin(tau)*np.cos(tau)*(-3*a**2*cos2theta+a**2*(L-12)-3*(L-5))+1/6*mu*tau**3*((9*L-5)*np.cos(2*tau)-3*L+5)-7/6*mu*tau**4*np.sin(tau)*np.cos(tau)
			F4 = 1/24*mu*tau**3*(3*a**2*cos2theta*(5*np.cos(2*tau)+1)+(21*a**2-L*(15*L+16)+43)*np.cos(2*tau)+9*a**2+L*(3*L+34)-73)+1/8*mu*tau**2*np.sin(2*tau)*(a**2*(5*L+4)*cos2theta+a**2*(3*L+40)-(L-7)*L-50)+3/4*a**2*mu*np.sin(2*tau)*(a**2*cos2theta+3*a**2+L-5)+1/8*mu*tau*(-18*a**4-a**2*cos2theta*((6*a**2-5*L-7)*np.cos(2*tau)+6*a**2+5*L+7)-5*a**2*(3*L+1)+(-18*a**4+a**2*(3*L+65)+(10-3*L)*L-55)*np.cos(2*tau)+L*(3*L-10)+55)+5/24*(4*L-1)*mu*tau**4*np.sin(2*tau)+1/24*mu*tau**5*(5*np.cos(2*tau)+1)
		elif cumulative:
			F0 = (mu*tau**2)/4-3/4*mu*(np.sin(tau)**2)+1/4*mu*tau*np.sin(2*tau)
			F1 = -1/4*mu*tau**2*(L+2*np.cos(2*tau))+3/4*(L-2)*mu*(np.sin(tau)**2)-1/4*(L-4)*mu*tau*np.sin(2*tau)
			F2 = 1/8*mu*tau**2*(-3*a**2*cos2theta-7*a**2+6*(L-2)*np.cos(2*tau)+4*L)+3/8*mu*(np.sin(tau)**2)*(3*a**2*cos2theta+7*a**2+2*L-8)-1/8*mu*tau*np.sin(2*tau)*(3*a**2*cos2theta+7*a**2+8*L-18)-mu*tau**3*np.sin(tau)*np.cos(tau)
			F3 = -1/8*mu*tau**2*(-4*a**2*cos2theta*np.cos(2*tau)\
			-10*a**2*cos2theta+2*a**2*L-8*a**2*np.cos(2*tau)\
			-34*a**2+L**2*np.cos(2*tau)+L**2-5*L*np.cos(2*tau)-6*L+7*np.cos(2*tau)+35)\
			-1/8*mu*(np.sin(tau)**2)*(10*a**2*cos2theta-6*a**2*(L-9)+2*L**2+13*L-78)\
			-1/8*mu*tau*np.sin(2*tau)*(2*a**2*cos2theta+2*a**2*(L-3)-2*L**2-L+18)\
			+1/24*mu*tau**4*(-3*L+7*np.cos(2*tau)+5)+1/4*(3*L-4)*mu*tau**3*np.sin(2*tau)
			F4 = 1/96*mu*tau**4*(3*a**2*cos2theta+9*a**2+3*L**2-5*(8*L-7)*np.cos(2*tau)+34*L-73)+1/48*mu*tau**3*np.sin(2*tau)*(15*a**2*cos2theta+21*a**2-15*L**2+24*L+8)-1/64*mu*tau**2*(72*a**4+2*a**2*(10*L-7)*cos2theta*np.cos(2*tau)+4*a**2*(6*a**2+5*L+7)*cos2theta+12*a**2*L*np.cos(2*tau)+60*a**2*L+118*a**2*np.cos(2*tau)+20*a**2+26*L**2*np.cos(2*tau)-12*L**2-20*L*np.cos(2*tau)+40*L-216*np.cos(2*tau)-220)+1/32*mu*(np.sin(tau)**2)*(108*a**4+a**2*(36*a**2-20*L-7)*cos2theta+3*a**2*(4*L-103)-7*L**2-10*L+218)-1/32*mu*tau*np.sin(2*tau)*(36*a**4+a**2*(12*a**2-20*L-7)*cos2theta-3*a**2*(4*L+63)-7*L**2-10*L+218)+(mu*tau**6)/144+5/48*mu*tau**5*np.sin(2*tau)
	Flux = F0 + F1/r + F2/r**2 + F3/r**3 + F4/r**4 
	return Flux

def time_average(x, n):
	N = len(x)
	n_chunks = int(np.floor(N/n))
	x_out = np.zeros(n_chunks)
	for i in range(0, n_chunks):
		x_out[i] = np.mean(x[i*n:(i+1)*n])
	x_out[-1] = np.mean(x[N-n:])
	return x_out

# choose datasets to compare

add_data_dir(1, 1, 1, "0.7", "0.4", 32, 32, "_theta_max0.98")

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"

output_dir = "data/flux_data"

half_box = True

KS_or_cartesian_r=True
phi0 = 0.1
R_max = 450
average_time = False
av_n = 1
plot_flux=False

def load_flux_data():
	# load data from csv files
	data = {}
	ang_flux_data = {}
	for dd in data_dirs:
		file_name = home_path + output_dir + "/" + dd.name + "_J_R_linear_n000000_nphi{:d}_ntheta{:d}{:s}.dat".format(dd.nphi, dd.ntheta, dd.suffix)
		data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		#file_name = home_path + output_dir + "/" + dd.name + "_J_azimuth_R_linear_n000000.dat"
		#ang_flux_data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		print("loaded flux data for " + dd.name)
	return data 	

def load_mass_data():
	# load data from csv files
	data = {}
	print(data_dirs)
	for dd in data_dirs:
		file_name = home_path + "data/mass_data/" + "{:s}_mass_in_r={:d}_conserved_rho.csv".format(dd.name, R_max)
		#file_name = home_path + "data/mass_data" + "/" + "l={:d}_m={:d}_a={:s}_mu={:s}_Al={:s}_mass_in_r={:d}_conserved_rho.csv".format(dd.l, dd.m, str(dd.a), dd.mu, dd.Al, R_max)
		data_line = np.genfromtxt(file_name, skip_header=1)
		data[dd.num] = data_line
		print("loaded mass data for " + file_name)
	return data

def plot_graph():
	mass_data = load_mass_data()
	if plot_flux:
		flux_data = load_flux_data()
	colours = ['r', 'b', 'g', 'm', 'y', 'c', 'k']
	i = 0
	fig, ax1 = plt.subplots()
	#ax2 = ax1.twinx()	
	for dd in data_dirs:
		# plot mass data
		mu = float(dd.mu)
		E0 = 0.5*(4*np.pi*(R_max**3)/3)*(phi0*mu)**2
		mass_line_data = mass_data[dd.num]
		delta_mass = mass_line_data[1:,1] - mass_line_data[0,1]
		tmass = mass_line_data[1:,0]
		label_ = "$l$={:d} $m$={:d}".format(dd.l, dd.m)
		ax1.plot(tmass,delta_mass/E0,colours[i]+"-", label="change in mass $R_+<R<$"+str(R_max)+" "+label_)
		analytic_outer_flux = analytic_flux(tmass, R_max, dd.l, dd.m, dd.a, mu, True)*(2*np.pi)*phi0**2/E0
		#label_ = "$\\mu$={:.2f}".format(mu)
		ax1.plot(tmass,analytic_outer_flux,colours[i]+"--", label="analytic flux into R={:.1f} ".format(R_max)+label_)
		#
		if plot_flux:
			flux_line_data = flux_data[dd.num]
			tflux = flux_line_data[1:,0]
			#r_min = line_data[0,1]
			outer_mass_flux = -flux_line_data[1:,2]*(4*np.pi)/E0
			outer_mass_flux = np.cumsum(outer_mass_flux)
			if average_time:
				tflux = time_average(t1, av_n)
				outer_mass_flux = time_average(outer_mass_flux, av_n)
			ax1.plot(tflux,outer_mass_flux,colours[i]+"-.", label="flux into R={:.1f}".format(R_max)+label_)			
		i = i + 1
	ax1.set_xlabel("$t$")
	#ax1.set_xlim((0, 300))
	#ax1.set_ylim((-0.0005, 0.0015))
	ax1.set_ylabel("$\\Delta$E / $E_0$")
	plt.title("Change in mass, $M=1$, $a=0.7$, $\\mu=0.4$")
	save_path = home_path + "plots/mass_in_R={:d}_vs_analytic_flux_compare_lm.png".format(R_max)
	#
	ax1.legend(loc='upper left', fontsize=8)
	plt.tight_layout()
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()

plot_graph()

