#!/bin/bash
variable=phi
subdir=run0001_l0_m0_a0_Al0_mu1_M0.48847892320123_phase0_KerrSchild
number=6000
echo "start scp"
# scp di76bej@skx.supermuc.lrz.de:
filename=KerrSF_${variable}_${subdir}_n$(printf "%06d" ${number}).png
#filename=BBH_SF_rho_test0001_n000003.png
scp supermuc:~/GRChombo/GRChombo/Analysis/plots/KerrBH/${filename} ~/GRChombo/Analysis/plots/KerrBH/${filename}
echo "saved ~/GRChombo/Analysis/plots/KerrBH/${filename}"
open ~/GRChombo/Analysis/plots/KerrBH/${filename}
