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
		self.name = "run{:04d}_KNL_l{:d}_m{:d}_a{:s}_Al{:s}_mu{:s}_M1_KerrSchild".format(num, l, m, a, "0", mu)

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
			F0 = mu*tau-mu*np.cos(tau)*np.sin(tau)
			F1 = tau*(-(L/(2*mu))-6*mu+4*mu*np.cos(2*tau))+1/2*((L/mu+4*mu)*np.cos(tau)-2*np.sin(tau))*np.sin(tau)
			F2 = (12*mu*np.sin(2*tau)-1)*tau**2+1/2*(-3*mu*cos2theta*a**2-(6*m+a*mu)*a+64*mu+(-((6*L)/mu)-52*mu)*np.cos(2*tau)+6*np.sin(2*tau)+(3*L)/mu)*tau+(np.sin(tau)**2)+(((a**2-12)*mu**2+3*a**2*cos2theta*mu**2+6*a*m*mu+3*L)*np.cos(tau)*np.sin(tau))/(2*mu)
			F3 = -((4*(16*np.cos(2*tau)*mu**2+1)*tau**3)/(3*mu))+((24*mu**2-2*a*m*mu+2*((-60*mu**2-6*L+1)*np.sin(2*tau)-8*mu*np.cos(2*tau))*mu+L+1)*tau**2)/mu**2+(1/(4*mu**3))*(8*(3*a**2-80)*mu**4+64*a*m*mu**3-4*(8*L+9)*mu**2+2*a**2*cos2theta*(-16*np.cos(2*tau)*mu**2+24*mu**2+L)*mu**2-4*(26*mu**2+2*a*m*mu+2*L-1)*np.sin(2*tau)*mu+(L-4)*L+2*(L**2+(20*mu**2-1)*L-8*mu**2*((a**2-35)*mu**2+2*a*m*mu+1))*np.cos(2*tau))*tau+(1/(8*mu**3))*(8*np.sin(tau)*(mu*(a**2*cos2theta*mu**2+3*(4*mu**2+2*a*m*mu+L-1))*np.sin(tau)-288*a**2*m**2)+(-8*(a**2-10)*mu**4-32*a*m*mu**3+4*(13-2*L)*mu**2-2*a**2*(8*mu**2+L)*cos2theta*mu**2+1152*a**2*m**2-3*(L-2)*L)*np.sin(2*tau))
			F4 = -((2*mu*tau**5)/3)-5/3*(15*mu*np.sin(2*tau)+4)*tau**4+1/24*(-120*mu*cos2theta*a**2-120*(2*m+a*mu)*a+3760*mu+(16*(374*mu**2+35*L-10)*np.cos(2*tau))/mu-880*np.sin(2*tau)+(400*L+52)/mu+(3*L*(5*L-6))/mu**3)*tau**3+(1/(16*mu**3))*(8*a**2*cos2theta*(2-45*mu*np.sin(2*tau))*mu**3-4*(424*mu**2-38*a*m*mu+18*L+21)*mu+4*(456*mu**2+10*a*m*mu+30*L-5)*np.cos(2*tau)*mu+(8*(1318-21*a**2)*mu**4-400*a*m*mu**3+4*(280*L-53)*mu**2+15*L*(3*L-2))*np.sin(2*tau))*tau**2+(1/(8*mu**3))*(-4*(3*a**4+6*a**2-836)*mu**4-8*a*(3*a**2+50)*m*mu**3+4*(51-2*(a**2-30)*L)*mu**2-4*a**2*cos2theta*((3*a**2+70)*mu**2+5*L-5*(14*mu**2+L)*np.cos(2*tau))*mu**2-20*a*m*L*mu+4*(2*(3*a**2+14)*mu**2-2*a*m*mu+3*L+1)*np.sin(2*tau)*mu+768*a**2*m**2+(18-5*L)*L+3072*a**2*m**2*np.cos(tau)-((18-5*L)*L+4*((-18*mu**4+L*mu**2+960*m**2)*a**2-5*m*mu*(20*mu**2+L)*a+mu**2*(836*mu**2+60*L+51)))*np.cos(2*tau))*tau+(1/(2*mu**3))*np.sin(tau)*(3*a**2*(256*m**2+((a**2-4)*mu**4+a**2*cos2theta*mu**4+2*a*m*mu**3+L*mu**2-256*m**2)*np.cos(tau))-mu*(2*a**2*cos2theta*mu**2+72*mu**2+20*a*m*mu+12*L-11)*np.sin(tau))
		elif cumulative:
			F0 = (mu*tau**2)/2 - 1/2*mu*(np.sin(tau)**2)
			F1 = (-(L/(4*mu))-3*mu)*tau**2+(4*mu*np.cos(tau)*np.sin(tau)-1/2)*tau+(np.sin(tau)*(2*mu*np.cos(tau)+(L-4*mu**2)*np.sin(tau)))/(4*mu)
			F2 = -(tau**3/3)+1/4*((3*L)/mu+64*mu-a*(6*m+a*mu)-3*mu*(cos2theta*a**2+8*np.cos(2*tau)))*tau**2+1/2*(-3*np.cos(2*tau)+(-((3*L)/mu)-14*mu)*np.sin(2*tau)+1)*tau+(np.sin(tau)*(4*mu*np.cos(tau)+9*L*np.sin(tau)+mu*(3*mu*cos2theta*a**2+6*m*a+(a**2+16)*mu)*np.sin(tau)))/(4*mu)
			F3 = -(tau**4/(3*mu))+((-64*np.cos(tau)*np.sin(tau)*mu**3+24*mu**2-2*a*m*mu+L+1)*tau**3)/(3*mu**2)+1/8*(64*a*m+8*(3*a**2-80)*mu+(2*(24*mu**2+L)*cos2theta*a**2+8*(44*mu**2+6*L-1)*np.cos(2*tau))/mu-64*np.sin(2*tau)-(4*(8*L+9))/mu+((L-4)*L)/mu**3)*tau**2+(1/(4*mu**3))*(2*a**2*cos2theta*(1-8*mu*np.sin(2*tau))*mu**3+6*(4*mu**2+2*a*m*mu+L-1)*mu+2*(2*L+2*mu*(a*m+5*mu)-1)*np.cos(2*tau)*mu+(-8*(a**2-13)*mu**4-16*a*m*mu**3-4*(L+1)*mu**2+(L-1)*L)*np.sin(2*tau))*tau+(1/(16*mu**3))*(8*(a**2-16)*mu**4+4*a**2*cos2theta*np.sin(tau)*(-2*mu*np.cos(tau)-(L-8*mu**2)*np.sin(tau))*mu**2+60*mu**2-4*(22*mu**2+8*a*m*mu+5*L-4)*np.sin(2*tau)*mu-3456*a**2*m**2-5*L**2+8*L+4608*a**2*m**2*np.cos(tau)-(-128*mu**4+60*mu**2+(8-5*L)*L+8*a**2*(mu**4+144*m**2))*np.cos(2*tau))
			F4 = -((mu*tau**6)/9)-(4*tau**5)/3+1/96*(-120*mu*cos2theta*a**2-120*(2*m+a*mu)*a+3760*mu+1200*mu*np.cos(2*tau)+(400*L+52)/mu+(3*L*(5*L-6))/mu**3)*tau**4+((-424*mu**2+38*a*m*mu+4*(mu*cos2theta*a**2+55*mu*np.cos(2*tau)+(299*mu**2+35*L-10)*np.sin(2*tau))*mu-18*L-21)*tau**3)/(12*mu**2)+(1/(32*mu**3))*(-8*a**2*cos2theta*((3*a**2+70)*mu**2-45*np.cos(2*tau)*mu**2+5*L)*mu**2+(24*(7*a**2-240)*mu**4+400*a*m*mu**3+4*(13-140*L)*mu**2+15*(2-3*L)*L)*np.cos(2*tau)+2*(-4*(3*a**4+6*a**2-836)*mu**4-8*a*(3*a**2+50)*m*mu**3+4*(-2*L*a**2+60*L+51)*mu**2-20*a*m*L*mu+2*(236*mu**2+10*a*m*mu+30*L-5)*np.sin(2*tau)*mu+768*a**2*m**2+(18-5*L)*L))*tau**2+(1/(32*mu**3))*(12288*a**2*np.sin(tau)*m**2-8*mu*(72*mu**2+20*a*m*mu+12*L-11)+4*mu*(24*L+2*mu*(-6*mu*a**2+7*m*a+90*mu)-7)*np.cos(2*tau)-(928*mu**4+20*(23-4*L)*mu**2-40*a*m*(10*mu**2+L)*mu+11*(6-5*L)*L+8*a**2*(3*mu**4+L*mu**2+960*m**2))*np.sin(2*tau)+8*a**2*mu**2*cos2theta*(5*(5*mu**2+L)*np.sin(2*tau)-2*mu))*tau+(1/(32*mu**3))*np.sin(tau)*(4*mu*(12*(a**2-3)*mu**2+4*a**2*cos2theta*mu**2+26*a*m*mu-15)*np.cos(tau)+(8*a**2*((3*a**2-25)*mu**2-5*L)*cos2theta*mu**2+11*(6-5*L)*L+4*(2*(3*a**4-9*a**2+116)*mu**4+4*a*(3*a**2-25)*m*mu**3+(8*L*a**2-20*L+115)*mu**2-10*a*m*L*mu+384*a**2*m**2))*np.sin(tau))
	elif (m==0):
		if not cumulative:
			F0 = 2*mu*tau*(np.cos(tau)**2)-2*mu*np.sin(tau)*np.cos(tau)
			F1 = 4*mu*np.sin(2*tau)*tau**2-((8*mu**2+2*np.sin(2*tau)*mu+L+L*np.cos(2*tau))*tau)/(2*mu)+((4*mu**2+L)*np.cos(tau)*np.sin(tau))/mu
			F2 = -8*mu*np.cos(2*tau)*tau**3+(3*np.cos(2*tau)+(-((3*L)/mu)-20*mu)*np.sin(2*tau)-1)*tau**2+(-3*mu*cos2theta*(np.cos(tau)**2)*a**2-(mu*a**2)/2+16*mu-(((a**2+8)*mu**2+6*L)*np.cos(2*tau))/(2*mu)+6*np.sin(2*tau))*tau+(np.sin(tau)*(((a**2-12)*mu**2+3*a**2*cos2theta*mu**2+3*L)*np.cos(tau)-2*mu*np.sin(tau)))/mu
			F3 = -(32/3)*mu*np.sin(2*tau)*tau**4+(4*(52*mu**2+6*L-1)*np.cos(2*tau)-4)*(tau**3)/(3*mu)+(mu*(18*mu**2+L+1)+(mu-22*mu**3)*np.cos(2*tau)+(-4*(a**2-22)*mu**4-8*(a**2)*cos2theta*mu**4+4*L*mu**2+0.5*(L-1)*L)*np.sin(2*tau))*(tau**2)/mu**3+(1/(2*mu**3))*(8*(a**2-16)*mu**4+a**2*cos2theta*(16*mu**2+2*np.sin(2*tau)*mu+L+L*np.cos(2*tau))*mu**2-28*mu**2-2*(36*mu**2+L+1)*np.sin(2*tau)*mu+(L-3)*L+(48*mu**4+8*(L-3)*mu**2+L*(2*L-3))*np.cos(2*tau))*tau+(4*mu*(12*(mu**2)+L)*(np.sin(tau)**2))/(4*mu**3)-(8*(a**2-10)*mu**4+4*(2*L-13)*mu**2+2*a**2*(8*mu**2+L)*cos2theta*mu**2+3*(L-2)*L)*np.sin(2*tau)*(1.0/(4*mu**3))
			F4 = 2/3*mu*(15*np.cos(2*tau)-1)*tau**5+(2*np.sin(tau)*((334*mu**2+35*L-10)*np.cos(tau)-20*mu*np.sin(tau))*tau**4)/(3*mu)+(1/(24*mu**3))*(40*(74-3*a**2)*mu**4+120*a**2*cos2theta*(3*np.cos(2*tau)-1)*mu**4+20*(16*L+5)*mu**2+12*(5-64*mu**2)*np.sin(2*tau)*mu+3*L*(5*L-6)-(8*(934-21*a**2)*mu**4+4*(200*L+7)*mu**2+15*L*(3*L-2))*np.cos(2*tau))*tau**3+(1/(2*mu**3))*(a**2*cos2theta*(-10*np.cos(2*tau)*mu+2*mu+5*(8*mu**2+L)*np.sin(2*tau))*mu**2-2*(128*mu**2+8*L+3)*mu+4*(-(a**2-92)*mu**2+4*L+1)*np.cos(2*tau)*mu-(184*mu**4+((a**2-10)*L+50)*mu**2+(7-5*L)*L)*np.sin(2*tau))*tau**2+(1/(8*mu**3))*(-12*(a**4+6*a**2-124)*mu**4+4*(87-5*(a**2-2)*L)*mu**2-4*a**2*cos2theta*((3*a**2+50)*mu**2+5*L+((3*a**2-50)*mu**2-5*L)*np.cos(2*tau))*mu**2+8*((6*a**2+4)*mu**2+L+1)*np.sin(2*tau)*mu+(26-15*L)*L+(-12*(a**4-14*a**2+124)*mu**4-4*((a**2+10)*L+87)*mu**2+L*(15*L-26))*np.cos(2*tau))*tau+(np.sin(tau)*(3*mu*((a**2-4)*mu**2+a**2*cos2theta*mu**2+L)*np.cos(tau)*a**2+(2*(a**2-32)*mu**2+4*a**2*cos2theta*mu**2-2*L-1)*np.sin(tau)))/mu**2
		elif cumulative:
			F0 = (mu*tau**2)/2+mu*np.cos(tau)*np.sin(tau)*tau-3/2*mu*(np.sin(tau)**2)
			F1 = (-(L/(4*mu))-2*mu-2*mu*np.cos(2*tau))*tau**2+(1/2*np.cos(2*tau)-((L-8*mu**2)*np.sin(2*tau))/(4*mu))*tau+(np.sin(tau)*(3*L*np.sin(tau)-2*mu*np.cos(tau)))/(4*mu)
			F2 = (-4*mu*np.sin(2*tau)-1/3)*tau**3+1/4*(-mu*a**2-3*mu*cos2theta*a**2+32*mu+((6*L)/mu+16*mu)*np.cos(2*tau)+6*np.sin(2*tau))*tau**2+1/8*(-6*mu*np.sin(2*tau)*cos2theta*a**2-2*mu*np.sin(2*tau)*a**2-12*np.cos(2*tau)-48*mu*np.sin(2*tau)-(24*L*np.sin(2*tau))/mu-8)*tau+(np.sin(tau)*(20*mu*np.cos(tau)+6*(a**2*mu**2+3*a**2*cos2theta*mu**2+6*L)*np.sin(tau)))/(8*mu)
			F3 = (16/3*mu*np.cos(2*tau)-1/(3*mu))*tau**4+((18*mu**2+2*(36*mu**2+6*L-1)*np.sin(2*tau)*mu+L+1)*tau**3)/(3*mu**2)+(1/(4*mu**3))*(8*(a**2-16)*mu**4+a**2*cos2theta*(16*np.cos(2*tau)*mu**2+16*mu**2+L)*mu**2-28*mu**2+2*(1-22*mu**2)*np.sin(2*tau)*mu+(L-3)*L+(8*(a**2-4)*mu**4+4*(4*L-1)*mu**2-(L-1)*L)*np.cos(2*tau))*tau**2+(1/(4*mu**3))*(2*mu*(12*mu**2+L+(-a**2*cos2theta*mu**2+14*mu**2+L+2)*np.cos(2*tau))+(-8*(a**2-10)*mu**4-4*(2*L+5)*mu**2+a**2*(L-16*mu**2)*cos2theta*mu**2+L*(3*L-4))*np.sin(2*tau))*tau+(np.sin(tau)*(2*mu*(a**2*mu**2*cos2theta-2*(13*mu**2+L+1))*np.cos(tau)+(-3*a**2*L*cos2theta*mu**2+72*mu**2+2*(5-3*L)*L)*np.sin(tau)))/(4*mu**3)
			F4 = -((mu*tau**6)/9)+(5*mu*np.sin(2*tau)-4/3)*tau**5+(1/(96*mu**3))*(40*(74-3*a**2)*mu**4+20*(16*L+5)*mu**2+8*(-15*a**2*cos2theta*mu**2+40*np.sin(2*tau)*mu+(-518*mu**2-70*L+20)*np.cos(2*tau))*mu**2+3*L*(5*L-6))*tau**4+(1/(24*mu**3))*(4*a**2*cos2theta*(45*mu*np.sin(2*tau)+2)*mu**3-8*(128*mu**2+8*L+3)*mu+2*((272*mu**2-15)*np.cos(2*tau)+mu*((42*a**2-832)*mu**2-60*L-47)*np.sin(2*tau))*mu+15*(2-3*L)*L*np.cos(tau)*np.sin(tau))*tau**3+(1/(32*mu**3))*(-24*(a**4+6*a**2-124)*mu**4+8*(87-5*(a**2-2)*L)*mu**2-8*a**2*cos2theta*((3*a**2+50)*mu**2+10*np.sin(2*tau)*mu+5*L+5*(L-mu**2)*np.cos(2*tau))*mu**2+4*(-8*(a**2-58)*mu**2+32*L+23)*np.sin(2*tau)*mu+2*(26-15*L)*L+(8*(21*a**2-232)*mu**4+4*(2*(a**2-40)*L+53)*mu**2+(86-85*L)*L)*np.cos(2*tau))*tau**2+(1/(32*mu**3))*(8*a**2*cos2theta*(-10*np.cos(2*tau)*mu+8*mu+(10*L-3*(a**2-15)*mu**2)*np.sin(2*tau))*mu**2+16*(2*(a**2-32)*mu**2-2*L-1)*mu+4*(-32*(a**2-14)*mu**2+28*L+19)*np.cos(2*tau)*mu+(-8*(3*(a**2-7)*a**2+140)*mu**4-4*(4*(a**2-15)*L+227)*mu**2+23*L*(5*L-6))*np.sin(2*tau))*tau+(1/(32*mu**3))*np.sin(tau)*(4*mu*(24*(a**2-8)*mu**2+4*a**2*cos2theta*mu**2-5*(4*L+3))*np.cos(tau)+(8*(9*(a**2-5)*a**2+140)*mu**4+4*(16*L*a**2-60*L+227)*mu**2+8*a**2*(9*(a**2-5)*mu**2-10*L)*cos2theta*mu**2+23*(6-5*L)*L)*np.sin(tau))
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

