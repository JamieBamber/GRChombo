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
	if (m!=0):
		if not cumulative:
			F0=(mu*tau)/2-1/2*mu*np.sin(tau)*np.cos(tau)
			F1=1/4*(L-1)*mu*np.sin(2*tau)-1/2*mu*tau*(L-2*np.cos(2*tau)+1)
			F2=1/4*tau*(-3*a**2*mu*cos2theta-7*a**2*mu-12*a*m+3*(1-2*L)*mu*np.cos(2*tau)+7*L*mu)+1/8*np.sin(2*tau)*(3*a**2*mu*cos2theta+7*a**2*mu+12*a*m-(L+3)*mu)+3*mu*tau**2*np.sin(tau)*np.cos(tau)
			F3=1/4*tau*(2*a**2*mu*cos2theta*(5-2*np.cos(2*tau))-mu*(2*a**2*(L-16)+L*(L+4)+20)+np.cos(2*tau)*(-8*a**2*mu-16*a*m+(L*(L+10)-10)*mu)+40*a*m)-1/4*np.sin(2*tau)*(3*a**2*mu*cos2theta+a**2*(-(L-12))*mu+12*a*m+3*(L-5)*mu)-1/6*mu*tau**3*(3*L+7*np.cos(2*tau)-4)+1/4*(1-9*L)*mu*tau**2*np.sin(2*tau)
			F4=1/24*tau**3*(3*a**2*mu*cos2theta+mu*(9*a**2+L*(3*L+35)-59)+12*a*m+5*(8*L+1)*mu*np.cos(2*tau))-1/16*tau**2*np.sin(2*tau)*(15*a**2*mu*cos2theta+mu*(21*a**2-L*(15*L+41)+52)+60*a*m)+3/8*a**2*np.sin(2*tau)*(a**2*mu*cos2theta+mu*(3*a**2+L-5)+4*a*m)+1/8*tau*(a**2*mu*cos2theta*(-6*a**2+(5*L+9)*np.cos(2*tau)-5*L-9)+np.cos(2*tau)*(mu*(a**2*(3*L+49)-6*L**2+L-35)+4*a*(5*L+9)*m)-4*a*m*(6*a**2+5*L+9)-mu*(18*a**4+a**2*(9*L+19)-6*L**2+L-35))+(mu*tau**5)/24-25/48*mu*tau**4*np.sin(2*tau)
		elif cumulative:
			F0=(tau**2)/4-1/4*(np.sin(tau)**2)
			F1=-1/4*(L+1)*tau**2+1/4*(L-3)*(np.sin(tau)**2)+tau*np.sin(tau)*np.cos(tau)
			F2=1/8*tau**2*(-3*a**2*cos2theta-7*a**2-12*a*m+7*L-6*np.cos(2*tau))+1/8*(np.sin(tau)**2)*(3*a**2*cos2theta+(7*a**2+5*L-12)+12*a*m)+3/8*(3-2*L)*tau*np.sin(2*tau)
			F3=-1/8*tau*np.sin(2*tau)*(4*a**2*cos2theta+8*a**2+16*a*m-(L**2+L-2))+1/8*tau**2*(10*a**2*cos2theta-(2*a**2*(L-16)+L*(L+4)+20)+40*a*m+(9*L-8)*np.cos(2*tau))-1/8*(np.sin(tau)**2)*(2*a**2*cos2theta-2*a**2*(L-8)+8*a*m+(L*(L+7)-32))+1/24*(4-3*L)*tau**4-7/6*tau**3*np.sin(tau)*np.cos(tau)
			F4=1/32*tau*np.sin(2*tau)*(a**2*(10*L+3)*cos2theta+a**2*(6*L+77)+4*a*(10*L+3)*m+3*(L**2+L-34))+1/96*tau**4*(3*a**2*cos2theta+(9*a**2+L*(3*L+35)-59)+12*a*m+25*np.cos(2*tau))+1/32*tau**2*(a**2*(-mu)*cos2theta*(2*(6*a**2+5*L+9)-15*np.cos(2*tau))+np.cos(2*tau)*((21*a**2-L*(15*L+1)+32)+60*a*m)-8*a*m*(6*a**2+5*L+9)-2*(18*a**4+a**2*(9*L+19)-6*L**2+L-35))+1/32*(np.sin(tau)**2)*(36*a**4+48*a**3*m+a**2*(12*a**2-10*L-3)*cos2theta+a**2*(6*L-137)-4*a*(10*L+3)*m-3*(L**2+L-34))+5/6*(2*L-1)*tau**3*np.sin(tau)*np.cos(tau)+(tau**6)/144
	elif (m==0):
		if not cumulative:
			F0=mu*tau*(np.sin(tau)**2)
			F1=-(L+2)*mu*tau*(np.sin(tau)**2)-mu*tau**2*np.sin(2*tau)
			F2=-1/2*mu*tau*(np.sin(tau)**2)*(3*a**2*cos2theta+7*a**2-10*L)-6*a**2*mu*np.sin(tau)*(np.cos(tau)-1)+3*(L+1)*mu*tau**2*np.sin(tau)*np.cos(tau)+mu*tau**3*np.cos(2*tau)
			F3=1/4*mu*tau**2*np.sin(2*tau)*(4*a**2*cos2theta+8*a**2-L*(L+22)+7)-mu*tau*(np.sin(tau/2)**2)*(-10*a**2*cos2theta*(np.cos(tau)+1)+(2*a**2*(L-7)+L*(L+14)+5)*np.cos(tau)+2*a**2*(L-13)+L*(L+14)+5)+9*a**2*mu*(np.sin(2*tau)-2*np.sin(tau))-1/2*mu*tau**3*(3*(L+1)*np.cos(2*tau)+L-1)+7/6*mu*tau**4*np.sin(tau)*np.cos(tau)
			F4=1/8*mu*tau**3*(a**2*cos2theta*(1-5*np.cos(2*tau))+(-7*a**2+L*(5*L+32)-11)*np.cos(2*tau)+3*a**2+L*(L+12)-15)-1/4*mu*tau**2*np.sin(tau)*(np.cos(tau)*(a**2*(5*L+19)*cos2theta+a**2*(3*L+41)-2*L*(8*L+17)+2)+12*a**2)+6*a**2*mu*(2*a**2+L+3)*(np.sin(tau/2)**2)*np.sin(tau)+1/2*mu*tau*(np.sin(tau/2)**2)*(-18*a**4-2*a**2*(6*a**2+5*L+11)*cos2theta*(np.cos(tau/2)**2)+5*a**2*(L-5)+(-18*a**4+a**2*(17*L+35)+L*(9*L+8)+15)*np.cos(tau)+L*(9*L+8)+15)-5/6*(L+1)*mu*tau**4*np.sin(2*tau)+1/24*tau**5*(mu-5*mu*np.cos(2*tau))
		elif cumulative:
			F0=tau**2/4+(np.sin(tau)**2)/4-1/4*tau*np.sin(2*tau)
			F1=1/4*tau**2*(-L+2*np.cos(2*tau)-2)-1/4*L*(np.sin(tau)**2)+1/4*L*tau*np.sin(2*tau)
			F2=1/8*tau**2*(-3*a**2*cos2theta-7*a**2-6*L*np.cos(2*tau)+10*L)+1/8*((np.sin(tau/2)**2)*((8*L-62*a**2)*np.cos(tau)+34*a**2+8*L)-3*a**2*cos2theta*(np.sin(tau)**2))+1/8*tau*np.sin(2*tau)*(3*a**2*cos2theta+7*a**2-4*L)+tau**3*np.sin(tau)*np.cos(tau)
			F3=1/8*tau**2*(2*a**2*cos2theta*(5-2*np.cos(2*tau))+(-8*a**2+L*(L+13)-9)*np.cos(2*tau)-2*a**2*(L-19)-L*(L+14)-5)+tau*(1/8*np.sin(2*tau)*(-6*a**2*cos2theta+2*a**2*(L-3)+L+14)-6*a**2*np.sin(tau))+3/4*a**2*cos2theta*(np.sin(tau)**2)-1/4*(np.sin(tau/2)**2)*((2*a**2*(L-39)+L+14)*np.cos(tau)+2*a**2*(L+9)+L+14)+1/24*tau**4*(-3*L-7*np.cos(2*tau)+3)-1/6*(9*L+2)*tau**3*np.sin(tau)*np.cos(tau)
			F4=1/96*tau**4*(3*a**2*cos2theta+9*a**2+5*(8*L+3)*np.cos(2*tau)+3*L*(L+12)-45)-1/48*tau**3*np.sin(2*tau)*(15*a**2*cos2theta+21*a**2-L*(15*L+56)+48)+1/32*tau**2*(-36*a**4+a**2*cos2theta*((10*L+23)*np.cos(2*tau)-2*(6*a**2+5*L+11))+(a**2*(6*L+61)-L*(17*L+12)-44)*np.cos(2*tau)-2*a**2*(7*L+85)+96*a**2*np.cos(tau)+2*L*(9*L+8)+30)+1/16*(np.sin(tau/2)**2)*(60*a**4+2*(1-12*a**2)*a**2*cos2theta*(np.cos(tau/2)**2)-a**2*(8*L+13)+(-132*a**4-a**2*(8*L+13)+L*(L+4)-14)*np.cos(tau)+L*(L+4)-14)+1/16*tau*np.sin(tau)*(48*a**2*(L+3)+np.cos(tau)*(36*a**4+(12*a**2-1)*a**2*cos2theta-a**2*(40*L+131)-L*(L+4)+14))+tau**6/144-5/48*tau**5*np.sin(2*tau)
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
#add_data_dir(7, 2, 2, "0.7", "0.4", 64, 64, "_theta_max0.99")
#add_data_dir(8, 4, 4, "0.7", "0.4", 64, 64, "_theta_max0.99")
#add_data_dir(9, 1, -1, "0.7", "0.4", 64, 64, "_theta_max0.99")
add_data_dir(11, 1, 1, "0.7", "2.0", 64, 64, "_theta_max0.99")
#add_data_dir(12, 1, 1, "0.7", "0.01", 64, 64, "_theta_max0.99")
#add_data_dir(19, 1, 1, "0.7", "0.01", 64, 64, "_theta_max0.99")
add_data_dir(20, 1, 1, "0.7", "0.1", 64, 64, "_theta_max0.99")
#add_data_dir(10, 8, 8, "0.7", "0.4", 64, 64, "_theta_max0.99")
#add_data_dir(10, 8, 8, "0.7", "0.4", 64, 64, "_theta_max0.99")

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
		file_name = home_path + output_dir + "/" + dd.name + "_J_R_linear_n000000_r_plus_to_{:d}_nphi{:d}_ntheta{:d}{:s}.dat".format(R_max, dd.nphi, dd.ntheta, dd.suffix)
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
		file_name = home_path + "data/mass_data" + "/" + "{:s}_mass_r_plus_to_{:d}.dat".format(dd.name, R_max)
		data_line = np.genfromtxt(file_name, skip_header=1)
		data[dd.num] = data_line
		print("loaded mass data for " + file_name)
	return data

