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

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"

output_dir = "data/flux_data"

half_box = True

phi0 = 0.1
R_min = 5
R_max = 500
average_time = False
av_n = 1
plot_ang_mom=False
cumulative=False

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
		F0=-(m*tau)/2+1/2*m*np.sin(tau)*np.cos(tau)
		F1=1/2*m*tau*(L-np.cos(2*tau))-1/4*(L-1)*m*np.sin(2*tau)
		F2=(m*tau*(3*a**2*mu*cos2theta+7*a**2*mu+12*a*m+3*(L-1)*mu*np.cos(2*tau)-4*L*mu))/(4*mu)+(m*np.sin(2*tau)*(-3*a**2*mu*cos2theta-7*a**2*mu-12*a*m+(L+3)*mu))/(8*mu)-m*tau**2*np.sin(tau)*np.cos(tau)
		F3=(1/(2*mu))*m*tau*(-3*a**2*mu*cos2theta-mu*(a**2+2*L-5)*np.cos(2*tau)+mu*(a**2*(L-11)-L+10)-12*a*m)+(m*np.sin(2*tau)*(3*a**2*mu*cos2theta+a**2*(-(L-12))*mu+12*a*m+3*(L-5)*mu))/(4*mu)+1/6*m*tau**3*(3*L+np.cos(2*tau)-4)+1/4*(L+1)*m*tau**2*np.sin(2*tau)
		F4=-(1/(24*mu))*m*tau**3*(3*a**2*mu*cos2theta+mu*(9*a**2+L*(3*L+14)-35)+12*a*m+(L+5)*mu*np.cos(2*tau))-(m*tau**2*np.sin(2*tau)*(a**2*mu*cos2theta+mu*(11*a**2+L*(L+3)-20)+4*a*m))/(16*mu)+(1/(4*mu))*tau*(a**2*m*(3*a**2*mu*cos2theta+9*a**2*mu+12*a*m+(3*L-7)*mu*np.cos(2*tau)-8*mu)+m*(np.sin(tau)**2)*(a**2*mu*cos2theta+mu*(3*a**2+L*(L+4)-15)+4*a*m))-(3*a**2*m*np.sin(tau)*np.cos(tau)*(a**2*mu*cos2theta+mu*(3*a**2+L-5)+4*a*m))/(4*mu)-(m*tau**5)/24+1/48*m*tau**4*np.sin(2*tau)
	elif cumulative:
		F0=-(m*tau**2)/4+1/4*m*(np.sin(tau)**2)
		F1=1/4*L*m*tau**2-1/4*(L-2)*m*(np.sin(tau)**2)-1/2*m*tau*np.sin(tau)*np.cos(tau)
		F2=(m*tau**2*(3*a**2*mu*cos2theta+7*a**2*mu+12*a*m-4*L*mu+2*mu*np.cos(2*tau)))/(8*mu)-(m*(np.sin(tau)**2)*(3*a**2*mu*cos2theta+7*a**2*mu+12*a*m+2*(L-4)*mu))/(8*mu)+1/8*(3*L-5)*m*tau*np.sin(2*tau)
		F3=-((m*tau**2*(6*a**2*mu*cos2theta+2*mu*(a**2*(-(L-11))+L-10)+24*a*m+L*mu*np.cos(2*tau)))/(8*mu))+(m*(np.sin(tau)**2)*(6*a**2*mu*cos2theta-2*a**2*(L-13)*mu+24*a*m+(9*L-40)*mu))/(8*mu)-1/8*m*tau*(2*a**2+3*L-10)*np.sin(2*tau)+1/24*(3*L-4)*m*tau**4+1/6*m*tau**3*np.sin(tau)*np.cos(tau)
		F4=-((m*tau**4*(3*a**2*mu*cos2theta+mu*(9*a**2+L*(3*L+14)-35)+12*a*m+mu*np.cos(2*tau)))/(96*mu))-(m*tau*np.sin(2*tau)*(3*a**2*mu*cos2theta+3*a**2*(15-4*L)*mu+12*a*m+(L*(3*L+10)-54)*mu))/(32*mu)+(1/(32*mu))*m*tau**2*(8*(6*a**3+a)*m+a**2*mu*cos2theta*(12*a**2+np.cos(2*tau)+2)+np.cos(2*tau)*(11*a**2*mu+4*a*m+(L-4)*(L+6)*mu)+2*mu*(18*a**4-13*a**2+L*(L+4)-15))+(1/(32*mu))*m*(np.sin(tau)**2)*(-36*a**4*mu-48*a**3*m+3*(1-4*a**2)*a**2*mu*cos2theta+3*a**2*(35-8*L)*mu+12*a*m+(L*(3*L+10)-54)*mu)-1/48*(L+4)*m*tau**3*np.sin(2*tau)-(m*tau**6)/144
	Flux = -(F0 + F1/r + F2/r**2 + F3/r**3 + F4/r**4)
	return Flux

