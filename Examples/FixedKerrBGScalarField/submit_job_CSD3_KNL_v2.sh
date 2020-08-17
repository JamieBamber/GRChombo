#!/bin/bash
#
# This script should make a new directory in ~/GRChombo_data for the data, and copy the slurm_submit file, params.txt file and output files to
# that directory, submit the job, then change back to the working directory

# this copy is for the KNL nodes

work_dir=/home/dc-bamb1/GRChombo/Examples/FixedKerrBGScalarField
cd $work_dir
data_directory=/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF

# specify the input params for each run I want to submit
# list for each is: l, m, a, Al, mu, dt
run0001=(1 1 0.7 0 0.4 0.0625)
run0002=(2 2 0.7 0 0.4 0.0625)
run0003=(0 0 0.7 0 0.4 0.0625)
run0004=(4 4 0.7 0 0.4 0.0625)
run0005=(1 -1 0.7 0 0.4 0.0625)
run0006=(8 8 0.7 0 0.4 0.0625)
run0007=(1 1 0.99 0 0.4 0.0625)
run0008=(1 1 0 0 0.4 0.0625)
run0009=(2 2 0.7 0 0.8 0.03125)
run0010=(4 4 0.7 0 1.6 0.03125)
run0011=(1 1 0.7 0 0.2 0.125)
run0012=(1 1 0.7 0 0.8 0.03125)

# specify runs to submit
run_list=(
	run0001
	run0002
	run0003
	run0004
	run0005
)

params_file=params_v2.txt

for run in "${run_list[@]}"
do
	cd $work_dir

	# extract parameters	
	val="$run[0]"; l="${!val}"
	val="$run[1]"; m="${!val}"
	val="$run[2]"; a="${!val}"
	val="$run[3]"; Al="${!val}"
	M=1
	val="$run[4]"; mu="${!val}"
	val="$run[5]"; dt="${!val}"

	# text_number=$(printf "%04d" ${run_number})
	
	new_dir=${run}_l${l}_m${m}_a${a}_Al${Al}_mu${mu}_M${M}_IsoKerr
	echo ${new_dir}
	new_dir_path=${data_directory}/${new_dir}
	#
	mkdir -p ${new_dir_path}
	cp slurm_submit_KNL ${new_dir_path}/slurm_submit
	cp ${params_file} ${new_dir_path}/params.txt
	
	cd ${new_dir_path}
	# add the input params to the input files
	sed -i "s|DATADIR|${new_dir_path}|" ${new_dir_path}/params.txt
	sed -i "s|DATASUBDIR|${new_dir}|" ${new_dir_path}/params.txt
	sed -i "s|DATADIR|${new_dir_path}|" ${new_dir_path}/slurm_submit
	sed -i "s|JOBNAME|${run}KS|" ${new_dir_path}/slurm_submit
	sed -i "s|SCALARL|${l}|" ${new_dir_path}/params.txt
	sed -i "s|SCALARM|${l}|" ${new_dir_path}/params.txt
	sed -i "s|BHSPIN|${a}|" ${new_dir_path}/params.txt
	sed -i "s|ALANGLE|${Al}|" ${new_dir_path}/params.txt
	sed -i "s|MUVAL|${mu}|" ${new_dir_path}/params.txt
	sed -i "s|DTMULT|${dt}|" ${new_dir_path}/params.txt
	# 
	mkdir -p outputs
	cd outputs
	sbatch ../slurm_submit
	#
	cd ${work_dir}
done
	
