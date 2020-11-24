import numpy as np
from matplotlib import rc
rc('text', usetex=True)
from matplotlib import pyplot as plt

# script to plot the expected angular momentum per unit mass needed for circular orbit by a massive particle 
# around a Kerr BH

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

# the particle J / mass for a circular orbit in the z = 0 plane
def particle_Lz(q, a):
	result = (q**2 + a**2 - 2*a*np.sqrt(q))/np.sqrt(q*(q**2 - 3*q + 2*a*np.sqrt(q)))
	return result

""" estimate expected initial angular momentum per unit mass
Take J_phi  = sqrt(g)*T^0_phi
	rho = sqrt(g)*T^0_0 
	L_z = -T^0_phi / T^0_0
	L_z = (2mM (\[Mu]M (a^2 (q+2)+q^3)-2 am))/(2 \[Mu]^2 M^2 (a^2 (q+1)+(q-1)q^2)+ m^2(q-2))
"""
# the field J / mass we expect for a field Phi = e^-i[mu]t Yml(theta, phi)
def field_Lz(q, Mmu, a, m):
	numerator = 2*m*(2*a*(a*Mmu-m)+ Mmu*q*(a**2 + q**2))
	denominator = 2*Mmu**2*((a**2 - q**2) + q*(a**2+q**2))+m**2*(q-2)   
	result = numerator / denominator
	return result

a = 0.7
r_plus = 1 + np.sqrt(1 - a**2)
Mmu_list = [0.2, 0.4, 0.8, 1.6]
colours = ['b--', 'g--', 'c--', 'm--']
q0 = np.linspace(r_plus, 15, 256)
L = particle_Lz(q0, a)

# plot setup
ax1 = plt.axes()
fig = plt.gcf()
fig.set_size_inches(3.375,3)
font_size = 10
title_font_size = 10
label_size = 10
legend_font_size = 9
rc('xtick',labelsize=font_size)
rc('ytick',labelsize=font_size)
ax1.plot(q0, L, 'r-', label="particle in a circular orbit")
for i in range(0,len(Mmu_list)):
	Mmu = Mmu_list[i]
	Lexp = field_Lz(q0, Mmu, a, 1)
	ax1.plot(q0, Lexp, colours[i], label="$\\mu=${:.2f}".format(Mmu), linewidth=1) 
plt.legend(fontsize=legend_font_size, ncol=2,labelspacing=0.2,handletextpad=0.2,columnspacing=0.5,borderaxespad=0.1)
plt.xlabel("$r_{BL}/M$", fontsize=label_size)
plt.ylabel("$L_z/M$", fontsize=label_size)
plt.ylim((-1, 7.5))
plt.title("Ang. mom. per unit mass, $\\chi=$ " + str(a), fontsize=title_font_size)
save_path = "/home/dc-bamb1/GRChombo/Analysis/plots/plots_for_first_paper/"
filename = "Fig_5_Kerr_circular_orbit_ang_mom.pdf"
file_path = save_path + filename
plt.xticks(fontsize=font_size)
plt.yticks(fontsize=font_size)
plt.tight_layout()
plt.savefig(file_path) 
plt.clf()
print("saved plot as " + file_path) 
