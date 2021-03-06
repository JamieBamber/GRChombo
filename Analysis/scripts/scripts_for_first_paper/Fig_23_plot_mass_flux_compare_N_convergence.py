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

KS_or_cartesian_r=True
phi0 = 0.1
R_min = 5
R_max = 300
average_time=False
av_n = 1
plot_mass=False
cumulative=False
differential=True
Theta_max="0.99"
Ntheta=64
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

"""def misaligned_analytic_flux(alpha, t, R, a, mu, cumulative):
	# only for l=m=1 at the moment
	# |Y11(alpha)|^2 = 0.25*(1 + cos\alpha)^2|Y11|^2 + 0.25*(1 - cos\alpha)^2|Y1m1|^2 + 0.5*\sin^2(\alpha)|Y10|^2
	Y11 = analytic_flux(t, R, 1, 1, a, mu, cumulative)
	Y1m1 = analytic_flux(t, R, 1, -1, a, mu, cumulative)
	Y10 = analytic_flux(t, R, 1, 0, a, mu, cumulative)
	result = 0.25*(1 + np.cos(alpha*np.pi))**2*Y11 + 0.25*(1 - np.cos(alpha*np.pi))**2*Y1m1 + 0.5*(np.sin(alpha)**2)*Y10
	return result"""

class data_dir:
	def __init__(self, num, l, m, a, mu, Al, nphi, ntheta, theta_max, N):
		self.num = num
		self.l = l
		self.m = m
		self.a = float(a)
		self.mu = float(mu)
		self.nphi = nphi
		self.ntheta = ntheta
		self.Al = float(Al)
		self.theta_max = theta_max 
		self.N = N
		Nfix = "_N{:d}".format(N)
		self.name = "run{:04d}_l{:d}_m{:d}_a{:s}_Al{:s}_mu{:s}_M1_IsoKerr{:s}".format(num, l, m, a, Al, mu, Nfix)
	#
	def load_data(self):
		# load flux and mass data from csv files	
		file_name = home_path + output_dir + "/" + self.name + "_J_R_linear_n000000_r_plus_to_{:d}_nphi{:d}_ntheta{:d}_theta_max{:s}.dat".format(R_max, self.nphi, self.ntheta, self.theta_max)
		flux_data = np.genfromtxt(file_name, skip_header=1)
		print("loaded " + file_name)
		mu = float(self.mu)
		self.tflux = flux_data[1:,0]
		self.r_min = flux_data[0,1]
		self.r_max = flux_data[0,2]
		E0 = 0.5*(4*np.pi*(self.r_max**3)/3)*(phi0*mu)**2
		self.inner_mass_flux = -flux_data[1:,1]/E0
		self.outer_mass_flux = -flux_data[1:,2]/E0	
		if cumulative:
			dt = self.tflux[2] - self.tflux[1]
			#inner_mass_flux = np.cumsum(inner_mass_flux)*dt
			self.outer_mass_flux = np.cumsum(self.outer_mass_flux)*dt
		self.analytic_outer_flux = analytic_flux(self.tflux, self.r_max, self.l, self.m, self.a, mu, cumulative)*(4*np.pi)*phi0**2/E0
		if plot_mass:
			file_name = home_path + "data/mass_data" + "/" + "{:s}_mass_r_plus_to_{:d}.dat".format(self.name, R_max)
			mass_data = np.genfromtxt(file_name, skip_header=1)
			print("loaded " + file_name)
			if cumulative:
				self.tmass = mass_data[1:,0]
				self.dmass = (mass_data[1:,1] - mass_data[0,1])/E0
			elif not cumulative:
				self.tmass = mass_data[:-1,0]
				dt = tmass[1] - tmass[0]
				self.tmass_mean = 0.5*(self.tmass[1:]+self.tmass[:-1])
				self.dmass = (mass_data[1:,1] - mass_data[:-1,1])/(E0*dt)
				
data_dirs = []
def add_data_dir(num, l, m, a, mu, Al="0", nphi=Nphi, ntheta=Ntheta, theta_max=Theta_max, N=128):
        x = data_dir(num, l, m, a, mu, Al, nphi, ntheta, theta_max, N)
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

