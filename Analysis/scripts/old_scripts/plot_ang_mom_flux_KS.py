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

# appropriate \int Ylm Ylm*** np.cos(2 theta) dtheta dphi factor for 0 <= l <= 10
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
	L = l*(l+1)*(mu**2)
	tau = mu*t
	""" #
	Integrating factor of 
		\int Ylm Ylm^* np.cos(2 theta) dtheta dphi
	assuming the spherical harmonics are normalised so that 
		\int Ylm Ylm^* np.cos(2 theta) dtheta dphi = 1 
	# """
	if not cumulative:
		F0=r*mu**2+tau*mu+1/2*(a*m-4*mu+4*mu*np.cos(2*tau)-np.sin(2*tau))*mu
		F1=1/2*mu*tau*(-L+8*np.cos(2*tau)+16*mu*np.sin(2*tau)-12)+1/4*(2*(L+16)*mu**2-8*a*m*mu+(L+12)*np.sin(2*tau)*mu-2*((L+16)*mu**2-1)*np.cos(2*tau)-2)
		F2=(4*mu*(3*np.sin(2*tau)-4*mu*np.cos(2*tau))-1)*tau**2+1/2*(-mu*a**2-4*m*a+5*(L+16)*mu+6*np.sin(2*tau)+mu*(-3*cos2theta*a**2-2*(3*L+38)*np.cos(2*tau)-8*(L+14)*mu*np.sin(2*tau)))*tau+1/2*np.sin(tau)*((3*mu*cos2theta*a**2+6*m*a+(a**2+L-36)*mu)*np.cos(tau)+4*mu*(mu*a**2+mu*cos2theta*a**2+2*m*a-2*(L+16)*mu)*np.sin(tau)+6*np.sin(tau))
		F3=(-(64/3)*mu*(np.cos(2*tau)+mu*np.sin(2*tau))-4/(3*mu))*tau**3+(-((2*a*m)/mu)+(3*L)/2+2*((6*L+80)*mu**2-9)*np.cos(2*tau)+(2/mu-4*(3*L+40)*mu)*np.sin(2*tau)+1/mu**2+32)*tau**2+(1/(4*mu**2))*(2*a**2*cos2theta*(L-16*np.cos(2*tau)-16*mu*np.sin(2*tau)+28)*mu**3+((32*a**2+(L-56)*L-992)*mu**2+64*a*m*mu-4*(L+9))*mu+2*((-8*a**2+L*(L+36)+488)*mu**2-12*a*m*mu-L-10)*np.cos(2*tau)*mu+2*((-16*a**2+L*(L+52)+608)*mu**4-16*a*m*mu**3-5*(L+16)*mu**2-4*a*m*mu+2)*np.sin(2*tau))*tau+(1/(8*mu**2))*(-4*a**2*cos2theta*np.sin(tau)*((L+16)*mu*np.cos(tau)+((L+32)*mu**2-2)*np.sin(tau))*mu**2+(-(24*a**2+L*(3*L+16)-272)*mu**2-72*a*m*mu+6*L+56)*np.sin(2*tau)*mu+2*((32*(L+16)-a**2*(L+32))*mu**4+8*a*(a**2-4)*m*mu**3+7*(L+4)*mu**2+12*a*m*mu-6)+2*(-32*(L+16)*mu**4+a**2*(L+32)*mu**4-7*(L+4)*mu**2+4*a*m*(8*mu**2-3)*mu+6)*np.cos(2*tau))
		F4=-((2*mu*tau**5)/3)+(4/3*((L+13)*mu**2-7)+5*mu*(4*mu*np.cos(2*tau)-5*np.sin(2*tau)))*tau**4+(((-120*a**2+L*(15*L+496)+5744)*mu**2-120*a**2*cos2theta*mu**2-336*a*m*mu+16*(4*(7*L+92)*mu**2-63)*np.sin(2*tau)*mu-18*L+16*((35*L+482)*mu**2-10)*np.cos(2*tau)+164)*tau**3)/(24*mu)+(1/(16*mu**2))*(8*a**2*cos2theta*(4*(L+21)*mu**2+9*(4*mu*np.cos(2*tau)-5*np.sin(2*tau))*mu+2)*mu**2+((-168*a**2+5*L*(9*L+320)+16688)*mu**2-368*a*m*mu-30*L-292)*np.sin(2*tau)*mu+4*((8*(L+21)*a**2-5*L**2-272*(L+11))*mu**4+8*a*m*(L+34)*mu**3-4*(7*L+177)*mu**2+a*m*(L+62)*mu-29)+4*((72*a**2-L*(9*L+352)-3504)*mu**4+80*a*m*mu**3+4*(9*L+167)*mu**2+10*a*m*mu-5)*np.cos(2*tau))*tau**2-(1/(8*mu**2))*((12*a**4+8*(2*L+27)*a**2+9*(L-48)*L-6864)*mu**3+4*a*m*(7*a**2+7*L+148)*mu**2+4*a**2*cos2theta*(-4*(L+24)*np.sin(2*tau)*mu**2+(3*a**2+7*L+118)*mu-(5*L+102)*np.cos(2*tau)*mu+a*m)*mu**2+2*(4*a**2*m**2-17*L-174)*mu+((4*(L-50)*a**2+L*(3*L+464)+6544)*mu**2-20*a*m*(L+28)*mu+10*(L+14))*np.cos(2*tau)*mu-4*a*m-4*(4*((L+24)*a**2-L*(L+46)-488)*mu**4+4*a*m*(L+32)*mu**3+(6*a**2+11*L+116)*mu**2+4*a*m*mu-3)*np.sin(2*tau))*tau+1/4*(cos2theta*(4*(2*(L+18)*mu**2-3)*(np.sin(tau)**2)+(3*a**2+2*(L+8))*mu*np.sin(2*tau))*a**2+(1/(mu**2))*np.sin(tau)*(2*((3*a**4+(5*L+4)*a**2+(L-4)*(3*L+20))*mu**3+2*a*m*(3*a**2+L+36)*mu**2+2*(a**2*m**2-3*L-26)*mu-a*m)*np.cos(tau)+(mu*(-2*(L*(L+88)+1040)*mu**3-4*(13*L+74)*mu+8*a**2*(2*m**2+(L+18)*mu**2-1)*mu+a*m*(8*(L+20)*mu**2-L-100))+46)*np.sin(tau)))
	elif cumulative:
		F0=tau**2/2+((a*m)/2-2*mu)*tau+r*mu*tau+1/2*(4*mu*np.cos(tau)-np.sin(tau))*np.sin(tau)
		F1=(-(L/4)-3)*tau**2+(-2*a*m+(L*mu)/2+8*mu-4*mu*np.cos(2*tau)+2*np.sin(2*tau)-1/(2*mu))*tau+(np.sin(tau)*((L+4)*mu*np.sin(tau)-2*((L+8)*mu**2-1)*np.cos(tau)))/(4*mu)
		F2=-(tau**3/(3*mu))+(-(3/4)*cos2theta*a**2-a**2/4-(m*a)/mu+(5*L)/4-6*np.cos(2*tau)-8*mu*np.sin(2*tau)+20)*tau**2+((2*(a**2-2*L-32)*mu**2+2*a**2*cos2theta*mu**2+4*a*m*mu-(3*L+26)*np.sin(2*tau)*mu+(4*(L+10)*mu**2-3)*np.cos(2*tau)+3)*tau)/(2*mu)+(np.sin(tau)*((3*mu*cos2theta*a**2+6*m*a+(a**2+7*L+16)*mu)*np.sin(tau)-4*mu*(mu*cos2theta*a**2+2*m*a+(a**2-12)*mu)*np.cos(tau)))/(4*mu)
		F3=-(tau**4/(3*mu**2))+((64*(mu*np.cos(2*tau)-np.sin(2*tau))*mu**3+(3*L+64)*mu**2-4*a*m*mu+2)*tau**3)/(6*mu**3)+(((32*a**2+(L-56)*L-992)*mu**2+64*a*m*mu+2*((L+28)*mu*cos2theta*a**2-36*np.sin(2*tau)+8*(3*L+32)*mu*(np.cos(2*tau)+mu*np.sin(2*tau)))*mu-4*(L+9)-8*np.cos(2*tau))*tau**2)/(8*mu**2)+(1/(4*mu**3))*((32*(L+16)-a**2*(L+32))*mu**4+8*a*(a**2-4)*m*mu**3+7*(L+4)*mu**2+a**2*cos2theta*(-(L+32)*mu**2+16*(mu*np.cos(2*tau)-np.sin(2*tau))*mu+2)*mu**2+12*a*m*mu+((-8*a**2+L*(L+12)+232)*mu**2-12*a*m*mu-L-6)*np.sin(2*tau)*mu+((16*a**2-L*(L+28)-352)*mu**4+16*a*m*mu**3+(5*L+44)*mu**2+4*a*m*mu-2)*np.cos(2*tau)-6)*tau+(1/(8*mu**3))*np.sin(tau)*(2*(((L+16)*a**2+(L-4)*L-160)*mu**4+16*a*m*mu**3-12*(L+6)*mu**2+a**2*((L+16)*mu**2-2)*cos2theta*mu**2-16*a*m*mu+8)*np.cos(tau)-mu*((8*a**2+5*L*(L+8)+192)*mu**2+2*a**2*L*cos2theta*mu**2+48*a*m*mu-8*L-68)*np.sin(tau))
		F4=-(tau**6/9)+(4*((L+13)*mu**2-7)*tau**5)/(15*mu)+(((-120*a**2+L*(15*L+496)+5744)*mu**2+120*(-cos2theta*a**2+10*np.cos(2*tau)+8*mu*np.sin(2*tau))*mu**2-336*a*m*mu-18*L+164)*tau**4)/(96*mu**2)+(1/(12*mu**3))*((8*(L+21)*a**2-5*L**2-272*(L+11))*mu**4+8*a*m*(L+34)*mu**3-4*(7*L+177)*mu**2+a*m*(L+62)*mu+4*(mu*(2*(L+21)*mu**2+1)*cos2theta*a**2-7*mu*(4*(L+11)*mu**2-9)*np.cos(2*tau)+((35*L+407)*mu**2-10)*np.sin(2*tau))*mu-29)*tau**3+(1/(32*mu**3))*(-2*(12*a**4+8*(2*L+27)*a**2+9*(L-48)*L-6864)*mu**3-8*a*m*(7*a**2+7*L+148)*mu**2-8*a**2*cos2theta*(a*m+(3*a**2+7*L+118)*mu-9*mu*(5*np.cos(2*tau)+4*mu*np.sin(2*tau)))*mu**2+4*(-4*a**2*m**2+17*L+174)*mu+((168*a**2-5*L*(9*L+208)-10176)*mu**2+368*a*m*mu+6*(5*L+22))*np.cos(2*tau)*mu+8*a*m+4*((72*a**2-3*L*(3*L+80)-2272)*mu**4+80*a*m*mu**3+4*(9*L+104)*mu**2+10*a*m*mu-5)*np.sin(2*tau))*tau**2+(1/(32*mu**3))*(4*(mu*(-2*(L*(L+88)+1040)*mu**3-4*(13*L+74)*mu+8*a**2*(2*m**2+(L+18)*mu**2-1)*mu+a*m*(8*(L+20)*mu**2-L-100))+np.cos(2*tau)+46)+mu*(-8*mu*cos2theta*(-4*(L+18)*mu**2+4*(L+15)*np.cos(2*tau)*mu**2-(5*L+57)*np.sin(2*tau)*mu+6)*a**2-4*((8*(L+15)*a**2+(L-128)*L-1632)*mu**3+8*a*m*(L+22)*mu**2+2*(6*a**2-7*L-92)*mu-2*a*m)*np.cos(2*tau)+((-8*(L-29)*a**2+L*(39*L+112)-2912)*mu**2+8*a*m*(5*L+94)*mu-50*L-412)*np.sin(2*tau)))*tau+(1/(32*mu**3))*np.sin(tau)*(4*(12*a**2*(1-2*mu**2)*cos2theta*mu**2+((3*L*(L+16)+448)*mu**3+2*(19*L+56)*mu-4*a**2*(4*m**2+6*mu**2-5)*mu+a*m*(16*mu**2+L+98))*mu-47)*np.cos(tau)+((24*a**4+8*(6*L-25)*a**2-3*L*(5*L+16)+2272)*mu**3+8*a**2*(3*a**2-3*L-41)*cos2theta*mu**3+8*a*m*(6*a**2-3*L-22)*mu**2+2*(8*a**2*m**2+L-2)*mu-8*a*m)*np.sin(tau))
	Flux=m*(F0 + F1/r + F2/r**2 + F3/r**3 + F4/r**4)
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

