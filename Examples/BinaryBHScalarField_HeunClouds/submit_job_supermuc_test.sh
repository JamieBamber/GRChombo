#!/bin/bash
#
# This script should make a new directory in ~/GRChombo_data for the data, and copy the slurm_submit file, params.txt file and output files to
# that directory, submit the job, then change back to the working directory

# this copy is for the KNL nodes

work_dir=/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Examples/BinaryBHScalarField
cd $work_dir
#data_directory=/hppfs/work/pn34tu/di76bej/GRChombo_data/BinaryBHScalarField

run_number=7
suffix=test_2_nodes_8_OMP_params_B_DensityAndMom_on_opt_true

params_file=params_test.txt

# extract parameters from params.txt
text_number=$(printf "%04d" ${run_number})

new_dir=test_${suffix}

echo ${new_dir}
new_dir_path=${work_dir}/${new_dir}
#
mkdir -p ${new_dir_path}
cp BinaryBHLevel.cpp ${new_dir_path}/BinaryBHLevel.cpp.txt
cp slurm_submit_supermuc_test ${new_dir_path}/slurm_submit
cp ${params_file} ${new_dir_path}/params.txt

cd ${new_dir_path}
# add the location of the new directory to the input files
sed -i "s|DATADIR|${new_dir_path}|" ${new_dir_path}/params.txt
sed -i "s|DATADIR|${new_dir_path}|" ${new_dir_path}/slurm_submit
# 
sbatch slurm_submit
#
cd ${work_dir}

