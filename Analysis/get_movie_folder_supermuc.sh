#!/bin/bash
variable=rho
subdir=run0005
echo "start scp"
# scp di76bej@skx.supermuc.lrz.de:
foldername=BBH_${subdir}_${variable}_movie
#filename=BBH_SF_rho_test0001_n000003.png
#scp -r supermuc:~/GRChombo/GRChombo/Analysis/plots/Binary_BH/BBH_${subdir}/${foldername} ~/GRChombo/Analysis/plots/Binary_BH/BBH_${subdir}
rsync -avuzh supermuc:~/GRChombo/GRChombo/Analysis/plots/Binary_BH/BBH_${subdir}/${foldername}/* ~/GRChombo/Analysis/plots/Binary_BH/BBH_${subdir}/${foldername}
