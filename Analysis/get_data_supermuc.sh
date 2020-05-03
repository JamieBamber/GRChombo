#!/bin/bash
process=Y00_integration
variable=S_azimuth
subdir=run0001_FlatScalar_mu1_G0
echo "start scp"
# scp di76bej@skx.supermuc.lrz.de:
foldername=${process}_data
filename=${subdir}_\*.dat
scp -r supermuc:~/GRChombo/GRChombo/Analysis/data/${foldername}/${filename} ~/GRChombo/Analysis/plots/${foldername}
