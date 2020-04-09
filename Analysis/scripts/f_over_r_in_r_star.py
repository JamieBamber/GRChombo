
import numpy as np
from matplotlib import pyplot as plt

r = 1 + np.logspace(-5, 1, 50)
r_star = r + np.log(r - 1)
F = (1 - 1/r)/r

plt.plot(r_star, F, 'r-')
plt.xlabel("$r_*$")
plt.ylabel("o$f(r)/r$")
save_root = "/Users/Jamie/GRChombo/Analysis/plots/"
plt.savefig(save_root +  "f_over_r_in_r_star.png")
print("made plot " + save_root +  "f_over_r_in_r_star.png")
plt.clf()
