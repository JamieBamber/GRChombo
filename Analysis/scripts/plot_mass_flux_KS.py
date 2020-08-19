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
	if (m!=0):
		if not cumulative:
			F0=r*mu**2+tau*mu-np.sin(tau)*(np.cos(tau)+4*mu*np.sin(tau))*mu
			F1=1/2*np.sin(tau)*((L+12)*mu*np.cos(tau)+2*((L+16)*mu**2-1)*np.sin(tau))+1/2*mu*tau*(-L+8*np.cos(2*tau)+16*mu*np.sin(2*tau)-12)
			F2=(-16*np.cos(2*tau)*mu**2+12*np.sin(2*tau)*mu-1)*tau**2+1/2*(-mu*a**2-3*mu*cos2theta*a**2-6*m*a+5*L*mu+80*mu-2*(3*L+38)*mu*np.cos(2*tau)-8*L*mu**2*np.sin(2*tau)-112*mu**2*np.sin(2*tau)+6*np.sin(2*tau))*tau+1/2*np.sin(tau)*((mu*a**2+3*mu*cos2theta*a**2+6*m*a+(L-36)*mu)*np.cos(tau)+2*(2*a**2*mu**2-4*L*mu**2+2*a**2*cos2theta*mu**2-64*mu**2+4*a*m*mu+3)*np.sin(tau))
			F3=-((4*(16*np.sin(2*tau)*mu**3+16*np.cos(2*tau)*mu**2+1)*tau**3)/(3*mu))+(-((2*a*m)/mu)+(3*L)/2+2*((6*L+80)*mu**2-9)*np.cos(2*tau)+(2/mu-4*(3*L+40)*mu)*np.sin(2*tau)+1/mu**2+32)*tau**2+(8*mu*a**2-8*mu**2*np.sin(2*tau)*a**2-1/2*mu*cos2theta*(-L+16*np.cos(2*tau)+16*mu*np.sin(2*tau)-28)*a**2+22*m*a-8*m*mu*np.sin(2*tau)*a-(2*m*np.sin(2*tau)*a)/mu+(L**2*mu)/4-14*L*mu-248*mu+(-4*mu*a**2-6*m*a+1/2*(L**2+36*L+488)*mu-(L+10)/(2*mu))*np.cos(2*tau)+L**2*(mu**2)*np.cos(tau)*np.sin(tau)-5*L*np.cos(tau)*np.sin(tau)+26*L*mu**2*np.sin(2*tau)+304*mu**2*np.sin(2*tau)+np.sin(2*tau)/mu**2-40*np.sin(2*tau)-L/mu-9/mu)*tau-(1/(4*mu**2))*np.sin(tau)*(mu*(3*L**2*mu**2+2*a**2*(L+16)*cos2theta*mu**2+2*L*(8*mu**2-3)+8*(3*a**2*mu**2-34*mu**2+8*a*m*mu-7))*np.cos(tau)+2*(-32*L*mu**4+a**2*(L+32)*mu**4-512*mu**4-7*L*mu**2+a**2*((L+32)*mu**2-2)*cos2theta*mu**2-28*mu**2+4*a*m*(8*mu**2-3)*mu+6)*np.sin(tau))
			F4=-((2*mu*tau**5)/3)+1/3*(4*(L+13)*mu**2+60*np.cos(2*tau)*mu**2-75*np.sin(2*tau)*mu-28)*tau**4+(-5*mu*a**2-5*mu*cos2theta*a**2-14*m*a+(5*L**2*mu)/8+(62*L*mu)/3+(718*mu)/3+(2*((35*L+482)*mu**2-10)*np.cos(2*tau))/(3*mu)+56/3*L*mu**2*np.sin(2*tau)+736/3*mu**2*np.sin(2*tau)-42*np.sin(2*tau)-(3*L)/(4*mu)+41/(6*mu))*tau**3+1/8*(16*L*mu**2*a**2+336*mu**2*a**2-84*mu*np.sin(2*tau)*a**2+4*cos2theta*(4*L*mu**2+36*np.cos(2*tau)*mu**2+84*mu**2-45*np.sin(2*tau)*mu+2)*a**2+544*m*mu*a+16*m*L*mu*a-184*m*np.sin(2*tau)*a+(108*m*a)/mu-10*L**2*mu**2-544*L*mu**2-5984*mu**2-56*L+(1/(mu**2))*2*(72*a**2*mu**4-(9*L**2+352*L+3504)*mu**4+4*(9*L+167)*mu**2+10*a*m*(8*mu**3+mu)-5)*np.cos(2*tau)+45*L**2*mu*np.cos(tau)*np.sin(tau)+800*L*mu*np.sin(2*tau)+8344*mu*np.sin(2*tau)-(15*L*np.sin(2*tau))/mu-(146*np.sin(2*tau))/mu-58/mu**2-1416)*tau**2+(-((3*mu*a**4)/2)-3*m*a**3-2*L*mu*a**2-27*mu*a**2+2*L*mu**2*np.sin(2*tau)*a**2+48*mu**2*np.sin(2*tau)*a**2+3*np.sin(2*tau)*a**2-1/2*mu*cos2theta*(3*a**2+7*L-(5*L+102)*np.cos(2*tau)-4*(L+24)*mu*np.sin(2*tau)+118)*a**2-82*m*a-(5*m*L*a)/2+64*m*mu*np.sin(2*tau)*a+2*m*L*mu*np.sin(2*tau)*a+(3*m*np.sin(2*tau)*a)/mu-(9*L**2*mu)/8+54*L*mu+858*mu+(-(1/2)*(L-50)*mu*a**2+m*((5*L)/2+66)*a-(3*L**2*mu**2+464*L*mu**2+6544*mu**2+10*L+140)/(8*mu))*np.cos(2*tau)+11*L*np.cos(tau)*np.sin(tau)-(3*np.cos(tau)*np.sin(tau))/mu**2-2*L**2*mu**2*np.sin(2*tau)-92*L*mu**2*np.sin(2*tau)-976*mu**2*np.sin(2*tau)+58*np.sin(2*tau)+(17*L)/(4*mu)+87/(2*mu))*tau+(1/(2*mu**2))*np.sin(tau)*(mu*(3*mu**2*a**4+6*m*mu*a**3+4*mu**2*a**2+(3*a**2+2*(L+8))*mu**2*cos2theta*a**2+32*m*mu*a+3*L**2*mu**2-80*mu**2+L*((5*a**2+8)*mu**2-6)-52)*np.cos(tau)-(L**2*mu**4+88*L*mu**4+1040*mu**4+26*L*mu**2-4*a**2*((L+18)*mu**2-1)*mu**2-2*a**2*(2*(L+18)*mu**2-3)*cos2theta*mu**2+148*mu**2-4*a*m*((L+20)*mu**2-11)*mu-23)*np.sin(tau))
		elif cumulative:
			F0=r*tau*mu**2-2*tau*mu**2+(tau**2*mu)/2+1/2*(4*mu*np.cos(tau)-np.sin(tau))*np.sin(tau)*mu
			F1=-(1/4)*(L+12)*mu*tau**2+1/2*((L+16)*mu**2-8*np.cos(2*tau)*mu**2+4*np.sin(2*tau)*mu-1)*tau+1/4*np.sin(tau)*((L+4)*mu*np.sin(tau)-2*((L+8)*mu**2-1)*np.cos(tau))
			F2=-(tau**3/3)+1/4*(-mu*a**2-3*mu*cos2theta*a**2-6*m*a+5*L*mu+80*mu-24*mu*np.cos(2*tau)-32*mu**2*np.sin(2*tau))*tau**2+1/2*(2*a**2*mu**2-4*L*mu**2+2*a**2*cos2theta*mu**2-64*mu**2+4*a*m*mu-3*L*np.sin(2*tau)*mu-26*np.sin(2*tau)*mu+(4*(L+10)*mu**2-3)*np.cos(2*tau)+3)*tau+1/4*np.sin(tau)*((mu*a**2+3*mu*cos2theta*a**2+6*m*a+7*L*mu+16*mu)*np.sin(tau)-4*mu*(mu*a**2+mu*cos2theta*a**2+2*m*a-12*mu)*np.cos(tau))
			F3=-(tau**4/(3*mu))+((64*np.cos(2*tau)*mu**4-64*np.sin(2*tau)*mu**3+3*L*mu**2+64*mu**2-4*a*m*mu+2)*tau**3)/(6*mu**2)+(4*mu*a**2+1/4*(L+28)*mu*cos2theta*a**2+11*m*a+(L**2*mu)/8-7*L*mu-124*mu+(6*L*mu+64*mu-1/mu)*np.cos(2*tau)+6*L*mu**2*np.sin(2*tau)+64*mu**2*np.sin(2*tau)-9*np.sin(2*tau)-L/(2*mu)-9/(2*mu))*tau**2+1/4*(-L*mu**2*a**2-32*mu**2*a**2-8*mu*np.sin(2*tau)*a**2+cos2theta*(-L*mu**2+16*np.cos(2*tau)*mu**2-32*mu**2-16*np.sin(2*tau)*mu+2)*a**2-32*m*mu*a-12*m*np.sin(2*tau)*a+(12*m*a)/mu+32*L*mu**2+512*mu**2+7*L+(1/(mu**2))*(16*a**2*mu**4-(L**2+28*L+352)*mu**4+(5*L+44)*mu**2+4*a*m*(4*mu**3+mu)-2)*np.cos(2*tau)+L**2*mu*np.sin(2*tau)+12*L*mu*np.sin(2*tau)+232*mu*np.sin(2*tau)-(L*np.sin(2*tau))/mu-(6*np.sin(2*tau))/mu-6/mu**2+28)*tau+(1/(8*mu**2))*np.sin(tau)*(2*(L**2*mu**4-4*L*mu**4+a**2*(L+16)*mu**4-160*mu**4-12*L*mu**2+a**2*((L+16)*mu**2-2)*cos2theta*mu**2-72*mu**2+16*a*m*(mu**2-1)*mu+8)*np.cos(tau)-mu*(8*a**2*mu**2+5*L**2*mu**2+2*a**2*L*cos2theta*mu**2+192*mu**2+40*a*m*mu+8*L*(5*mu**2-1)-68)*np.sin(tau))
			F4=-((mu*tau**6)/9)+4/15*((L+13)*mu**2-7)*tau**5+1/96*(-120*mu*a**2-120*mu*cos2theta*a**2-336*m*a+15*L**2*mu+496*L*mu+5744*mu+1200*mu*np.cos(2*tau)+960*mu**2*np.sin(2*tau)-(18*L)/mu+164/mu)*tau**4+(1/(12*mu**2))*(168*a**2*mu**4-5*L**2*mu**4+8*a**2*L*mu**4-272*L*mu**4-2992*mu**4+272*a*m*mu**3+8*a*m*L*mu**3+140*L*np.sin(2*tau)*mu**3+1628*np.sin(2*tau)*mu**3-28*L*mu**2+4*a**2*(2*(L+21)*mu**2+1)*cos2theta*mu**2-28*(4*(L+11)*mu**2-9)*np.cos(2*tau)*mu**2-708*mu**2+54*a*m*mu-40*np.sin(2*tau)*mu-29)*tau**3-(1/(32*mu**2))*(8*a**2*cos2theta*(3*a**2+7*L-45*np.cos(2*tau)-36*mu*np.sin(2*tau)+118)*mu**3+2*(9*L**2*mu**2+2*L*(8*a**2*mu**2-216*mu**2+10*a*m*mu-17)+4*(3*mu**2*a**4+6*m*mu*a**3+54*mu**2*a**2+164*m*mu*a-1716*mu**2-87))*mu+(45*L**2*mu**2+10*L*(104*mu**2-3)-4*(42*a**2*mu**2-2544*mu**2+92*a*m*mu+33))*np.cos(2*tau)*mu-4*(72*a**2*mu**4-(9*L**2+240*L+2272)*mu**4+4*(9*L+104)*mu**2+10*a*m*(8*mu**3+mu)-5)*np.sin(2*tau))*tau**2+1/16*(16*L*mu**2*a**2+288*mu**2*a**2-4*L*mu*np.sin(2*tau)*a**2+116*mu*np.sin(2*tau)*a**2-4*cos2theta*(-4*L*mu**2+4*(L+15)*np.cos(2*tau)*mu**2-72*mu**2-(5*L+57)*np.sin(2*tau)*mu+6)*a**2-16*a**2+320*m*mu*a+16*m*L*mu*a+344*m*np.sin(2*tau)*a+20*m*L*np.sin(2*tau)*a-(176*m*a)/mu-4*L**2*mu**2-352*L*mu**2-4160*mu**2-104*L-(1/(mu**2))*2*((L**2-128*L-1632)*mu**4-2*(7*L+92)*mu**2+4*a**2*(2*(L+15)*mu**2+3)*mu**2+2*a*m*(4*(L+22)*mu**2+1)*mu-1)*np.cos(2*tau)+39*L**2*mu*np.cos(tau)*np.sin(tau)+56*L*mu*np.sin(2*tau)-1456*mu*np.sin(2*tau)-(25*L*np.sin(2*tau))/mu-(206*np.sin(2*tau))/mu+92/mu**2-592)*tau+(1/(32*mu**2))*np.sin(tau)*(4*(3*L**2*mu**4+48*L*mu**4+448*mu**4+38*L*mu**2-4*a**2*(6*mu**2-5)*mu**2-12*a**2*(2*mu**2-1)*cos2theta*mu**2+112*mu**2+2*a*m*(8*mu**2+45)*mu-47)*np.cos(tau)-mu*(15*L**2*mu**2-8*a**2*(3*a**2-3*L-41)*cos2theta*mu**2+L*(-48*a**2*mu**2+48*mu**2+40*a*m*mu-2)+4*(-6*mu**2*a**4-12*m*mu*a**3+50*mu**2*a**2+108*m*mu*a-568*mu**2+1))*np.sin(tau))
	elif (m==0):
		if not cumulative:
			F0=2*r*mu**2*(np.sin(tau)**2)-8*mu**2*(np.sin(tau)**2)+2*mu*tau*(np.sin(tau)-4*mu*np.cos(tau))*np.sin(tau)
			F1=4*mu*(2*mu*np.cos(2*tau)-np.sin(2*tau))*tau**2+np.sin(tau)*(2*((L+28)*mu**2+1)*np.cos(tau)-(L+16)*mu*np.sin(tau))*tau+2*((L+16)*mu**2-1)*(np.sin(tau)**2)
			F2=8/3*mu*(3*np.cos(2*tau)+4*mu*np.sin(2*tau))*tau**3+(-(4*(L+20)*mu**2+3)*np.cos(2*tau)+3*(L+16)*mu*np.sin(2*tau)-1)*tau**2+np.sin(tau)*(4*(a**2*mu**2-5*L*mu**2+a**2*cos2theta*mu**2-76*mu**2+2*a*m*mu-1)*np.cos(tau)-(mu*a**2+3*mu*cos2theta*a**2+6*m*a-8*(L+15)*mu)*np.sin(tau))*tau+(1/mu)*8*np.cos(tau/2)*(np.sin(tau/2)**2)*(2*a**2*cos2theta*np.cos(tau/2)*mu**3+2*((mu**2-8*m**2)*a**2+2*m*mu*a-2*(L+16)*mu**2+2)*np.cos(tau/2)*mu+a**2*(12*m**2*np.sin(tau/2)))
			F3=-(32/3)*mu*(mu*np.cos(2*tau)-np.sin(2*tau))*tau**4-(1/(3*mu))*4*((6*(L+16)*mu**2-1)*np.cos(2*tau)+mu*(2*(3*L+52)*mu**2-1)*np.sin(2*tau)+1)*tau**3+(1/(2*mu**2))*(3*L*mu**2+80*mu**2-4*a*m*mu+(8*a**2*mu**2-L**2*mu**2-68*L*mu**2+16*a**2*cos2theta*mu**2-864*mu**2+36*a*m*mu+L+6)*np.sin(2*tau)*mu-(16*a**2*mu**4-L**2*mu**4-88*L*mu**4+16*a**2*cos2theta*mu**4-1104*mu**4+L*mu**2+24*mu**2+4*a*m*(8*mu**2-1)*mu+2)*np.cos(2*tau)+2)*tau**2+(L*mu*cos2theta*(np.sin(tau)**2)*a**2+36*mu*cos2theta*(np.sin(tau)**2)*a**2+10*mu*a**2+48*m**2*np.sin(2*tau)*a**2-28*mu**2*np.sin(2*tau)*a**2+20*m*a-40*m*mu*np.sin(2*tau)*a-(6*m*np.sin(2*tau)*a)/mu-26*L*mu-400*mu+(1/(2*mu))*(4*(24*m**2-5*mu**2)*a**2-40*m*mu*a+52*L*mu**2+800*mu**2+L+6)*np.cos(2*tau)-(1/mu)*np.cos(tau)*(48*a**2*m**2+mu*(((L+56)*mu**2+2)*cos2theta*a**2+L*(a**2*mu**2+7))*np.sin(tau))+3/4*L**2*mu**2*np.sin(2*tau)+58*L*mu**2*np.sin(2*tau)+748*mu**2*np.sin(2*tau)+(3*np.sin(2*tau))/mu**2-19*np.sin(2*tau)-L/(2*mu)-3/mu)*tau-(1/(mu**2))*4*np.cos(tau/2)*(np.sin(tau/2)**2)*(96*a**2*mu*np.sin(tau/2)*m**2+(-32*(L+16)*mu**4-2*(3*L+5)*mu**2+a**2*((L+32)*mu**2-2)*cos2theta*mu**2+4*a*m*(8*mu**2-3)*mu+a**2*((L+32)*mu**4-96*m**2*mu**2)+6)*np.cos(tau/2))
			#F4=-(2/3)*mu*(15*np.cos(2*tau)+12*mu*np.sin(2*tau)+1)*tau**5+(1/(3*mu))*(4*mu*((L+14)*mu**2-7)+4*mu*((7*L+114)*mu**2-7)*np.cos(2*tau)+(10-(35*L+564)*mu**2)*np.sin(2*tau))*tau**4+(-5*mu*a**2-12*mu**2*np.sin(2*tau)*a**2-mu*cos2theta*(15*np.cos(2*tau)+12*mu*np.sin(2*tau)+5)*a**2-14*m*a-24*m*mu*np.sin(2*tau)*a+(5*m*np.sin(2*tau)*a)/mu+(5*L**2*mu)/8+24*L*mu+286*mu+(-7*mu*a**2-34*m*a+((15*L**2)/8+96*L+1082)*mu+(-((5*L)/4)-77/6)/mu)*np.cos(2*tau)+3*L**2*mu**2*np.cos(tau)*np.sin(tau)-(5*np.cos(tau)*np.sin(tau))/mu**2+256/3*L*mu**2*np.sin(2*tau)+2840/3*mu**2*np.sin(2*tau)-L*np.sin(2*tau)-58*np.sin(2*tau)-(3*L)/(4*mu)+29/(6*mu))*tau**3+(2*L*mu**2*a**2+48*mu**2*a**2+L*mu*np.cos(tau)*np.sin(tau)*a**2-(48*m**2*np.sin(tau)*a**2)/mu-33*mu*np.sin(2*tau)*a**2+(80*m**2*np.sin(2*tau)*a**2)/mu+1/2*cos2theta*(4*L*mu**2+96*mu**2-(5*L+154)*np.sin(2*tau)*mu+2*(2*(L+36)*mu**2+5)*np.cos(2*tau)+2)*a**2+64*m*mu*a+2*m*L*mu*a-5*m*L*np.cos(tau)*np.sin(tau)*a-118*m*np.sin(2*tau)*a+(18*m*a)/mu-2*L**2*mu**2-92*L*mu**2-976*mu**2-3*L-(1/(2*mu**2))*(2*(5*L**2+220*L+2272)*mu**4-6*(3*L+28)*mu**2-4*a**2*(-32*m**2+(L+36)*mu**2+1)*mu**2-4*a*m*((L+56)*mu**2+5)*mu+5)*np.cos(2*tau)-(19*np.cos(tau)*np.sin(tau))/mu+33/8*L**2*mu*np.sin(2*tau)+197*L*mu*np.sin(2*tau)+2170*mu*np.sin(2*tau)-(5*L*np.sin(2*tau))/(4*mu)-19/(2*mu**2)-152)*tau**2+(-3*mu*cos2theta*(*np.sin(tau)**2)*a**4-(3*mu*a**4)/2-3*m*a**3-7*L*mu*cos2theta*(*np.sin(tau)**2)*a**2-146*mu*cos2theta*(*np.sin(tau)**2)*a**2-1/2*L*mu*a**2-25*mu*a**2+(24*m**2*np.sin(tau)*a**2)/mu**2+(1/mu)*4*np.cos(tau)*(3*(L+28)*m**2+mu*(2*(L+24)*mu**2+1)*cos2theta*np.sin(tau))*a**2-224*m**2*np.sin(2*tau)*a**2+4*L*mu**2*np.sin(2*tau)*a**2+96*mu**2*np.sin(2*tau)*a**2-8*m**2*L*np.sin(2*tau)*a**2-(20*m**2*np.sin(2*tau)*a**2)/mu**2+2*np.sin(2*tau)*a**2-(48*m**2*a**2)/mu-(2*m**2*L*a**2)/mu-74*m*a-(5*m*L*a)/2+128*m*mu*np.sin(2*tau)*a+4*m*L*mu*np.sin(2*tau)*a+(12*m*np.sin(2*tau)*a)/mu+(5*L**2*mu)/8+95*L*mu+1242*mu+(1/(8*mu))*(12*mu**2*a**4+24*m*mu*a**3-4*(4*m**2*(5*L+144)-(L+50)*mu**2)*a**2+4*m*(5*L+148)*mu*a-5*L**2*mu**2-108*(92*mu**2+1)-2*L*(380*mu**2+9))*np.cos(2*tau)-4*L**2*mu**2*np.sin(2*tau)-184*L*mu**2*np.sin(2*tau)-1952*mu**2*np.sin(2*tau)+8*L*np.sin(2*tau)-(6*np.sin(2*tau))/mu**2+56*np.sin(2*tau)+\
