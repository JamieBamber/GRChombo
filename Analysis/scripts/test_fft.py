import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math
from scipy.fft import fft, fftshift

x = np.linspace(0, 10, 100)
y = np.sin(5*2*np.pi*x)
print("len(y) = ", len(y))
f = fft(y)
print("len(f) = ", len(f))
f_shifted = fftshift(f)
print("len(f_shifted) = ", len(f_shifted))