#add_data_dir(2, 0, 0, "0.7", "0.4", "0", 64, 64, "0.99")
#add_data_dir(5, 1, 1, "0.7", "0.4", "0", 64, 64, "0.99", 128)
#add_data_dir(5, 1, 1, "0.7", "0.4", "0", 64, 64, "0.99", 256)
#add_data_dir(7, 2, 2, "0.7", "0.4", "0", 64, 64, "0.99")
#add_data_dir(8, 4, 4, "0.7", "0.4", "0", 64, 64, "0.99")
#add_data_dir(9, 1, -1, "0.7", "0.4", "0", 64, 64, "0.99")
#add_data_dir(15, 1, 1, "0.7", "0.4", "0.5", 64, 64, "0.99")
#add_data_dir(6, 1, 1, "0.99", "0.4", "0", 64, 64, "0.99")
#add_data_dir(16, 1, -1, "0.99", "0.4", "0", 64, 64, "0.99")
#add_data_dir(17, 1, 1, "0.99", "0.4", "0.5", 64, 64, "0.99")
#add_data_dir(18, 1, 1, "0.99", "0.4", "0.25", 64, 64, "0.99")

add_data_dir(22, 8, 8, "0.99", "2.0", "0", 64, 18, "1.0", 32)
add_data_dir(22, 8, 8, "0.99", "2.0", "0", 64, 18, "1.0", 64) 
add_data_dir(22, 8, 8, "0.99", "2.0", "0", 64, 18, "1.0", 128)
add_data_dir(22, 8, 8, "0.99", "2.0", "0", 64, 18, "1.0", 256)
#add_data_dir(22, 8, 8, "0.99", "2.0", "0", 64, 18, "1.0", 512)

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
	colours = ['r', 'b', 'g', 'm', 'c', 'y']
	colours2 = ['k', 'm', 'c']
	#styles = ['-', ':']
	i = 0
	#dd0 = data_dirs[0]
        #dd0.load_data()
	for dd in data_dirs:
		dd.load_data()
	for i in range(0, len(data_dirs)-1):
		dd_HR = data_dirs[i+1] # higher resolution data
		dd_LR = data_dirs[i] # lower resolution data
		tau_LR = dd_LR.tflux*dd_LR.mu
		tau_HR = dd_HR.tflux[0::2]*dd_HR.mu
		flux_HR = dd_HR.outer_mass_flux[0::2]
		flux_LR = dd_LR.outer_mass_flux
		print("tau_LR.shape = ", tau_LR.shape)
		print("tau_HR.shape = ", tau_HR.shape)
		ds_length = min(tau_LR.size, tau_HR.size)
		tau = tau_LR[:ds_length]
		dflux = np.abs((flux_HR[:ds_length] - flux_LR[:ds_length]))
		label_ = "$(N$={:d}-$N$={:d}$)$".format(dd_HR.N, dd_LR.N)
		ax1.plot(tau,np.log(dflux)/np.log(2),colours[i]+"-", label=label_, linewidth=1)
		#
	ax1.set_xlabel("$\\tau$", fontsize=label_size)
	ax1.set_xlim((0, 150))
	ax1.set_ylim((-30, -15))
	if cumulative:
		ax1.set_ylabel("cumulative flux / $E_0$", fontsize=label_size)
		ax1.set_title("Cumulative mass flux, $M=1,\\mu=0.4$,\n$\\chi=0.7,l=m=1$", wrap=True, fontsize=title_font_size)
		save_path = home_path + "plots/mass_flux_in_R{:.0f}_IsoKerr_compare_N_cumulative.pdf".format(R_max)
	else:
		ax1.set_ylabel("$\\log_{2}(|f_{2N}-f_{N}|/E_0)$", fontsize=label_size)
		plt.title("Difference in mass flux \n $M=1,\\mu=2.0,\\chi=0.99,l=m=8$", wrap=True, fontsize=title_font_size)
		save_path = home_path + "plots/plots_for_first_paper/Fig_23_mass_flux_in_R{:.0f}_IsoKerr_compare_N_convergence.pdf".format(R_max)
	ax1.legend(loc='best', fontsize=legend_font_size, ncol=1, labelspacing=0.2, handletextpad=0, columnspacing=1)
	plt.xticks(fontsize=font_size)
	plt.yticks(fontsize=font_size)
	plt.tight_layout()
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()
	
plot_graph()

