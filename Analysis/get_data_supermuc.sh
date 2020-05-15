#!/bin/bash
process=Circular_Extraction
variable=phi
subdir=run000-1_FlatScalar_mu0.4_G0
echo "start scp"
# scp di76bej@skx.supermuc.lrz.de:
foldername=${process}_data
filename=${subdir}_\*.dat
scp -r supermuc:~/GRChombo/GRChombo/Analysis/data/${foldername}/${filename} ~/GRChombo/Analysis/data/${foldername}
