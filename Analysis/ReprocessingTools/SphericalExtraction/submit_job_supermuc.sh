#!/bin/bash
#
# this copy is for SupermucNG

work_dir=/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Analysis/ReprocessingTools/SphericalExtraction

subdir=run0005_FlatScalar_mu1_G0
start_number=2165
end_number=2165
linear_or_log=1 # 0 for log, 1 for linear
variable_index=1
suffix=

# set parameters
name=${subdir}_var${variable_index}_linlog${linear_or_log}_start_number\=${start_number}
new_dir_path=outputs/${name}
echo ${name} "Y00 integration"

#
mkdir -p ${new_dir_path}

cp slurm_submit_supermuc ${new_dir_path}/slurm_submit
cp params.txt ${new_dir_path}

cd ${new_dir_path}
# add the location of the new directory to the params file
sed -i "s|SUBDIR|${subdir}|" params.txt
sed -i "s|SNUMBER|${start_number}|" params.txt
sed -i "s|ENUMBER|${end_number}|" params.txt
sed -i "s|LINLOG|${linear_or_log}|" params.txt
sed -i "s|VARINDEX|${variable_index}|" params.txt
sed -i "s|SUFFIXSTRING|${suffix}|" params.txt
sbatch slurm_submit
#
cd ${work_dir}
