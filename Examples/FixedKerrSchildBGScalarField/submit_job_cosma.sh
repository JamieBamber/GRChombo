#!/bin/bash
#
# This script should make a new directory in ~/GRChombo_data for the data, and copy the slurm_submit file, params.txt file and output files to
# that directory, submit the job, then change back to the working directory

# this copy is for COSMA6 nodes

work_dir=/cosma/home/dp174/dc-bamb1/GRChombo/Examples/FixedKerrSchildBGScalarField
cd $work_dir
data_directory=/cosma6/data/dp174/dc-bamb1/GRChombo_data/KerrSF

# specify the input params for each run I want to submit
# list for each is: l, m, a, Al, mu, M, dt
run0001=(0 0 0 0 1 0.48847892320123 0.0625)

# specify runs to submit
run_list=(
       run0001
)

params_file=params.txt
plot_interval=20
L=512
N1=64
box_size=8

for run in "${run_list[@]}"
do
	cd $work_dir

	# extract parameters	
	val="$run[0]"; l="${!val}"
	val="$run[1]"; m="${!val}"
	val="$run[2]"; a="${!val}"
	val="$run[3]"; Al="${!val}"
	val="$run[4]"; mu="${!val}"
	val="$run[5]"; M="${!val}"
	val="$run[6]"; dt="${!val}"

	# text_number=$(printf "%04d" ${run_number})
	new_dir=${run}_l${l}_m${m}_a${a}_Al${Al}_mu${mu}_M${M}_KerrSchild
	echo ${new_dir}
	new_dir_path=${data_directory}/${new_dir}
	#
	mkdir -p ${new_dir_path}
	cp slurm_submit_cosma ${new_dir_path}/slurm_submit
	cp ${params_file} ${new_dir_path}/params.txt
	
	cd ${new_dir_path}
	# add the input params to the input files
	sed -i "s|DATADIR|${new_dir_path}|" ${new_dir_path}/params.txt
	sed -i "s|DATASUBDIR|${new_dir}|" ${new_dir_path}/params.txt
	sed -i "s|DATADIR|${new_dir_path}|" ${new_dir_path}/slurm_submit
	sed -i "s|JOBNAME|${run}KS|" ${new_dir_path}/slurm_submit
	sed -i "s|NBASIC|${N1}|" ${new_dir_path}/slurm_submit
	sed -i "s|BOXLENGTH|${L}|" ${new_dir_path}/params.txt
        sed -i "s|BOXSIZE|${box_size}|" ${new_dir_path}/params.txt
        sed -i "s|CENTERX|$(($L/2))|" ${new_dir_path}/params.txt
        sed -i "s|CENTERY|$(($L/2))|" ${new_dir_path}/params.txt
	sed -i "s|SCALARL|${l}|" ${new_dir_path}/params.txt
	sed -i "s|SCALARM|${l}|" ${new_dir_path}/params.txt
	sed -i "s|BHMASS|${M}|" ${new_dir_path}/params.txt
	sed -i "s|BHSPIN|${a}|" ${new_dir_path}/params.txt
	sed -i "s|ALANGLE|${Al}|" ${new_dir_path}/params.txt
	sed -i "s|MUVAL|${mu}|" ${new_dir_path}/params.txt
	sed -i "s|DTMULT|${dt}|" ${new_dir_path}/params.txt
	sed -i "s|PLOTINTERVAL|${plot_interval}|" ${new_dir_path}/params.txt
	# half box or full box?
	if (( $(echo "$Al > 0.0" |bc -l) )); then
		echo "Al = $Al so full box"
		sed -i "s|NSPACE3|${N1}|" ${new_dir_path}/params.txt
		sed -i "s|CENTERZ|$(($L/2))|" ${new_dir_path}/params.txt
		sed -i "s|ZBOUND|3|" ${new_dir_path}/params.txt
	else
		echo "Al = $Al so half box"
		sed -i "s|NSPACE3|$(($N1/2))|" ${new_dir_path}/params.txt
                sed -i "s|CENTERZ|0.0|" ${new_dir_path}/params.txt
                sed -i "s|ZBOUND|2|" ${new_dir_path}/params.txt
	fi
	# 
	mkdir -p outputs
	cd outputs
	sbatch ../slurm_submit
	#
	cd ${work_dir}
done
	
