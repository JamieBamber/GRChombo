###################
"""
Script to open the hdf5 files produced by GRChombo, analyse the data
and plot the results
"""
###################

from __future__ import print_function

import numpy as np
import h5py

path = "~/GRChombo_data/KerrSF/run5_l0_m0_a0.99_Al0/KerrSFp_000001.3d.hdf5"

f = h5py.File(path, 'r')
print(f.keys())




	

