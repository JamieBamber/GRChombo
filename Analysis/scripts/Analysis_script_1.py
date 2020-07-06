###################
""" Script to open the hdf5 files produced by GRChombo, analyse the data
and plot the results """ 
###################

from __future__ import print_function

import numpy as np
import h5py

root_data_path="/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
path = root_data_path + "/run1_l0_m1_a0_Al0/KerrSFp_000001.3d.hdf5"

f = h5py.File(path, 'r')
print(f.keys())

""" Top level groups are 
'Chombo_global', 'level_0', 'level_1', 'level_2', 'level_3', 'level_4', 'level_5', 'level_6'
"""
""" <HDF5 group "/Chombo_global" (0 members)>  contains  <KeysViewHDF5 []>
has attributes  <KeysViewHDF5 ['SpaceDim', 'testReal']>
<HDF5 group "/level_0" (5 members)>  contains  <KeysViewHDF5 ['Processors', 'boxes', 'data:datatype=0', 'data:offsets=0', 'data_attributes']>
<HDF5 group "/level_1" (5 members)>  contains  <KeysViewHDF5 ['Processors', 'boxes', 'data:datatype=0', 'data:offsets=0', 'data_attributes']>
<HDF5 group "/level_2" (5 members)>  contains  <KeysViewHDF5 ['Processors', 'boxes', 'data:datatype=0', 'data:offsets=0', 'data_attributes']>
<HDF5 group "/level_3" (5 members)>  contains  <KeysViewHDF5 ['Processors', 'boxes', 'data:datatype=0', 'data:offsets=0', 'data_attributes']>
<HDF5 group "/level_4" (5 members)>  contains  <KeysViewHDF5 ['Processors', 'boxes', 'data:datatype=0', 'data:offsets=0', 'data_attributes']>
<HDF5 group "/level_5" (5 members)>  contains  <KeysViewHDF5 ['Processors', 'boxes', 'data:datatype=0', 'data:offsets=0', 'data_attributes']>
<HDF5 group "/level_6" (5 members)>  contains  <KeysViewHDF5 ['Processors', 'boxes', 'data:datatype=0', 'data:offsets=0', 'data_attributes']> 
has attributes  <KeysViewHDF5 ['dt', 'dx', 'is_periodic_0', 'is_periodic_1', 'is_periodic_2', 'prob_domain', 'ref_ratio', 'tag_buffer_size', 'time']>

<HDF5 dataset "data:datatype=0": shape (2097152,), type "<f8">
<HDF5 dataset "Processors": shape (256,), type "<i4">
<HDF5 dataset "boxes": shape (256,), type "|V28">
<HDF5 dataset "data:datatype=0": shape (2097152,), type "<f8">
<HDF5 dataset "data:offsets=0": shape (257,), type "<i8">
<HDF5 group "/level_0/data_attributes" (0 members)>  contains  <KeysViewHDF5 []> 
has attributes  <KeysViewHDF5 ['comps', 'ghost', 'objectType', 'outputGhost']>

2097152 = 2^21

number of boxes = 128^2 * 64 = 2^20
number of output variables = 2 (phi and Pi)
 
8192 = 2^13 """
# 
""" for member in f.keys():
	m = f[member]
	try:
		print(m," contains ", m.keys())
		print("has attributes ", m.attrs.keys())
	except: 
		print("Not a group, is type ", type(m)) """

level_0 = f['level_0']

""" for member in level_0.keys():
	m = level_0[member]
	try:
		print(m," contains ", m.keys())
		print("has attributes ", m.attrs.keys())
	except:
		print(member, " is ", m[0:]) """

print(level_0['data:datatype=0'][0:8])



