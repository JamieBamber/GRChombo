#!/bin/bash
#
# this copy is for SupermucNG

work_dir=/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Analysis/ReprocessingTools/YlmIntegration

subdir=run0004_FlatScalar_mu0.4_G0

# set parameters
echo ${subdir} "Ylm integration"
new_dir_path=outputs/${subdir}
#
mkdir -p ${new_dir_path}

cp slurm_submit_supermuc ${new_dir_path}/slurm_submit
cp params.txt ${new_dir_path}

cd ${new_dir_path}
# add the location of the new directory to the params file
sed -i "s|SUBDIR|${subdir}|" params.txt
sbatch slurm_submit
#
cd ${work_dir}
