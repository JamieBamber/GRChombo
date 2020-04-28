#!/bin/bash
variable=rho
subdir=run0001
echo "start scp"
# scp di76bej@skx.supermuc.lrz.de:
filename=BBH_SF_${variable}_${subdir}_movie
#filename=BBH_SF_rho_test0001_n000003.png
scp -r supermuc:~/GRChombo/GRChombo/Analysis/plots/${filename} ~/GRChombo/Analysis/plots/
