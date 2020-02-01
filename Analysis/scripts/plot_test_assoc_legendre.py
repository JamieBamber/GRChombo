import numpy as np
from matplotlib import pyplot as plt

root_path = "/home/dc-bamb1/GRChombo/Analysis/"
inputfile = root_path + "data/test_assoc_legendre_data.dat"

def plot():
	# load data
	data = np.genfromtxt(inputfile, skip_header=1)
	x = data[0][2:]
	#
	colours = ["r-", "r--", "b-", "b--", "b-.", "g-", "g--", "g-.", "c--"]
	for i in range(0, data.shape[0]-1):
		l, m = data[i][0:2]
		l = int(l)
		m = int(m)
		plt.plot(x, data[i][2:], colours[i], label = "l,m = {:d},{:d}".format(l, m))
		print("plotted for l,m = {:d},{:d}".format(l, m))
	plt.xlabel("$\\cos(\\theta)$")
	plt.ylabel("$P^l_m$")
	plt.legend()
	plt.ylim((-1.5, 1.5))
	plt.tight_layout()
	plt.savefig(root_path + "plots/assoc_legendre_plot.png")
	plt.clf()

plot()	
