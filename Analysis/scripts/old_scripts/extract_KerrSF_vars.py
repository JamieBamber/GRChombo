import yt
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve
from yt import derived_field
import time
import sys

start_time = time.time()

# load dataset time series
data_root_path = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF"
data_sub_dir = "run0022_KNL_l0_m0_a0_Al0_mu1_M1_correct_Ylm"

dataset_path = data_root_path + "/" + data_sub_dir + "/KerrSFp_000000.3d.hdf5"
ds = yt.load(dataset_path) # this loads a dataset time series
print("loaded data from ", dataset_path)
print("time = ", time.time() - start_time)

print(ds.field_list)
""" [('chombo', 'Pi'), ('chombo', 'S_azimuth'), ('chombo', 'S_azimuth_prime'), ('chombo', 'chi'), ('chombo', 'phi'), ('chombo', 'rho')]"""
print(ds.derived_field_list)
""" [('chombo', 'Pi'), ('chombo', 'S_azimuth'), ('chombo', 'S_azimuth_prime'), ('chombo', 'cell_volume'), ('chombo', 'chi'), 
('chombo', 'dx'), ('chombo', 'dy'), ('chombo', 'dz'), ('chombo', 'path_element_x'), ('chombo', 'path_element_y'), ('chombo', 'path_element_z'), 
('chombo', 'phi'), ('chombo', 'rho'), ('chombo', 'vertex_x'), ('chombo', 'vertex_y'), ('chombo', 'vertex_z'), ('chombo', 'x'), ('chombo', 'y'), ('chombo', 'z'), 

('gas', 'cell_volume'), ('gas', 'dx'), ('gas', 'dy'), ('gas', 'dz'), ('gas', 'path_element_x'), ('gas', 'path_element_y'), ('gas', 'path_element_z'), ('gas', 'vertex_x'), 
('gas', 'vertex_y'), ('gas', 'vertex_z'), ('gas', 'x'), ('gas', 'y'), ('gas', 'z'), 

('index', 'cell_volume'), ('index', 'cylindrical_r'), ('index', 'cylindrical_radius'), ('index', 'cylindrical_theta'), ('index', 'cylindrical_z'), ('index', 'disk_angle'), 
('index', 'dx'), ('index', 'dy'), ('index', 'dz'), ('index', 'grid_indices'), ('index', 'grid_level'), ('index', 'height'), ('index', 'morton_index'), 
('index', 'ones'), ('index', 'ones_over_dx'), ('index', 'path_element_x'), ('index', 'path_element_y'), ('index', 'path_element_z'), ('index', 'radius'), 
('index', 'spherical_phi'), ('index', 'spherical_r'), ('index', 'spherical_radius'), ('index', 'spherical_theta'), ('index', 'vertex_x'), ('index', 'vertex_y'), 
('index', 'vertex_z'), ('index', 'virial_radius_fraction'), ('index', 'x'), ('index', 'y'), ('index', 'z'), ('index', 'zeros')]"""

