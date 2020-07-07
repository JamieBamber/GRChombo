#!/bin/bash
#
# This script should make a new directory in ~/GRChombo_data for the data, and copy the slurm_submit file, params.txt file and output files to
# that directory, submit the job, then change back to the working directory

# this copy is for the KNL nodes

work_dir=/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Examples/BinaryBHScalarField
cd $work_dir
data_directory=/hppfs/work/pn34tu/di76bej/GRChombo_data/BinaryBHScalarField

run_number=11

params_file=params.txt

# extract parameters from params.txt
cd $work_dir
l=$(grep "scalar_l" ${params_file} | tr -cd '(\-)?[0-9]+([.][0-9]+)?+')
m=$(grep "scalar_m " ${params_file} | grep -v "scalar_mass" | tr -cd '(\-)?[0-9]+([.][0-9]+)?+')
G_Newton=$(grep "G_Newton" ${params_file} | tr -cd '(\-)?[0-9]+([.][0-9]+)?+' | sed -r '/^0$/! s/(\.)??0+$//')
mu=$(grep "scalar_mass" ${params_file} | tr -cd '(\-)?[0-9]+([.][0-9]+)?+' | sed -r '/^0$/! s/(\.)??0+$//')

text_number=$(printf "%04d" ${run_number})

new_dir=run${text_number}_FlatScalar_mu${mu}_G${G_Newton}
echo ${new_dir}
new_dir_path=${data_directory}/${new_dir}
#
mkdir -p ${new_dir_path}
cp slurm_submit_supermuc ${new_dir_path}/slurm_submit
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