#(9*L)/(4*mu)+\
#27/(2*mu))*tau+\
#(1/(mu**2))*4*np.cos(tau/2)*(np.sin(tau/2)**2)*(12*a**2*(2*a**2+L+20)*mu*np.sin(tau/2)*m**2-((L**2+88*L+1040)*mu**4+22*(L+2)*mu**2-4*a*m*((L+20)*mu**2-13)*mu+2*a**2*(-2*(L+18)*mu**4+3*mu**2+8*m**2*((L+16)*mu**2-1))-24)*np.cos(tau/2)+2*a**2*mu**2*(2*(L+18)*mu**2-5)*cos2theta*np.cos(tau/2))
			F4=0
		elif cumulative:
			F0=(mu*tau**2)/2+1/2*mu*(4*np.cos(2*tau)*mu-8*mu-np.sin(2*tau))*tau+1/2*mu*np.sin(tau)*(4*mu*np.cos(tau)+np.sin(tau))+r*(mu**2*tau-mu**2*np.cos(tau)*np.sin(tau))
			F1=1/4*mu*(-L+8*np.cos(2*tau)+16*mu*np.sin(2*tau)-16)*tau**2+1/4*(4*L*mu**2+64*mu**2+(L+8)*np.sin(2*tau)*mu-2*((L+20)*mu**2+1)*np.cos(2*tau)-4)*tau-1/4*np.sin(tau)*(2*((L+12)*mu**2-3)*np.cos(tau)+(L+8)*mu*np.sin(tau))
			F2=(-(16/3)*np.cos(2*tau)*mu**2+4*np.sin(2*tau)*mu-1/3)*tau**3+1/4*(-mu*a**2-3*mu*cos2theta*a**2-6*m*a+8*L*mu+120*mu-6*(L+12)*mu*np.cos(2*tau)-8*L*mu**2*np.sin(2*tau)-128*mu**2*np.sin(2*tau)-6*np.sin(2*tau))*tau**2+1/4*(-64*m**2*a**2+8*mu**2*a**2-mu*cos2theta*(4*np.cos(2*tau)*mu-8*mu-3*np.sin(2*tau))*a**2+mu*np.sin(2*tau)*a**2+16*m*mu*a+6*m*np.sin(2*tau)*a-16*L*mu**2-256*mu**2-2*(2*a**2*mu**2-2*(3*L+44)*mu**2+4*a*m*mu+1)*np.cos(2*tau)-2*L*mu*np.sin(2*tau)-48*mu*np.sin(2*tau)+16)*tau+(1/(8*mu))*(-4*a**2*np.sin(2*tau)*mu**3+4*L*np.sin(2*tau)*mu**3+80*np.sin(2*tau)*mu**3-8*a**2*cos2theta*np.sin(2*tau)*mu**3-a**2*mu**2-6*a**2*cos2theta*(np.sin(tau)**2)*mu**2+2*L*mu**2-8*a*m*np.sin(2*tau)*mu**2+48*mu**2-6*a*m*mu+64*a**2*m**2*np.sin(2*tau)*mu-14*np.sin(2*tau)*mu+144*a**2*m**2+((48*m**2+mu**2)*a**2+6*m*mu*a-2*(L+24)*mu**2)*np.cos(2*tau)+8*a**2*np.cos(tau)*(mu**3*cos2theta*np.sin(tau)-24*m**2))
			F3=-(((16*np.sin(2*tau)*mu**3+16*np.cos(2*tau)*mu**2+1)*tau**4)/(3*mu))+(1/(6*mu**2))*(3*L*mu**2+4*((6*L+88)*mu**2-1)*np.cos(2*tau)*mu**2+80*mu**2-4*a*m*mu-4*((6*L+80)*mu**2-1)*np.sin(2*tau)*mu+2)*tau**3-(1/(4*mu**2))*(16*a**2*np.sin(2*tau)*mu**4-L**2*np.sin(2*tau)*mu**4-64*L*np.sin(2*tau)*mu**4-752*np.sin(2*tau)*mu**4-20*a**2*mu**3+52*L*mu**3+32*a*m*np.sin(2*tau)*mu**3+a**2*cos2theta*(-L+16*np.cos(2*tau)+16*mu*np.sin(2*tau)-36)*mu**3+800*mu**3-40*a*m*mu**2+L*np.sin(2*tau)*mu**2+20*np.sin(2*tau)*mu**2+L*mu+(8*a**2*mu**2-L**2*mu**2-44*L*mu**2-544*mu**2+36*a*m*mu+L+2)*np.cos(2*tau)*mu-4*a*m*np.sin(2*tau)*mu+6*mu+2*np.sin(2*tau))*tau**2+(1/(8*mu**2))*(2*a**2*cos2theta*(((L+40)*mu**2+2)*np.cos(2*tau)-2*((L+32)*mu**2+(L+20)*np.cos(tau)*np.sin(tau)*mu-2))*mu**2+(-(L**2+104*L+1488)*mu**4+12*(L+3)*mu**2+32*a*m*(3*mu**3+mu)+a**2*(2*(L+40)*mu**4-192*m**2*mu**2)-16)*np.cos(2*tau)+4*(-32*a**2*mu**4-a**2*L*mu**4+32*L*mu**4+512*mu**4-32*a*m*mu**3+96*a**2*m**2*mu**2+6*L*mu**2+10*mu**2+12*a*m*mu-(96*a**2*m**2+L**2*mu**2*np.cos(tau))*np.sin(tau)*mu+(6*(8*m**2-mu**2)*a**2-2*m*mu*a+4*L*mu**2+128*mu**2+L+4)*np.sin(2*tau)*mu-6))*tau+(1/(8*mu**2))*(2*a**2*cos2theta*np.sin(tau)*(((L+24)*mu**2-6)*np.cos(tau)+(L+20)*mu*np.sin(tau))*mu**2+(-288*a**2*m**2+4*a*mu*m+12*a**2*mu**2+L**2*mu**2-8*L*mu**2-256*mu**2-2*L+(-12*(8*m**2+mu**2)*a**2-4*m*mu*a-L**2*mu**2+8*L*mu**2+256*mu**2+2*L+8)*np.cos(2*tau)+(((L+24)*mu**3-96*m**2*mu)*a**2+8*m*(2*mu**2-5)*a-2*mu*(140*mu**2+9*L+19))*np.sin(2*tau)-8)*mu+np.cos(tau)*(384*a**2*mu*m**2+(L**2*mu**4-24*L*mu**4+40)*np.sin(tau)))
			F4=-((mu*tau**6)/9)+1/15*(4*L*mu**2+60*np.cos(2*tau)*mu**2+56*mu**2-75*np.sin(2*tau)*mu-28)*tau**5+1/96*(-120*mu*a**2-120*mu*cos2theta*a**2-336*m*a+15*L**2*mu+576*L*mu+6864*mu+(560*L*mu+7824*mu-160/mu)*np.cos(2*tau)+448*L*mu**2*np.sin(2*tau)+6336*mu**2*np.sin(2*tau)-448*np.sin(2*tau)-(18*L)/mu+116/mu)*tau**4+1/48*(32*L*mu**2*a**2+768*mu**2*a**2-168*mu*np.sin(2*tau)*a**2+8*cos2theta*(4*L*mu**2+36*np.cos(2*tau)*mu**2+96*mu**2-45*np.sin(2*tau)*mu+2)*a**2+1024*m*mu*a+32*m*L*mu*a-816*m*np.sin(2*tau)*a+(288*m*a)/mu-32*L**2*mu**2-1472*L*mu**2-15616*mu**2-48*L+(1/(mu**2))*4*(72*a**2*mu**4-(9*L**2+400*L+4096)*mu**4+(6*L+236)*mu**2+6*a*m*(24*mu**2-5)*mu+15)*np.cos(2*tau)+45*L**2*mu*np.sin(2*tau)+1744*L*mu*np.sin(2*tau)+18144*mu*np.sin(2*tau)-(30*L*np.sin(2*tau))/mu-(148*np.sin(2*tau))/mu-152/mu**2-2432)*tau**3+(-((3*mu*a**4)/4)-(3*m*a**3)/2-1/4*L*mu*a**2-(25*mu*a**2)/2+(48*m**2*np.cos(tau)*a**2)/mu-1/4*L*mu*np.cos(2*tau)*a**2+45/4*mu*np.cos(2*tau)*a**2-(40*m**2*np.cos(2*tau)*a**2)/mu-32*m**2*np.sin(2*tau)*a**2+L*mu**2*np.sin(2*tau)*a**2+27*mu**2*np.sin(2*tau)*a**2+np.sin(2*tau)*a**2+1/4*cos2theta*(-(3*a**2+7*L+146)*mu+(5*L+109)*np.cos(2*tau)*mu+2*(2*(L+27)*mu**2+5)*np.sin(2*tau))*a**2-(24*m**2*a**2)/mu-(m**2*L*a**2)/mu-37*m*a-(5*m*L*a)/4+67/2*m*np.cos(2*tau)*a+5/4*m*L*np.cos(2*tau)*a+38*m*mu*np.sin(2*tau)*a+m*L*mu*np.sin(2*tau)*a+(35*m*np.sin(2*tau)*a)/(4*mu)+(5*L**2*mu)/16+(95*L*mu)/2+621*mu-21/32*L**2*mu*np.cos(2*tau)-44*L*mu*np.cos(2*tau)-518*mu*np.cos(2*tau)-(5*L*np.cos(2*tau))/(16*mu)+np.cos(2*tau)/(8*mu)+25*np.cos(tau)*np.sin(tau)-11/8*L**2*mu**2*np.sin(2*tau)-60*L*mu**2*np.sin(2*tau)-624*mu**2*np.sin(2*tau)+15/4*L*np.sin(2*tau)-(25*np.sin(2*tau))/(8*mu**2)+(9*L)/(8*mu)+27/(4*mu))*tau**2+(3/4*mu*np.sin(2*tau)*a**4+3*m*np.cos(tau)*np.sin(tau)*a**3-128*m**2*a**2+2*L*mu**2*a**2+36*mu**2*a**2-8*m**2*L*a**2-(24*m**2*np.cos(tau)*a**2)/mu**2+80*m**2*np.cos(2*tau)*a**2-L*mu**2*np.cos(2*tau)*a**2-21*mu**2*np.cos(2*tau)*a**2+4*m**2*L*np.cos(2*tau)*a**2+(10*m**2*np.cos(2*tau)*a**2)/mu**2+L*mu*np.cos(tau)*np.sin(tau)*a**2+(240*m**2*np.sin(tau)*a**2)/mu+(12*m**2*L*np.sin(tau)*a**2)/mu+5/4*mu*np.sin(2*tau)*a**2-(104*m**2*np.sin(2*tau)*a**2)/mu-(5*m**2*L*np.sin(2*tau)*a**2)/mu+1/4*cos2theta*(8*(L+18)*mu**2+(3*a**2+2*L+37)*np.sin(2*tau)*mu+(6-4*(L+21)*mu**2)*np.cos(2*tau)-20)*a**2+(8*m**2*a**2)/mu**2-3*a**2+40*m*mu*a+2*m*L*mu*a-26*m*mu*np.cos(2*tau)*a-m*L*mu*np.cos(2*tau)*a+(11*m*np.cos(2*tau)*a)/(4*mu)+7*m*np.cos(tau)*np.sin(tau)*a-(26*m*a)/mu-(L**2*mu**2)/2-44*L*mu**2-520*mu**2-11*L+5/8*L**2*mu**2*np.cos(2*tau)+32*L*mu**2*np.cos(2*tau)+352*mu**2*np.cos(2*tau)-1/4*L*np.cos(2*tau)*-np.cos(2*tau)/(8*mu**2)-31/2*np.cos(2*tau)-7*L*mu*np.cos(tau)*np.sin(tau)-(13*L*np.cos(tau)*np.sin(tau))/(8*mu)+11/32*L**2*mu*np.sin(2*tau)-103*mu*np.sin(2*tau)-(55*np.sin(2*tau))/(8*mu)+12/mu**2-22)*tau+1/64*(-48*mu*cos2theta*(np.sin(tau)**2)*a**4-24*mu*a**4+(1152*m**2*a**4)/mu-48*m*a**3-32*L*mu*cos2theta*(np.sin(tau)**2)*a**2-592*mu*cos2theta*(np.sin(tau)**2)*a**2-16*L*mu*a**2-40*mu*a**2+(1536*m**2*np.sin(tau)*a**2)/mu**2-(32*np.cos(tau)*(48*a**2*m**2+mu*(2*(L+15)*mu**2-7)*cos2theta*np.sin(tau))*a**2)/mu+1536*m**2*np.sin(2*tau)*a**2-32*L*mu**2*np.sin(2*tau)*a**2-480*mu**2*np.sin(2*tau)*a**2+128*m**2*L*np.sin(2*tau)*a**2-(576*m**2*np.sin(2*tau)*a**2)/mu**2+96*np.sin(2*tau)*a**2-(512*m**2*a**2)/mu-(32*m**2*L*a**2)/mu-112*m*a-448*m*mu*np.sin(2*tau)*a-32*m*L*mu*np.sin(2*tau)*a+(744*m*np.sin(2*tau)*a)/mu-11*L**2*mu+112*L*mu+3296*mu+(1/mu)*(24*(16*m**2+mu**2)*a**4+48*m*mu*a**3+8*(4*(L+16)*m**2+(2*L+5)*mu**2)*a**2+112*m*mu*a+11*L**2*mu**2-2*L*(56*mu**2+13)-4*(824*mu**2+55))*np.cos(2*tau)-4*L**2*mu**2*np.sin(2*tau)+384*L*mu**2*np.sin(2*tau)+5376*mu**2*np.sin(2*tau)+360*L*np.sin(2*tau)-(380*np.sin(2*tau))/mu**2+1200*np.sin(2*tau)+(26*L)/mu+220/mu)
	Flux=(F0 + F1/r + F2/r**2 + F3/r**3 + F4/r**4)
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

