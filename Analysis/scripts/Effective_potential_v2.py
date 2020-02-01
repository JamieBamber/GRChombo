import yt
from yt import derived_field
from yt.units import cm
import numpy as np
import matplotlib.pyplot as plt
import cmath

z_position = 0.001	# s position of slice
r_outer_horizon = 0.25  # R_outer = r_+ / 4 ~= 1 / 4 for an extremal Kerr BH
r_min = r_outer_horizon
r_max = 150
N_bins = 128
a = 0.99		# J / M^2

### derived fields
# weighting field = (cell_volume)^(2/3) / (2*pi * r * dr) 
@derived_field(name = "weighting_field", units = "")
def _weighting_field(field, data):
        return pow(data["cell_volume"].in_base("cgs"),2.0/3) * N_bins / (2*cmath.pi* data["cylindrical_radius"]*(r_max - r_min)*cm)

def get_profile_data(ds):
        slice = ds.r[:,:,z_position]
        slice.set_field_parameter("center", center)
        rp = yt.create_profile(slice, "cylindrical_radius", fields=["rho"], n_bins=N_bins, weight_field="weighting_field", extrema={"cylindrical_radius" : (r_min, r_max)})
        rho = rp["rho"].value
        R = rp.x.value
        return (R, rho, J)

def h(l, m):
	h_ = (l**2 - m**2)*l/(2*(l**2 - 1/4))
	return h_

def Lambda_func(l, m, c=0):
	if c==0:
		return l*(l+1)
	if c!=0:
		h0 = h(l, m)
		h1 = h(l+1, m)
		h2 = h(l+2, m)
		h3 = h(l+3, m)
		h_1 = h(l-1, m)
		h_2 = h(l-2, m)
		f_0 = l*(l+1)
		f_2 = h1 - h0 - 1
		f_4 = - (l+2)*h1*h2/(2*(l+1)*(2*l+3)) + h1**2/(2*(l+1)) +\
		h0*h1/(2*l*(l + 1)) - h0**2/(2*l) + (l-1)*h_1*h0/(2*l*(2*l-1))
		f_6_1 = (h1*h2/(4*(l+1)*(2*l+3)**2))*((l+3)*h3/3 + ((l+2)/(l+1))*\
		((l+2)*h2 - (7*l+10)*h1 + (3*l**2 + 2*l - 3)*h0/l))
		f_6_2 =  h1**3/(2*(l+1)**2) - h0**3/(2*l**2) \
		+(h0*h1/(4*(l**2)*(l+1)**2))*((2*l**2 + 4*l + 3)*h0 - (2*l**2 + 1)*h1 \
		- (l**2 - 1)*(3*l**2 + 4*l - 2)*h_1/(2*l-1)**2)
		f_6_3 = (h_1*h0/4*l**2*(2*l-1)**2)*((l-1)*(7*l-3)*h0 \
		- ((l-1)**2)*h_1 - l*(l-2)*h_2/3)
		f_6 = f_6_1 + f_6_2 + f_6_3
		#
		print("f_0 = {:.6f}".format(f_0), flush=True)
		print("f_2 = {:.6f}".format(f_2), flush=True)
		print("f_4 = {:.6f}".format(f_4), flush=True)
		print("f_6 = {:.6f}".format(f_6), flush=True)
		# 
		result = f_0 + f_2*(c**2) + f_4*(c**4) + f_6*(c**6)
		return result

# R max
R_max = 20

# define effective potential
def V_eff(r, a, l, m, Momega=1, Mmu=1):
	#
	c = a*cmath.sqrt(Momega**2 - Mmu**2)
	Lambda = Lambda_func(l, m, c)
	#
	V = ((Momega)**2)*(1 + (a/r)**2)**2 + 4*Momega*a/r**3 - ((m*a)**2)*(1/r**4)\
	 + (1 - 2/r + (a/r)**2)*((Mmu)**2 + 2/r**3 + ((Momega*a)**2 + Lambda)/r**2 - 2*a**2/r**4)
 	#
	return V

# plot potential
colours = ['r--', 'b--', 'r-', 'b-', 'g-', 'r-.', 'b-.', 'g-.']
almw = [(0, 0, 0, 1), (0, 2, 0, 1), (0.99, 0, 0, 1), (0.99, 2, 0, 1), (0.99, 2, 2, 1), (0.7, 0, 0, 1), (0.7, 2, 0, 1), (0.7, 2, 2, 1)]
for i in range(0, len(almw)):
	a, l, m, Momega  = almw[i]
	M = 1
	r_plus = M*(1 + cmath.sqrt(1 - a**2))
	r_minus = M*(1 - cmath.sqrt(1 - a**2))
	r_min = r_plus*1.1
	r_max = R_max*(1 + r_plus/(4*R_max))**2
	r = np.logspace(np.log10(r_min), np.log10(r_max), 500)
	r_star = r + ((r_plus**2)*np.log(r - r_plus) - (r_minus**2)*np.log(r - r_minus))/(r_plus - r_minus)
	y = V_eff(r, a, l, m, Momega=Momega)
	plt.plot(r_star, y, colours[i], label="a={:.2f} $M\\omega=M\\mu$={:.2f} l={:d} m={:d}".format(a, Momega, l, m))
	print("plotted V_eff for a={:.2f} Momega=Mmu={:.2f} l={:d} m={:d}".format(a, Momega, l, m))
plt.ylabel("$V_{eff}$")
plt.xlabel("$r_*$")
plt.legend()
plt.title("Effective potential for a Kerr Black Hole")
plt.tight_layout()
plot_path = "/home/dc-bamb1/GRChombo/Analysis/plots/"
save_name = "Effective_Kerr_potential_v2.png"
save_path = plot_path + save_name
plt.savefig(plot_path + save_name)
print("saved plot as " + save_path)
plt.clf()