class data_dir:
	def __init__(self, num, l, m, a, mu, Al, nphi, ntheta, suffix):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = mu
		self.nphi = nphi
		self.ntheta = ntheta
		self.suffix = suffix
		self.Al = Al
		self.name = "run{:04d}_l{:d}_m{:d}_a{:s}_Al{:s}_mu{:s}_M1_IsoKerr".format(num, l, m, a, Al, mu)
	#
	def load_data(self):
		# load flux and mass data from csv files	
		file_name = home_path + output_dir + "/" + self.name + "_J_azimuth_R_linear_n000000_r_plus_to_{:d}_nphi{:d}_ntheta{:d}{:s}.dat".format(R_max, self.nphi, self.ntheta, self.suffix)
		flux_data = np.genfromtxt(file_name, skip_header=1)
		print("loaded " + file_name)
		mu = float(self.mu)
		self.tflux = flux_data[1:,0]*mu
		self.r_min = flux_data[0,1]
		self.r_max = flux_data[0,2]
		E0 = 0.5*(4*np.pi*(self.r_max**3)/3)*(phi0*mu)**2
		self.inner_ang_mom_flux = -flux_data[1:,1]/E0
		self.outer_ang_mom_flux = -flux_data[1:,2]/E0	
		if cumulative:
			dt = (flux_data[2,0] - flux_data[1,0])
			#inner_ang_mom_flux = np.cumsum(inner_ang_mom_flux)*dt
			self.outer_ang_mom_flux = np.cumsum(self.outer_ang_mom_flux)*dt
		self.analytic_outer_flux = analytic_flux(self.tflux, self.r_max, self.l, self.m, self.a, mu, cumulative)*(4*np.pi)*phi0**2/E0
		if plot_ang_mom:
			file_name = home_path + "data/mass_data" + "/" + "{:s}_ang_mom_r_plus_to_{:d}.dat".format(self.name, R_max)
			self.ang_mom_data = np.genfromtxt(file_name, skip_header=1)
			print("loaded " + file_name)
			if cumulative:
				self.tang_mom = ang_mom_data[1:,0]*mu
				self.dang_mom = (ang_mom_data[1:,1] - ang_mom_data[0,1])/E0
			elif not cumulative:
				self.tang_mom = ang_mom_line_data[:-1,0]
				dt = ang_mom_data[2,0] - ang_mom_data[1,0]
				self.tang_mom_mean = 0.5*(self.tang_mom[1:]+self.tang_mom[:-1])
				self.dang_mom = (ang_mom_line_data[1:,1] - ang_mom_line_data[:-1,1])/(E0*dt)
				
data_dirs = []
def add_data_dir(num, l, m, a, mu, Al, nphi, ntheta, suffix=""):
        x = data_dir(num, l, m, a, mu, Al, nphi, ntheta, suffix)
        data_dirs.append(x)

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

add_data_dir(2, 0, 0, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
add_data_dir(5, 1, 1, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
add_data_dir(7, 2, 2, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
add_data_dir(8, 4, 4, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
add_data_dir(9, 1, -1, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")
add_data_dir(10, 8, 8, "0.7", "0.4", "0", 64, 64, "_theta_max0.99")

#add_data_dir(15, 1, 1, "0.7", "0.4", "0.5", 64, 64, "_theta_max0.99")

#add_data_dir(6, 1, 1, "0.99", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(16, 1, -1, "0.99", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(17, 1, 1, "0.99", "0.4", "0.5", 64, 64, "_theta_max0.99")
#add_data_dir(18, 1, 1, "0.99", "0.4", "0.25", 64, 64, "_theta_max0.99")

def plot_graph():
	# plot setup
	ax1 = plt.axes()
	fig = plt.gcf()
	fig.set_size_inches(3.8,3)
	font_size = 10
	title_font_size = 10
	label_size = 10
	legend_font_size = 8
	rc('xtick',labelsize=font_size)
	rc('ytick',labelsize=font_size)
	#
	colours = ['r', 'b', 'g', 'm', 'c', 'y']
	colours2 = ['k', 'm', 'c']
	i = 0
	for dd in data_dirs:
		dd.load_data()
		#net_flux = outer_ang_mom_flux - inner_ang_mom_flux
		#label_ = "$\\mu$={:.2f}".format(mu)
		label_ = "$l$={:d} $m$={:d}".format(dd.l, dd.m)
		#label_ = "$m$={:d} $\\alpha$={:s}".format(dd.m, dd.Al)
		#ax1.plot(dd.tflux,dd.inner_ang_mom_flux,colours[i]+":", label="flux into $R_+$ "+label_)
		ax1.plot(dd.tflux,dd.outer_ang_mom_flux,colours[i]+"-", label=label_, linewidth=1)
		ax1.plot(dd.tflux,dd.analytic_outer_flux,colours[i]+"--", label="_4th order t$\\mu$/r analytic flux into R={:.1f} ".format(R_max)+label_, linewidth=1)
		#
		if plot_ang_mom:
			if cumulative:
				ax1.plot(dd.tang_mom,dd.dang_mom,colours[i]+"-.", label="_change in ang_mom $R_+<R<${:.1f} ".format(R_max)+label_, linewidth=1)
			elif not cumulative:
				ax1.plot(dd.tang_mom,dd.dang_mom,colours[i]+"-.", label="_rate of change in ang_mom $R_+<R<${:.1f} ".format(R_max)+label_, linewidth=1)
		i = i + 1
	ax1.set_xlabel("$\\tau$", fontsize=label_size)
	#ax1.set_xlim((0, 200))
	#ax1.set_ylim((0, 0.00001))
	if cumulative:
		ax1.set_ylabel("cumulative flux / $E_0$", fontsize=label_size)
		ax1.set_title("Cumulative ang. mom. flux, $M=1$, $\\chi=0.7$, $\\mu=0.4$", wrap=True, fontsize=title_font_size)
		save_path = home_path + "plots/ang_mom_flux_in_R{:.0f}_IsoKerr_compare_lm_cumulative.png".format(R_max)
	else:
		ax1.set_ylabel("flux / $E_0$", fontsize=label_size)
		plt.title("Mass flux, $M=1$, $\\chi=0.7$, $\\mu=0.4$")
		save_path = home_path + "plots/ang_mom_flux_in_R{:.0f}_IsoKerr_compare_lm.png".format(R_max)
	ax1.legend(loc='upper left', fontsize=legend_font_size)
	plt.tight_layout()
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()
	
plot_graph()