#add_data_dir(101, 1, 1, "0.7", "0.4", 32, 32, "_theta_max0.98")
#add_data_dir(102, 2, 2, "0.7", "0.4", 32, 32, "_theta_max0.98")
#add_data_dir(103, 0, 0, "0.7", "0.4", 32, 32, "_theta_max0.98")
#add_data_dir(104, 4, 4, "0.7", "0.4", 32, 32, "_theta_max0.98")
#add_data_dir(105, 1, -1, "0.7", "0.4", 32, 32, "_theta_max0.98")
#add_data_dir(106, 8, 8, "0.7", "0.4", 32, 32, "_theta_max0.98")
#add_data_dir(107, 1, 1, "0.99", "0.4", 32, 32, "_theta_max0.98")
#add_data_dir(108, 1, 1, "0", "0.4", 32, 32, "_theta_max0.98")
#add_data_dir(109, 2, 2, "0.7", "0.8", 32, 32, "_theta_max0.98")
#add_data_dir(110, 0, 0, "0.0", "0.4", 32, 32, "_theta_max0.98")
add_data_dir(111, 0, 0, "0.0", "0.05", 64, 64, "_theta_max1.0")

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
plot_mass=True

def load_flux_data():
	# load data from csv files
	data = {}
	ang_flux_data = {}
	for dd in data_dirs:
		file_name = home_path + output_dir + "/" + dd.name + "_J_rKS_linear_n000000min_r{:d}_max_r{:d}_nphi{:d}_ntheta{:d}{:s}.dat".format(r_min, r_max, dd.nphi, dd.ntheta, dd.suffix)
		data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		#file_name = home_path + output_dir + "/" + dd.name + "_J_azimuth_rKS_linear_n000000.dat"
		#ang_flux_data[dd.num] = np.genfromtxt(file_name, skip_header=1)
		print("loaded flux data for " + file_name)
	return data 	

