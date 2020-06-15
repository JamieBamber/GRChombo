#!/bin/bash
#
# This script should make a new directory in ~/GRChombo_data for the data, and copy the slurm_submit file, params.txt file and output files to
# that directory, submit the job, then change back to the working directory

# this copy is for the KNL nodes

work_dir=~/GRChombo/Analysis

script_dir=~/GRChombo/Analysis/scripts
script=mass_ang_mom_flux_parallel_compare_almmu_KS.py

new_dir=batch_analysis_python
echo ${new_dir}
new_dir_path=$(pwd)/${new_dir}
#
mkdir -p ${new_dir_path}
cp slurm_submit_Skylake_python ${new_dir_path}/slurm_submit
cp ${script_dir}/${script} ${new_dir_path}/python_script.py

cd ${new_dir_path}
# add the location of the new directory to the input files
sed -i "s|PYTHON_SCRIPT|${new_dir_path}/python_script.py|" ${new_dir_path}/slurm_submit
# 
sbatch slurm_submit
#
cd ${work_dir}