def plot_graph():
	# plot setup
	ax1 = plt.axes()
	fig = plt.gcf()
	fig.set_size_inches(3.8,3)
	font_size = 10
	title_font_size = 10
	label_size = 10
	legend_font_size = 10
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
		E0 = 0.5*(4*np.pi*(r_max**3)/3)*(phi0)**2
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
		label_ = "$\\mu$={:.2f}".format(mu)
		#label_ = "$l$={:d} $m$={:d}".format(dd.l, dd.m)
		#ax1.plot(tflux,inner_mass_flux,colours[i]+"--", label="flux into R={:.1f} ".format(r_min)+label_)
		#ax1.plot(tflux,outer_mass_flux,colours[i]+"-", label="flux into R={:.1f} ".format(r_max)+label_)
		ax1.plot(tflux*mu,outer_mass_flux,colours[i]+"-", label=label_, linewidth=1)
		ax1.plot(tflux*mu,analytic_outer_flux,colours[i]+"--", label="_4th order t$\\mu$/r analytic flux into R={:.1f} ".format(r_max)+label_, linewidth=1)
		#ax1.plot(tflux,net_flux,colours[i]+":", label="net flux " + label_)
		#
		if plot_mass:
			mass_line_data = mass_data[dd.num]
			delta_mass = mass_line_data[1:,1] - mass_line_data[0,1]
			tmass = mass_line_data[1:,0]
			ax1.plot(tmass*mu,delta_mass/E0,colours[i]+"-.", label="_change in mass {:.1f}$<R<${:.1f} ".format(r_min,r_max)+label_, linewidth=1)
		i = i + 1
	ax1.set_xlim((0, 200))
	ax1.set_ylim((0, 0.001))
	ax1.set_xlabel("$\\tau$")
	if cumulative:
		ax1.set_ylabel("cumulative flux / $V_0 \\frac{1}{2} \\varphi^2_0$")
		plt.title("Cumulative mass flux, $M=1$, $a=0.7$, $l=m=1$", fontsize=title_font_size)
		save_path = home_path + "plots/mass_flux_in_R{:.0f}_IsoKerr_compare_mu_cumulative.png".format(R_max)
	else:
		ax1.set_ylabel("flux / $E_0$")
		plt.title("Mass flux, $M=1$, $a=0.7$, $l=m=1$", fontsize=title_font_size)
		save_path = home_path + "plots/mass_flux_in_R{:.0f}_IsoKerr_compare_mu.png".format(R_max)
	ax1.legend(loc='upper left', fontsize=legend_font_size)
	plt.xticks(fontsize=font_size)
	plt.yticks(fontsize=font_size)
	plt.tight_layout()
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()
	
plot_graph()

