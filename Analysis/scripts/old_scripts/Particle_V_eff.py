import math
from matplotlib import pyplot as plt
import numpy as np

mu = 0.4
M = 1

l_arr = np.linspace(0, 10, 6)

def V_eff_Sch(l, R):
	lamb = l*(l + 1)/(mu*2*M)**2
	r_s = 2*M 
	x = (R/r_s)*(1 + r_s/(4*R))**2
	U = -1/x + lamb/x**2 - lamb/x**3
	return U

# plot graph

colours = ["r-", "b-", "g-", "m-", "y-", "c-"]

R = np.linspace(0.5, 512, 256)

for i in range(0, len(l_arr)):
	l = int(l_arr[i])
	U = V_eff_Sch(l, R)
	plt.plot(R, U, colours[i], label="l = {:d}".format(l))
	print("plotted for l = " + str(l))
plt.xlabel("$R$")
plt.ylabel("$V_{eff}$")
plt.title("Schwarzchild particle effective potential")
plt.legend(fontsize=8)
plt.ylim((-5, 5))
plt.tight_layout()
save_path = "/home/dc-bamb1/GRChombo/Analysis/plots/Schwarzchild_Particle_V_eff.png"
plt.savefig(save_path)
print("saved plot as " + save_path) 
plt.clf()
