import numpy as np
import math
import time
import sys
from matplotlib import rc
rc('text', usetex=True)
from matplotlib import pyplot as plt

# 
tex_fonts = {
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
}

#plt.rc("text.latex", preamble=r'''
#       \usepackage{newtxmath}
#       ''')

plt.rcParams.update(tex_fonts)

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"

output_dir = "data/flux_data"

half_box = True

phi0 = 0.1
#R_min = 5
R_max = 300
average_time = False
av_n = 1
plot_mass=False
cumulative=True
Theta_max="1.0"
Ntheta=18
Nphi=64

# appropriate \int Ylm Ylm^* cos(2 theta) sin(theta) dtheta dphi factor for 0 <= l <= 10
cos2theta_integrals = [[-(1/3)],[1/5,-(3/5)],[1/21,-(1/7),-(5/7)],\
[1/45,-(1/15),-(1/3),-(7/9)],[1/77,-(3/77),-(15/77),-(5/11),-(9/11)],\
[1/117,-(1/39),-(5/39),-(35/117),-(7/13),-(11/13)],\
[1/165,-(1/55),-(1/11),-(7/33),-(21/55),-(3/5),-(13/15)],\
[1/221,-(3/221),-(15/221),-(35/221),-(63/221),-(99/221),-(11/17),-(15/17)],\
[1/285,-(1/95),-(1/19),-(7/57),-(21/95),-(33/95),-(143/285),-(13/19),-(17/19)],\
[1/357,-(1/119),-(5/119),-(5/51),-(3/17),-(33/119),-(143/357),-(65/119),-(5/7),-(19/21)],\
[1/437,-(3/437),-(15/437),-(35/437),-(63/437),-(99/437),-(143/437),-(195/437),-(255/437),-(17/23),-(21/23)]]

def analytic_mass_flux(t, R, l, m, a, mu, cumulative):	
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
	Flux = F0 + F1/r + F2/r**2 + F3/r**3 + F4/r**4 
	return Flux

def analytic_ang_mom_flux(t, R, l, m, a, mu, cumulative):	
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
		F0=m*(-(tau**2/(4*mu))+(np.sin(tau)**2)/(4*mu))
		F1=m*((L*tau**2)/(4*mu)-((L-2)*(np.sin(tau)**2))/(4*mu)-(tau*np.sin(tau)*np.cos(tau))/(2*mu))
		F2=m*((tau**2*(3*a**2*mu*cos2theta+7*a**2*mu+12*a*m-4*L*mu+2*mu*np.cos(2*tau)))/(8*mu**2)-((np.sin(tau)**2)*(3*a**2*mu*cos2theta+7*a**2*mu+12*a*m+2*(L-4)*mu))/(8*mu**2)+((3*L-5)*tau*np.sin(2*tau))/(8*mu))
		F3=m*((tau*np.sin(2*tau)*(4*a**2*mu**2*cos2theta+mu**2*(10*a**2-(L-4)*L-11)+2*(L-3)))/(8*mu**3)+(1/(4*mu**3))*tau**2*(-a**2*(L+3)*mu**2*cos2theta+a*mu*(5*a*mu-4*m)+((3-2*L)*mu**2+1)*np.cos(2*tau)+L*(2-L*mu**2)-2)+(1/(4*mu**3))*(np.sin(tau)**2)*(a**2*(L-1)*mu**2*cos2theta+mu**2*(-15*a**2+2*(L-1)*L+8)+4*a*mu*m-4*L+7)+tau**4/(12*mu**3)+(tau**3*np.sin(2*tau))/(6*mu))
		F4=m*((1/(192*mu**3))*tau**4*(mu**2*(30*a**2*cos2theta-11*np.cos(2*tau))+5*mu**2*(18*a**2+(4-3*L)*L-15)+120*a*mu*m+18*L-44)+(1/(64*mu**3))*tau*np.sin(2*tau)*(-34*a**2*mu**2*cos2theta+mu**2*(6*a**2*(4*L-29)+(L-60)*L+234)-72*a*mu*m-14*L+36)+(1/(64*mu**3))*tau**2*(2*a**2*mu**2*cos2theta*(2*(6*a**2+8*L-5)-5*np.cos(2*tau))+np.cos(2*tau)*(mu**2*(-14*a**2+L*(5*L+4)-24)+56*a*mu*m-6*L+4)+48*a*(2*a**2-5)*mu*m+2*mu**2*(36*a**4+2*a**2*(8*L-159)+L*(21*L-20)+175)-76*L+88)-(1/(64*mu**3))*(np.sin(tau)**2)*(2*a**2*mu**2*(12*a**2+16*L-49)*cos2theta+8*a*(12*a**2-41)*mu*m+mu**2*(72*a**4+a**2*(80*L-998)+L*(49*L-156)+794)-110*L+164)+(tau**3*((21-20*L)*mu**2+12)*np.sin(2*tau))/(96*mu**3)+tau**6/(288*mu))
	Flux = -(F0 + F1/r + F2/r**2 + F3/r**3 + F4/r**4)
	return Flux

