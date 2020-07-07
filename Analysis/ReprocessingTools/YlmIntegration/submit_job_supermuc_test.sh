#!/bin/bash
#
# this copy is for SupermucNG

work_dir=/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Analysis/ReprocessingTools/YlmIntegration

subdir=run0001_FlatScalar_mu1_G0
start_number=5
end_number=10
linear_or_log=1 # 0 for log, 1 for linear
suffix=_test

# set parameters
name=${subdir}_linlog${linear_or_log}_start_number_${start_number}${suffix}
new_dir_path=${name}
echo ${name} "Ylm integration"

#
mkdir -p ${new_dir_path}

cp slurm_submit_supermuc_test ${new_dir_path}/slurm_submit
cp params_test.txt ${new_dir_path}/params.txt

cd ${new_dir_path}
# add the location of the new directory to the params file
sed -i "s|SUBDIR|${subdir}|" params.txt
sed -i "s|SNUMBER|${start_number}|" params.txt
sed -i "s|ENUMBER|${end_number}|" params.txt
sed -i "s|LINLOG|${linear_or_log}|" params.txt
sed -i "s|SUFFIXSTRING|${suffix}|" params.txt
sed -i "s|OUTDIR|${name}|" params.txt
sbatch slurm_submit
#
cd ${work_dir}
