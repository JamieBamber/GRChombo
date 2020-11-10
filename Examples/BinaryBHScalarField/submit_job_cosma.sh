#!/bin/bash
#
# This script should make a new directory in GRChombo_data for the data, and copy the slurm_submit file, params.txt file and output files to
# that directory, submit the job, then change back to the working directory

# this copy is for COSMA6

work_dir=/cosma/home/dp174/dc-bamb1/GRChombo/Examples/BinaryBHScalarField
cd $work_dir
data_directory=/cosma6/data/dp174/dc-bamb1/GRChombo_data/BinaryBHSF

# specify the input params for each run I want to submit
# list for each is: mu, delay, dt, G, BH mass ratio

run0001=(1 0 0.125 0 1)
run0002=(1 10000 0.125 0 1)
run0003=(0.08187607564 0 0.25 0 1)
run0004=(1 0 0.125 0 2)
run0005=(1 10000 0.125 0 2)
run0006=(0.5 0 0.25 0 1)
run0007=(0.5 10000 0.25 0 1)
run0008=(0.5 0 0.25 0.000001 1)

params_file=params.txt

run_list=(
	run0001
)

plot_interval=10
L=512
N1=64
box_size=16
reflect_z=0

for run in "${run_list[@]}"
do
  	cd $work_dir
        # extract parameters    
        val="$run[0]"; mu="${!val}"
        val="$run[1]"; delay="${!val}"
        val="$run[2]"; dt_mult="${!val}"
        val="$run[3]"; G="${!val}"
        val="$run[4]"; ratio="${!val}"

        # text_number=$(printf "%04d" ${run_number})
        new_dir=${run}_mu${mu}_delay${delay}_G${G}_ratio${ratio}_v8
        #_L${L}_N$N1
        echo ${new_dir}
        new_dir_path=${data_directory}/${new_dir}
        #
	mkdir -p ${new_dir_path}
        cp slurm_submit_cosma ${new_dir_path}/slurm_submit
	params_file=params_ratio${ratio}.txt
        cp ${params_file} ${new_dir_path}/params.txt
	cp BinaryBHLevel.cpp ${new_dir_path}/BinaryBHLevel.cpp.txt

	cd ${new_dir_path}
        # add the input params to the input files
        sed -i "s|DATADIR|${new_dir_path}|" ${new_dir_path}/params.txt
        sed -i "s|DATASUBDIR|${new_dir}|" ${new_dir_path}/params.txt
        sed -i "s|DTMULT|${dt_mult}|" ${new_dir_path}/params.txt
        sed -i "s|JOBNAME|${run}BBH|" ${new_dir_path}/slurm_submit
        sed -i "s|BOXLENGTH|${L}|" ${new_dir_path}/params.txt
        sed -i "s|BOXSIZE|${box_size}|" ${new_dir_path}/params.txt
        sed -i "s|CENTERX|$(($L/2))|" ${new_dir_path}/params.txt
        sed -i "s|CENTERY|$(($L/2))|" ${new_dir_path}/params.txt
        sed -i "s|MUVAL|${mu}|" ${new_dir_path}/params.txt
        sed -i "s|DELAYTIME|${delay}|" ${new_dir_path}/params.txt
        sed -i "s|NBASIC|${N1}|" ${new_dir_path}/params.txt
        sed -i "s|PLOTINTERVAL|${plot_interval}|" ${new_dir_path}/params.txt
	#
	if [ $reflect_z==1 ]
	    then
		sed -i "s|NSPACE3|$((${N1}/2))|" ${new_dir_path}/params.txt
		sed -i "s|CENTERZ|0|" ${new_dir_path}/params.txt
		sed -i "s|ZBOUND|2|" ${new_dir_path}/params.txt
	    else
		sed -i "s|NSPACE3|${N1}|" ${new_dir_path}/params.txt
                sed -i "s|CENTERZ|$(($L/2))|" ${new_dir_path}/params.txt
                sed -i "s|ZBOUND|4|" ${new_dir_path}/params.txt
	fi
	#
	mkdir -p outputs
        cd outputs
        sbatch ../slurm_submit
        #
	cd ${work_dir}
done
