#!/bin/bash
variable=rho
subdir=run0004_FlatScalar_mu0.4_G0
number=595
echo "start scp"
# scp di76bej@skx.supermuc.lrz.de:
#filename=BBH_SF_${variable}_${subdir}_n$(printf "%06d" ${number}).png
filename=BBH_SF_rho_test0001_n000003.png
scp supermuc:~/GRChombo/GRChombo/Analysis/plots/${filename} ~/GRChombo/Analysis/plots/${filename}
