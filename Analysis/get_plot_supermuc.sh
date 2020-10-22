#!/bin/bash
variable=rho
subdir=run0005_FlatScalar_mu1_G0
folder=BBH_run0005
number=1160
echo "start scp"
# scp di76bej@skx.supermuc.lrz.de:
filename=BBH_SF_${variable}_${subdir}_n$(printf "%06d" ${number}).png
#filename=BBH_SF_rho_test0001_n000003.png
scp supermuc:~/GRChombo/GRChombo/Analysis/plots/Binary_BH/${folder}/${filename} ~/GRChombo/Analysis/plots/Binary_BH/${filename}
echo "saved ~/GRChombo/Analysis/plots/Binary_BH/${filename}"
open ~/GRChombo/Analysis/plots/Binary_BH/${filename}