#add_data_dir(101, 1, 1, "0.7", "0.4", 75, 63)
#add_data_dir(101, 1, 1, "0.7", "0.4", 123, 123)
add_data_dir(103, 0, 0, "0.7", "0.4", 32, 32, "_theta_max0.98")
#add_data_dir(102, 2, 2, "0.7", "0.4")
#add_data_dir(103, 0, 0, "0.7", "0.4")
#add_data_dir(104, 1, -1, "0.7", "0.4")
#add_data_dir(105, 0, 0, "0.99", "0.4")
#add_data_dir(106, 1, 1, "0.99", "0.4")
#add_data_dir(107, 4, 4, "0.7", "0.4")
#add_data_dir(108, 2, 2, "0.7", "0.8")
#add_data_dir(109, 8, 8, "0.7", "0.4")
#add_data_dir(110, 1, 1, "0.7", "0.05")
#add_data_dir(111, 1, 1, "0.7", "1")

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"

output_dir = "data/flux_data"

half_box = True

KS_or_cartesian_r=True
phi0 = 0.1
r_max = 450
average_time = False
av_n = 1
cumulative=True
plot_mass=True

def load_flux_data():
	# load data from csv files
	data = {}
	ang_flux_data = {}
	for dd in data_dirs:
		file_name = home_path + output_dir + "/" + dd.name + "_J_rKS_linear_n000000_nphi{:d}_ntheta{:d}{:s}.dat".format(dd.nphi, dd.ntheta, dd.suffix)
		data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		#file_name = home_path + output_dir + "/" + dd.name + "_J_azimuth_rKS_linear_n000000.dat"
		#ang_flux_data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		print("loaded flux data for " + dd.name)
	return data 	

