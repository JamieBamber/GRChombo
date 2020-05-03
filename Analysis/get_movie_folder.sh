#!/bin/bash
variable=S_azimuth
subdir=run0001
echo "start scp"
# scp di76bej@skx.supermuc.lrz.de:
foldername=BBH_SF_${variable}_${subdir}_movie
#filename=BBH_SF_rho_test0001_n000003.png
scp -r supermuc:~/GRChombo/GRChombo/Analysis/plots/${foldername} ~/GRChombo/Analysis/plots/