class data_dir:
	def __init__(self, num, l, m, a, mu, Al, nphi, ntheta, suffix):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = float(mu)
		self.nphi = nphi
		self.ntheta = ntheta
		self.suffix = suffix
		self.Al = float(Al)
		self.name = "run{:04d}_l{:d}_m{:d}_a{:s}_Al{:s}_mu{:s}_M1_IsoKerr".format(num, l, m, a, Al, mu)
	#
	def load_data(self):
		# load flux and mass data from csv files	
		mass_file_name = home_path + output_dir + "/" + self.name + "_J_R_linear_n000000_r_plus_to_{:d}_nphi{:d}_ntheta{:d}{:s}.dat".format(R_max, self.nphi, self.ntheta, self.suffix)
		mass_flux_data = np.genfromtxt(mass_file_name, skip_header=1)
		print("loaded " + mass_file_name)
		mu = float(self.mu)
		tflux_m = mass_flux_data[1:,0]
		self.r_min = mass_flux_data[0,1]
		self.R_max = mass_flux_data[0,2]
		E0 = 0.5*(4*np.pi*(self.R_max**3)/3)*(phi0*mu)**2
		self.outer_mass_flux = -mass_flux_data[1:,2]/(E0)
		#
		ang_mom_file_name = home_path + output_dir + "/" + self.name + "_J_azimuth_R_linear_n000000_r_plus_to_{:d}_nphi{:d}_ntheta{:d}{:s}.dat".format(R_max, self.nphi, self.ntheta, self.suffix)
		ang_mom_flux_data = np.genfromtxt(ang_mom_file_name, skip_header=1)
		print("loaded " + ang_mom_file_name)
		mu = float(self.mu)
		tflux_a = ang_mom_flux_data[1:,0]
		self.outer_ang_mom_flux = -ang_mom_flux_data[1:,2]/E0
		#
		ds_length = min(tflux_m.size, tflux_a.size)
		self.tau = mu*tflux_m[:ds_length]
		if cumulative:
			dt = (ang_mom_flux_data[2,0] - ang_mom_flux_data[1,0])
			self.outer_ang_mom_flux = np.cumsum(self.outer_ang_mom_flux)*dt
			self.outer_mass_flux = np.cumsum(self.outer_mass_flux)*dt
		#analytic_outer_mass_flux = analytic_mass_flux(tflux_m[:ds_length], self.R_max, self.l, self.m, self.a, mu, False)
		self.analytic_outer_ang_mom_flux = analytic_ang_mom_flux(tflux_a[:ds_length], R_max, self.l, self.m, self.a, mu, cumulative)/E0
		#self.j_diff_numerical = self.outer_ang_mom_flux[:ds_length] - self.m*self.outer_mass_flux[:ds_length]/self.mu
		#self.j_diff_analytic = analytic_outer_ang_mom_flux - self.m*analytic_outer_mass_flux/self.mu
				
