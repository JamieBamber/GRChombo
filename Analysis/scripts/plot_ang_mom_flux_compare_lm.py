import yt
import numpy as np
import math
from yt import derived_field
from yt.units import cm
import time
import sys
from matplotlib import rc
rc('text', usetex=True)
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
                self.name = "run{:04d}_l{:d}_m{:d}_a{:s}_Al{:s}_mu{:s}_M1_IsoKerr".format(num, l, m, a, "0", mu)

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

def analytic_flux(t, R, l, m, a, mu, cumulative):	
	## calculate the Boyer Lindquist r
	## assume M = 1
	r_plus = 1 + np.sqrt(1 - a*a)
	r = R*(1 + r_plus/(4.0*R))**2 
	## calculate the perturbative flux at large radius to order 
	cos2theta = cos2theta_integrals[l][int(np.abs(m))]
	L = l*(l+1)/(mu**2)
	tau = mu*t
	""" #
	Integrating factor of 
		\int Ylm Ylm^* cos(2 theta) dtheta dphi
	assuming the spherical harmonics are normalised so that 
		\int Ylm Ylm^* cos(2 theta) dtheta dphi = 1 
	# """
	if not cumulative:
		F0=(m*tau)/2+1/2*m*np.sin(tau)*np.cos(tau)
		F1=1/2*m*tau*(L-np.cos(2*tau))-1/4*(L-1)*m*np.sin(2*tau)
		F2=(m*tau*(3*a**2*mu*cos2theta+7*a**2*mu+12*a*m+3*(L-1)*mu*np.cos(2*tau)-4*L*mu))/(4*mu)+(m*np.sin(2*tau)*(-3*a**2*mu*cos2theta-7*a**2*mu-12*a*m+(L+3)*mu))/(8*mu)-m*tau**2*np.sin(tau)*np.cos(tau)
		F3=(1/(2*mu))*m*tau*(-3*a**2*mu*cos2theta-mu*(a**2+2*L-5)*np.cos(2*tau)+mu*(a**2*(L-11)-L+10)-12*a*m)+(m*np.sin(2*tau)*(3*a**2*mu*cos2theta+a**2*(-(L-12))*mu+12*a*m+3*(L-5)*mu))/(4*mu)+1/6*m*tau**3*(3*L+np.cos(2*tau)-4)+1/4*(L+1)*m*tau**2*np.sin(2*tau)
		F4=-(1/(24*mu))*m*tau**3*(3*a**2*mu*cos2theta+mu*(9*a**2+L*(3*L+14)-35)+12*a*m+(L+5)*mu*np.cos(2*tau))-(m*tau**2*np.sin(2*tau)*(a**2*mu*cos2theta+mu*(11*a**2+L*(L+3)-20)+4*a*m))/(16*mu)+(1/(4*mu))*tau*(a**2*m*(3*a**2*mu*cos2theta+9*a**2*mu+12*a*m+(3*L-7)*mu*np.cos(2*tau)-8*mu)+m*(np.sin(tau)**2)*(a**2*mu*cos2theta+mu*(3*a**2+L*(L+4)-15)+4*a*m))-(3*a**2*m*np.sin(tau)*np.cos(tau)*(a**2*mu*cos2theta+mu*(3*a**2+L-5)+4*a*m))/(4*mu)-(m*tau**5)/24+1/48*m*tau**4*np.sin(2*tau)
	elif cumulative:
		F0=(m*tau**2)/(4*mu)+(m*(np.sin(tau)**2))/(4*mu)
		F1=(L*m*tau**2)/(4*mu)-((L-2)*m*(np.sin(tau)**2))/(4*mu)-(m*tau*np.sin(tau)*np.cos(tau))/(2*mu)
		F2=(m*tau**2*(3*a**2*mu*cos2theta+7*a**2*mu+12*a*m-4*L*mu+2*mu*np.cos(2*tau)))/(8*mu**2)-(m*(np.sin(tau)**2)*(3*a**2*mu*cos2theta+7*a**2*mu+12*a*m+2*(L-4)*mu))/(8*mu**2)+((3*L-5)*m*tau*np.sin(2*tau))/(8*mu)
		F3=-((m*tau**2*(6*a**2*mu*cos2theta+2*mu*(a**2*(-(L-11))+L-10)+24*a*m+L*mu*np.cos(2*tau)))/(8*mu**2))+(m*(np.sin(tau)**2)*(6*a**2*mu*cos2theta-2*a**2*(L-13)*mu+24*a*m+(9*L-40)*mu))/(8*mu**2)-(m*tau*(2*a**2+3*L-10)*np.sin(2*tau))/(8*mu)+((3*L-4)*m*tau**4)/(24*mu)+(m*tau**3*np.sin(tau)*np.cos(tau))/(6*mu)
		F4=-((m*tau**4*(3*a**2*mu*cos2theta+mu*(9*a**2+L*(3*L+14)-35)+12*a*m+mu*np.cos(2*tau)))/(96*mu**2))-(m*tau*np.sin(2*tau)*(3*a**2*mu*cos2theta+3*a**2*(15-4*L)*mu+12*a*m+(L*(3*L+10)-54)*mu))/(32*mu**2)+(1/(32*mu**2))*m*tau**2*(8*(6*a**3+a)*m+a**2*mu*cos2theta*(12*a**2+np.cos(2*tau)+2)+np.cos(2*tau)*(11*a**2*mu+4*a*m+(L-4)*(L+6)*mu)+2*mu*(18*a**4-13*a**2+L*(L+4)-15))+(1/(32*mu**2))*m*(np.sin(tau)**2)*(-36*a**4*mu-48*a**3*m+3*(1-4*a**2)*a**2*mu*cos2theta+3*a**2*(35-8*L)*mu+12*a*m+(L*(3*L+10)-54)*mu)-((L+4)*m*tau**3*np.sin(2*tau))/(48*mu)-(m*tau**6)/(144*mu)
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

