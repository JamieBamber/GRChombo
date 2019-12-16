#!/bin/bash
#
# This script should make a new directory in ~/GRChombo_data for the data, and copy the slurm_submit file, params.txt file and output files to
# that directory, submit the job, then change back to the working directory

work_dir=/home/dc-bamb1/GRChombo/Examples/FixedKerrBGScalarField
cd $work_dir
data_directory=/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF

# work out the current run number
#cd $data_directory
#run_number=$(grep '[0-9]' run_number.txt)
#run_number=$((run_number+1))
#echo $run_number > run_number.txt

run_number=1

# extract parameters from params.txt
cd $work_dir
l=$(grep "scalar_l" params.txt | tr -cd '(\-)?[0-9]+([.][0-9]+)?+' | sed -r '/^0$/! s/(\.)??0+$//')
m=$(grep "scalar_m " params.txt | grep -v "scalar_mass" | tr -cd '(\-)?[0-9]+([.][0-9]+)?+' | sed -r '/^0$/! s/(\.)??0+$//')
Al=$(grep "alignment" params.txt | tr -cd '(\-)?[0-9]+([.][0-9]+)?+' | sed -r '/^0$/! s/(\.)??0+$//')
a=$(grep "bh_spin" params.txt | tr -cd '(\-)?[0-9]+([.][0-9]+)?+' | sed -r '/^0$/! s/(\.)??0+$//')
new_dir=run${run_number}_l${l}_m${m}_a${a}_Al${Al}
echo ${new_dir}
new_dir_path=${data_directory}/${new_dir}
#
mkdir -p ${new_dir_path}
cp slurm_submit ${new_dir_path}/slurm_submit
cp params.txt ${new_dir_path}

cd ${new_dir_path}
# add the location of the new directory to the input files
sed -i "s|DATADIR|${new_dir_path}|" ${new_dir_path}/params.txt
# sed -i "s|DATADIR|${new_dir_path}|" ${new_dir_path}/slurm_submit
# 
mkdir -p outputs
cd outputs
sbatch ../slurm_submit
#
cd ${work_dir}

