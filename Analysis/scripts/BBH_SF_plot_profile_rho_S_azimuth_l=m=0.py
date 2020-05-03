import numpy as np
import sys
import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit
#import ctypes

start_time = time.time()

# set up parameters 
data_root_path = "../data/Y00_integration_data/"
run_number = 1
mu = 1
subdir = "run000{:d}_FlatScalar_mu{:s}_G0".format(run_number, str(mu))
scale = "linear"
number = 1004
file_name_root = subdir + "_" + "{:s}" + "_" + scale + "_n{:06d}".format(number) + ".dat"
time = 0
phi0 = 1
#
rho0 = 0.5*(mu**2)*(phi0**2)
S_az0 = 0.5*(phi0**2)*mu
### get data
rho_data = np.genfromtxt(data_root_path + file_name_root.format("rho"), skip_header=1)
S_azimuth_data = np.genfromtxt(data_root_path + file_name_root.format("S_azimuth"), skip_header=1)
# --- need datasets to have the same R values and the same t
time = rho_data[1, 0]
R = rho_data[0,1:]
rho = rho_data[1, 1:]
S_azimuth = S_azimuth_data[1, 1:]

# plot graph
log_x = False
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
# plot rho
ax1.plot(R, rho, 'r-', label="Eulerian energy density $\\rho_E$")
ax1.set_ylabel("$\\rho_E$")
# plot S_azimuth
ax2.plot(R, S_azimuth, 'b-', label="Eulerian axial angular momentum  density $\\rho_J$")
ax2.set_ylabel("$\\rho_J$")
#
plt.legend(fontsize=8)
plt.xlabel("$R$")
title = "Binary BH Eulerian $\\rho_E$ and $\\rho_J$ profile $Y^0_0$ mode, $\\mu={:.1}$, time = {:.1f}".format(mu, time) 
plt.title(title)
plt.tight_layout()
save_name =  "../plots/BBHSF_" + subdir + "_rho_S_azimuth_Y00_mode_t={:.1f}.png".format(time)
print("saved " + save_name)
plt.savefig(save_name, transparent=False)
plt.clf()