add_data_dir(104, 1, 1, "0.0", "0.4", 64, 64, "_theta_max0.99")

# set up parameters
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
home_path="/home/dc-bamb1/GRChombo/Analysis/"

output_dir = "data/flux_data"

half_box = True

KS_or_cartesian_r=True
phi0 = 0.1
r_min = 5
r_max = 500
average_time = False
av_n = 1
cumulative=True
plot_ang_mom=True

def load_flux_data():
	# load data from csv files
	data = {}
	for dd in data_dirs:
		#file_name = home_path + output_dir + "/" + dd.name + "_J_azimuth_rKS_linear_n000000_{:d}_to_{:d}_nphi{:d}_ntheta{:d}{:s}.dat".format(r_min, r_max, dd.nphi, dd.ntheta, dd.suffix)
		file_name = home_path + output_dir + "/" + dd.name + "_J_azimuth_rKS_linear_n000000_r_plus_to_{:d}_nphi{:d}_ntheta{:d}{:s}.dat".format(r_max, dd.nphi, dd.ntheta, dd.suffix)
		data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		print("loaded flux data for " + file_name)
	return data 	

def load_ang_mom_data():
        # load data from csv files
        data = {}
        print(data_dirs)
        for dd in data_dirs:
                #file_name = home_path + "data/mass_data" + "/" + "{:s}_ang_mom_in_{:d}_to_{:d}.dat".format(dd.name, r_min, r_max)
                file_name = home_path + "data/mass_data" + "/" + "{:s}_ang_mom_in_r_plus_to_{:d}.dat".format(dd.name, r_max)
                data_line = np.genfromtxt(file_name, skip_header=1)
                data[dd.num] = data_line
                print("loaded ang mom data for " + file_name)
        return data

