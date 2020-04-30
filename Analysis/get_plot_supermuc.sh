#!/bin/bash
variable=phi
subdir=failurerun0002_FlatScalar_mu0.4_G0
number=300
echo "start scp"
# scp di76bej@skx.supermuc.lrz.de:
filename=BBH_SF_${variable}_${subdir}_n$(printf "%06d" ${number}).png
#filename=BBH_SF_rho_test0001_n000003.png
scp supermuc:~/GRChombo/GRChombo/Analysis/plots/${filename} ~/GRChombo/Analysis/plots/${filename}
