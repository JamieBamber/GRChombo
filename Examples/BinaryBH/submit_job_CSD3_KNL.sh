#!/bin/bash
#
# This script should make a new directory in ~/GRChombo_data for the data, and copy the slurm_submit file, params.txt file and output files to
# that directory, submit the job, then change back to the working directory

# this copy is for the KNL nodes

work_dir=/home/dc-bamb1/GRChombo/Examples/BinaryBH
cd $work_dir
data_directory=/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/BinaryBHSF

run_number=1

params_file=params.txt

# extract parameters from params.txt

text_number=$(printf "%04d" ${run_number})
new_dir=run${text_number}_no_SF
echo ${new_dir}
new_dir_path=${data_directory}/${new_dir}
#
mkdir -p ${new_dir_path}
cp slurm_submit_KNL ${new_dir_path}/slurm_submit
cp ${params_file} ${new_dir_path}/params.txt

cd ${new_dir_path}
# add the location of the new directory to the input files
sed -i "s|DATADIR|${new_dir_path}|" ${new_dir_path}/params.txt
# 
mkdir -p outputs
cd outputs
sbatch ../slurm_submit
#
cd ${work_dir}

