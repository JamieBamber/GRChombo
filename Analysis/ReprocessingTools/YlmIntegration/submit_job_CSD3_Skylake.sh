#!/bin/bash
#
# this copy is for the Skylake nodes

work_dir=/home/dc-bamb1/GRChombo/Analysis/ReprocessingTools/YlmIntegration

subdir=run0002.2_KNL_l0_m0_a0.99_Al0_mu1_M1
suffix=_log_correct_r_min

# extract parameters from params.txt
echo ${subdir} "Ylm Integration"
new_dir_path=outputs/${subdir}${suffix}
#
mkdir -p ${new_dir_path}

cp slurm_submit_Skylake ${new_dir_path}/slurm_submit
cp params.txt ${new_dir_path}

cd ${new_dir_path}
# add the location of the new directory to the params file
sed -i "s|SUBDIR|${subdir}|" params.txt
sbatch slurm_submit
#
cd ${work_dir}

