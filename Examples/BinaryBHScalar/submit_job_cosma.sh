#!/bin/bash
#
# This script should make a new directory in GRChombo_data for the data, and copy the slurm_submit file, params.txt file and output files to
# that directory, submit the job, then change back to the working directory

# this copy is for COSMA6

work_dir=/cosma/home/dp174/dc-bamb1/GRChombo/Examples/BinaryBHScalar
cd $work_dir
data_directory=/cosma6/data/dp174/dc-bamb1/GRChombo_data/BinaryBHSF

# specify the input params for each run I want to submit
# list for each is: mu, delay, dt, G, BH mass ratio

plot_interval=10
L=512
N1=64
box_size=16

cd $work_dir

new_dir=test_run_mu1_delay0_G0_ratio1

echo ${new_dir}
new_dir_path=${data_directory}/${new_dir}
#
mkdir -p ${new_dir_path}
cp slurm_submit_cosma ${new_dir_path}/slurm_submit
params_file=params.txt
cp ${params_file} ${new_dir_path}/params.txt

cd ${new_dir_path}
# add the input params to the input files
sed -i "s|DATADIR|${new_dir_path}|" ${new_dir_path}/params.txt
sed -i "s|DATASUBDIR|${new_dir}|" ${new_dir_path}/params.txt
sed -i "s|JOBNAME|${run}BBH|" ${new_dir_path}/slurm_submit
#
mkdir -p outputs
cd outputs
sbatch ../slurm_submit
#
cd ${work_dir}
