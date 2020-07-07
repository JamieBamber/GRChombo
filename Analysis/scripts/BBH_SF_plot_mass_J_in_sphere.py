import numpy as np
from matplotlib import pyplot as plt

run_number=1
mu="1"
G=0
plot_interval=1
dt_multiplier=0.125
dt=8*dt_multiplier

# data sub dir
data_sub_dir = "run{:04d}_FlatScalar_mu{:s}_G{:d}".format(run_number, mu, G)

phi0 = 1
rho0 = 0.5*(float(mu)*phi0)**2
sphere_radius=100
E0 = 4*np.pi*(sphere_radius**3)*rho0/3

# output file
root_path="/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Analysis/data/BBH_SF_mass_J_in_sphere/"
output_file = data_sub_dir + "_mass_J_in_sphere_r=" + str(sphere_radius) + ".dat"

# load data
data = np.genfromtxt(root_path + output_file, skip_header=1)
t = data[:,0]
E = data[:,1]
J = data[:,2]

# average J data

def averaging(y, av_num):
	N = len(y)
	y_av = np.zeros(N - av_num)
	for i in range(0, av_num):
		y_av += y[i:N - av_num + i]/av_num
	return y_av

av_num = 10
J_av = averaging(J, av_num)
t_av = averaging(t, av_num)
E_av = averaging(E, av_num)
# plot graph
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(t_av, J_av, 'b-', linewidth=1, label="Eulerian angular momentum inside R={:.0f}".format(sphere_radius))
ax2.plot(t_av, np.log10(E_av/E0), 'r-', label="Eulerian energy inside R={:.0f}".format(sphere_radius))
ax1.set_xlabel("time")
ax2.set_ylabel("$\\log_{10}(E/E_0)$")
ax1.set_ylabel("$J$")
ax2.set_ylim((0, 4))
ax1.set_ylim((-5e9, 5e9))
# legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc=0)
plt.title("Binary BH with scalar field, $\mu={:s}$, E and J inside R={:.0f}".format(mu, sphere_radius))
plt.tight_layout()
savename = "/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Analysis/plots/" + data_sub_dir + "_mass_J_in_sphere_r=" + str(sphere_radius) + ".png"
plt.savefig(savename, transparent=False)
print("saved plot as ", savename)
plt.clf()

