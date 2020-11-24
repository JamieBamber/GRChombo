from setuptools import setup, Extension

# Compile *mysum.cpp* into a shared library 

utils_dir = '/home/dc-bamb1/GRChombo/Source/utils'

setup(    
    ext_modules=[Extension('KerrBH_Rfunc', [utils_dir+'/KerrBH_Rfunc.cpp'],
    include_dirs=[utils_dir])],
)

