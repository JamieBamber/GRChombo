#!/bin/bash
work_dir=/home/dc-bamb1/GRChombo/Analysis/ReprocessingTools/SphericalPhiExtract
subdir=run0022_KNL_l0_m0_a0_Al0_mu1_M1_new_rho_more_levels
cd ${work_dir}/outputs/
mkdir -p ${subdir}
cd ${subdir}
cp ${work_dir}/params.txt .
sed -i "s|SUBDIR|${subdir}|" params.txt
#
echo "running phi extract directly on ${subdir}"
mpirun -np 8 ${work_dir}/ReprocessingTool3d.Linux.64.mpicxx.ifort.OPTHIGH.MPI.OPENMPCC.ex params.txt
cd ${work_dir}
