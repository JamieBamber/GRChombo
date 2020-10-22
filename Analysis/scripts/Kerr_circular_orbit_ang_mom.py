import numpy as np
from matplotlib import pyplot as plt

# script to plot the expected angular momentum per unit mass needed for circular orbit by a massive particle 
# around a Kerr BH

# the particle J / mass for a circular orbit in the z = 0 plane
def particle_Lz(q, a):
	result = np.sqrt((q**2 + a**2 - 2*a*np.sqrt(q))/(q*(q**2 - 3*q + 2*a*np.sqrt(q))))
	return result

""" estimate expected initial angular momentum per unit mass
Take J_phi  = sqrt(g)*T^0_phi
	rho = sqrt(g)*T^0_0 
	L_z = -T^0_phi / T^0_0
	L_z = (2mM (\[Mu]M (a^2 (q+2)+q^3)-2 am))/(2 \[Mu]^2 M^2 (a^2 (q+1)+(q-1)q^2)+ m^2(q-2))
"""
# the field J / mass we expect for a field Phi = e^-i[mu]t Yml(theta, phi)
def field_Lz(q, Mmu, a, m):
	numerator = 2*m*( Mmu*((a**2)*(q + 2) + q**3) - 2*a*m)
	denominator = 2*(Mmu**2)*((a**2)*(q+1) + (q-1)*q**2) + (m**2)*(q-2)
	result = numerator / denominator
	return result

a = 0.7
r_plus = 1 + np.sqrt(1 - a**2)
Mmu_list = [0.05, 0.4, 1, 2]
colours = ['b--', 'g--', 'c--', 'm--']
q0 = np.linspace(r_plus, 15, 256)
L = particle_Lz(q0, a)
plt.plot(q0, L, 'r-', label="particle $L_z/M$ per unit mass for circular orbit")
for i in range(0,len(Mmu_list)):
	Mmu = Mmu_list[i]
	Lexp = field_Lz(q0, Mmu, a, 1)
	plt.plot(q0, Lexp, colours[i], label="expected initial $L_z/M$ per unit mass for $m=l=1$ $M\\mu=${:.2f}".format(Mmu)) 
plt.legend(fontsize=8)
plt.xlabel("$r_{BL}/M$")
plt.ylabel("$L_z/M$")
plt.ylim((-1, 7.5))
plt.title("Ang. mom. per unit mass for a Kerr circular orbit in z=0 plane, a = " + str(a))
save_path = "/home/dc-bamb1/GRChombo/Analysis/plots/"
filename = "Kerr_circular_orbit_ang_mom.png"
file_path = save_path + filename
plt.savefig(file_path) 
plt.clf()
print("saved plot as " + file_path) 
