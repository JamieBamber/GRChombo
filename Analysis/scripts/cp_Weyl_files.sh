#!/bin/bash

subdirs=(
    run0016_mu0.5_delay0_G0_ratio1
    run0023_mu0.5_delay0_G0.0000000001_ratio1
    run0024_mu0.5_delay0_G0.00000000000000000001_ratio1_restart
    run0025_mu0.5_delay0_G0_ratio1_l1_m1_Al0
    run0026_mu0.5_delay0_G0.000000000000001_ratio1
    run0027_mu0.5_delay0_G0.00000000000000000001_ratio1
    run0028_mu0.5_delay0_G0.00000001_ratio1
    run0029_mu1_delay0_G0.0000000001_ratio1
    run0030_mu0.5_delay0_G0_ratio1_l2_m2_Al0
    run0031_mu0.5_delay0_G0.0000000000000000000000001_ratio1
    run0032_mu0.5_delay0_G0.000000000000000000000000000001_ratio1
    run0033_mu0.5_delay0_G0.000000001_ratio1
    run0034_mu0.5_delay0_G0.000000000001_ratio1
    run0035_mu0.5_delay0_G0.00000000000001_ratio1
    run0036_mu0.5_delay0_G0_ratio1_l1_m-1_Al0    
)

new_loc=/p/home/jusers/bamber1/juwels/GRChombo/Analysis/data/GR_Binary_BH_data/Weyl_data/
old_loc=/p/project/pra116/bamber1/BinaryBHScalarField/

for subdir in "${subdirs[@]}"
do
    cp ${old_loc}${subdir}/outputs/Weyl_integral_20.dat ${new_loc}/${subdir}_Weyl_20.dat
    cp ${old_loc}${subdir}/outputs/Weyl_integral_21.dat ${new_loc}/${subdir}_Weyl_21.dat
    cp ${old_loc}${subdir}/outputs/Weyl_integral_22.dat ${new_loc}/${subdir}_Weyl_22.dat
    echo "copied Weyl files for ${subdir}"
done

