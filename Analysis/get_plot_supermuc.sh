#!/bin/bash
variable=S_azimuth
folder=
subdir=run0003_FlatScalar_mu0.02822_G0
number=598
echo "start scp"
# scp di76bej@skx.supermuc.lrz.de:
filename=BBH_SF_${variable}_${subdir}_n$(printf "%06d" ${number}).png
#filename=BBH_SF_rho_test0001_n000003.png
scp supermuc:~/GRChombo/GRChombo/Analysis/plots/${folder}${filename} ~/GRChombo/Analysis/plots/
echo "saved ~/GRChombo/Analysis/plots/${filename}"
open ~/GRChombo/Analysis/plots/${filename}
