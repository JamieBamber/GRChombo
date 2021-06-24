# -*- Mode: Makefile -*-

### This makefile produces an executable for each name in the `ebase'
###  variable using the libraries named in the `LibNames' variable.

# Included makefiles need an absolute path to the Chombo installation
# CHOMBO_HOME := Please set the CHOMBO_HOME locally (e.g. export CHOMBO_HOME=... in bash)

GRCHOMBO_SOURCE = /home/dc-bamb1/GRChombo/Source

include_dirs := -I$(GRCHOMBO_SOURCE)/utils \
            -I$(GRCHOMBO_SOURCE)/simd  \
            -I$(GRCHOMBO_SOURCE)/CCZ4  \
            -I$(GRCHOMBO_SOURCE)/Matter  \
            -I$(GRCHOMBO_SOURCE)/BoxUtils  \
            -I$(GRCHOMBO_SOURCE)/GRChomboCore  \
            -I$(GRCHOMBO_SOURCE)/TaggingCriteria  \
            -I$(GRCHOMBO_SOURCE)/AMRInterpolator  \
            -I$(GRCHOMBO_SOURCE)/InitialConditions/ScalarFields  \
            -I$(GRCHOMBO_SOURCE)/FixedBackground

KerrBH_Rfunc_general_s :
	icpc -shared -c -fPIC KerrBH_Rfunc_general_s.cpp -o KerrBH_Rfunc_general_s.o ${include_dirs} -I$(CHOMBO_HOME)/include -std=c++14

HeunC_function_test :
	icpc -shared -c -fPIC HeunC_function_test.cpp -o HeunC_function_test.o ${include_dirs} -I$(CHOMBO_HOME)/include -std=c++14