"""run0002_l0_m0_a0.7_Al0_mu0.4_M1_IsoKerr
run0005_l1_m1_a0.7_Al0_mu0.4_M1_IsoKerr
run0006_l1_m1_a0.99_Al0_mu0.4_M1_IsoKerr
run0007_l2_m2_a0.7_Al0_mu0.4_M1_IsoKerr
run0008_l4_m4_a0.7_Al0_mu0.4_M1_IsoKerr
run0009_l1_m-1_a0.7_Al0_mu0.4_M1_IsoKerr
run0010_l8_m8_a0.7_Al0_mu0.4_M1_IsoKerr
run0011_l1_m1_a0.7_Al0_mu2.0_M1_IsoKerr
run0012_l1_m1_a0.7_Al0_mu0.01_M1_IsoKerr
run0013_l2_m2_a0.7_Al0_mu0.8_M1_IsoKerr
run0014_l8_m8_a0.7_Al0_mu3.2_M1_IsoKerr
run0015_l1_m1_a0.7_Al0.5_mu0.4_M1_IsoKerr
run0016_l1_m-1_a0.99_Al0_mu0.4_M1_IsoKerr
run0017_l1_m1_a0.99_Al0.5_mu0.4_M1_IsoKerr
run0018_l1_m1_a0.99_Al0.25_mu0.4_M1_IsoKerr"""

#add_data_dir(2, 0, 0, "0.7", "0.4", 64, 64, "_theta_max0.99")
add_data_dir(5, 1, 1, "0.7", "0.4", 64, 64, "_theta_max0.99")
add_data_dir(7, 2, 2, "0.7", "0.4", 64, 64, "_theta_max0.99")
add_data_dir(8, 4, 4, "0.7", "0.4", 64, 64, "_theta_max0.99")
add_data_dir(9, 1, -1, "0.7", "0.4", 64, 64, "_theta_max0.99")
add_data_dir(10, 8, 8, "0.7", "0.4", 64, 64, "_theta_max0.99")

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"

output_dir = "data/flux_data"

half_box = True

KS_or_cartesian_r=True
phi0 = 0.1
R_min = 5
R_max = 500
average_time = False
av_n = 1
plot_mass=False
cumulative=True

def load_flux_data():
	# load data from csv files
	data = {}
	ang_flux_data = {}
	for dd in data_dirs:
		file_name = home_path + output_dir + "/" + dd.name + "_J_azimuth_R_linear_n000000_r_plus_to_{:d}_nphi{:d}_ntheta{:d}{:s}.dat".format(R_max, dd.nphi, dd.ntheta, dd.suffix)
		data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		print("loaded flux data for " + dd.name)
	return data 	

