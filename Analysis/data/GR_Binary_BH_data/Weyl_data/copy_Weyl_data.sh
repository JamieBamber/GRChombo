#!/bin/bash

subdirs=(
run0018_mu0.5_delay0_G0.000001_ratio1
)

#data_dir=/cosma6/data/dp174/dc-bamb1/GRChombo_data/BinaryBHSF
data_dir=/p/project/pra116/bamber1/BinaryBHScalarField
Weyl_dir=/p/home/jusers/bamber1/juwels/GRChombo/Analysis/data/GR_Binary_BH_data/Weyl_data

for subdir in "${subdirs[@]}"
do
  	cp ${data_dir}/${subdir}/outputs/Weyl_integral_20.dat ${Weyl_dir}/${subdir}_Weyl_20.dat
        cp ${data_dir}/${subdir}/outputs/Weyl_integral_21.dat ${Weyl_dir}/${subdir}_Weyl_21.dat
        cp ${data_dir}/${subdir}/outputs/Weyl_integral_22.dat ${Weyl_dir}/${subdir}_Weyl_22.dat
        echo "copied Weyl data for ${subdir}"
done
