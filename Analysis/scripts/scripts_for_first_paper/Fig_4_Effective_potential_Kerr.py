import numpy as np
from matplotlib import rc
rc('text', usetex=True)
import matplotlib.pyplot as plt
import cmath

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

r_max = 50
a = 0.7		# J / M^2

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
def V_eff(r, chi, l, m, mu, M=1):
	#
	a = chi*M
	Delta = r**2 + a**2 - 2*M*r
	d2 = a**2 + r**2
	V = Delta/d2*(mu**2 + a**2/d2**2 + 2*M*r*(r**2 - 2*a**2)/d2**3 + l*(l+1)/d2)\
		+ a*m*(4*M*mu*r - a*m)/d2**2 - mu**2
 	#
	return V

# plot potential
colours = ['b--', 'b-', 'b-.','r-', 'g-', 'c-', 'y-', 'r-.']
#almmu = [(0.99, 1, 1, 0.4), (0.99, 2, 2, 0.4), (0.99, 1, 1, 0.05), (0.99, 1, 1, 0.5), (0.99, 0, 0, 0.194), (0.99, 0, 0, 0.01), (0.99, 0, 0, 0.4)]
almmu = [(a, 1, 1, 0.1), (a, 1, 1, 0.4), (a, 1, 1, 0.5), (a, 0, 0, 0.4), (a, 1, -1, 0.4), (0.99, 1, 1, 0.4), (0, 1, 1, 0.4)]
# plot setup
ax1 = plt.axes()
fig = plt.gcf()
fig.set_size_inches(3.9,3.5)
font_size = 10
title_font_size = 10
label_size = 11
legend_font_size = 9
#rc('xtick',labelsize=font_size)
#rc('ytick',labelsize=font_size)
for i in range(0, len(almmu)):
	a, l, m, mu  = almmu[i]
	M = 1
	r_plus = M*(1 + cmath.sqrt(1 - a**2))
	r_minus = M*(1 - cmath.sqrt(1 - a**2))
	r = r_plus + np.logspace(np.log10(0.001), np.log10(r_max), 500)
	r_star = r + ((r_plus**2)*np.log(r - r_plus) - (r_minus**2)*np.log(r - r_minus))/(r_plus - r_minus)
	y = V_eff(r, a, l, m, mu, M)
	ax1.plot(r_star, y, colours[i], label="$\\chi=${:.2f} $l,m=${:d},{:d} $\\mu$={:.1f}".format(a, l, m, mu), linewidth=1)
	print("plotted V_eff for a={:.2f} l={:d} m={:d} $M\\mu$={:.2f}".format(a, l, m, mu))
plt.ylabel("$V_{eff} - \\mu^2$", fontsize=label_size)
plt.xlabel("$r_*$", fontsize=label_size)
plt.legend(fontsize=legend_font_size)
plt.title("Quasi-effective potential for a Kerr Black Hole", fontsize=title_font_size)
plt.tight_layout()
plot_path = "/home/dc-bamb1/GRChombo/Analysis/plots/plots_for_first_paper/"
save_name = "Fig_4_Effective_Kerr_potential.png"
save_path = plot_path + save_name
plt.savefig(plot_path + save_name)
print("saved plot as " + save_path)
plt.clf()
