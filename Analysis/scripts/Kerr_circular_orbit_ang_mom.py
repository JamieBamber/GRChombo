import numpy as np
from matplotlib import pyplot as plt

# script to plot the expected angular momentum per unit mass needed for circular orbit by a massive particle 
# around a Kerr BH

a = 0.7	# spin J/M^2
# using M = 1 units

def Lz(q):
	result = np.sqrt((q**2 + a**2 - 2*a*np.sqrt(q))/(q*(q**2 - 3*q + 2*a*np.sqrt(q))))
	return result

""" estimate expected initial angular momentum per unit mass
Take J_phi  = sqrt(g)*T^0_phi
	rho = sqrt(g)*T^0_0 
	L_z = -T^0_phi / T^0_0
	T^0_phi = mu*(1 - 2M(r^2 - a^2)/(Delta*r)) - 2aM/(Delta*r)
	T^0_0   = 0.5*(mu^2*(1 - 2M(r^2 - a^2)/(Delta*r)) + r^2/A)
"""
def expected_field_Lz(q, mu):
	Delta = q**2 + a**2 - 2*q
	A = (q**2)*(q**2 + a**2) + 2*q*(a**2)
	g00up = 1 - 2*(q**2 - a**2)/(Delta*q)
	result = 2*(mu*g00up - 2*a/(Delta*q))/((mu**2)*g00up + (q**2)/A)
	return result

r_plus = 1 + np.sqrt(1 - a**2)

mu_list = [0.05, 0.4, 1, 2]
colours = ['b--', 'g--', 'c--', 'm--']
q0 = np.linspace(r_plus, 15, 256)
L = Lz(q0)
plt.plot(q0, L, 'r-', label="particle $L_z/M$ per unit mass for circular orbit")
for i in range(0,len(mu_list)):
	mu = mu_list[i]
	Lexp = expected_field_Lz(q0, mu)
	plt.plot(q0, Lexp, colours[i], label="expected initial $L_z/M$ per unit mass for $m=l=1$ $\\mu=${:.2f}".format(mu)) 
plt.legend(fontsize=8)
plt.xlabel("$r_{BL}/M$")
plt.ylabel("$L_z/M$")
plt.ylim((-1, 7.5))
plt.title("Ang. mom. per unit mass for a Kerr circular orbit, a = " + str(a))
save_path = "/home/dc-bamb1/GRChombo/Analysis/plots/"
filename = "Kerr_circular_orbit_ang_mom.png"
file_path = save_path + filename
plt.savefig(file_path) 
plt.clf()
print("saved plot as " + file_path) 