data_dirs = []
def add_data_dir(num, l, m, a, mu, Al="0", nphi=Nphi, ntheta=Ntheta, suffix="_theta_max" + Theta_max):
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

add_data_dir(5, 1, 1, "0.7", "0.4")
add_data_dir(7, 2, 2, "0.7", "0.4")
add_data_dir(8, 4, 4, "0.7", "0.4")
add_data_dir(10, 8, 8, "0.7", "0.4")
add_data_dir(9, 1, -1, "0.7", "0.4")
#add_data_dir(15, 1, 1, "0.7", "0.4", "0.5", 64, 64, "_theta_max0.99")
#add_data_dir(6, 1, 1, "0.99", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(16, 1, -1, "0.99", "0.4", "0", 64, 64, "_theta_max0.99")
#add_data_dir(17, 1, 1, "0.99", "0.4", "0.5", 64, 64, "_theta_max0.99")
#add_data_dir(18, 1, 1, "0.99", "0.4", "0.25", 64, 64, "_theta_max0.99")

def plot_graph():
	# plot setup
	ax1 = plt.axes()
	fig = plt.gcf()
	fig.set_size_inches(3.375,3)
	font_size = 10
	title_font_size = 10
	label_size = 10
	legend_font_size = 10
	rc('xtick',labelsize=font_size)
	rc('ytick',labelsize=font_size)
	#
	colours = ['b', 'g', 'm', 'c', 'y']
	colours2 = ['k', 'm', 'c']
	i = 0
	for dd in data_dirs:
		dd.load_data()
		label_ = "$l$={:d} $m$={:d}".format(dd.l, dd.m)
		#ax1.plot(tflux,inner_mass_flux,colours[i]+"--", label="flux into R={:.1f} ".format(r_min)+label_)
		ax1.plot(dd.tau,dd.outer_ang_mom_flux,colours[i]+"-", label=label_, linewidth=1)
		#ax1.plot(dd.tau,dd.analytic_outer_ang_mom_flux,colours[i]+"--", label="_analytic", linewidth=1)
		ax1.plot(dd.tau,dd.m*dd.outer_mass_flux/dd.mu,colours[i]+"-.", label="_ang. momentum flux into R={:.1f} ".format(R_max)+label_, linewidth=2)
		#ax1.plot(dd.tau,np.log10(np.abs(dd.j_diff_numerical)),colours[i]+"-", label=label_, linewidth=1)
		#ax1.plot(dd.tau,np.log10(np.abs(dd.j_diff_analytic)),colours[i]+"--", label="_4th order t$\\mu$/r analytic flux into R={:.1f} ".format(R_max)+label_, linewidth=1)
		#ax1.plot(tflux,net_flux,colours[i]+":", label="net flux " + label_)
		#
		i = i + 1
	ax1.set_xlabel("$\\tau$", fontsize=label_size)
	ax1.set_xlim((0, 500))
	#ax1.set_ylim((-10, 2))
	if cumulative:
		ax1.set_ylabel("cumulative ang. mom. flux $/ E_0$", fontsize=label_size)
		plt.title("Cumulative angular momentum flux, \n$M=1,\\mu=0.4,\\chi=0.7$")
		save_path = home_path + "plots/plots_for_first_paper/Fig_19_ang_mom_flux_in_R{:.0f}_IsoKerr_compare_lm_cumulative.pdf".format(R_max)
	else:
		ax1.set_ylabel("angular momentum flux $/ E_0$", fontsize=label_size)
		plt.title("Angular momentum flux, \n$M=1,\\mu=0.4,\\chi=0.7$")
		save_path = home_path + "plots/ang_mom_flux_in_R{:.0f}_IsoKerr_compare_lm.pdf".format(R_max)
	ax1.legend(loc='best', ncol=2, fontsize=legend_font_size, labelspacing=0.05, borderpad=0.1, columnspacing=0.7, handletextpad=0.2)
	plt.xticks(fontsize=font_size)
	plt.yticks(fontsize=font_size)
	plt.tight_layout()
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()
	
plot_graph()