def load_mass_data():
        # load data from csv files
        data = {}
        print(data_dirs)
        for dd in data_dirs:
                file_name = home_path + "data/mass_data" + "/" + "{:s}_mass_in_{:d}_to_{:d}.dat".format(dd.name, r_min, r_max)
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
		r_min = flux_line_data[0,1]
		r_max = flux_line_data[0,2]
		E0 = 0.5*(4*np.pi*(r_max**3)/3)*(phi0*mu)**2
		inner_mass_flux = -flux_line_data[1:,1]/E0
		outer_mass_flux = -flux_line_data[1:,2]/E0
		if average_time:
			tflux = time_average(tflux, av_n)
			inner_mass_flux = time_average(inner_mass_flux, av_n)
			outer_mass_flux = time_average(outer_mass_flux, av_n)
		if cumulative:
			dt = tflux[2] - tflux[1]
			inner_mass_flux = np.cumsum(inner_mass_flux)*dt
			outer_mass_flux = np.cumsum(outer_mass_flux)*dt
			analytic_outer_flux = analytic_flux(tflux, r_max, dd.l, dd.m, dd.a, mu, True)*(4*np.pi)*phi0**2/(E0*mu)
		elif not cumulative:
			analytic_outer_flux = analytic_flux(tflux, r_max, dd.l, dd.m, dd.a, mu, False)*(4*np.pi)*phi0**2/(E0)
		net_flux = outer_mass_flux - inner_mass_flux
		#label_ = "$\\mu$={:.2f}".format(mu)
		label_ = "$l$={:d} $m$={:d}".format(dd.l, dd.m)
		ax1.plot(tflux,inner_mass_flux,colours[i]+"--", label="flux into r={:.1f} ".format(r_min)+label_)
		ax1.plot(tflux,outer_mass_flux,colours[i]+"-.", label="flux into r={:.1f} ".format(r_max)+label_)
		ax1.plot(tflux,analytic_outer_flux,colours2[i]+"-.", label="4th order t$\\mu$/r analytic flux into r={:.1f} ".format(r_max)+label_) #+" times 4$\\pi$")
		ax1.plot(tflux,net_flux,colours[i]+":", label="net flux " + label_)
		ax1.plot(tflux,tflux*(r_max-2)*(mu**2)*(4*np.pi)*phi0**2/(E0),color="0.5",linestyle="dashed",label="$t(r_{max}-2)\\mu^2 4\\pi \\varphi^2_0$")
		#
		if plot_mass:
			mass_line_data = mass_data[dd.num]
			#print(mass_line_data[0:,1])
			delta_mass = mass_line_data[1:,1] - mass_line_data[0,1]
			tmass = mass_line_data[1:,0]
			ax1.plot(tmass,delta_mass/E0,colours[i]+"-", label="change in mass {:.1f}$<r<${:.1f} ".format(r_min,r_max)+label_)
		i = i + 1
	ax1.set_xlabel("$t$")
	#ax1.set_xlim((0, 300))
	#ax1.set_ylim((-0.0005, 0.0015))
	dd0 = data_dirs[0]
	if cumulative:
		ax1.set_ylabel("cumulative flux / $E_0$")
		plt.title("Cumulative mass flux, $M=1$, $a=0.0$, $\\mu=0.05$")
		save_path = home_path + "plots/mass_flux_Kerr_Schild_cumulative_test_Schwarzchild.png"
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