def load_mass_data():
	# load data from csv files
	data = {}
	print(data_dirs)
	for dd in data_dirs:
		file_name = home_path + "data/mass_data" + "/" + "{:s}_ang_mom_r_plus_to_{:d}.dat".format(dd.name, R_max)
		data_line = np.genfromtxt(file_name, skip_header=1)
		data[dd.num] = data_line
		print("loaded mass data for " + file_name)
	return data

def plot_graph():
	# plot setup
	ax1 = plt.axes()
	fig = plt.gcf()
	fig.set_size_inches(3.8,3)
	font_size = 6
	title_font_size = 7
	label_size = 9
	legend_font_size = 7
	rc('xtick',labelsize=font_size)
	rc('ytick',labelsize=font_size)
	#
	flux_data = load_flux_data()
	if plot_mass:
		mass_data = load_mass_data()
	colours = ['r', 'b', 'g', 'm', 'c', 'y']
	colours2 = ['k', 'm', 'c']
	i = 0
	for dd in data_dirs:
		flux_line_data = flux_data[dd.num]
		mu = float(dd.mu)
		tflux = flux_line_data[1:,0]
		r_min = flux_line_data[0,1]
		r_max = flux_line_data[0,2]
		E0 = 0.5*(4*np.pi*(r_max**3)/3)*(phi0*mu)**2
		#inner_mass_flux = -flux_line_data[1:,1]/E0
		outer_mass_flux = -2*flux_line_data[1:,2]/E0
		if average_time:
			tflux = time_average(tflux, av_n)
			#inner_mass_flux = time_average(inner_mass_flux, av_n)
			outer_mass_flux = time_average(outer_mass_flux, av_n)
		if cumulative:
			dt = tflux[2] - tflux[1]
			#inner_mass_flux = np.cumsum(inner_mass_flux)*dt
			outer_mass_flux = np.cumsum(outer_mass_flux)*dt
			analytic_outer_flux = analytic_flux(tflux, r_max, dd.l, dd.m, dd.a, mu, True)*(4*np.pi)*phi0**2*2/E0
		elif not cumulative:
			analytic_outer_flux = analytic_flux(tflux, r_max, dd.l, dd.m, dd.a, mu, False)*(4*np.pi)*phi0**2*2/E0
		#net_flux = outer_mass_flux - inner_mass_flux
		#label_ = "$\\mu$={:.2f}".format(mu)
		label_ = "$l$={:d} $m$={:d}".format(dd.l, dd.m)
		#ax1.plot(tflux,inner_mass_flux,colours[i]+"--", label="flux into R={:.1f} ".format(r_min)+label_)
		#ax1.plot(tflux,outer_mass_flux,colours[i]+"-", label="flux into R={:.1f} ".format(r_max)+label_)
		ax1.plot(tflux,outer_mass_flux,colours[i]+"-", label=label_, linewidth=1)
		ax1.plot(tflux,analytic_outer_flux,colours[i]+"--", label="_4th order t$\\mu$/r analytic flux into R={:.1f} ".format(r_max)+label_, linewidth=1)
		#ax1.plot(tflux,net_flux,colours[i]+":", label="net flux " + label_)
		#
		if plot_mass:
			mass_line_data = mass_data[dd.num]
			delta_mass = mass_line_data[1:,1] - mass_line_data[0,1]
			tmass = mass_line_data[1:,0]
			ax1.plot(tmass,delta_mass/E0,colours[i]+"-.", label="_change in mass {:.1f}$<R<${:.1f} ".format(r_min,r_max)+label_, linewidth=1)
		i = i + 1
	ax1.set_xlabel("$t$")
	if cumulative:
		ax1.set_ylabel("cumulative flux / $E_0$")
		plt.title("Cumulative ang. mom. flux, $M=1$, $a=0.7$, $\\mu=0.4$")
		save_path = home_path + "plots/ang_mom_flux_in_R{:.0f}_IsoKerr_compare_lm_cumulative_with_mass.png".format(R_max)
	else:
		ax1.set_ylabel("flux / $E_0$")
		plt.title("Ang. mom. flux, $M=1$, $a=0.7$, $\\mu=0.4$")
		save_path = home_path + "plots/ang_mom_flux_in_R{:.0f}_IsoKerr_compare_lm.png".format(R_max)
	ax1.legend(loc='upper left', fontsize=8)
	plt.tight_layout()
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()
	
plot_graph()

