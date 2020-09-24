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
# test adding spin
run0001=(0 0 0.0 0 0.4 0.0625)
run0002=(0 0 0.7 0 0.4 0.0625)
run0003=(0 0 0.99 0 0.4 0.0625)
# same for l=m=1
run0004=(1 1 0.0 0 0.4 0.0625)
run0005=(1 1 0.7 0 0.4 0.0625)
run0006=(1 1 0.99 0 0.4 0.0625)
# test lm
run0007=(2 2 0.7 0 0.4 0.0625)
run0008=(4 4 0.7 0 0.4 0.0625)
run0009=(1 -1 0.7 0 0.4 0.0625)
run0010=(8 8 0.7 0 0.4 0.0625)
# test effect of mu
# run0111=(0 0 0.0 0 0.05 0.4)
run0011=(1 1 0.7 0 2.0 0.015625)
run0012=(1 1 0.7 0 0.01 0.0625)
# test effect of m / mu ratio
run0013=(2 2 0.7 0 0.8 0.03125)
run0014=(8 8 0.7 0 3.2 0.0078125)
# test effect of alignment
run0015=(1 1 0.7 0.5 0.4 0.0625)
run0016=(1 -1 0.99 0 0.4 0.0625)
run0017=(1 1 0.99 0.5 0.4 0.0625)
run0018=(1 1 0.99 0.25 0.4 0.0625)
run0019=(1 1 0.7 0 0.01 1.0)
run0020=(1 1 0.7 0 0.1 0.25)
run0021=(0 0 0.7 0 2.0 0.015625)

run0022=(8 8 0.99 0 2.0 0.015625)

# specify runs to submit
#run0001
#run0003
#run0004

#	run0002
#	run0005
#	run0006
#	run0007
#	run0008
#	run0009
#	run0010
#	run0011
#	run0012
#	run0013	
#	run0014
#	run0015
#	run0016
#	run0017
#	run0018


run_list=(
	run0017
)

params_file=params_v2.txt
plot_interval=10
L=1024
N1=128
box_size=16

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
	new_dir=${run}_l${l}_m${m}_a${a}_Al${Al}_mu${mu}_M${M}_IsoKerr_N$N1
	#_L${L}_N$N1
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
	sed -i "s|BOXLENGTH|${L}|" ${new_dir_path}/params.txt
	sed -i "s|BOXSIZE|${box_size}|" ${new_dir_path}/params.txt
	sed -i "s|CENTERX|$(($L/2))|" ${new_dir_path}/params.txt
	sed -i "s|CENTERY|$(($L/2))|" ${new_dir_path}/params.txt
	sed -i "s|SCALARL|${l}|" ${new_dir_path}/params.txt
	sed -i "s|SCALARM|${m}|" ${new_dir_path}/params.txt
	sed -i "s|BHSPIN|${a}|" ${new_dir_path}/params.txt
	sed -i "s|ALANGLE|${Al}|" ${new_dir_path}/params.txt
	sed -i "s|MUVAL|${mu}|" ${new_dir_path}/params.txt
	sed -i "s|DTMULT|${dt}|" ${new_dir_path}/params.txt
	sed -i "s|NBASIC|${N1}|" ${new_dir_path}/params.txt
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
	
