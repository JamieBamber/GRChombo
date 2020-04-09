#!/bin/bash
variable=rho
subdir=run0004_FlatScalar_mu0.4_G0
number=595
echo "start scp"
# scp di76bej@skx.supermuc.lrz.de:
filename=BBH_SF_phi_${subdir}_n$(printf "%06d" ${number})_full.png
scp supermuc:~/GRChombo/GRChombo/Analysis/plots/${filename} ~/GRChombo/Analysis/plots/${filename}
