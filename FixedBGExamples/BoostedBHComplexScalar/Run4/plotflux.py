# A simple python script to plot the GW
# signals over time, for a chosen mode

import numpy as np;
import matplotlib.pyplot as plt;

# output data from running merger
M = 1.0
mu = 0.05
v = 0.1
r = 500
symmetry = 4
data1 = np.loadtxt("RhoIntegral.dat")
data2 = np.loadtxt("Force_integrals.dat")

# make the plot
fig = plt.figure()

# flux dataset out
labelstring = "outer Flux"
timedata = data2[:,0]
Fdata = data2[:,3]
plt.plot(timedata, Fdata, '--', lw = 1.0, label=labelstring)

# flux dataset in
labelstring = "inner Flux"
timedata = data2[:,0]
Fdata = data2[:,1]
plt.plot(timedata, Fdata, '--', lw = 1.0, label=labelstring)

# make the plot look nice
plt.xlabel("time")
plt.ylabel("Force")
#plt.xlim(0, 1000)
#plt.ylim(1e-1, 1e2)
plt.legend(loc=2)

# save as png image
filename = "FvsT" + "_mu" + str(mu) + ".png"
plt.savefig(filename)