def plot_graph():
	flux_data = load_flux_data()
	if plot_ang_mom:
		ang_mom_data = load_ang_mom_data()
	colours = ['r', 'b', 'g', 'm', 'y', 'c']
	colours2 = ['k', 'm', 'c']
	i = 0
	fig, ax1 = plt.subplots()
	#ax2 = ax1.twinx()	
	for dd in data_dirs:
		flux_line_data = flux_data[dd.num]
		mu = float(dd.mu)
		tflux = flux_line_data[1:,0]
		r_min = flux_line_data[0,1]
		r_max = flux_line_data[0,2]
		E0 = 0.5*(4*np.pi*(r_max**3)/3)*(phi0*mu)**2
		inner_ang_mom_flux = -flux_line_data[1:,1]/E0
		outer_ang_mom_flux = -flux_line_data[1:,2]/E0
		if average_time:
			tflux = time_average(tflux, av_n)
			inner_ang_mom_flux = time_average(inner_ang_mom_flux, av_n)
			outer_ang_mom_flux = time_average(outer_ang_mom_flux, av_n)
		if cumulative:
			dt = tflux[2] - tflux[1]
			inner_ang_mom_flux = np.cumsum(inner_ang_mom_flux)*dt
			outer_ang_mom_flux = np.cumsum(outer_ang_mom_flux)*dt
			analytic_outer_flux = analytic_flux(tflux, r_max, dd.l, dd.m, dd.a, mu, True)*(4*np.pi)*phi0**2/(E0)
		elif not cumulative:
			analytic_outer_flux = analytic_flux(tflux, r_max, dd.l, dd.m, dd.a, mu, False)*(4*np.pi)*phi0**2/(E0)
			pass
		net_flux = outer_ang_mom_flux - inner_ang_mom_flux
		#label_ = "$\\mu$={:.2f}".format(mu)
		label_ = "$l$={:d} $m$={:d}".format(dd.l, dd.m)
		ax1.plot(tflux,inner_ang_mom_flux,colours[i]+"--", label="flux into BH"+label_)# r={:.1f} ".format(r_min)+label_)
		ax1.plot(tflux,outer_ang_mom_flux,colours[i]+"-.", label="flux into r={:.1f} ".format(r_max)+label_)
		ax1.plot(tflux,analytic_outer_flux,colours2[i]+"-.", label="4th order t$\\mu$/r analytic flux into r={:.1f} ".format(r_max)+label_) #+" times 4$\\pi$")
		ax1.plot(tflux,net_flux,colours[i]+":", label="net flux " + label_)
		#ax1.plot(tflux,tflux*(r_max-2)*(mu**2)*(4*np.pi)*phi0**2/(E0),color="0.5",linestyle="dashed",label="$t(r_{max}-2)\\mu^2 4\\pi \\varphi^2_0$")
		#
		if plot_ang_mom:
			ang_mom_line_data = ang_mom_data[dd.num]
			#print(ang_mom_line_data[0:,1])
			delta_ang_mom = ang_mom_line_data[1:,1] - ang_mom_line_data[0,1]
			tang_mom = ang_mom_line_data[1:,0]
			#ax1.plot(tang_mom,delta_ang_mom/E0,colours[i]+"-", label="change in ang mom {:.1f}$<r<${:.1f} ".format(r_min,r_max)+label_)
			ax1.plot(tang_mom,delta_ang_mom/E0,colours[i]+"-", label="change in ang mom $r_+<r<${:.1f} ".format(r_max)+label_)
		i = i + 1
	ax1.set_xlabel("$t$")
	dd0 = data_dirs[0]
	if cumulative:
		ax1.set_ylabel("cumulative flux / $E_0$")
		plt.title("Cumulative ang. mom flux, $M=1$, $a=0.0$, $\\mu=0.05$")
		save_path = home_path + "plots/ang_mom_flux_Kerr_Schild_cumulative_run104_r_plus_to_500.png"
	else:
		ax1.set_ylabel("flux / $E_0$")
		plt.title("Ang. mom flux, $M=1$, $\\mu=0.4$ $n_{\\phi}=$"+str(dd.nphi)+" $n_{\\theta}=$"+str(dd.ntheta))
		save_path = home_path + "plots/ang_mom_flux_Kerr_Schild_nphi{:d}_ntheta{:d}{:s}.png".format(dd.nphi, dd.ntheta, dd.suffix)
	ax1.legend(loc='upper left', fontsize=8)
	plt.tight_layout()
	plt.savefig(save_path)
	print("saved plot as " + str(save_path))
	plt.clf()

plot_graph()

