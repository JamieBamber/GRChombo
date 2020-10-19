#!/bin/bash
#
# This script should make a new directory in ~/GRChombo_data for the data, and copy the slurm_submit file, params.txt file and output files to
# that directory, submit the job, then change back to the working directory

# this copy is for the KNL nodes

work_dir=/home/dc-bamb1/GRChombo/Examples/FixedKerrSchildBGScalarField
cd $work_dir
data_directory=/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF

# specify the input params for each run I want to submit
# list for each is: l, m, a, Al, mu, dt
# test adding spin
run0101=(0 0 0.0 0 0.4 0.0625)
run0102=(0 0 0.7 0 0.4 0.0625)
run0103=(0 0 0.99 0 0.4 0.0625)
# same for l=m=1
run0104=(1 1 0.0 0 0.4 0.0625)
run0105=(1 1 0.7 0 0.4 0.0625)
run0106=(1 1 0.99 0 0.4 0.0625)
# test lm
run0107=(2 2 0.7 0 0.4 0.0625)
run0108=(4 4 0.7 0 0.4 0.0625)
run0109=(1 -1 0.7 0 0.4 0.0625)
run0110=(8 8 0.7 0 0.4 0.0625)
# test effect of mu
# run0111=(0 0 0.0 0 0.05 0.4)
run0112=(1 1 0.7 0 0.2 0.0625)
run0113=(1 1 0.7 0 0.8 0.03125)
run0114=(1 1 0.7 0 0.1 0.0625)
# test effect of m / mu ratio
run0119=(2 2 0.7 0 0.8 0.03125)
run0115=(8 8 0.7 0 3.2 0.0078125)
# test effect of alignment
run0116=(1 1 0.7 0.5 0.4 0.0625)
run0117=(1 -1 0.99 0 0.4 0.0625)
run0118=(1 1 0.99 0.5 0.4 0.0625)

# specify runs to submit
run_list=(
       run0105
)

#	run0101
#	run0102
#	run0103
#	run0104
#	run0105
#	run0106
#	run0107
#	run0108
#	run0109
#	run0110
#	run0112
#	run0113
#	run0114
#	run0115
#	run0116
#	run0117	
#	run0118

params_file=params.txt
plot_interval=5

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
	new_dir=${run}_l${l}_m${m}_a${a}_Al${Al}_mu${mu}_M${M}_KerrSchild_N256
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
	sed -i "s|BHMASS|${M}|" ${new_dir_path}/params.txt
	sed -i "s|BHSPIN|${a}|" ${new_dir_path}/params.txt
	sed -i "s|ALANGLE|${Al}|" ${new_dir_path}/params.txt
	sed -i "s|MUVAL|${mu}|" ${new_dir_path}/params.txt
	sed -i "s|DTMULT|${dt}|" ${new_dir_path}/params.txt
	sed -i "s|PLOTINTERVAL|${plot_interval}|" ${new_dir_path}/params.txt
	# half box or full box?
	if (( $(echo "$Al > 0.0" |bc -l) )); then
		echo "Al = $Al so full box"
		sed -i "s|NSPACE3|256|" ${new_dir_path}/params.txt
		sed -i "s|CENTERZ|512.0|" ${new_dir_path}/params.txt
		sed -i "s|ZBOUND|3|" ${new_dir_path}/params.txt
	else
		echo "Al = $Al so half box"
		sed -i "s|NSPACE3|128|" ${new_dir_path}/params.txt
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
	
