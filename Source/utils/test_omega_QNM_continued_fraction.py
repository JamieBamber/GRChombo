
import numpy as np
import ctypes
import matplotlib.pyplot as plt
import sys
from scipy import special
from math import factorial, nan

compute_omega_CFlib = ctypes.cdll.LoadLibrary('/cosma/home/dp174/dc-bamb1/GRChombo/Source/utils/omega_QNM_continued_fraction.so')
compute_omega_CFlib.F_func.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double]
compute_omega_CFlib.F_func.restype = ctypes.c_double

def f_func(M, mu, a, l, m, s, N, omega_Re, omega_Im):
	result = compute_omega_CFlib.F_func(M, mu, a, l, m, s, N, omega_Re, omega_Im)
	return result

def Cnl(n, l, m, mu, M, a):
        term = 0
        r_plus = M*(1 + np.sqrt(1 - a**2))
        for j in range(0,l,):
                term += j**2*(1-a**2)+(a*m - 2*mu*r_plus)**2
        result = (2**(4*l+2)*factorial(2*l+n+1))/((n+l+1)**(2*l+4)*factorial(n))*(factorial(l)/(factorial(2*l)*factorial(2*l+1)))**2*\
                term
        return result

def omega_estimate(M, mu, n, l, m, a):
        r_plus = M*(1 + np.sqrt(1 - a**2))
        omega = mu*(1-0.5*(mu*M/(n+l+1))**2) + (1j/M)*(a*m-2*mu*r_plus)*(M*mu)**(4*l+5)*Cnl(n,l,m,mu,M,a)
        return omega

mu = 0.1
M = 1
	
print("f_func(M, mu, 0, 1, 1, 0, 1000, 0.98*mu, 0) = ", f_func(M, mu, 0, 1, 1, 0, 1000, 0.98*mu, 0))

### now try covering the complex plane (for real part > 0)
omega_re_max = mu
N_re = 256
N_im = 256
# estimate QNM frequencies using Brito formula
N = 10
omega_est_l0 = []
omega_est_l1 = []
for n in range(0, 10):
        omega_est_l0.append(omega_estimate(M, mu, n, 0, 0, 0))
        omega_est_l1.append(omega_estimate(M, mu, n, 1, 1, 0))
#omega_re_min = np.min(np.real(omega_est_l1))
#omega_im_max = np.max(np.concatenate((np.abs(np.imag(omega_est_l0)),np.abs(np.imag(omega_est_l1)))))
omega_est = omega_estimate(M, mu, 0, 1, 1, 0)
y_min = np.real(omega_est)/mu - 0.005
y_max = np.real(omega_est)/mu + 0.005
x_min = np.abs(np.imag(omega_est))/(mu) - 0.005
x_max = np.abs(np.imag(omega_est))/(mu) + 0.005
y_min = 0.9975
y_max = 1.00
x_min = -0.001
x_max= 0.001
print("y_min = ", y_min)
print("x_max = ", x_max)
x = np.linspace(x_min, x_max,N_im)
y = np.linspace(y_min, y_max, N_re)
y_abs = np.zeros((N_im, N_re))
for i in range(0, N_im):
        for j in range(0, N_re):
                #print("x,y = {:f},{:f}".format(x[i],y[j]))
                try:
                    	f = f_func(M, mu, 0, 1, 1, 0, 1000, mu*y[j], mu*x[i])
                except:
                       	y_abs[j,i] = nan
                else:
                     	y_abs[j,i] = np.log10(f)
ax1 = plt.axes()
fig = plt.gcf()
cm = 'inferno'
rho_max=np.max(y_abs)
rho_min=np.min(y_abs)
#print('max={:.2f} min={:.2f}'.format(phi_max, phi_min))
zmin=0
zmax=1
mesh = ax1.pcolormesh(x,y,y_abs,cmap=cm)
fig.colorbar(mesh, pad=0.01)
ax1.scatter(np.imag(omega_est_l0)/(mu), np.real(omega_est_l0)/mu, s=20, c="g", marker="+", label="QNM estimate l=m=0")
ax1.scatter(np.imag(omega_est_l1)/(mu), np.real(omega_est_l1)/mu, s=20, c="c", marker="x", label="QNM estimate l=m=1")
plt.ylim((y_min, y_max))
plt.xlim((x_min, x_max))
plt.legend(loc="lower right")
plt.xlabel("$\\omega_I/\\mu$")
plt.ylabel("$\\omega_R/\\mu$")
plt.title("f function from continued fraction computation of omega")
save_root_path = "/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/plots/"
save_name = "test_omega_QNM_continued_fraction_f_func_mu{:.2f}.png".format(mu)
plt.savefig(save_root_path + save_name)
print("saved plot as " + save_root_path + save_name)
plt.clf()