def load_mass_data():
        # load data from csv files
        data = {}
        print(data_dirs)
        for dd in data_dirs:
                file_name = home_path + "data/mass_data" + "/" + "{:s}_mass_in_r={:d}.dat".format(dd.name, r_max)
                data_line = np.genfromtxt(file_name, skip_header=1)
                data[dd.num] = data_line
                print("loaded mass data for " + file_name)
        return data

def plot_graph():
	flux_data = load_flux_data()
	if plot_mass:
		mass_data = load_mass_data()
	colours = ['r', 'b', 'g', 'm', 'y', 'c']
	colours2 = ['k', 'm', 'c']
	i = 0
	fig, ax1 = plt.subplots()
	#ax2 = ax1.twinx()	
	for dd in data_dirs:
		flux_line_data = flux_data[dd.num]
		mu = float(dd.mu)
		tflux = flux_line_data[1:,0]
		#r_min = line_data[0,1]
		r_max = flux_line_data[0,2]
		E0 = 0.5*(4*np.pi*(r_max**3)/3)*(phi0*mu)**2
		inner_mass_flux = -flux_line_data[1:,1]*(4*np.pi)/E0
		outer_mass_flux = -flux_line_data[1:,2]*(4*np.pi)/E0
		if average_time:
			tflux = time_average(tflux, av_n)
			inner_mass_flux = time_average(inner_mass_flux, av_n)
			outer_mass_flux = time_average(outer_mass_flux, av_n)
		if cumulative:
			dt = tflux[2] - tflux[1]
			inner_mass_flux = np.cumsum(inner_mass_flux)*dt
			outer_mass_flux = np.cumsum(outer_mass_flux)*dt
			analytic_outer_flux = analytic_flux(tflux, r_max, dd.l, dd.m, dd.a, mu, True)*(4*np.pi)*phi0**2/E0
		elif not cumulative:
			analytic_outer_flux = analytic_flux(tflux, r_max, dd.l, dd.m, dd.a, mu, False)*(4*np.pi)*phi0**2/E0
		net_flux = outer_mass_flux - inner_mass_flux
		#label_ = "$\\mu$={:.2f}".format(mu)
		label_ = "$l$={:d} $m$={:d}".format(dd.l, dd.m)
		ax1.plot(tflux,inner_mass_flux,colours[i]+"--", label="flux into BH " + label_)
		ax1.plot(tflux,outer_mass_flux,colours[i]+"-.", label="flux into r={:.1f} ".format(r_max)+label_)
		ax1.plot(tflux,analytic_outer_flux,colours2[i]+"-.", label="flux into r={:.1f} ".format(r_max)+label_)
		ax1.plot(tflux,net_flux,colours[i]+"-", label="net flux " + label_)
		#
		if plot_mass:
			mass_line_data = mass_data[dd.num]
			delta_mass = mass_line_data[1:,1] - mass_line_data[0,1]
			tmass = mass_line_data[1:,0]
			ax1.plot(tmass,delta_mass/E0,colours[i+1]+"-", label="change in mass $r_+<r<$"+str(r_max)+" "+label_)
		i = i + 1
	ax1.set_xlabel("$t$")
	#ax1.set_xlim((0, 300))
	#ax1.set_ylim((-0.0005, 0.0015))
	dd0 = data_dirs[0]
	if cumulative:
		ax1.set_ylabel("cumulative flux / $E_0$")
		plt.title("Cumulative mass flux, $M=1$, $a=0.7$, $\\mu=0.4$")
		save_path = home_path + "plots/mass_flux_Kerr_Schild_cumulative_nphi{:d}_ntheta{:d}{:s}.png".format(dd.nphi, dd.ntheta, dd.suffix)
	else:
		ax1.set_ylabel("flux / $E_0$")
		plt.title("Mass flux, $M=1$, $\\mu=0.4$ $n_{\\phi}=$"+str(dd.nphi)+" $n_{\\theta}=$"+str(dd.ntheta))
		save_path = home_path + "plots/mass_flux_Kerr_Schild_nphi{:d}_ntheta{:d}{:s}.png".format(dd.nphi, dd.ntheta, dd.suffix)
	ax1.legend(loc='upper left', fontsize=8)
	plt.tight_layout()
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()

plot_graph()

