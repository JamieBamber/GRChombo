#!/bin/bash
variable=phi
subdir=run0005_FlatScalar_mu1_G0
number=1000
echo "start scp"
# scp di76bej@skx.supermuc.lrz.de:
filename=*_${variable}_${subdir}_n$(printf "%06d" ${number}).png
#filename=BBH_SF_rho_test0001_n000003.png
scp supermuc:~/GRChombo/GRChombo/Analysis/plots/Binary_BH/${filename} ~/GRChombo/Analysis/plots/Binary_BH
echo "saved ~/GRChombo/Analysis/plots/Binary_BH/${filename}"
open ~/GRChombo/Analysis/plots/Binary_BH/${filename}
